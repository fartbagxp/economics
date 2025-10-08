# Economics

US economic data collection and analysis project using FRED and BLS data sources.

## Data Sources

- **FRED (Federal Reserve Economic Data)**: CPI, GDP, Consumer Confidence, Unemployment
- **BLS (Bureau of Labor Statistics)**: Additional labor and economic statistics

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create `.env` file with API keys:

```
FRED_API_TOKEN=your_fred_api_key
BLS_API_KEY=your_bls_api_key (optional)
```

## Usage

Collect all data from FRED:

```bash
python collect.py --source fred
```

Collect from all sources:

```bash
python collect.py --source all
```

Collect specific series:

```bash
python collect.py --source fred --series CPIAUCSL
```

## Data Collected

- **CPIAUCSL**: CPI - All Urban Consumers
- **GDP**: Gross Domestic Product
- **UMCSENT**: Consumer Confidence (U. Michigan)
- **UNRATE**: Unemployment Rate
- **CIVPART**: Labor Force Participation Rate

Raw data is saved to `data/raw/` as CSV files.
