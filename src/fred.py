from pathlib import Path
import json

import polars as pl
from fredapi import Fred


class FredCollector:
    """Collector for FRED economic data."""

    def __init__(self, api_key: str, output_dir: str = "data/raw"):
        self.client = Fred(api_key=api_key)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.output_dir.parent / "metadata.json"

    def get_series_metadata(self, series_id: str):
        """Fetch metadata for a series from FRED."""
        info = self.client.get_series_info(series_id)
        last_updated = info.get("last_updated", "")
        if hasattr(last_updated, "isoformat"):
            last_updated = last_updated.isoformat()
        return {
            "title": info.get("title", ""),
            "units": info.get("units", "Value"),
            "frequency": info.get("frequency", ""),
            "seasonal_adjustment": info.get("seasonal_adjustment", ""),
            "last_updated": str(last_updated) if last_updated else "",
        }

    def save_metadata(self, series_id: str, metadata: dict):
        """Save or update metadata for a series."""
        if self.metadata_file.exists():
            with open(self.metadata_file, "r") as f:
                all_metadata = json.load(f)
        else:
            all_metadata = {}

        all_metadata[series_id.lower()] = metadata

        with open(self.metadata_file, "w") as f:
            json.dump(all_metadata, f, indent=2)

    def collect_series(self, series_id: str, name: str, start_date=None):
        """Collect a single series from FRED."""
        print(f"📊 Fetching {name} ({series_id})...")
        data = self.client.get_series(series_id, observation_start=start_date)

        # Fetch and save metadata
        try:
            metadata = self.get_series_metadata(series_id)
            self.save_metadata(series_id, metadata)
        except Exception as e:
            print(f"⚠️  Could not fetch metadata: {e}")

        df = pl.DataFrame({"date": data.index.to_list(), "value": data.to_list()})

        filename = f"{series_id.lower()}.csv"
        filepath = self.output_dir / filename
        df.write_csv(filepath)
        print(
            f"✅ Saved {filename} ({len(df)} rows, {df['date'].min()} to {df['date'].max()})"
        )
        return df

    def collect_all(self):
        """Collect all available economic indicators."""
        series_map = {
            "CPIAUCSL": "CPI - All Urban Consumers",
            "GDP": "Gross Domestic Product",
            "UMCSENT": "Consumer Confidence (U. Michigan)",
            "UNRATE": "Unemployment Rate",
            "CIVPART": "Labor Force Participation Rate",
            "U6RATE": "Total Unemployed + Marginally Attached + Part Time (U-6)",
            "U5RATE": "Total Unemployed + Discouraged + Marginally Attached (U-5)",
            "U4RATE": "Total Unemployed + Discouraged Workers (U-4)",
            "U2RATE": "Unemployment Rate - Job Losers (U-2)",
            "U1RATE": "Unemployed 15 Weeks and Over (U-1)",
            "LNS14000012": "Unemployment Rate - 16-19 Yrs.",
            "LNS14000036": "Unemployment Rate - 20-24 Yrs.",
            "LNS14000089": "Unemployment Rate - 25-34 Yrs.",
            "LNS14024230": "Unemployment Rate - 55 Yrs. & Over",
            "ICSA": "Initial Claims",
            "CCSA": "Continued Claims",
        }

        for series_id, name in series_map.items():
            try:
                self.collect_series(series_id, name)
            except Exception as e:
                print(f"❌ Error fetching {series_id}: {e}")
