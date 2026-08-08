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
  <!-- DATASET-COUNT --><img src="https://img.shields.io/badge/datasets-74-blue?style=flat-square" alt="74 datasets"><!-- /DATASET-COUNT -->
</p>

- [Setup](docs/setup.md): how to run the repo
- [Collection](docs/collection.md): what data is collected and where it comes from
- [Dashboard](https://fartbagxp.github.io/economics/): interactive vizualization

<!-- ECONOMIC-DATA-START -->
## Economic Dashboard

_Last updated: 2026-08-08 03:52 UTC_

_Sparklines show the last 24 data points (monthly), 52 points (weekly), or 8 points (quarterly)._

### Labor Market Overview

| Indicator                 | Trend                      | Latest    | Chg (prev) | Chg (1Y) | As of      |
| ------------------------- | -------------------------- | --------- | ---------- | -------- | ---------- |
| Unemployment Rate (U-3)   | `▃▃▂▂▃▂▁▃▃▃▅▂▅▅▆█▆▅▆▅▅▅▃▂` | 4.1%      | -0.1pp     | +0.0pp   | 2026-07-01 |
| Total Nonfarm Payrolls    | `▁▁▂▃▄▄▄▄▅▅▅▅▅▅▅▅▅▆▅▆▇▇█▇` | 158,858K  | -23K       | +316K    | 2026-07-01 |
| Labor Force Participation | `███▆▆▆▇▆▆▇▆▅▅▅▆▆▆▄▄▃▃▃▁▁` | 61.4%     | -0.1pp     | -0.9pp   | 2026-07-01 |
| Initial Jobless Claims    | `▄▅▅▃▄▃▅▄▅▁▂▄▄▄▇█▇▅▅▅▄▁▂▂` | 199,000   | +1,000     | -27,000  | 2026-08-01 |
| Continued Claims          | `▅█▆▆▄▅▂▄▄▂▁▂▁▂▁▂▃▄▃▄▃▂▂▃` | 1,801,000 | +24,000    | -162,000 | 2026-07-25 |

### Unemployment Measures (U1–U6)

| Indicator                  | Trend                      | Latest | MoM    | YoY (12m) | As of      |
| -------------------------- | -------------------------- | ------ | ------ | --------- | ---------- |
| U-1: 15+ Weeks Unemployed  | `▃▃▃▅▅▃▁▁▁▃▁▃█▅██████▅██▅` | 1.7%   | -0.1pp | +0.1pp    | 2026-07-01 |
| U-2: Job Losers            | `█▄▁▄▄▁▁▄▁▄▄▁▄▄██▄██▄█▄▁▄` | 2.0%   | +0.1pp | +0.1pp    | 2026-07-01 |
| U-3: Official Rate         | `▃▃▂▂▃▂▁▃▃▃▅▂▅▅▆█▆▅▆▅▅▅▃▂` | 4.1%   | -0.1pp | +0.0pp    | 2026-07-01 |
| U-4: + Discouraged Workers | `▃▂▁▁▂▂▂▂▃▂▃▃▃▄▅█▄▄▄▃▄▄▃▂` | 4.4%   | -0.1pp | -0.1pp    | 2026-07-01 |
| U-5: + Marginally Attached | `▃▂▂▂▃▂▁▃▃▃▃▃▄▅▆█▅▄▅▅▅▅▄▃` | 5.1%   | -0.1pp | +0.0pp    | 2026-07-01 |
| U-6: + Part-Time Economic  | `▂▂▂▂▂▁▁▃▃▂▂▂▃▄▄█▆▄▃▃▅▄▃▃` | 7.9%   | +0.0pp | +0.2pp    | 2026-07-01 |

### Unemployment by Age

| Indicator  | Trend                      | Latest | MoM    | YoY (12m) | As of      |
| ---------- | -------------------------- | ------ | ------ | --------- | ---------- |
| Ages 16–19 | `▂▄▄▄▂▁▁▂▄▂▃▅▆▄▃█▇▃▅▃▅▅▅▁` | 12.1%  | -2.5pp | -2.4pp    | 2026-07-01 |
| Ages 20–24 | `▄▄▂▄▄▃▅▅▃▅▅▅▄██▅▅▂▃▁▃▃▂▂` | 7.1%   | +0.0pp | -1.1pp    | 2026-07-01 |
| Ages 25–54 | `▇▅▂▂▄▅▃▄▂▃▂▁▄▄▇█▄█▇▇▇▆▆▆` | 4.6%   | +0.0pp | +0.8pp    | 2026-07-01 |
| Ages 55+   | `▅▃▁▂▃▅▃▂▂▅▃▃▂▂▆▅▃▆██▃▃▁▅` | 3.1%   | +0.3pp | +0.1pp    | 2026-07-01 |

### Economy

| Indicator                     | Trend                      | Latest     | Chg (prev) | Chg (1Y) | As of      |
| ----------------------------- | -------------------------- | ---------- | ---------- | -------- | ---------- |
| GDP                           | `▁▁▁▂▂▃▃▃▄▄▄▄▅▅▅▅▆▆▆▆▇▇▇█` | $32,475.2B | +609.5B    | +1989.5B | 2026-04-01 |
| CPI (All Urban)               | `▁▁▁▁▁▂▂▂▃▃▃▃▃▄▄▄▅▅▅▅▆▇█▇` | 332.57     | -1.41      | +11.95   | 2026-06-01 |
| Consumer Sentiment (U. Mich.) | `▆▆▇▇▇█▇▅▃▂▂▄▅▄▃▃▂▂▃▃▃▂▁▂` | 49.50      | +4.70      | -11.20   | 2026-06-01 |
| Supply Chain Pressure (GSCPI) | `▂▂▁▁▁▁▂▁▁▃▂▂▁▂▁▁▄▃▄▄█▇▅▄` | 0.80       | -0.38      | +0.78    | 2026-07-01 |

### Mortgage Rates

| Indicator     | Trend                      | Latest | WoW    | YoY (52w) | As of      |
| ------------- | -------------------------- | ------ | ------ | --------- | ---------- |
| 30-Year Fixed | `▁▁▂▃▄▅▄▄▃▄▄▄▆▆▅▆▅▆▅▆▆▆▇█` | 6.7%   | +0.0pp | +0.1pp    | 2026-08-06 |
| 15-Year Fixed | `▁▁▁▂▄▄▄▃▂▃▄▄▅▆▅▅▅▅▅▅▆▇█▇` | 6.0%   | -0.0pp | +0.3pp    | 2026-08-06 |

### Household Credit — 90+ Day Delinquency (% of balance)

| Indicator     | Trend                      | Latest | QoQ    | YoY (4q) | As of      |
| ------------- | -------------------------- | ------ | ------ | -------- | ---------- |
| Credit Cards  | `▃▃▃▄▃▂▁▂▁▁▁▁▁▃▃▄▅▅▅▆▆▇▇█` | 13.1%  | +0.4pp | +0.8pp   | 2026-03-01 |
| Auto Loans    | `▅▅▄▄▃▂▁▂▁▁▁▁▁▁▂▃▃▄▅▅▅▅▆█` | 5.6%   | +0.4pp | +0.6pp   | 2026-03-01 |
| Student Loans | `▅▅▅▅▄▄▄▃▃▃▁▁▁▁▁▁▁▁▁▆▇▇▇█` | 10.3%  | +0.8pp | +2.6pp   | 2026-03-01 |
| Mortgages     | `▅▄▃▃▁▁▁▁▂▁▁▁▁▂▂▃▂▄▄▅▅▅▆█` | 1.1%   | +0.2pp | +0.2pp   | 2026-03-01 |
| HELOC         | `█▇▆▇▆▆▄▄▅▆▅▄▃▃▃▂▁▁▂▅▄▄▄▅` | 0.9%   | +0.1pp | +0.1pp   | 2026-03-01 |
| All Debt      | `▅▄▄▄▃▂▂▂▂▁▁▁▁▁▂▂▂▃▃▆▆▆▇█` | 3.4%   | +0.2pp | +0.5pp   | 2026-03-01 |
<!-- ECONOMIC-DATA-END -->
