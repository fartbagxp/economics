# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

US economic data collection and analysis project. Collects historical data from FRED and BLS APIs, stores as CSV files in git, and generates visualizations.

## Code Style

- Use 2-space indentation
- Follow PEP 8 naming conventions
- Use Polars for data manipulation (not Pandas)

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Create `.env` file with: `FRED_API_TOKEN=your_fred_api_key`
3. Config validation happens automatically via `Config` class in `src/config.py`

## Commands

**Data Collection:**
- `python main.py --source fred` - Collect all FRED data
- `python main.py --source bls` - Collect BLS data
- `python main.py --source all` - Collect from all sources
- `python main.py --source fred --series CPIAUCSL` - Collect specific series

**Visualization:**
- `python main.py --plot unrate` - Plot single series
- `python main.py --plot unrate civpart` - Plot multiple series
- `python main.py --plot unrate --plot-output chart.png --plot-title "Custom Title"`

## Architecture

### Data Flow

1. **Collection** → API data fetched via collector classes (`FredCollector`, `BlsCollector`)
2. **Storage** → Raw data saved as CSV to `data/raw/`, metadata to `data/metadata.json`
3. **Visualization** → Charts generated via `EconomicChart` class reading CSV + metadata

### Key Components

**main.py** - Entry point that orchestrates CLI → Collector → Chart flow

**src/cli.py** - CLI argument parsing
**src/config.py** - Environment variable validation (checks FRED_API_TOKEN)

**src/fred.py (FredCollector):**
- Fetches data from FRED API using `fredapi` library
- Automatically fetches and stores series metadata (units, title, frequency, seasonal adjustment)
- Saves metadata to `data/metadata.json` for use by charting

**src/bls.py (BlsCollector):**
- Fetches data from BLS public API
- No authentication required
- Does not yet store metadata (future enhancement)

**src/chart.py (EconomicChart):**
- Loads metadata from `data/metadata.json` on initialization
- Automatically uses correct units for Y-axis labels (e.g., "Percent" for UNRATE)
- Falls back to "Value" if metadata unavailable
- Methods: `plot_single()`, `plot_multiple()`

### Metadata System

When collecting FRED data, metadata is automatically fetched and stored in `data/metadata.json` with structure:
```json
{
  "seriesid": {
    "title": "Full Series Title",
    "units": "Percent|Index|Billions of Dollars|etc",
    "frequency": "Monthly|Quarterly|etc",
    "seasonal_adjustment": "Seasonally Adjusted|Not Seasonally Adjusted",
    "last_updated": "ISO date string"
  }
}
```

Charts automatically read this metadata to set Y-axis labels and titles. Can be overridden via CLI args.

## Data Storage

- **data/raw/*.csv** - Time series data (date, value columns)
- **data/metadata.json** - Series metadata (units, titles, etc.)
- Both are committed to git for version control and tracking changes over time

## Economic Indicators Tracked

- **CPIAUCSL**: CPI - All Urban Consumers
- **GDP**: Gross Domestic Product
- **UMCSENT**: Consumer Confidence (U. Michigan)
- **UNRATE**: Unemployment Rate
- **CIVPART**: Labor Force Participation Rate

## Development Philosophy

- Start with practical implementation first
- Refactor into classes when patterns emerge
- CLI-based tools for all operations
- Separate collection from visualization
- Focus on long-term economic trends
- Keep data format simple (CSV) for version control
