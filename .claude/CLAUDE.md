# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

US economic data from FRED, BLS, NY Fed, and Yahoo Finance. Raw series stored as CSV in git, derived metrics computed on top, with a README dashboard and a SvelteKit viz deployed to GitHub Pages.

## Code Style

- Use 2-space indentation
- Follow PEP 8 naming conventions
- Use Polars for data manipulation (not Pandas)

## Setup

1. Install dependencies: `uv sync`
2. Create `.env` file with: `FRED_API_TOKEN=your_fred_api_key`
3. Config validation happens automatically via `Config` class in `src/config.py`

## Commands

**Data Collection:**

- `uv run python main.py --source fred` - Collect all FRED data
- `uv run python main.py --source bls` - Collect BLS data
- `uv run python main.py --source nyfed` - Collect NY Fed household debt data
- `uv run python main.py --source oil` - Collect Brent crude oil futures curve
- `uv run python main.py --source all` - Collect from all sources
- `uv run python main.py --source fred --series CPIAUCSL` - Collect specific series

**Derived Series:**

- `uv run python main.py --derive` - Compute derived series (YoY inflation, etc.) from raw data into `data/derived/`

**Visualization (matplotlib charts):**

- `uv run python main.py --plot unrate` - Plot single series
- `uv run python main.py --plot unrate civpart` - Plot multiple series
- `uv run python main.py --plot unrate --plot-output chart.png --plot-title "Custom Title"`

**README Dashboard:**

- `uv run python -m src.readme_updater` - Regenerate the economic dashboard in README.md

**SvelteKit Viz (viz/):**

- `cd viz && pnpm install && pnpm dev` - Run interactive viz locally
- `cd viz && pnpm build` - Build for deployment

## Architecture

### Data Flow

1. **Collection** → API data fetched via collector classes and saved as CSV to `data/raw/`
2. **Derivation** → `Deriver` computes YoY inflation and other derived series into `data/derived/`
3. **Dashboard** → `src/readme_updater.py` rebuilds the README table with sparklines from raw CSVs
4. **Viz** → `viz/` SvelteKit app reads CSVs at build time and renders interactive D3 charts

### Key Components

**main.py** - Entry point that orchestrates CLI → Collector → Chart flow

**src/cli.py** - CLI argument parsing
**src/config.py** - Environment variable validation (checks FRED_API_TOKEN)

**src/fred.py (FredCollector):**

- Fetches data from FRED API using `fredapi` library
- Automatically fetches and stores series metadata (units, title, frequency, seasonal adjustment)
- Saves metadata to `data/metadata.json` for use by charting

**src/bls.py (BlsCollector):**

- Fetches data from BLS public API; no authentication required

**src/nyfed.py (NyFedCollector):**

- Downloads the NY Fed quarterly household debt Excel workbook
- Extracts per-category balances (mortgage, HELOC, auto, credit card, student, other/medical)
- Saves as CSV in millions of dollars to match FRED series units

**src/oil.py (OilCollector):**

- Fetches WTI crude oil futures curve from Yahoo Finance via `yfinance`
- Applies the live Brent-WTI spread to produce an estimated Brent futures curve

**src/derive.py (Deriver):**

- Computes derived series from raw CSVs (YoY inflation, income growth)
- Writes results to `data/derived/`

**src/sparkline.py:**

- Builds Unicode block-character sparklines for the README dashboard
- `build_dashboard()` generates the full Markdown table inserted into README.md

**src/readme_updater.py:**

- Replaces the `<!-- ECONOMIC-DATA-START/END -->` block in README.md with a fresh dashboard
- Run automatically by the GitHub Actions update workflow after each data collection

**src/chart.py (EconomicChart):**

- Matplotlib-based chart generator; reads CSV + metadata
- Methods: `plot_single()`, `plot_multiple()`

### Viz Layer (viz/)

SvelteKit 2 / Svelte 5 app deployed to GitHub Pages via `deploy-viz.yml`.

- **viz/src/routes/+page.server.js** - Loads raw and derived CSVs at build time; exposes `data.series` and `data.metadata` to the page
- **viz/src/routes/+page.svelte** - Main dashboard page with D3 / svelteplot charts
- **viz/src/routes/LazyChart.svelte** - Intersection-observer-based lazy loading wrapper
- Uses `pnpm` as the package manager; `pnpm build` outputs to `viz/build/`

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

Charts and the README dashboard read this metadata for axis labels and titles.

## Data Storage

- **data/raw/\*.csv** - Raw time series data (date, value columns)
- **data/derived/\*.csv** - Computed series (YoY rates, etc.) produced by `Deriver`
- **data/metadata.json** - Series metadata (units, titles, frequency, seasonal adjustment)
- All data files are committed to git for version control and change tracking

## Economic Indicators Tracked

See `docs/collection.md` for the full catalog. Key series:

**Labor Market:** UNRATE (U-3), U1RATE-U6RATE, CIVPART, initial/continued jobless claims, unemployment by age group (LNS series)

**Economy:** GDP, CPIAUCSL (+ core/PCE/PPI variants), UMCSENT, real disposable income (W875RX1)

**Household Debt (FRED):** HHMSDODNS (mortgage), REVOLSL (credit cards), NONREVSL (auto+student)

**Household Debt (NY Fed/Equifax):** nyfed_mortgage, nyfed_auto, nyfed_credit_card, nyfed_student, nyfed_other, nyfed_total

**Commodities:** Brent crude oil futures curve (estimated from WTI via Yahoo Finance)

**Derived:** YoY inflation rates for CPI/PCE/PPI series, income YoY growth

## Tech Stack

**Python backend:**
- `uv`: package manager (pyproject.toml, no requirements.txt)
- Python 3.13
- `polars`: data manipulation
- `fredapi`: FRED API client
- `requests`: BLS and NY Fed HTTP requests
- `openpyxl`: NY Fed Excel workbook parsing
- `yfinance`: oil futures data from Yahoo Finance
- `matplotlib`: static chart generation
- `python-dotenv`: `.env` file loading

**Viz frontend (viz/):**
- SvelteKit 2 / Svelte 5
- D3 7 + svelteplot
- Vite 8
- pnpm

**CI (GitHub Actions):**
- `update.yml`: daily data collection, freshness tests, README dashboard update, git commit
- `deploy-viz.yml`: builds SvelteKit app and deploys to GitHub Pages
- `lint.yml`: pre-commit checks

## Development Philosophy

- Start with practical implementation first
- Refactor into classes when patterns emerge
- CLI-based tools for all operations
- Separate collection from visualization
- Focus on long-term economic trends
- Keep data format simple (CSV) for version control
