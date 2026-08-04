# Collection

## Prerequisites

- [uv](https://docs.astral.sh/uv/) — Python package manager

## Installation

Install dependencies:

```bash
uv sync
```

Create a `.env` file with your FRED API key:

```bash
FRED_API_TOKEN=your_fred_api_key
```

A FRED API key is free. Register at [fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html).

## Data Sources

- **FRED (Federal Reserve Economic Data)**: CPI, GDP, Consumer Confidence, Unemployment, Household Debt
- **BLS (Bureau of Labor Statistics)**: Additional labor and economic statistics
- **NY Fed Consumer Credit Panel / Equifax**: Household debt by category (mortgage, HELOC, auto, credit card, student, other)
- **Yahoo Finance (via yfinance)**: Brent crude oil futures curve (estimated from WTI contracts + live Brent–WTI spread)

## Data Collected

### Core Economic Indicators

- **CPIAUCSL**: CPI - All Urban Consumers
- **GDP**: Gross Domestic Product
- **UMCSENT**: Consumer Confidence (U. Michigan)
- **UNRATE**: Unemployment Rate (U-3, official rate)
- **CIVPART**: Labor Force Participation Rate

### Alternative Unemployment Measures

- **U1RATE**: Persons unemployed 15 weeks or longer
- **U2RATE**: Job losers and persons who completed temporary jobs
- **U4RATE**: Total unemployed plus discouraged workers
- **U5RATE**: U-4 plus all other marginally attached to labor force
- **U6RATE**: U-5 plus employed part time for economic reasons (broadest measure)

### Unemployment by Age

- **LNS14000012**: Unemployment Rate - Ages 16-19
- **LNS14000036**: Unemployment Rate - Ages 20-24
- **LNS14000089**: Unemployment Rate - Ages 25-54
- **LNS14024230**: Unemployment Rate - Ages 55 and over

### Fed Funds & Treasury Rates

- **FEDFUNDS**: Federal Funds Effective Rate (monthly)
- **GS2, GS10, GS20, GS30**: Treasury Constant Maturity Rates — 2/10/20/30-Year (monthly)
- **DFEDTARU, DFEDTARL**: Federal Funds Target Range — Upper/Lower Limit (daily)

### Mortgage Rates

- **MORTGAGE30US**: 30-Year Fixed Rate Mortgage Average (Freddie Mac Primary Mortgage Market Survey, weekly since 1971)
- **MORTGAGE15US**: 15-Year Fixed Rate Mortgage Average (Freddie Mac PMMS, weekly since 1991)

Both are stored **downsampled**: full weekly resolution for the last 5 years, first observation of each month before that (see `SPARSE_SERIES` in `src/fred.py`). This keeps each CSV under ~30 KB while preserving the long-term shape for plotting.

Raw data is saved to `data/raw/` as CSV files, with metadata stored in `data/metadata.json`.

### Payrolls (BLS)

Collected via `uv run python main.py --source bls` (fetched directly from the BLS public API, not mirrored through FRED).

- **CES0000000001**: Total Nonfarm Payroll Employment (thousands of persons, seasonally adjusted)

Two derived series are computed by `Deriver`: the month-over-month change in thousands (`ces0000000001_chg`) and its 3-month rolling average (`ces0000000001_chg_3mo`), since the initial print is volatile and gets revised.

### Household Debt

All series are stored in **millions of dollars** and displayed as **trillions** in the dashboard.

| Series          | Description                                               | Frequency | Coverage                      |
| --------------- | --------------------------------------------------------- | --------- | ----------------------------- |
| **HHMSDODNS**   | Home Mortgages (1–4 family residential); Liability, Level | Quarterly | 1945–present                  |
| **REVOLSL**     | Revolving Consumer Credit — primarily credit cards        | Monthly   | 1968–present                  |
| **SLOAS**       | Student Loans Owned and Securitized                       | Quarterly | 2006–Q4 2024 *(discontinued)* |
| **MVLOAS**      | Motor Vehicle Loans Owned and Securitized                 | Quarterly | 1943–Q4 2024 *(discontinued)* |
| **NONREVSL**    | Nonrevolving Consumer Credit (auto + student combined)    | Monthly   | 1943–present                  |

**Source**: Federal Reserve via FRED — [G.19 Consumer Credit](https://www.federalreserve.gov/releases/g19/) and [Z.1 Flow of Funds](https://www.federalreserve.gov/releases/z1/).

**Note on medical debt**: There is no standalone FRED time series for medical debt. It is embedded in "Other" in the NY Fed Consumer Credit Panel (see below).

---

### NY Fed Household Debt and Credit (Equifax-sourced)

Collected via `uv run python main.py --source nyfed`.

The NY Fed publishes a quarterly Excel workbook based on the NY Fed Consumer Credit Panel, a nationally representative 5% sample of Equifax credit bureau records. It has the most detailed public breakdown by debt category, including a separate "Other" that captures medical debt, personal loans, and retail financing.

**Report page**: [newyorkfed.org/microeconomics/hhdc](https://www.newyorkfed.org/microeconomics/hhdc)

**File downloaded**: `HHD_C_Report_YYYYQn.xlsx` — the collector auto-detects the latest available quarter or accepts `--nyfed-quarter 2024Q4`.

| Series                   | Description                                  | Coverage        |
| ------------------------ | -------------------------------------------- | --------------- |
| **nyfed_mortgage**       | Home mortgage balance                        | Q1 1999–present |
| **nyfed_he_revolving**   | Home equity revolving / HELOC balance        | Q1 1999–present |
| **nyfed_auto**           | Auto loan balance                            | Q1 1999–present |
| **nyfed_credit_card**    | Credit card balance                          | Q1 1999–present |
| **nyfed_student**        | Student loan balance                         | Q1 1999–present |
| **nyfed_other**          | Other debt — incl. medical, personal, retail | Q1 1999–present |
| **nyfed_total**          | Total household debt                         | Q1 1999–present |

Values in Excel are in **trillions of dollars**; stored in `data/raw/` as **millions** (×10⁶) for consistency with FRED series. The viz divides by 10⁶ before displaying.

The same workbook's "Page 12 Data" sheet provides **percent of balance 90+ days delinquent by loan type**, stored in percent:

| Series                          | Description                             | Coverage        |
| ------------------------------- | --------------------------------------- | --------------- |
| **nyfed_delinq_mortgage**       | Mortgage balance 90+ days delinquent    | Q1 2003–present |
| **nyfed_delinq_he_revolving**   | HELOC balance 90+ days delinquent       | Q1 2003–present |
| **nyfed_delinq_auto**           | Auto loan balance 90+ days delinquent   | Q1 2003–present |
| **nyfed_delinq_credit_card**    | Credit card balance 90+ days delinquent | Q1 2003–present |
| **nyfed_delinq_student**        | Student loan balance 90+ days delinquent — artificially low 2020–2024 while pandemic forbearance paused delinquency reporting | Q1 2003–present |
| **nyfed_delinq_other**          | Other debt balance 90+ days delinquent  | Q1 2003–present |
| **nyfed_delinq_total**          | All debt balance 90+ days delinquent    | Q1 2003–present |

---

### NY Fed Global Supply Chain Pressure Index (GSCPI)

Collected via `uv run python main.py --source gscpi`.

- **gscpi**: Monthly composite of global transportation costs (Baltic Dry, Harpex, airfreight) and PMI subcomponents (delivery times, backlogs, purchased inventories) across seven economies. Units are standard deviations from the historical average (0 = normal pressure). Coverage: January 1998–present, updated ~4th business day of each month.

**Source page**: [newyorkfed.org/research/policy/gscpi](https://www.newyorkfed.org/research/policy/gscpi). The download URL ends in `.xlsx` but the file is a legacy `.xls` workbook — parsed with `xlrd`. Month-end observation labels are stored as first-of-month dates for consistency with FRED monthly series.

The dashboard shows the NY Fed chart when data is present; otherwise falls back to the FRED-only chart.
