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
- **NY Fed Consumer Credit Panel / Equifax**: Household debt by category (mortgage, HELOC, auto, credit card, student, other), delinquency, and new bankruptcies by age
- **Yahoo Finance (via yfinance)**: Brent crude oil futures curve (estimated from WTI contracts + live Brent–WTI spread)
- **USDA Food and Nutrition Service**: SNAP national participation (persons)
- **CMS (Centers for Medicare & Medicaid Services)**: Medicare national total enrollment, Medicaid & CHIP national total enrollment

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

### Regional Manufacturing Surveys (ISM PMI Proxies)

- **GACDFSA066MSFRBPHI**: Philadelphia Fed Manufacturing Business Outlook Survey — Current General Activity, diffusion index (monthly since 1968)
- **GACDISA066MSFRBNY**: Empire State (NY Fed) Manufacturing Survey — Current General Business Conditions, diffusion index (monthly since 2001)
- **BACTSAMFRBDAL**: Dallas Fed Texas Manufacturing Outlook Survey — Current General Business Activity, diffusion index (monthly since 2004)

All three are seasonally adjusted diffusion indexes: positive values indicate expansion, negative values contraction, 0 is the breakeven point.

**Why these instead of the ISM Manufacturing PMI**: ISM's own PMI is a paid, copyrighted product. FRED discontinued its `NAPM` mirror of the series in 2016 after a licensing dispute with ISM, and ISM's website only publishes the current month's headline figure (no bulk history, no API). These three regional Fed surveys are the standard free proxies economists watch ahead of the ISM release each month — they're freely licensed, historical, and directionally track the national PMI closely.

### Payrolls (BLS)

Collected via `uv run python main.py --source bls` (fetched directly from the BLS public API, not mirrored through FRED).

- **CES0000000001**: Total Nonfarm Payroll Employment (thousands of persons, seasonally adjusted)

Two derived series are computed by `Deriver`: the month-over-month change in thousands (`ces0000000001_chg`) and its 3-month rolling average (`ces0000000001_chg_3mo`), since the initial print is volatile and gets revised.

### Consumer Spending by Age (BLS Consumer Expenditure Survey)

Collected via `uv run python main.py --source ce` (fetched directly from the BLS public API, not mirrored through FRED — FRED only carries the 2020+ vintage of these series).

Total average annual expenditures per consumer unit, broken out by the age of the reference person (CE table 1300). Annual, not seasonally adjusted, in current dollars. Coverage: 1984–present (the combined "65 and older" band starts 1988). Data for calendar year Y is published by BLS in September of year Y+1; the observation date is stored as January 1 of year Y.

| Series                  | BLS ID              | Age of reference person |
| ----------------------- | ------------------- | ----------------------- |
| **ce_totalexp_all**     | CXUTOTALEXPLB0401M  | All consumer units (baseline) |
| **ce_totalexp_lt25**    | CXUTOTALEXPLB0402M  | Under 25                |
| **ce_totalexp_25_34**   | CXUTOTALEXPLB0403M  | 25 to 34                |
| **ce_totalexp_35_44**   | CXUTOTALEXPLB0404M  | 35 to 44                |
| **ce_totalexp_45_54**   | CXUTOTALEXPLB0405M  | 45 to 54                |
| **ce_totalexp_55_64**   | CXUTOTALEXPLB0406M  | 55 to 64                |
| **ce_totalexp_65up**    | CXUTOTALEXPLB0407M  | 65 and older            |
| **ce_totalexp_65_74**   | CXUTOTALEXPLB0408M  | 65 to 74                |
| **ce_totalexp_75up**    | CXUTOTALEXPLB0409M  | 75 and older            |

