# Raw Data Sources: Household Wealth vs. National Debt

Provenance for the datasets backing the "US Household Wealth vs. National Debt"
chart. Retrieval date for every dataset below: **2026-09-09**.

## fed_dfa_wealth_by_percentile.csv

| Field               | Value                                                                      |
| ------------------- | -------------------------------------------------------------------------- |
| Source              | Federal Reserve Board, Distributional Financial Accounts (DFA)             |
| Landing page        | <https://www.federalreserve.gov/releases/z1/dataviz/dfa/>                  |
| Exact URL used      | <https://www.federalreserve.gov/releases/z1/dataviz/download/zips/dfa.zip> |
| File inside archive | `dfa-networth-levels.csv`                                                  |
| Retrieved           | 2026-09-09                                                                 |
| Release vintage     | 2026-06-18 (archive timestamp; latest observation 2026:Q1)                 |
| Units               | Millions of dollars, not seasonally adjusted, as published                 |
| Frequency           | Quarterly (end-of-period balance sheet levels)                             |
| Coverage            | 1989:Q3 – 2026:Q1                                                          |

Columns are the `Net worth` measure from the source file, reshaped from long to
wide. All five wealth-percentile categories the source publishes are kept
one-to-one, so charts can regroup them (top 1% = `top_0_1pct` + `pct_99_99_9`;
next 9.9% = `pct_99_99_9` + `pct_90_99`):

| Output column  | Source category | Meaning                  |
| -------------- | --------------- | ------------------------ |
| `top_0_1pct`   | `TopPt1`        | Top 0.1%                 |
| `pct_99_99_9`  | `RemainingTop1` | 99th–99.9th percentile   |
| `pct_90_99`    | `Next9`         | 90th–99th percentile     |
| `pct_50_90`    | `Next40`        | 50th–90th percentile     |
| `bottom_50pct` | `Bottom50`      | Bottom 50%               |

Values stay in millions of dollars as published.

Dates: the source labels quarters as `1989:Q3`. These are converted to the first
day of the quarter (`1989-07-01`), matching how FRED dates the equivalent
`WFRBL*` series and how quarterly FRED series are stored elsewhere in this repo.
The value is the level at the **end** of that quarter.

**Known gaps:** none. 147 consecutive quarters, no missing cells, no duplicate
dates. The series cannot start earlier than 1989:Q3 — that is the first quarter
the Federal Reserve publishes DFA data for.

## treasury_national_debt.csv

| Field           | Value                                                                                                                                                                                 |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source          | U.S. Treasury, Fiscal Data — Debt to the Penny                                                                                                                                        |
| Exact URL used  | `https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny?fields=record_date,tot_pub_debt_out_amt&sort=record_date&format=csv&page[size]=10000` |
| Dataset / field | `debt_to_penny`, field `tot_pub_debt_out_amt` (Total Public Debt Outstanding)                                                                                                         |
| Retrieved       | 2026-09-09                                                                                                                                                                            |
| Units           | Dollars, as published (no conversion)                                                                                                                                                 |
| Frequency       | Daily (business days)                                                                                                                                                                 |
| Coverage        | 1993-04-01 – 2026-09-04                                                                                                                                                               |

The work order specified the `v1` endpoint; `v1` returns HTTP 404 for this
dataset. `v2` is the current published version and was used instead.

**Known gaps:**

- **No data before 1993-04-01.** `debt_to_penny` begins there, so the requested
  1989 start date is not available from this endpoint and the "earliest date is
  1989 or earlier" check cannot pass for this file. `gfdebtn.csv` below covers
  1989–1993.
- Business days only — no weekend or federal holiday rows. Gaps between
  consecutive dates are expected and are not missing data.
- `debt_held_public_amt` and `intragov_hold_amt` are `null` in the earliest
  records; neither is collected here.

## gfdebtn.csv

| Field          | Value                                                                    |
| -------------- | ------------------------------------------------------------------------ |
| Source         | FRED, Federal Reserve Bank of St. Louis (underlying data: U.S. Treasury) |
| Exact URL used | FRED API via `fredapi`, series `GFDEBTN` (see `src/fred.py`)             |
| Series ID      | `GFDEBTN` — Federal Debt: Total Public Debt                              |
| Retrieved      | 2026-09-09                                                               |
| Units          | Millions of dollars, not seasonally adjusted, as published               |
| Frequency      | Quarterly, end of period                                                 |
| Coverage       | 1966:Q1 – 2026:Q1                                                        |

Collected with the other FRED series. It serves two purposes the daily Treasury
file cannot: it reaches back before 1993, covering the
1989:Q3–1993:Q1 stretch where DFA wealth data exists but `debt_to_penny` does
not, and its quarterly end-of-period frequency lines up one-to-one with the DFA
wealth quarters.

Dates follow FRED's convention — the observation is dated the first day of the
quarter and holds the value as of that quarter's **end**, the same convention
used for `fed_dfa_wealth_by_percentile.csv`.

Validated against the daily Treasury file at quarter ends: `GFDEBTN` dated
2026-01-01 equals `debt_to_penny` on 2026-03-31 ($39.065T) to the published
precision; spot checks at 2025:Q4 and 2000:Q2 also match exactly.

**Known gaps:** none within the covered range. 241 consecutive quarters, no
duplicate dates.

## Refresh

All three refresh with the rest of the data:

| File                               | Command                                                |
| ---------------------------------- | ------------------------------------------------------ |
| `fed_dfa_wealth_by_percentile.csv` | `uv run python main.py --source dfa`                   |
| `treasury_national_debt.csv`       | `uv run python main.py --source treasury`              |
| `gfdebtn.csv`                      | `uv run python main.py --source fred --series GFDEBTN` |

All three are also covered by `--source all`, which is what the daily
`update.yml` workflow runs, and by freshness thresholds in
`tests/test_freshness.py`.
