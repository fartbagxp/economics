<p align="center">
  <img src="viz/static/apple-touch-icon.png" width="72" height="72" alt="Economics logo">
</p>

# Economics

US economic data from FRED, BLS, NY Fed, and Yahoo Finance. Time series stored as CSV in git, with derived metrics and an interactive SvelteKit dashboard.

<p>
  <a href="https://github.com/fartbagxp/economics/actions/workflows/update.yml"><img src="https://img.shields.io/github/actions/workflow/status/fartbagxp/economics/update.yml?label=data%20update&style=flat-square" alt="Data Update"></a>
  <a href="https://github.com/fartbagxp/economics/actions/workflows/deploy-viz.yml"><img src="https://img.shields.io/github/actions/workflow/status/fartbagxp/economics/deploy-viz.yml?label=deploy%20viz&style=flat-square" alt="Deploy Viz"></a>
  <a href="https://github.com/fartbagxp/economics/actions/workflows/lint.yml"><img src="https://img.shields.io/github/actions/workflow/status/fartbagxp/economics/lint.yml?label=lint&style=flat-square" alt="Lint"></a>
  <a href="https://fartbagxp.github.io/economics/"><img src="https://img.shields.io/badge/dashboard-live-brightgreen?style=flat-square" alt="Live Dashboard"></a>
  <!-- DATASET-COUNT --><img src="https://img.shields.io/badge/datasets-98-blue?style=flat-square" alt="98 datasets"><!-- /DATASET-COUNT -->
</p>

