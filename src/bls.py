from datetime import datetime
from pathlib import Path

import polars as pl


class BlsCollector:
    """Collector for BLS economic data."""

    def __init__(self, output_dir: str = "data/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def collect_series(self, series_id: str, name: str):
        """Collect a single series from BLS."""
        print(f"📊 Fetching {name} ({series_id}) from BLS...")
        import requests

        headers = {"Content-type": "application/json"}
        data = {
            "seriesid": [series_id],
            "startyear": "1990",
            "endyear": str(datetime.now().year),
        }

        response = requests.post(
            "https://api.bls.gov/publicAPI/v2/timeseries/data/",
            json=data,
            headers=headers,
        )

        if response.status_code == 200:
            json_data = response.json()
            if json_data["status"] == "REQUEST_SUCCEEDED":
                series = json_data["Results"]["series"][0]["data"]

                dates = []
                values = []
                for item in series:
                    year = item["year"]
                    period = item["period"]
                    if period.startswith("M"):
                        month = period[1:]
                        date_str = f"{year}-{month}-01"
                        dates.append(datetime.strptime(date_str, "%Y-%m-%d"))
                        values.append(float(item["value"]))

                df = pl.DataFrame({"date": dates, "value": values}).sort("date")

                filename = f"{series_id.lower()}.csv"
                filepath = self.output_dir / filename
                df.write_csv(filepath)
                print(f"✅ Saved {filename} ({len(df)} rows)")
                return df
            else:
                print(f"❌ BLS API error: {json_data.get('message', 'Unknown error')}")
        else:
            print(f"❌ HTTP error: {response.status_code}")
