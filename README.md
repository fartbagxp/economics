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
  <!-- DATASET-COUNT --><img src="https://img.shields.io/badge/datasets-53-blue?style=flat-square" alt="53 datasets"><!-- /DATASET-COUNT -->
</p>

- [Setup](docs/setup.md): how to run the repo
- [Collection](docs/collection.md): what data is collected and where it comes from
- [Dashboard](https://fartbagxp.github.io/economics/): interactive vizualization

<!-- ECONOMIC-DATA-START -->
## Economic Dashboard

_Last updated: 2026-06-27 07:10 UTC_

_Sparklines show the last 24 data points (monthly), 52 points (weekly), or 8 points (quarterly)._

### Labor Market Overview

| Indicator                 | Trend                      | Latest    | Chg (prev) | Chg (1Y) | As of      |
| ------------------------- | -------------------------- | --------- | ---------- | -------- | ---------- |
| Unemployment Rate (U-3)   | `▁▃▄▄▃▃▄▃▂▄▄▄▅▃▅▅▆█▆▅▆▅▅▅` | 4.3%      | +0.0pp     | +0.1pp   | 2026-05-01 |
| Labor Force Participation | `▇▇███▆▅▆▇▆▆▇▅▄▄▄▆▆▅▃▂▁▁▁` | 61.8%     | +0.0pp     | -0.8pp   | 2026-05-01 |
| Initial Jobless Claims    | `▂▄▄██▄▄▅▅▃▄▃▅▄▅▁▂▄▄▄▇█▇▅` | 215,000   | -12,000    | -21,000  | 2026-06-20 |
| Continued Claims          | `█▇▄▆▇▇▅▇▆▆▄▅▂▄▃▂▁▂▁▂▁▂▃▄` | 1,821,000 | +21,000    | -139,000 | 2026-06-13 |

### Unemployment Measures (U1–U6)

| Indicator                  | Trend                      | Latest | MoM    | YoY (12m) | As of      |
| -------------------------- | -------------------------- | ------ | ------ | --------- | ---------- |
| U-1: 15+ Weeks Unemployed  | `▁▂▄▄▄▆▆▄▂▂▂▄▂▄█▆██████▆█` | 1.8%   | +0.1pp | +0.2pp    | 2026-05-01 |
| U-2: Job Losers            | `▁▁█▄▁▄▄▁▁▄▁▄▄▁▄▄██▄██▄█▄` | 2.0%   | -0.1pp | +0.0pp    | 2026-05-01 |
| U-3: Official Rate         | `▁▃▄▄▃▃▄▃▂▄▄▄▅▃▅▅▆█▆▅▆▅▅▅` | 4.3%   | +0.0pp | +0.1pp    | 2026-05-01 |
| U-4: + Discouraged Workers | `▁▁▃▃▁▁▃▃▃▃▃▃▃▃▃▄▅█▄▄▄▃▄▄` | 4.6%   | +0.0pp | +0.2pp    | 2026-05-01 |
| U-5: + Marginally Attached | `▁▂▃▃▃▃▃▃▂▃▃▃▃▃▅▅▇█▅▅▅▅▅▅` | 5.3%   | +0.0pp | +0.2pp    | 2026-05-01 |
| U-6: + Part-Time Economic  | `▁▁▃▃▂▂▂▂▁▄▃▃▃▂▃▄▄█▆▄▃▄▅▄` | 8.1%   | -0.1pp | +0.3pp    | 2026-05-01 |

### Unemployment by Age

| Indicator  | Trend                      | Latest | MoM    | YoY (12m) | As of      |
| ---------- | -------------------------- | ------ | ------ | --------- | ---------- |
| Ages 16–19 | `▁▁▂▄▄▄▂▁▁▂▄▂▃▅▆▄▃█▇▃▅▃▅▅` | 14.7%  | +0.3pp | +1.7pp    | 2026-05-01 |
| Ages 20–24 | `▄▃▄▄▂▄▄▃▅▅▃▅▅▅▄██▅▅▂▃▁▃▃` | 7.2%   | -0.4pp | -1.0pp    | 2026-05-01 |
| Ages 25–54 | `▂▅▇▅▂▂▄▅▃▄▂▃▂▁▄▄▇█▄█▇▇▇▆` | 4.7%   | -0.1pp | +0.5pp    | 2026-05-01 |
| Ages 55+   | `▁▂▅▄▂▃▄▅▄▃▃▅▄▄▃▃▆▅▄▆██▄▄` | 3.0%   | +0.0pp | -0.1pp    | 2026-05-01 |

### Economy

| Indicator                     | Trend                      | Latest     | Chg (prev) | Chg (1Y) | As of      |
| ----------------------------- | -------------------------- | ---------- | ---------- | -------- | ---------- |
| GDP                           | `▁▂▂▂▃▃▃▄▄▄▅▅▅▅▅▆▆▆▆▆▇▇▇█` | $31,865.7B | +443.2B    | +1823.6B | 2026-01-01 |
| CPI (All Urban)               | `▁▁▁▁▁▁▂▂▂▃▃▃▃▃▄▄▄▅▅▅▅▆▇█` | 333.98     | +1.57      | +13.68   | 2026-05-01 |
| Consumer Sentiment (U. Mich.) | `▆▆▆▇▇▇█▇▅▃▂▂▄▅▄▃▃▂▂▃▃▃▂▁` | 44.80      | -5.00      | -7.40    | 2026-05-01 |
<!-- ECONOMIC-DATA-END -->
