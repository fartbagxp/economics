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
  <!-- DATASET-COUNT --><img src="https://img.shields.io/badge/datasets-89-blue?style=flat-square" alt="89 datasets"><!-- /DATASET-COUNT -->
</p>

- [Setup](docs/setup.md): how to run the repo
- [Collection](docs/collection.md): what data is collected and where it comes from
- [Dashboard](https://fartbagxp.github.io/economics/): interactive vizualization

<!-- ECONOMIC-DATA-START -->
## Economic Dashboard

_Last updated: 2026-09-06 04:08 UTC_

_Sparklines show the last 24 data points (monthly or annual), 52 points (weekly), or 8 points (quarterly)._

### Labor Market Overview

| Indicator                 | Trend                      | Latest    | Chg (prev) | Chg (1Y) | As of      |
| ------------------------- | -------------------------- | --------- | ---------- | -------- | ---------- |
| Unemployment Rate (U-3)   | `▃▂▂▃▂▁▃▃▃▅▂▅▅▆█▆▅▆▅▅▅▃▂▂` | 4.1%      | +0.0pp     | -0.2pp   | 2026-08-01 |
| Total Nonfarm Payrolls    | `▁▁▂▃▃▃▃▄▄▄▄▄▄▃▄▄▅▄▅▆▆▆▇█` | 159,075K  | +162K      | +603K    | 2026-08-01 |
| Labor Force Participation | `██▆▆▆▇▆▆▇▆▅▅▅▆▆▆▄▄▃▃▃▁▁▂` | 61.6%     | +0.2pp     | -0.6pp   | 2026-08-01 |
| Initial Jobless Claims    | `▄▃▅▄▅▁▂▄▄▄▇█▇▅▅▅▄▁▂▂▄▄▃▃` | 206,000   | +2,000     | -30,000  | 2026-08-29 |
| Continued Claims          | `▆█▃▅▅▂▁▂▂▃▂▃▄▆▅▆▄▃▂▄▃▄▂▂` | 1,779,000 | +8,000     | -158,000 | 2026-08-22 |

### Unemployment Measures (U1–U6)

| Indicator                  | Trend                      | Latest | MoM    | YoY (12m) | As of      |
| -------------------------- | -------------------------- | ------ | ------ | --------- | ---------- |
| U-1: 15+ Weeks Unemployed  | `▃▃▅▅▃▁▁▁▃▁▃█▅██████▅██▅█` | 1.8%   | +0.1pp | +0.0pp    | 2026-08-01 |
| U-2: Job Losers            | `▄▁▄▄▁▁▄▁▄▄▁▄▄██▄██▄█▄▁▄▁` | 1.9%   | -0.1pp | -0.1pp    | 2026-08-01 |
| U-3: Official Rate         | `▃▂▂▃▂▁▃▃▃▅▂▅▅▆█▆▅▆▅▅▅▃▂▂` | 4.1%   | +0.0pp | -0.2pp    | 2026-08-01 |
| U-4: + Discouraged Workers | `▂▁▁▂▂▂▂▃▂▃▃▃▄▅█▄▄▄▃▄▄▃▂▂` | 4.4%   | +0.0pp | -0.1pp    | 2026-08-01 |
| U-5: + Marginally Attached | `▂▂▂▃▂▁▃▃▃▃▃▄▅▆█▅▄▅▅▅▅▄▃▃` | 5.1%   | +0.0pp | -0.1pp    | 2026-08-01 |
| U-6: + Part-Time Economic  | `▂▂▂▂▁▁▃▃▂▂▂▃▄▄█▆▄▃▃▅▄▃▃▂` | 7.7%   | -0.2pp | -0.2pp    | 2026-08-01 |

### Unemployment by Age

| Indicator  | Trend                      | Latest | MoM    | YoY (12m) | As of      |
| ---------- | -------------------------- | ------ | ------ | --------- | ---------- |
| Ages 16–19 | `▄▄▄▂▁▁▂▄▂▃▅▆▄▃█▇▃▅▃▅▅▅▁▄` | 14.1%  | +2.0pp | -1.1pp    | 2026-08-01 |
| Ages 20–24 | `▄▂▄▄▃▅▅▃▅▅▅▄██▅▅▂▃▁▃▃▂▂▂` | 7.1%   | +0.0pp | -0.8pp    | 2026-08-01 |
| Ages 25–54 | `▅▂▂▄▅▃▄▂▃▂▁▄▄▇█▄█▇▇▇▆▆▆▄` | 4.3%   | -0.3pp | +0.0pp    | 2026-08-01 |
| Ages 55+   | `▃▁▂▃▅▃▂▂▅▃▃▂▂▆▅▃▆██▃▃▁▅▃` | 3.0%   | -0.1pp | +0.1pp    | 2026-08-01 |

### Economy

| Indicator                          | Trend                      | Latest  | Chg (prev) | Chg (1Y) | As of      |
| ---------------------------------- | -------------------------- | ------- | ---------- | -------- | ---------- |
| GDP                                | `▁▁▁▂▂▃▃▃▄▄▄▄▅▅▅▅▆▆▆▆▇▇▇█` | $32,486 | +$620      | +$2,000  | 2026-04-01 |
| CPI (All Urban)                    | `▁▁▁▁▂▂▂▃▃▃▃▃▃▄▄▄▅▅▅▆▇█▇▇` | 332.81  | +0.25      | +11.38   | 2026-07-01 |
| Avg. Hourly Earnings (Wage Growth) | `▁▁▁▂▂▂▃▃▃▃▄▄▄▅▅▅▆▆▆▇▇▇▇█` | $38     | +$0        | +$1      | 2026-08-01 |
| Consumer Sentiment (U. Mich.)      | `▆▇▇▇█▇▅▃▂▂▄▅▄▃▃▂▂▃▃▃▂▁▂▃` | 55.20   | +5.70      | -6.50    | 2026-07-01 |
| Supply Chain Pressure (GSCPI)      | `▂▁▁▁▁▂▁▁▃▂▂▁▂▁▁▄▃▄▄█▇▅▅▅` | 1.06    | +0.13      | +1.15    | 2026-08-01 |

### Manufacturing (Regional Fed Surveys — ISM PMI Proxies)

| Indicator             | Trend                      | Latest | MoM    | YoY (12m) | As of      |
| --------------------- | -------------------------- | ------ | ------ | --------- | ---------- |
| Philadelphia Fed      | `▂▃▂▁▆▄▃▁▂▂▃▂▄▁▂▁▃▄▄▅▂▃▇█` | 47.40  | +6.00  | +46.70    | 2026-08-01 |
| Empire State (NY Fed) | `▄▁▇▄▂▄▁▂▂▁▄▅▂▅▆▃▅▅▃▆▇▅▇█` | 20.60  | +5.00  | +11.50    | 2026-08-01 |
| Dallas Fed            | `▄▅▅▆█▄▃▁▃▄▆▅▄▅▄▄▅▆▅▅▆▅▆▇` | 11.60  | +10.30 | +13.30    | 2026-08-01 |

### Mortgage Rates

| Indicator     | Trend                      | Latest | WoW    | YoY (52w) | As of      |
| ------------- | -------------------------- | ------ | ------ | --------- | ---------- |
| 30-Year Fixed | `▃▄▃▂▁▂▃▂▅▅▄▅▄▄▃▄▅▆▇▇▇▇▇█` | 6.7%   | +0.0pp | +0.2pp    | 2026-09-03 |
| 15-Year Fixed | `▃▃▃▂▁▁▃▂▅▅▄▄▄▄▄▄▆▆█▇▆▆▇█` | 6.0%   | +0.1pp | +0.4pp    | 2026-09-03 |

### Consumer Spending by Age (BLS Consumer Expenditure Survey, annual)

| Indicator                 | Trend                      | Latest   | YoY (1y) | Chg (5y) | As of      |
| ------------------------- | -------------------------- | -------- | -------- | -------- | ---------- |
| All Consumer Units        | `▁▁▁▁▂▂▂▂▂▂▂▃▃▃▃▄▄▄▅▄▅▇▇█` | $78,535  | +$1,255  | +$15,499 | 2024-01-01 |
| Reference Person Under 25 | `▁▁▁▁▂▂▂▂▂▂▂▃▃▃▃▄▃▃▅▅▆▇█▇` | $47,283  | -$2,277  | +$7,990  | 2024-01-01 |
| Reference Person 25–34    | `▁▁▁▁▂▂▂▂▂▂▂▃▂▃▃▃▄▄▄▄▅▆▇█` | $74,475  | +$2,608  | +$17,347 | 2024-01-01 |
| Reference Person 35–44    | `▁▁▁▁▂▂▂▂▂▂▂▂▂▃▃▄▄▄▅▅▆▇▇█` | $91,229  | +$290    | +$16,339 | 2024-01-01 |
| Reference Person 45–54    | `▁▁▁▁▂▂▂▂▂▂▂▂▂▃▃▄▄▄▄▄▅▆▇█` | $100,327 | +$3,008  | +$22,971 | 2024-01-01 |
| Reference Person 55–64    | `▁▁▁▁▂▂▂▃▂▂▂▃▃▃▃▄▄▄▅▄▅▆▇█` | $84,946  | +$1,567  | +$15,452 | 2024-01-01 |
| Reference Person 65+      | `▁▁▁▁▂▂▂▂▃▂▃▃▃▄▄▄▅▅▅▅▆▇▇█` | $61,432  | +$1,345  | +$11,212 | 2024-01-01 |

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
