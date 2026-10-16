import json
from datetime import UTC, datetime
from pathlib import Path

import polars as pl


class BlsCollector:
    """Collector for BLS economic data."""

    def __init__(self, output_dir: str = "data/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.output_dir.parent / "metadata.json"

    def save_metadata(self, series_id: str, name: str, units: str = "Value"):
        """Save or update metadata for a BLS series."""
        if self.metadata_file.exists():
            with open(self.metadata_file, "r") as f:
                all_metadata = json.load(f)
        else:
            all_metadata = {}

        all_metadata[series_id.lower()] = {
            "title": name,
            "units": units,
            "frequency": "Monthly",
            "seasonal_adjustment": "Seasonally Adjusted",
            "last_updated": "",
            "source": "U.S. Bureau of Labor Statistics",
            "source_url": f"https://data.bls.gov/timeseries/{series_id.upper()}",
        }

        with open(self.metadata_file, "w") as f:
            json.dump(all_metadata, f, indent=2)
            f.write("\n")

    def _fetch_year_range(self, series_id: str, start_year: int, end_year: int):
        """Fetch one BLS API request. The public (unregistered) API silently
        truncates any request spanning more than 10 years instead of erroring,
        so callers must chunk requests into <=10-year windows."""
        import requests

        headers = {"Content-type": "application/json"}
        data = {
            "seriesid": [series_id],
            "startyear": str(start_year),
            "endyear": str(end_year),
        }

        response = requests.post(
            "https://api.bls.gov/publicAPI/v2/timeseries/data/",
            json=data,
            headers=headers,
        )

        if response.status_code != 200:
            print(f"❌ HTTP error: {response.status_code}")
            return []

        json_data = response.json()
        if json_data["status"] != "REQUEST_SUCCEEDED":
            print(f"❌ BLS API error: {json_data.get('message', 'Unknown error')}")
            return []

        return json_data["Results"]["series"][0]["data"]

    def collect_series(
        self, series_id: str, name: str, units: str = "Value", start_year: int = 1990
    ):
        """Collect a single series from BLS, from start_year to the current year."""
        print(f"📊 Fetching {name} ({series_id}) from BLS...")

        current_year = datetime.now(UTC).year
        raw_items = []
        year = start_year
        while year <= current_year:
            end_year = min(year + 9, current_year)
            raw_items.extend(self._fetch_year_range(series_id, year, end_year))
            year = end_year + 1

        dates = []
        values = []
        for item in raw_items:
            year = item["year"]
            period = item["period"]
            if period.startswith("M"):
                month = period[1:]
                date_str = f"{year}-{month}-01"
                # Naive on purpose: this is a calendar month, not an instant,
                # and every other collector in this repo stores dates the same
                # way (tz-aware here breaks strict=False parsing downstream —
                # see sparkline.py's load_series and derive.py's _load).
                dates.append(datetime.strptime(date_str, "%Y-%m-%d"))  # noqa: DTZ007
                # BLS reports months it never published as "-" (e.g. October
                # 2025, when the appropriations lapse cancelled that month's
                # CPI). Keep the row as NaN, as FRED does, so the Deriver's
                # row-based 12-period shift stays 12 calendar months.
                value = item["value"]
                values.append(float("nan") if value == "-" else float(value))

        if not dates:
            print(f"❌ No data returned for {series_id}")
            return None

        df = pl.DataFrame({"date": dates, "value": values}).unique("date").sort("date")

        filename = f"{series_id.lower()}.csv"
        filepath = self.output_dir / filename
        df.write_csv(filepath)
        self.save_metadata(series_id, name, units)
        print(f"✅ Saved {filename} ({len(df)} rows)")
        return df

    def collect_all(self):
        """Collect all default BLS economic indicators."""
        series_map = {
            "CES0000000001": (
                "Total Nonfarm Payroll Employment",
                "Thousands of Persons",
                1990,
            ),
            # Real (CPI-U deflated) earnings from the BLS Real Earnings release.
            # FRED doesn't mirror these, and they only start in March 2006, so
            # starting there saves requests against the 25/day unregistered limit.
            "CES0500000013": (
                "Real Average Hourly Earnings of All Employees, Total Private",
                "1982-1984 Dollars per Hour",
                2006,
            ),
            "CES0500000012": (
                "Real Average Weekly Earnings of All Employees, Total Private",
                "1982-1984 Dollars per Week",
                2006,
            ),
        }

        for series_id, (name, units, start_year) in series_map.items():
            try:
                self.collect_series(series_id, name, units, start_year)
            except (OSError, ValueError, KeyError, pl.exceptions.PolarsError) as e:
                print(f"❌ Error fetching {series_id}: {e}")
