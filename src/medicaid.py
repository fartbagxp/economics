"""
Medicaid & CHIP enrollment collector.

Data source: CMS Performance Indicator dataset, published via the
data.medicaid.gov datastore API (stable dataset id — the underlying CSV file
is re-published under a new dated filename every month, so the API is used
instead of a direct download link).
https://www.medicaid.gov/medicaid/national-medicaid-chip-program-information/medicaid-chip-enrollment-data

Each state reports one row per month, sometimes twice (a preliminary "P"
estimate followed later by a final "Y" report for the same period) — the
final report is preferred when both exist. National totals are the sum of
"Total Medicaid and CHIP Enrollment" across all reporting states/DC.

Coverage is not fully continuous: states began reporting under this format
in September 2013, then consistently from June 2017 onward.
"""

from collections import defaultdict
from datetime import date
from pathlib import Path
import json

import polars as pl
import requests


DATASET_ID = "6165f45b-ca93-5bb5-9d06-db29c692a360"
API_URL = f"https://data.medicaid.gov/api/1/datastore/query/{DATASET_ID}/0"
PAGE_SIZE = 5000

METADATA = {
    "title": "Medicaid & CHIP: Total Enrollment (National)",
    "units": "Persons",
    "frequency": "Monthly",
    "seasonal_adjustment": "Not Seasonally Adjusted",
    "source": "CMS Performance Indicator Dataset",
    "source_url": "https://www.medicaid.gov/medicaid/national-medicaid-chip-program-information/medicaid-chip-enrollment-data",
}


class MedicaidCollector:
    """Collector for CMS Medicaid & CHIP national total enrollment data."""

    def __init__(self, output_dir: str = "data/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.output_dir.parent / "metadata.json"

    def _fetch_all(self) -> list[dict]:
        rows = []
        offset = 0
        while True:
            print(f"⬇️  Fetching {API_URL} (offset {offset}) ...")
            r = requests.get(API_URL, params={"limit": PAGE_SIZE, "offset": offset}, timeout=60)
            r.raise_for_status()
            page = r.json().get("results", [])
            rows.extend(page)
            if len(page) < PAGE_SIZE:
                break
            offset += PAGE_SIZE
        return rows

    def save_metadata(self):
        if self.metadata_file.exists():
            with open(self.metadata_file) as f:
                all_meta = json.load(f)
        else:
            all_meta = {}
        entry = dict(METADATA)
        entry["last_updated"] = date.today().isoformat()
        all_meta["medicaid_chip_enrollment"] = entry
        with open(self.metadata_file, "w") as f:
            json.dump(all_meta, f, indent=2)

    def collect_all(self):
        rows = self._fetch_all()

        # Prefer the final report per (state, period); fall back to the
        # preliminary one if no final report has been published yet.
        best: dict[tuple, dict] = {}
        for row in rows:
            key = (row.get("state_name"), row.get("reporting_period"))
            if key not in best or row.get("final_report") == "Y":
                best[key] = row

        totals = defaultdict(float)
        for row in best.values():
            period = row.get("reporting_period")
            value = row.get("total_medicaid_and_chip_enrollment")
            if not period or len(period) != 6 or value in (None, ""):
                continue
            try:
                totals[period] += float(value)
            except (TypeError, ValueError):
                continue

        records = [
            {"date": f"{period[:4]}-{period[4:]}-01", "value": total}
            for period, total in totals.items()
        ]
        if not records:
            raise RuntimeError("No Medicaid enrollment records parsed from data.medicaid.gov")

        df = (
            pl.DataFrame(records)
            .with_columns(pl.col("date").str.to_date())
            .sort("date")
        )

        filepath = self.output_dir / "medicaid_chip_enrollment.csv"
        df.write_csv(filepath)
        self.save_metadata()
        print(f"✅ Saved medicaid_chip_enrollment.csv ({len(df)} rows, {df['date'].min()} to {df['date'].max()})")
        return df
