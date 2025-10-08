from pathlib import Path

import polars as pl
from fredapi import Fred


class FredCollector:
    """Collector for FRED economic data."""

    def __init__(self, api_key: str, output_dir: str = "data/raw"):
        self.client = Fred(api_key=api_key)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def collect_series(self, series_id: str, name: str, start_date=None):
        """Collect a single series from FRED."""
        print(f"📊 Fetching {name} ({series_id})...")
        data = self.client.get_series(series_id, observation_start=start_date)

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
        }

        for series_id, name in series_map.items():
            try:
                self.collect_series(series_id, name)
            except Exception as e:
                print(f"❌ Error fetching {series_id}: {e}")
