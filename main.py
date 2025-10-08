
# import polars as pl
# import matplotlib.pyplot as plt
import os

# from datetime import datetime
# from fredapi import Fred
# from dotenv import load_dotenv

from src.cli import Cli
from src.config import Config
from src.fred import FredCollector
from src.bls import BlsCollector

# load_dotenv()

# fred = Fred(api_key=os.getenv("FRED_API_TOKEN"))
# start = datetime(2000, 1, 1)
# end = datetime.today()

# unrate = fred.get_series('UNRATE', start, end)
# lfpr = fred.get_series('CIVPART', start, end)

# # Convert to Polars DataFrames
# df_unrate = pl.DataFrame({
#   "date": unrate.index.to_list(),
#   "unemployment_rate": unrate.to_list()
# })
# df_lfpr = pl.DataFrame({
#   "date": lfpr.index.to_list(),
#   "lfpr": lfpr.to_list()
# })

# # Join on date
# df = df_unrate.join(df_lfpr, on="date", how="inner")

# # Plot
# plt.figure(figsize=(14, 6))
# plt.plot(df["date"].to_list(), df["unemployment_rate"].to_list(), label="Unemployment Rate (%)", color="red", linewidth=2)
# plt.plot(df["date"].to_list(), df["lfpr"].to_list(), label="Labor Force Participation Rate (%)", color="blue", linewidth=2)

# plt.title("U.S. Labor Market: Unemployment Rate vs Labor Force Participation Rate", fontsize=14)
# plt.xlabel("Year")
# plt.ylabel("Percentage")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.savefig("labor_chart.png")
# print("✅ Chart saved as labor_chart.png")


def main():
  cli = Cli()
  config = Config()
  errors, valid = config.verify()
  if not valid:
    print(f"❌ Configuration errors:\n{errors}")
    return
  args = cli.run()
  if args.source in ['fred', 'all']:
    fred_key = config.get_fred_key()
    if not fred_key:
      print("❌ FRED_API_TOKEN not found in environment")
      return

    fred_collector = FredCollector(fred_key, args.output)
    if args.series:
      fred_collector.collect_series(args.series, args.series)
    else:
      fred_collector.collect_all()

  if args.source in ['bls', 'all']:
    bls_collector = BlsCollector(args.output)

    if args.series:
      bls_collector.collect_series(args.series, args.series)


if __name__ == '__main__':
  main()
