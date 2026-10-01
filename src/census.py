"""
Census Bureau official poverty rate collector.

Data source: U.S. Census Bureau, Current Population Survey Annual Social and
Economic Supplement (CPS ASEC), Historical Poverty Tables, Table 2
("Poverty Status of People by Family Relationship, Race, and Hispanic Origin"),
https://www.census.gov/data/tables/time-series/demo/income-poverty/historical-poverty-people.html

This is the official poverty measure (OPM), released each September for the
prior calendar year. FRED only carries the Census SAIPE/ACS model estimate
(PPAAUS00000A156NCEN), which runs ~1pp above the official CPS ASEC rate, so the
workbook is read directly.

Only the "All Races" block, "All people / Below poverty / Percent" column is
kept. The table is newest-first and repeats a year where the methodology
changed (2013: redesigned income questions; 2017: updated processing system).
The first row listed is the newer method, consistent with every year after it,
so the first occurrence of each year wins. Years are stored as Jan 1 of the
data year (FRED annual convention).
"""

import io
import json
import re
from datetime import UTC, datetime
from pathlib import Path

import openpyxl
import polars as pl
import requests

DATA_URL = "https://www2.census.gov/programs-surveys/cps/tables/time-series/historical-poverty-people/hstpov2.xlsx"
SERIES_ID = "census_poverty_rate"

YEAR_RE = re.compile(r"^(\d{4})(?:\s*\(\d+\))?$")
PERCENT_COL = 3  # All people -> Below poverty -> Percent

METADATA = {
    "title": "Official Poverty Rate: All People (CPS ASEC)",
    "units": "Percent",
    "frequency": "Annual",
    "seasonal_adjustment": "Not Seasonally Adjusted",
    "source": "U.S. Census Bureau, Current Population Survey ASEC, Historical Poverty Table 2",
    "source_url": "https://www.census.gov/data/tables/time-series/demo/income-poverty/historical-poverty-people.html",
}


class CensusPovertyCollector:
    def __init__(self, output_dir: str = "data/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.output_dir.parent / "metadata.json"

    def _download(self) -> bytes:
        print(f"⬇️  Downloading {DATA_URL} ...")
        r = requests.get(DATA_URL, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        return r.content

    def _parse(self, content: bytes) -> pl.DataFrame:
        book = openpyxl.load_workbook(io.BytesIO(content), read_only=True)
        sheet = book.worksheets[0]

        records = {}
        in_all_races = False
        for row in sheet.iter_rows(values_only=True):
            label = str(row[0]).strip() if row[0] is not None else ""
            if label == "All Races":
                in_all_races = True
                continue
            if not in_all_races:
                continue
            match = YEAR_RE.match(label)
            if match is None:
                # A non-year label after data rows begins the next race block
                if records and label not in ("", "Year"):
                    break
                continue
            year = int(match.group(1))
            value = row[PERCENT_COL]
            if year in records or not isinstance(value, (int, float)):
                continue
            records[year] = float(value)

        if not records:
            raise RuntimeError("No 'All Races' poverty rows found — check table layout")
        return pl.DataFrame(
            {
                "date": [f"{y}-01-01" for y in sorted(records)],
                "value": [records[y] for y in sorted(records)],
            }
        )

    def save_metadata(self):
        if self.metadata_file.exists():
            with open(self.metadata_file) as f:
                all_meta = json.load(f)
        else:
            all_meta = {}
        entry = dict(METADATA)
        entry["last_updated"] = datetime.now(UTC).date().isoformat()
        all_meta[SERIES_ID] = entry
        with open(self.metadata_file, "w") as f:
            json.dump(all_meta, f, indent=2)
            f.write("\n")

    def collect_all(self):
        print("📊 Census official poverty rate")
        df = self._parse(self._download())
        filepath = self.output_dir / f"{SERIES_ID}.csv"
        df.write_csv(filepath)
        self.save_metadata()
        print(
            f"✅ Saved {SERIES_ID}.csv ({len(df)} rows, {df['date'].min()} to {df['date'].max()})"
        )
