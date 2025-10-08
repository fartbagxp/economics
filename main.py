from src.cli import Cli
from src.config import Config
from src.fred import FredCollector
from src.bls import BlsCollector
from src.chart import EconomicChart

def main():
  cli = Cli()
  config = Config()
  errors, valid = config.verify()
  if not valid:
    print(f"❌ Configuration errors:\n{errors}")
    return
  args = cli.run()

  # Handle plotting
  if args.plot:
    chart = EconomicChart(args.output)
    if len(args.plot) == 1:
      chart.plot_single(
        args.plot[0],
        args.plot_output,
        args.plot_title
      )
    else:
      series_configs = [{'name': series} for series in args.plot]
      chart.plot_multiple(
        series_configs,
        args.plot_output,
        args.plot_title
      )
    return

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
