# Economics Data Collection Project

## Code Style

- Use 2-space indentation
- Follow PEP 8 naming conventions
- Use Polars for data manipulation (not Pandas)

## Data Sources

- FRED API for CPI, GDP, consumer confidence, unemployment
- BLS API for additional labor statistics
- Store raw data in data/raw/ as CSV files
- Collect data from earliest available date

## Project Goals

- Collect historical US economic data for long-term understanding
- Focus on long-term economic trends
- Keep data format simple (CSV) for version control
- Data should be committed to git repository

## Architecture

- Start with practical implementation first
- Refactor into classes later when patterns emerge
- CLI-based data collection tools
- Separate collection from visualization

## Commands

- `python collect.py --source fred` - Collect all FRED data
- `python collect.py --source all` - Collect from all sources
- `python collect.py --series CPIAUCSL` - Collect specific series
- `python main.py` - Generate labor market visualization

## Economic Indicators Tracked

- **CPIAUCSL**: CPI - All Urban Consumers
- **GDP**: Gross Domestic Product
- **UMCSENT**: Consumer Confidence (U. Michigan)
- **UNRATE**: Unemployment Rate
- **CIVPART**: Labor Force Participation Rate
