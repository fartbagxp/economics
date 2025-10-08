import argparse

class Cli:
  def run(self):
    parser = argparse.ArgumentParser(description='Collect US economic data')
    parser.add_argument(
      '--source',
      choices=['fred', 'bls', 'all'],
      default='all',
      help='Data source to collect from'
    )
    parser.add_argument(
      '--series',
      help='Specific series ID to collect'
    )
    parser.add_argument(
      '--output',
      default='data/raw',
      help='Output directory for CSV files'
    )

    args = parser.parse_args()
    return args
