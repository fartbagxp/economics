# Economics

US economic data from FRED, BLS, NY Fed, and Yahoo Finance. Time series stored as CSV in git, with derived metrics and an interactive SvelteKit dashboard.

- [Setup](docs/setup.md): how to run the repo
- [Collection](docs/collection.md): what data is collected and where it comes from

<!-- ECONOMIC-DATA-START -->
## Economic Dashboard

_Last updated: 2026-06-26 10:52 UTC_

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
| Consumer Sentiment (U. Mich.) | `▆▆▅▆▆▆▇█▇▅▃▁▁▄▄▃▂▂▁▁▂▂▂▁` | 49.80      | -3.50      | -2.40    | 2026-04-01 |
<!-- ECONOMIC-DATA-END -->
