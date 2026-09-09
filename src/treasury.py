"""
U.S. national debt collector (Treasury "Debt to the Penny").

Data source: U.S. Treasury, Fiscal Data.
https://fiscaldata.treasury.gov/datasets/debt-to-the-penny/

Total public debt outstanding for every business day since 1993-04-01, which is
as far back as this dataset goes. For the 1989-1993 stretch — and for a
quarterly series that lines up with the DFA wealth quarters — the dashboard uses
FRED's GFDEBTN instead, collected by the FRED collector.

Values stay in the units Treasury publishes: dollars, to the penny.
"""

import json
from datetime import UTC, datetime
from pathlib import Path

import polars as pl
import requests

API_URL = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny"
PAGE_SIZE = 10000

METADATA = {
    "title": "Total Public Debt Outstanding (Debt to the Penny)",
    "units": "U.S. Dollars",
    "frequency": "Daily",
    "seasonal_adjustment": "Not Seasonally Adjusted",
    "source": "U.S. Treasury, Fiscal Data",
    "source_url": "https://fiscaldata.treasury.gov/datasets/debt-to-the-penny/",
}


class TreasuryCollector:
    """Collector for U.S. Treasury total public debt outstanding."""

    def __init__(self, output_dir: str = "data/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.output_dir.parent / "metadata.json"

    def _fetch(self) -> list[dict]:
        """Page through the full history. One page holds every row today, but the
        series grows by ~250 rows a year, so follow the API's own page count."""
        print(f"⬇️  Fetching {API_URL} ...")
        rows = []
        page = 1
        while True:
            r = requests.get(
                API_URL,
                params={
                    "fields": "record_date,tot_pub_debt_out_amt",
                    "sort": "record_date",
                    "page[size]": PAGE_SIZE,
                    "page[number]": page,
                },
                timeout=120,
            )
            r.raise_for_status()
            payload = r.json()
            rows.extend(payload.get("data", []))
            total_pages = payload.get("meta", {}).get("total-pages", 1)
            if page >= total_pages:
                break
            page += 1
        return rows

    def save_metadata(self):
        if self.metadata_file.exists():
            with open(self.metadata_file) as f:
                all_meta = json.load(f)
        else:
            all_meta = {}
        entry = dict(METADATA)
        entry["last_updated"] = datetime.now(UTC).date().isoformat()
        all_meta["treasury_national_debt"] = entry
        with open(self.metadata_file, "w") as f:
            json.dump(all_meta, f, indent=2)
            f.write("\n")

    def collect_all(self):
        print("📊 U.S. Treasury Debt to the Penny")
        rows = self._fetch()

        records = []
        for row in rows:
            try:
                value = float(row["tot_pub_debt_out_amt"])
            except (KeyError, TypeError, ValueError):
                continue  # the API returns the string "null" for unreported fields
            records.append({"date": row["record_date"], "value": value})

        if not records:
            raise RuntimeError("No debt records parsed from the Treasury API response")

        df = (
            pl.DataFrame(records)
            .with_columns(pl.col("date").str.to_date())
            .unique(subset="date")
            .sort("date")
            .rename({"value": "total_public_debt_outstanding"})
        )

        filepath = self.output_dir / "treasury_national_debt.csv"
        df.write_csv(filepath)
        self.save_metadata()
        print(
            f"✅ Saved treasury_national_debt.csv ({len(df)} rows, "
            f"{df['date'].min()} to {df['date'].max()})"
        )
        return df
