"""
NY Fed Global Supply Chain Pressure Index (GSCPI) collector.

Data source: Federal Reserve Bank of New York,
https://www.newyorkfed.org/research/policy/gscpi

Monthly composite of global transportation costs (Baltic Dry, Harpex,
airfreight) and PMI subcomponents (delivery times, backlogs, purchased
inventories) across seven economies, expressed in standard deviations from the
historical average. Updated around the 4th business day of each month.

The download URL ends in .xlsx but the file is a legacy .xls workbook, hence
xlrd rather than openpyxl. Observations are labeled with month-end dates
("31-Jan-1998"); stored as the first of the month for consistency with FRED
monthly series.
"""

from datetime import date, datetime
from pathlib import Path
import json

import polars as pl
import requests
import xlrd


DATA_URL = "https://www.newyorkfed.org/medialibrary/research/interactives/gscpi/downloads/gscpi_data.xlsx"
SHEET_NAME = "GSCPI Monthly Data"
SERIES_ID = "gscpi"

METADATA = {
    "title": "NY Fed: Global Supply Chain Pressure Index (GSCPI)",
    "units": "Standard Deviations from Average",
    "frequency": "Monthly",
    "seasonal_adjustment": "Not Seasonally Adjusted",
    "source": "Federal Reserve Bank of New York",
    "source_url": "https://www.newyorkfed.org/research/policy/gscpi",
}


class GscpiCollector:
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
        book = xlrd.open_workbook(file_contents=content)
        if SHEET_NAME in book.sheet_names():
            sheet = book.sheet_by_name(SHEET_NAME)
        else:
            sheet = book.sheet_by_index(0)

        records = []
        for rx in range(sheet.nrows):
            parsed = _parse_date_cell(sheet.cell(rx, 0), book.datemode)
            value_cell = sheet.cell(rx, 1)
            if parsed is None or value_cell.ctype != xlrd.XL_CELL_NUMBER:
                continue
            records.append({"date": parsed, "value": float(value_cell.value)})

        return pl.DataFrame(records)

    def save_metadata(self):
        if self.metadata_file.exists():
            with open(self.metadata_file) as f:
                all_meta = json.load(f)
        else:
            all_meta = {}
        entry = dict(METADATA)
        entry["last_updated"] = date.today().isoformat()
        all_meta[SERIES_ID] = entry
        with open(self.metadata_file, "w") as f:
            json.dump(all_meta, f, indent=2)

    def collect_all(self):
        print("📊 NY Fed Global Supply Chain Pressure Index")
        df = self._parse(self._download())
        if df.is_empty():
            print("❌ Parsed DataFrame is empty — check sheet structure")
            return
        filepath = self.output_dir / f"{SERIES_ID}.csv"
        df.write_csv(filepath)
        self.save_metadata()
        print(f"✅ Saved {SERIES_ID}.csv ({len(df)} rows, {df['date'].min()} to {df['date'].max()})")


def _parse_date_cell(cell, datemode: int) -> str | None:
    """Convert a month-end date cell ('31-Jan-1998' or Excel serial) to YYYY-MM-01."""
    if cell.ctype == xlrd.XL_CELL_DATE:
        dt = xlrd.xldate_as_datetime(cell.value, datemode)
    elif cell.ctype == xlrd.XL_CELL_TEXT:
        try:
            dt = datetime.strptime(str(cell.value).strip(), "%d-%b-%Y")
        except ValueError:
            return None
    else:
        return None
    return f"{dt.year}-{dt.month:02d}-01"