- [Setup](docs/setup.md): how to run the repo
- [Collection](docs/collection.md): what data is collected and where it comes from
- [Dashboard](https://fartbagxp.github.io/economics/): interactive vizualization

<!-- ECONOMIC-DATA-START -->
## Economic Dashboard

_Last updated: 2026-10-31 21:23 UTC_

_Sparklines show the last 24 data points (monthly or annual), 52 points (weekly), or 8 points (quarterly)._

### Labor Market Overview

| Indicator                 | Trend                      | Latest    | Chg (prev) | Chg (1Y) | As of      |
| ------------------------- | -------------------------- | --------- | ---------- | -------- | ---------- |
| Unemployment Rate (U-3)   | `▂▂▃▂▁▃▃▃▅▂▅▅▆█▆▅▆▅▅▅▃▂▂▃` | 4.2%      | +0.1pp     | -0.1pp   | 2026-09-01 |
| Total Nonfarm Payrolls    | `▁▁▃▃▃▃▄▄▄▄▄▄▃▄▄▅▄▅▆▆▇▆▇█` | 159,044K  | +29K       | +496K    | 2026-09-01 |
| Labor Force Participation | `█▆▆▆▇▆▆▇▆▅▅▅▆▆▆▄▄▃▃▃▁▁▂▃` | 61.8%     | +0.2pp     | -0.5pp   | 2026-09-01 |
| Initial Jobless Claims    | `▄▄▇█▇▅▅▅▄▁▂▂▄▄▃▄▄▂▂▂▂▂▂▁` | 194,000   | -1,000     | -27,000  | 2026-10-24 |
| Continued Claims          | `▅▅▅▅▆▇▇█▆▆▅▆▅▆▅▅▄▂▁▁▁▁▂▁` | 1,701,000 | -21,000    | -252,000 | 2026-10-17 |

### Unemployment Measures (U1–U6)

| Indicator                  | Trend                      | Latest | MoM    | YoY (12m) | As of      |
| -------------------------- | -------------------------- | ------ | ------ | --------- | ---------- |
| U-1: 15+ Weeks Unemployed  | `▃▅▅▃▁▁▁▃▁▃█▅██████▅██▅██` | 1.8%   | +0.0pp | +0.1pp    | 2026-09-01 |
| U-2: Job Losers            | `▁▄▄▁▁▄▁▄▄▁▄▄██▄██▄█▄▁▄▁▁` | 1.9%   | +0.0pp | -0.1pp    | 2026-09-01 |
| U-3: Official Rate         | `▂▂▃▂▁▃▃▃▅▂▅▅▆█▆▅▆▅▅▅▃▂▂▃` | 4.2%   | +0.1pp | -0.1pp    | 2026-09-01 |
| U-4: + Discouraged Workers | `▁▁▂▂▂▂▃▂▃▃▃▄▅█▄▄▄▃▄▄▃▂▂▂` | 4.4%   | +0.0pp | -0.2pp    | 2026-09-01 |
| U-5: + Marginally Attached | `▂▂▃▂▁▃▃▃▃▃▄▅▆█▅▄▅▅▅▅▄▃▃▂` | 5.0%   | -0.1pp | -0.3pp    | 2026-09-01 |
| U-6: + Part-Time Economic  | `▂▂▂▁▁▃▃▂▂▂▃▄▄█▆▄▃▃▅▄▃▃▂▁` | 7.6%   | -0.1pp | -0.5pp    | 2026-09-01 |

### Unemployment by Age

| Indicator  | Trend                      | Latest | MoM    | YoY (12m) | As of      |
| ---------- | -------------------------- | ------ | ------ | --------- | ---------- |
| Ages 16–19 | `▄▄▂▁▁▂▄▂▃▅▆▄▃█▇▃▅▃▅▅▅▁▄▅` | 14.5%  | +0.4pp | +0.6pp    | 2026-09-01 |
| Ages 20–24 | `▂▄▄▃▅▅▃▅▅▅▄██▅▅▂▃▁▃▃▂▂▂▅` | 8.0%   | +0.9pp | -1.2pp    | 2026-09-01 |
| Ages 25–54 | `▂▂▄▅▃▄▂▃▂▁▄▄▇█▄█▇▇▇▆▆▆▄▄` | 4.3%   | +0.0pp | -0.1pp    | 2026-09-01 |
| Ages 55+   | `▂▃▅▆▅▃▃▆▅▅▃▃▇▆▅▇██▅▅▂▆▅▁` | 2.6%   | -0.4pp | -0.3pp    | 2026-09-01 |

### Economy

| Indicator                          | Trend                      | Latest  | Chg (prev) | Chg (1Y) | As of      |
| ---------------------------------- | -------------------------- | ------- | ---------- | -------- | ---------- |
| GDP                                | `▁▁▁▂▂▃▃▃▄▄▄▄▅▅▅▅▆▆▆▆▇▇▇█` | $33,010 | +$447      | +$1,830  | 2026-07-01 |
| CPI (All Urban)                    | `▁▁▁▁▂▂▂▂▂▃▃▃▄▄▄▄▅▆▆▇▆▆▇█` | 336.30  | +2.17      | +13.01   | 2026-09-01 |
| Avg. Hourly Earnings (Wage Growth) | `▁▁▁▂▂▂▂▃▃▄▄▄▅▅▅▆▆▆▆▇▇▇▇█` | $38     | +$0        | +$1      | 2026-09-01 |
| Consumer Sentiment (U. Mich.)      | `▇▇█▇▅▃▂▂▄▅▄▃▃▂▂▃▃▃▂▁▂▃▂▁` | 48.10   | -3.60      | -7.00    | 2026-09-01 |
| Supply Chain Pressure (GSCPI)      | `▁▁▁▁▁▁▁▂▂▂▁▂▁▁▃▃▃▄▇█▆▅▆▆` | 1.28    | +0.09      | +1.32    | 2026-09-01 |

### Income & Poverty (Census CPS ASEC, annual)

| Indicator                    | Trend                      | Latest  | YoY (1y) | Chg (5y) | As of      |
| ---------------------------- | -------------------------- | ------- | -------- | -------- | ---------- |
| Real Median Household Income | `▂▂▂▂▂▃▂▂▁▁▁▁▁▃▄▄▅▇▆▆▅▆▇█` | $87,460 | +$2,250  | +$3,870  | 2025-01-01 |
| Official Poverty Rate        | `▃▄▄▄▄▄▅▆█▇▇▇▇▅▄▄▃▁▂▃▂▂▁▁` | 10.2%   | -0.5pp   | -1.3pp   | 2025-01-01 |

### Manufacturing (Regional Fed Surveys — ISM PMI Proxies)

| Indicator             | Trend                      | Latest | MoM    | YoY (12m) | As of      |
| --------------------- | -------------------------- | ------ | ------ | --------- | ---------- |
| Philadelphia Fed      | `▂▁▆▄▃▁▂▂▃▂▄▁▂▁▃▄▄▅▂▃▇█▆▄` | 20.90  | -16.90 | +31.00    | 2026-10-01 |
| Empire State (NY Fed) | `▆▄▂▄▁▂▂▁▄▅▂▄▅▃▄▄▃▅▆▄▆▇▄█` | 25.50  | +17.90 | +17.70    | 2026-10-01 |
| Dallas Fed            | `▅▅▆█▄▃▁▃▄▆▅▄▅▄▄▅▆▅▅▆▅▆▇▇` | 9.80   | -1.80  | +18.60    | 2026-09-01 |

### Mortgage Rates

| Indicator     | Trend                      | Latest | WoW    | YoY (52w) | As of      |
| ------------- | -------------------------- | ------ | ------ | --------- | ---------- |
| 30-Year Fixed | `▁▁▁▁▁▁▁▁▁▂▂▂▂▂▂▃▃▄▅▇██▇▆` | 7.2%   | -0.1pp | +1.1pp    | 2026-10-29 |
| 15-Year Fixed | `▁▁▁▁▁▁▁▁▂▂▂▂▂▂▂▂▃▄▅▇█▇▇▇` | 6.6%   | -0.1pp | +1.2pp    | 2026-10-29 |

### Consumer Spending by Age (BLS Consumer Expenditure Survey, annual)

| Indicator                 | Trend                      | Latest   | YoY (1y) | Chg (5y) | As of      |
| ------------------------- | -------------------------- | -------- | -------- | -------- | ---------- |
| All Consumer Units        | `▁▁▁▁▂▂▂▂▂▂▂▂▃▃▃▄▄▄▄▅▆▇▇█` | $81,905  | +$3,370  | +$20,573 | 2025-01-01 |
| Reference Person Under 25 | `▁▁▁▂▂▂▂▂▂▂▂▂▃▃▃▃▃▄▄▅▆▆▆█` | $54,136  | +$6,853  | +$16,061 | 2025-01-01 |
| Reference Person 25–34    | `▁▁▁▁▂▂▂▂▂▂▂▂▂▃▃▃▃▄▄▅▆▆▇█` | $78,579  | +$4,104  | +$20,935 | 2025-01-01 |
| Reference Person 35–44    | `▁▁▁▂▂▂▂▂▂▂▂▂▃▃▃▄▄▅▅▅▆▇▇█` | $93,650  | +$2,421  | +$19,489 | 2025-01-01 |
| Reference Person 45–54    | `▁▁▁▁▂▂▂▂▂▂▂▂▃▃▃▄▄▄▄▅▆▆▇█` | $106,658 | +$6,331  | +$31,867 | 2025-01-01 |
| Reference Person 55–64    | `▁▁▁▁▂▂▂▂▂▂▂▂▃▃▃▄▄▅▄▅▆▇▇█` | $85,442  | +$496    | +$20,524 | 2025-01-01 |
| Reference Person 65+      | `▁▁▁▁▂▂▂▂▂▃▃▃▃▄▄▅▅▅▄▅▆▇▇█` | $64,445  | +$3,013  | +$16,872 | 2025-01-01 |

### Household Credit — 90+ Day Delinquency (% of balance)

| Indicator     | Trend                      | Latest | QoQ    | YoY (4q) | As of      |
| ------------- | -------------------------- | ------ | ------ | -------- | ---------- |
| Credit Cards  | `▃▃▄▃▂▁▂▁▁▁▁▁▃▃▄▅▅▅▆▆▇▇█▇` | 12.9%  | -0.2pp | +0.7pp   | 2026-06-01 |
| Auto Loans    | `▅▄▄▃▂▁▂▁▁▁▁▁▁▂▃▃▄▅▅▅▅▆█▇` | 5.5%   | -0.1pp | +0.5pp   | 2026-06-01 |
| Student Loans | `▅▅▄▄▄▄▃▃▃▁▁▁▁▁▁▁▁▁▆▇▇▇▇█` | 10.6%  | +0.3pp | +0.4pp   | 2026-06-01 |
| Mortgages     | `▄▃▃▁▁▁▁▂▁▁▁▁▂▂▃▂▄▄▅▅▅▆█▇` | 1.0%   | -0.1pp | +0.2pp   | 2026-06-01 |
| HELOC         | `█▇▇▆▆▄▄▅▆▅▄▃▄▃▂▁▁▂▅▄▄▄▅▆` | 1.0%   | +0.0pp | +0.1pp   | 2026-06-01 |
| All Debt      | `▄▄▄▃▂▂▂▂▁▁▁▁▁▂▂▂▃▃▆▆▆▇█▇` | 3.3%   | -0.0pp | +0.3pp   | 2026-06-01 |
<!-- ECONOMIC-DATA-END -->
