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
- `uv run python main.py --source ce` - Collect BLS Consumer Expenditure Survey spending by age of reference person
- `uv run python main.py --source nyfed` - Collect NY Fed household debt data
- `uv run python main.py --source gscpi` - Collect NY Fed Global Supply Chain Pressure Index
- `uv run python main.py --source oil` - Collect Brent crude oil futures curve
- `uv run python main.py --source snap` - Collect USDA SNAP national participation data
- `uv run python main.py --source medicare` - Collect CMS Medicare national total enrollment
- `uv run python main.py --source medicaid` - Collect CMS Medicaid & CHIP national total enrollment
- `uv run python main.py --source dfa` - Collect Fed Distributional Financial Accounts household net worth by wealth percentile
- `uv run python main.py --source treasury` - Collect Treasury Debt to the Penny total public debt outstanding
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

**src/ce.py (CeCollector):**

- Fetches BLS Consumer Expenditure Survey "total average annual expenditures by age of reference person" (CE table 1300) directly from the BLS public API
- Nine `CXUTOTALEXPLB04xxM` series (all consumer units + 8 age bands), all batched into ~5 requests to respect the unregistered API rate limit
- Saves annual `data/raw/ce_totalexp_*.csv` in current dollars, dated Jan 1 of each data year; coverage 1984–present

**src/nyfed.py (NyFedCollector):**

- Downloads the NY Fed quarterly household debt Excel workbook
- Extracts per-category balances (mortgage, HELOC, auto, credit card, student, other/medical)
- Saves as CSV in millions of dollars to match FRED series units
- Also extracts delinquency, plus new bankruptcies by age of filer — the age bands go to a **wide** CSV (`nyfed_bankruptcy_by_age.csv`, one column per band) since they only mean anything read together, alongside the tidy national `nyfed_bankruptcy_total`
- The bands never sum to the national total (filers with unknown birth years are in the total but in no band — up to 13% apart in the early 2000s, ~0.2% today; one quarter runs the other way), so charts must use `nyfed_bankruptcy_total` for a total line

**src/gscpi.py (GscpiCollector):**

- Downloads the NY Fed Global Supply Chain Pressure Index workbook (legacy .xls, parsed with xlrd)
- Saves monthly index values (standard deviations from average) since 1998

**src/oil.py (OilCollector):**

- Fetches WTI crude oil futures curve from Yahoo Finance via `yfinance`
- Applies the live Brent-WTI spread to produce an estimated Brent futures curve

**src/snap.py (SnapCollector):**

- Downloads USDA's per-fiscal-year SNAP National Data Bank workbook archive (zip)
- Extracts national monthly persons-participating from each workbook's "US Summary" sheet
- Saves `snap_persons.csv`; covers October 1988–present

**src/medicare.py (MedicareCollector):**

- Fetches national monthly Medicare enrollment from the CMS data.cms.gov public API
- Saves `medicare_total_enrollment.csv`; covers January 2013–present

**src/medicaid.py (MedicaidCollector):**

- Fetches state-level monthly Medicaid & CHIP enrollment from the CMS Performance Indicator dataset via the data.medicaid.gov datastore API (stable dataset id, not a dated filename)
- Prefers each state's final report over its preliminary one, then sums nationally
- Saves `medicaid_chip_enrollment.csv`; covers September 2013 and June 2017–present (gap in between)

**src/dfa.py (DfaCollector):**

- Downloads the Federal Reserve Distributional Financial Accounts bulk archive (`dfa.zip`) and extracts `dfa-networth-levels.csv`
- Writes a **wide** CSV — one column per wealth percentile group instead of the usual single `value` column — since the groups only mean anything read together as a distribution
- The Fed publishes five groups; the top 0.1% and next 0.9% are summed into one top-1% column
- Saves `fed_dfa_wealth_by_percentile.csv` in millions of dollars; quarterly, covers 1989:Q3–present

**src/treasury.py (TreasuryCollector):**

