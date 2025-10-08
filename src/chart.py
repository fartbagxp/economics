import polars as pl
import matplotlib.pyplot as plt

from pathlib import Path

class EconomicChart:
  def __init__(self, data_dir="data/raw"):
    self.data_dir = Path(data_dir)

  def load_series(self, series_name):
    """Load a CSV file for a given series (e.g., 'cpiaucsl', 'unrate')."""
    file_path = self.data_dir / f"{series_name.lower()}.csv"
    df = pl.read_csv(file_path)
    df = df.with_columns(pl.col("date").str.to_datetime())
    return df

  def plot_single(self, series_name, output_file=None, title=None, 
ylabel="Value"):
    """Plot a single economic series."""
    df = self.load_series(series_name)

    plt.figure(figsize=(14, 6))
    plt.plot(df["date"].to_list(), df["value"].to_list(), linewidth=2)
    plt.title(title or f"{series_name.upper()}", fontsize=14)
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
      df = self.load_series(config['name'])
      plt.plot(
        df["date"].to_list(),
        df["value"].to_list(),
        label=config.get('label', config['name'].upper()),
        color=config.get('color'),
        linewidth=2
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
