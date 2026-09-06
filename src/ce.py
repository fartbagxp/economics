"""
Consumer Expenditure Survey collector — spending by age of reference person.

Data source: BLS Consumer Expenditure Surveys (CE), pulled directly from the
BLS public timeseries API (same endpoint as src/bls.py, no auth required).
https://www.bls.gov/cex/

Each series is the total average annual expenditure for a consumer unit whose
reference person falls in a given age band. The reference person is "the first
member mentioned by the respondent when asked to 'Start with the name of the
person or one of the persons who owns or rents the home.'"

Series are annual (BLS period "A01"); the observation date is stored as the
first of the year for consistency with the monthly series in this repo. Data
for calendar year Y is published by BLS in September of year Y+1.
"""

import json
from datetime import UTC, datetime
from pathlib import Path

import polars as pl
import requests

API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

START_YEAR = 1984

# csv slug -> (BLS series id, human label). The "LB04xxM" tail is CE table
# 1300 (age of reference person); 0401 is the all-consumer-units total, kept
# as a baseline to compare the age bands against.
AGE_GROUPS = {
    "ce_totalexp_all": ("CXUTOTALEXPLB0401M", "All consumer units"),
    "ce_totalexp_lt25": ("CXUTOTALEXPLB0402M", "Reference person under 25"),
    "ce_totalexp_25_34": ("CXUTOTALEXPLB0403M", "Reference person 25 to 34"),
    "ce_totalexp_35_44": ("CXUTOTALEXPLB0404M", "Reference person 35 to 44"),
    "ce_totalexp_45_54": ("CXUTOTALEXPLB0405M", "Reference person 45 to 54"),
    "ce_totalexp_55_64": ("CXUTOTALEXPLB0406M", "Reference person 55 to 64"),
    "ce_totalexp_65up": ("CXUTOTALEXPLB0407M", "Reference person 65 and older"),
    "ce_totalexp_65_74": ("CXUTOTALEXPLB0408M", "Reference person 65 to 74"),
    "ce_totalexp_75up": ("CXUTOTALEXPLB0409M", "Reference person 75 and older"),
}

METADATA_BASE = {
    "units": "U.S. Dollars",
    "frequency": "Annual",
    "seasonal_adjustment": "Not Seasonally Adjusted",
    "source": "U.S. Bureau of Labor Statistics — Consumer Expenditure Surveys",
    "source_url": "https://www.bls.gov/cex/tables.htm",
}


class CeCollector:
    """Collector for BLS Consumer Expenditure Survey spending-by-age data."""

    def __init__(self, output_dir: str = "data/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.output_dir.parent / "metadata.json"

    def _fetch_year_range(
        self, series_ids: list[str], start_year: int, end_year: int
    ) -> list[dict]:
        """One BLS API request for several series over a <=10-year window. The
        public (unregistered) API silently truncates windows wider than 10
        years and caps a request at 50 series, so callers chunk on both axes."""
        resp = requests.post(
            API_URL,
            json={
                "seriesid": series_ids,
                "startyear": str(start_year),
                "endyear": str(end_year),
            },
            headers={"Content-type": "application/json"},
            timeout=60,
        )
        resp.raise_for_status()
        payload = resp.json()
        if payload.get("status") != "REQUEST_SUCCEEDED":
            raise RuntimeError(f"BLS API error: {payload.get('message', 'unknown')}")
        return payload["Results"]["series"]

    def _fetch_all(self) -> dict[str, list[tuple[int, float]]]:
        """Fetch every age-band series across the full history in 10-year
        chunks. Batching all series into each request keeps the run to ~5 API
        calls, well under the unregistered API's 25-requests-per-day limit."""
        series_ids = [sid for sid, _ in AGE_GROUPS.values()]
        current_year = datetime.now(UTC).year
        by_series: dict[str, list[tuple[int, float]]] = {sid: [] for sid in series_ids}

        year = START_YEAR
        while year <= current_year:
            end_year = min(year + 9, current_year)
            print(f"📊 Fetching CE spending by age {year}–{end_year} from BLS...")
            for series in self._fetch_year_range(series_ids, year, end_year):
                sid = series["seriesID"]
                for item in series["data"]:
                    if item["period"] != "A01":
                        continue
                    by_series[sid].append((int(item["year"]), float(item["value"])))
            year = end_year + 1

        return by_series

    def save_metadata(self, all_meta: dict, slug: str, label: str):
        entry = dict(METADATA_BASE)
        entry["title"] = f"Total Average Annual Expenditures — {label}"
        entry["last_updated"] = datetime.now(UTC).date().isoformat()
        all_meta[slug] = entry

    def collect_all(self):
        by_series = self._fetch_all()

        if self.metadata_file.exists():
            with open(self.metadata_file) as f:
                all_meta = json.load(f)
        else:
            all_meta = {}

        for slug, (series_id, label) in AGE_GROUPS.items():
            rows = by_series.get(series_id, [])
            if not rows:
                print(f"❌ No data returned for {series_id} ({slug})")
                continue

            df = (
                pl.DataFrame(rows, schema=["year", "value"], orient="row")
                .with_columns(pl.date(pl.col("year"), 1, 1).alias("date"))
                .select("date", "value")
                .unique("date")
                .sort("date")
            )

            filepath = self.output_dir / f"{slug}.csv"
            df.write_csv(filepath)
            self.save_metadata(all_meta, slug, label)
            print(
                f"✅ Saved {slug}.csv ({len(df)} rows, "
                f"{df['date'].min()} to {df['date'].max()})"
            )

        with open(self.metadata_file, "w") as f:
            json.dump(all_meta, f, indent=2)
            f.write("\n")