- Fetches total public debt outstanding from the Treasury Fiscal Data "Debt to the Penny" API (v2; v1 is retired)
- Pages through the full history using the API's own page count
- Saves `treasury_national_debt.csv` in dollars; daily (business days), covers April 1993–present
- For years before 1993, and for a quarterly series aligned to the DFA wealth quarters, the dashboard uses FRED's `GFDEBTN` instead

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

- **viz/src/routes/+page.server.js** - Loads raw and derived CSVs at build time; exposes `data.series` and `data.metadata` to the page. Wide CSVs (the DFA wealth file and the NY Fed bankruptcy-by-age file) load through `loadWideCsvOptional` and arrive as `data.wealth` and `data.bankruptcyByAge`; the daily Treasury debt file is read last-line-only as `data.treasuryDebtLatest` so 8k rows don't ship to the client
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

- **data/raw/\*.csv** - Raw time series data (date, value columns; `fed_dfa_wealth_by_percentile.csv` and `nyfed_bankruptcy_by_age.csv` are wide, with one column per group)
- **data/raw/SOURCES.md** - Provenance for the wealth and debt datasets (exact URLs, retrieval dates, known gaps)
- **data/derived/\*.csv** - Computed series (YoY rates, etc.) produced by `Deriver`
- **data/metadata.json** - Series metadata (units, titles, frequency, seasonal adjustment)
- All data files are committed to git for version control and change tracking

## Economic Indicators Tracked

See `docs/collection.md` for the full catalog. Key series:

**Labor Market:** UNRATE (U-3), U1RATE-U6RATE, CIVPART, initial/continued jobless claims, unemployment by age group (LNS series)

**Economy:** GDP, CPIAUCSL (+ core/PCE/PPI variants), UMCSENT, real disposable income (W875RX1)

**Consumer Spending by Age (BLS CE Survey):** ce_totalexp_all + ce_totalexp_{lt25,25_34,35_44,45_54,55_64,65up,65_74,75up} — total average annual expenditures per consumer unit by age of reference person, annual since 1984

**Household Debt (FRED):** HHMSDODNS (mortgage), REVOLSL (credit cards), NONREVSL (auto+student)

**Household Debt (NY Fed/Equifax):** nyfed_mortgage, nyfed_auto, nyfed_credit_card, nyfed_student, nyfed_other, nyfed_total

**Delinquency (NY Fed/Equifax):** nyfed_delinq_* — percent of balance 90+ days delinquent per loan type (mortgage, HELOC, auto, credit_card, student, other, total)

**Bankruptcy (NY Fed/Equifax):** nyfed_bankruptcy_by_age — consumers entering bankruptcy by age band (18-29, 30-39, 40-49, 50-59, 60-69, 70+), quarterly since 2000:Q1, whole persons, wide CSV; nyfed_bankruptcy_total — the national figure, quarterly since 2003:Q1. No US agency publishes *cause* of filing, and BLS publishes no bankruptcy data at all.

**Mortgage Rates:** MORTGAGE30US, MORTGAGE15US (Freddie Mac PMMS weekly; stored downsampled — weekly last 5 years, monthly before)

**Commodities:** Brent crude oil futures curve (estimated from WTI via Yahoo Finance), GASREGW/GASDESW (EIA weekly national retail gasoline/diesel prices via FRED)

**Supply Chain:** gscpi — NY Fed Global Supply Chain Pressure Index (monthly, std devs from average)

**Social Programs:** snap_persons (USDA, national SNAP participants, monthly since Oct 1988), medicare_total_enrollment (CMS, national Medicare beneficiaries, monthly since Jan 2013), medicaid_chip_enrollment (CMS, national Medicaid+CHIP enrollees, monthly since Jun 2017 with a Sep 2013 data point)

**Household Wealth (Fed DFA):** fed_dfa_wealth_by_percentile — household net worth by wealth percentile (top 1%, 90th–99th, 50th–90th, bottom 50%), quarterly since 1989:Q3, millions of dollars, wide CSV

**Government Debt:** treasury_national_debt (Treasury Debt to the Penny, daily since April 1993, dollars), GFDEBTN (FRED, quarterly end-of-period since 1966, millions of dollars)

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
