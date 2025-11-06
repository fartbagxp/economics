from pathlib import Path
import json

import matplotlib.pyplot as plt
import polars as pl


class EconomicChart:
    def __init__(self, data_dir="data/raw"):
        self.data_dir = Path(data_dir)
        self.metadata_file = self.data_dir.parent / "metadata.json"
        self.metadata = self._load_metadata()

    def _load_metadata(self):
        """Load metadata from JSON file."""
        if self.metadata_file.exists():
            with open(self.metadata_file, "r") as f:
                return json.load(f)
        return {}

    def load_series(self, series_name):
        """Load a CSV file for a given series (e.g., 'cpiaucsl', 'unrate')."""
        file_path = self.data_dir / f"{series_name.lower()}.csv"
        df = pl.read_csv(file_path)
        df = df.with_columns(pl.col("date").str.to_datetime())
        return df

    def get_ylabel(self, series_name):
        """Get the y-axis label for a series from metadata."""
        series_key = series_name.lower()
        if series_key in self.metadata:
            return self.metadata[series_key].get("units", "Value")
        return "Value"

    def get_title(self, series_name):
        """Get the full title for a series from metadata."""
        series_key = series_name.lower()
        if series_key in self.metadata:
            return self.metadata[series_key].get("title", series_name.upper())
        return series_name.upper()

    def get_short_title(self, series_name):
        """Get a shortened title for chart legends."""
        series_key = series_name.lower()

        # Custom short labels for U-series
        short_labels = {
            "u1rate": "U-1: 15+ Weeks Unemployed",
            "u2rate": "U-2: Job Losers",
            "unrate": "U-3: Official Rate",
            "u4rate": "U-4: + Discouraged Workers",
            "u5rate": "U-5: + Marginally Attached",
            "u6rate": "U-6: + Part-Time Economic",
        }

        if series_key in short_labels:
            return short_labels[series_key]

        # For other series, use full title
        return self.get_title(series_name)

    def plot_single(self, series_name, output_file=None, title=None, ylabel=None):
        """Plot a single economic series."""
        df = self.load_series(series_name)

        # Use metadata if ylabel not explicitly provided
        if ylabel is None:
            ylabel = self.get_ylabel(series_name)

        # Use metadata title if not provided
        if title is None:
            title = self.get_title(series_name)

        plt.figure(figsize=(14, 6))
        plt.plot(df["date"].to_list(), df["value"].to_list(), linewidth=2)
        plt.title(title, fontsize=14)
        plt.xlabel("Year")
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.tight_layout()

        if output_file:
            plt.savefig(output_file)
            print(f"✅ Chart saved as {output_file}")
        else:
            plt.show()

    def plot_multiple(self, series_configs, output_file=None, title=None):
        """
            Plot multiple series on the same chart.

            series_configs: list of dicts with keys: 'name', 'label', 'color'
            Example: [{'name': 'unrate', 'label': 'Unemployment Rate (%)',
        'color': 'red'}]
        """
        plt.figure(figsize=(14, 6))

        for config in series_configs:
            df = self.load_series(config["name"])
            # Use short title for legend if label not provided
            label = config.get("label")
            if label is None:
                label = self.get_short_title(config["name"])
            plt.plot(
                df["date"].to_list(),
                df["value"].to_list(),
                label=label,
                color=config.get("color"),
                linewidth=2,
            )

        plt.title(title or "Economic Indicators", fontsize=14)
        plt.xlabel("Year")
        plt.ylabel("Value")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        if output_file:
            plt.savefig(output_file)
            print(f"✅ Chart saved as {output_file}")
        else:
            plt.show()

    # Usage examples:

    # # Single series
    # chart = EconomicChart()
    # chart.plot_single('cpiaucsl', 'cpi_chart.png', 'CPI - All Urban
    # Consumers', 'Index')

    # # Multiple series
    # chart.plot_multiple([
    #   {'name': 'unrate', 'label': 'Unemployment Rate (%)', 'color': 'red'},
    #   {'name': 'civpart', 'label': 'Labor Force Participation Rate (%)',
    # 'color': 'blue'}
    # ], 'labor_chart.png', 'U.S. Labor Market')