**Source page**: [bls.gov/cex/tables.htm](https://www.bls.gov/cex/tables.htm). All nine series are requested in a single batched API call per 10-year window (~5 calls total) to stay under the unregistered BLS API's 25-requests-per-day limit.

### Wage Growth

- **CES0500000003**: Average Hourly Earnings of All Employees, Total Private (dollars/hour, seasonally adjusted, monthly since March 2006)

`Deriver` computes `ces0500000003_yoy`, the year-over-year percent change — the standard "wage growth" figure reported in the news. The viz dashboard's "Wage Growth vs. Inflation" chart plots it against CPI YoY inflation (`cpiaucsl_yoy`) and 1-year inflation expectations (`MICH`) so you can see whether pay is keeping pace with prices.

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

The same workbook's "Page 30 Data" sheet provides **consumers entering bankruptcy
by age of the filer**. The six age bands are an ordered distribution that only
means anything read together, so they are stored as a single **wide** CSV — one
column per band — rather than one file per band:

| File                                | Columns                                                              | Coverage        |
| ----------------------------------- | -------------------------------------------------------------------- | --------------- |
| **nyfed_bankruptcy_by_age.csv**     | `age_18_29`, `age_30_39`, `age_40_49`, `age_50_59`, `age_60_69`, `age_70up` | Q1 2000–present |

"Page 17 Data" supplies the matching national figure:

| Series                       | Description                                  | Coverage        |
| ---------------------------- | -------------------------------------------- | --------------- |
| **nyfed_bankruptcy_total**   | Consumers with a new bankruptcy, national     | Q1 2003–present |

Both are published in **thousands of consumers** and stored as **whole persons**
(×10³). The viz divides by 10³ before displaying.

**The age bands do not sum to the national total.** Filers whose birth year is
unknown are counted in the total but fall into no band, so the bands sum to as
much as 13% below it in the early 2000s, narrowing to ~0.2% today. The two come
from separately computed sheets, so the gap is not strictly one-signed — in
2024:Q3 the bands run 1.4% *above* the total. Use `nyfed_bankruptcy_total`
whenever a total is needed — never the band sum.

The Q4 2005 spike in every band is the filing rush ahead of BAPCPA, which
tightened Chapter 7 eligibility on 17 October 2005.

**On age and cause**: this is the only regularly updated US series that breaks
consumer bankruptcy down by age. No statistical agency — BLS included — publishes
one, and none publishes *cause* of filing at all: bankruptcy petitions do not
record a reason. Survey estimates of cause (income loss, medical debt) come from
the academic Consumer Bankruptcy Project, which has no machine-readable feed.

---

### NY Fed Global Supply Chain Pressure Index (GSCPI)

Collected via `uv run python main.py --source gscpi`.

- **gscpi**: Monthly composite of global transportation costs (Baltic Dry, Harpex, airfreight) and PMI subcomponents (delivery times, backlogs, purchased inventories) across seven economies. Units are standard deviations from the historical average (0 = normal pressure). Coverage: January 1998–present, updated ~4th business day of each month.

**Source page**: [newyorkfed.org/research/policy/gscpi](https://www.newyorkfed.org/research/policy/gscpi). The download URL ends in `.xlsx` but the file is a legacy `.xls` workbook — parsed with `xlrd`. Month-end observation labels are stored as first-of-month dates for consistency with FRED monthly series.

---

### SNAP Participation (USDA Food and Nutrition Service)

Collected via `uv run python main.py --source snap`.

- **snap_persons**: National count of persons participating in SNAP (Supplemental Nutrition Assistance Program), monthly. Coverage: October 1988–present.

**Source page**: [fna.usda.gov/pd/supplemental-nutrition-assistance-program-snap](https://www.fna.usda.gov/pd/supplemental-nutrition-assistance-program-snap). The collector downloads USDA's zip archive of per-fiscal-year National Data Bank workbooks (`snap-zip-fy69tocurrent`) and extracts the "US Summary" sheet's Persons column from each. Fiscal years 1969–1988 use a different, hand-formatted national-only layout and are skipped, since FY1989 onward already gives 35+ years of consistent monthly history. The most recent 1–2 months in each fiscal year are preliminary and subject to revision.

---

### Medicare Total Enrollment (CMS)

Collected via `uv run python main.py --source medicare`.

- **medicare_total_enrollment**: National count of total Medicare beneficiaries (Original Medicare + Medicare Advantage/other plans) with hospital/medical coverage, monthly. Coverage: January 2013–present.

**Source page**: [data.cms.gov — Medicare Monthly Enrollment](https://data.cms.gov/summary-statistics-on-beneficiary-enrollment/medicare-and-medicaid-reports/medicare-monthly-enrollment). Pulled from the dataset's public API, filtered to `BENE_GEO_LVL=National` and the `TOT_BENES` column; annual-average rows (`MONTH=Year`) are excluded.

---

### Household Wealth by Percentile (Federal Reserve DFA)

Collected via `uv run python main.py --source dfa`.

- **fed_dfa_wealth_by_percentile**: Household net worth by wealth percentile group, quarterly, in millions of dollars. Coverage: 1989:Q3–present.

Unlike every other file in `data/raw/`, this one is **wide**: `date` plus one column per percentile group (`top_1pct`, `pct_90_99`, `pct_50_90`, `bottom_50pct`), because the groups are only meaningful read together as a distribution.

**Source page**: [federalreserve.gov — Distributional Financial Accounts](https://www.federalreserve.gov/releases/z1/dataviz/dfa/). The DFA bulk archive (`dfa.zip`) is downloaded and `dfa-networth-levels.csv` extracted from it. The Fed publishes five groups — top 0.1%, next 0.9%, next 9%, next 40%, bottom 50% — and the first two are summed into a single top-1% column; units are left as published. Quarters labelled `1989:Q3` are stored as the first day of the quarter (`1989-07-01`), matching how FRED dates the equivalent `WFRBL*` series, though the value is the level at the quarter's **end**.

---

### National Debt (U.S. Treasury)

Collected via `uv run python main.py --source treasury`.

- **treasury_national_debt**: Total public debt outstanding, in dollars, for every business day. Coverage: 1993-04-01–present.

**Source page**: [fiscaldata.treasury.gov — Debt to the Penny](https://fiscaldata.treasury.gov/datasets/debt-to-the-penny/). Pulled from the `v2` Fiscal Data API (the `v1` path for this dataset returns 404), paging through the full history using the API's own page count. Business days only — gaps between consecutive dates are weekends and federal holidays, not missing data.

This dataset does not reach back before April 1993. For the 1989–1993 stretch, and for a quarterly series that lines up with the DFA wealth quarters, the dashboard uses **GFDEBTN** (FRED, Federal Debt: Total Public Debt, quarterly end-of-period, millions of dollars, back to 1966) which is collected with the other FRED series. The two agree exactly at quarter ends.

---

### Medicaid & CHIP Enrollment (CMS)

Collected via `uv run python main.py --source medicaid`.

- **medicaid_chip_enrollment**: National count of Medicaid + CHIP enrollees, summed across all states and DC, monthly. Coverage: September 2013 (single month), then June 2017–present — states did not consistently report this indicator at monthly granularity in between.

**Source page**: [medicaid.gov — Medicaid & CHIP Enrollment Data](https://www.medicaid.gov/medicaid/national-medicaid-chip-program-information/medicaid-chip-enrollment-data). Pulled from the CMS Performance Indicator dataset via its stable `data.medicaid.gov` datastore API (the underlying CSV is republished under a new dated filename each month, so the API — keyed by dataset id, not filename — is used instead). Each state reports one row per month, sometimes both a preliminary ("P") and a later final ("Y") report for the same period; the final report is preferred when both exist, since the preliminary one is often revised significantly.

The dashboard shows the NY Fed chart when data is present; otherwise falls back to the FRED-only chart.
