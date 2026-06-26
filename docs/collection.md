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

Raw data is saved to `data/raw/` as CSV files, with metadata stored in `data/metadata.json`.

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

The dashboard shows the NY Fed chart when data is present; otherwise falls back to the FRED-only chart.
