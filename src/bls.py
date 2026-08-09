import json
from datetime import datetime
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

    def collect_series(self, series_id: str, name: str, units: str = "Value"):
        """Collect a single series from BLS, from 1990 to the current year."""
        print(f"📊 Fetching {name} ({series_id}) from BLS...")

        current_year = datetime.now().year  # noqa: DTZ005 — only the calendar year is used
        start_year = 1990
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
                dates.append(datetime.strptime(date_str, "%Y-%m-%d"))  # noqa: DTZ007 — calendar date, not an instant
                values.append(float(item["value"]))

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
            ),
        }

        for series_id, (name, units) in series_map.items():
            try:
                self.collect_series(series_id, name, units)
            except Exception as e:  # noqa: BLE001 — one series' failure shouldn't stop the rest
                print(f"❌ Error fetching {series_id}: {e}")
