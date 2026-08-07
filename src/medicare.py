"""
Medicare total enrollment collector.

Data source: CMS (Centers for Medicare & Medicaid Services) Medicare Monthly
Enrollment dataset, published via the data.cms.gov API.
https://data.cms.gov/summary-statistics-on-beneficiary-enrollment/medicare-and-medicaid-reports/medicare-monthly-enrollment

National-level monthly counts of total Medicare beneficiaries (TOT_BENES),
covering hospital/medical coverage under Original Medicare and Medicare
Advantage. Coverage starts January 2013.
"""

from datetime import date
from pathlib import Path
import json

import polars as pl
import requests


API_URL = "https://data.cms.gov/data-api/v1/dataset/d7fabe1e-d19b-4333-9eff-e80e0643f2fd/data"

MONTH_NUM = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
}

METADATA = {
    "title": "Medicare: Total Beneficiaries Enrolled (National)",
    "units": "Persons",
    "frequency": "Monthly",
    "seasonal_adjustment": "Not Seasonally Adjusted",
    "source": "CMS Medicare Monthly Enrollment",
    "source_url": "https://data.cms.gov/summary-statistics-on-beneficiary-enrollment/medicare-and-medicaid-reports/medicare-monthly-enrollment",
}


class MedicareCollector:
    """Collector for CMS Medicare national total enrollment data."""

    def __init__(self, output_dir: str = "data/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.output_dir.parent / "metadata.json"

    def _fetch(self) -> list[dict]:
        print(f"⬇️  Fetching {API_URL} ...")
        r = requests.get(
            API_URL,
            params={"filter[BENE_GEO_LVL]": "National", "size": 2000},
            timeout=60,
        )
        r.raise_for_status()
        return r.json()

    def save_metadata(self):
        if self.metadata_file.exists():
            with open(self.metadata_file) as f:
                all_meta = json.load(f)
        else:
            all_meta = {}
        entry = dict(METADATA)
        entry["last_updated"] = date.today().isoformat()
        all_meta["medicare_total_enrollment"] = entry
        with open(self.metadata_file, "w") as f:
            json.dump(all_meta, f, indent=2)

    def collect_all(self):
        rows = self._fetch()

        records = []
        for row in rows:
            month_name = row.get("MONTH", "").strip().lower()
            if month_name not in MONTH_NUM:
                continue  # skip "Year" annual-average rows
            try:
                year = int(row["YEAR"])
                value = float(row["TOT_BENES"])
            except (KeyError, TypeError, ValueError):
                continue
            records.append({
                "date": f"{year}-{MONTH_NUM[month_name]:02d}-01",
                "value": value,
            })

        if not records:
            raise RuntimeError("No Medicare enrollment records parsed from CMS API response")

        df = (
            pl.DataFrame(records)
            .with_columns(pl.col("date").str.to_date())
            .unique(subset="date")
            .sort("date")
        )

        filepath = self.output_dir / "medicare_total_enrollment.csv"
        df.write_csv(filepath)
        self.save_metadata()
        print(f"✅ Saved medicare_total_enrollment.csv ({len(df)} rows, {df['date'].min()} to {df['date'].max()})")
        return df
