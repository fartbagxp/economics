"""
Sanity checks for data freshness and viz coverage.

Freshness thresholds are based on typical release lags per frequency:
  - Weekly (ICSA, CCSA): released every Thursday, expect data within 21 days
  - Monthly (labor): observation date is the 1st of the month; released the first
    Friday of the following month. Worst case is two adjacent 31-day months plus
    a release as late as the 7th, e.g. Jul 1 -> Aug 1 (31) -> Sep 1 (31) -> Sep 7
    release (7) = 69 days just before the next release (70-day threshold)
  - Monthly (CPI/PPI, BLS real earnings): BLS releases ~2 weeks after month end,
    as late as the 15th-16th, e.g. Aug 1 -> Oct 15 release = 75 days just before
    it arrives (80-day threshold)
  - Monthly (Michigan): UMich releases at end of the month; 90-day threshold
  - Monthly (PCE/PI): BEA's Personal Income and Outlays release lands at the end
    of the following month, but some months it slips into the first days of the
    month after, e.g. Jul 1 -> Aug 1 (31) -> Sep 1 (31) -> Oct 1 (30) release
    = ~92 days just before it arrives (100-day threshold)
  - Monthly (JOLTS): BLS releases ~5-6 weeks after month end; worst-case ~93 days
    (95-day threshold)
  - Quarterly (GDP): advance estimate ~30 days after quarter end; observation date
    is the quarter start, so the threshold is wider (215 days covers the full
    quarter + release lag + one additional quarter of buffer before next release)
"""

import re
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import polars as pl
import pytest

DATA_DIR = Path(__file__).parent.parent / "data"

SERIES_MAX_AGE = [
    # Weekly
    ("icsa", 21),
    ("ccsa", 21),
    # Monthly
    ("unrate", 70),
    ("civpart", 70),
    ("u1rate", 70),
    ("u2rate", 70),
    ("u4rate", 70),
    ("u5rate", 70),
    ("u6rate", 70),
    ("lns14000012", 70),
    ("lns14000036", 70),
    ("lns14000089", 70),
    ("lns14024230", 70),
    ("uemp27ov", 70),
    ("lns13025703", 70),
    ("lns11300001", 70),
    ("lns11300002", 70),
    ("lns11327659", 70),
    ("lns11327660", 70),
    ("lns11327689", 70),
    ("lns11327662", 70),
    ("jtshir", 95),
    ("cpiaucsl", 80),
    ("cpilfesl", 80),
    ("umcsent", 90),
    ("pcepi", 100),
    ("pcepilfe", 100),
    ("ppifid", 80),
    ("ppifes", 80),
    # Monthly — CES payrolls and earnings, in the same first-Friday release as
    # the labor series above
    ("ces0000000001", 70),
    ("ces0500000003", 70),
    # Monthly — BLS Real Earnings, released with CPI
    ("ces0500000013", 80),
    ("ces0500000012", 80),
    # Monthly — regional Fed manufacturing surveys, released within the
    # survey month itself (Dallas, the latest, on its last Monday)
    ("gacdfsa066msfrbphi", 70),
    ("gacdisa066msfrbny", 70),
    ("bactsamfrbdal", 70),
    # Quarterly — observation date is quarter start, not release date
    ("gdp", 215),
    # Monthly — BEA personal income & outlays (released end of following month,
    # occasionally the first days of the month after)
    ("pi", 100),
    ("dspi", 100),
    ("pce", 100),
    ("psave", 215),
    ("psavert", 100),
    ("mich", 90),
    ("w875rx1", 100),
    # Monthly — Fed G.19 consumer credit, released ~5th business day of the
    # second month after, e.g. Aug 1 -> Nov 7 = ~98 days just before it arrives
    ("revolsl", 105),
    ("nonrevsl", 105),
    # SLOAS and MVLOAS are deliberately absent: FRED discontinued both after
    # 2024:Q4, and the viz only draws them in the fallback chart shown when the
    # NY Fed data is missing.
    # Weekly — EIA retail fuel prices (Mondays) and Brent spot, which EIA posts
    # to FRED about a week behind
    ("gasregw", 21),
    ("gasdesw", 21),
    ("dcoilbrenteu", 21),
    # Daily — TIPS-based breakeven rates
    ("t5yie", 21),
    ("t10yie", 21),
    # Monthly — Fed funds & treasury constant maturity rates
    ("fedfunds", 70),
    ("gs2", 70),
    ("gs10", 70),
    ("gs20", 70),
    ("gs30", 70),
    # Daily — Fed funds target range (updates on FOMC decisions, but FRED
    # republishes the unchanged value daily)
    ("dfedtaru", 21),
    ("dfedtarl", 21),
    # Monthly — NY Fed GSCPI, released ~4th business day of the following month
    ("gscpi", 75),
    # Weekly — Freddie Mac Primary Mortgage Market Survey (released Thursdays)
    ("mortgage30us", 21),
    ("mortgage15us", 21),
    # Quarterly — NY Fed 90+ day delinquency rates; report lags quarter end by
    # ~2.5 months and the observation date is the quarter's last month
    ("nyfed_delinq_mortgage", 215),
    ("nyfed_delinq_he_revolving", 215),
    ("nyfed_delinq_auto", 215),
    ("nyfed_delinq_credit_card", 215),
    ("nyfed_delinq_student", 215),
    ("nyfed_delinq_other", 215),
    ("nyfed_delinq_total", 215),
    # Quarterly — new bankruptcies from the same NY Fed workbook, same release lag
    ("nyfed_bankruptcy_by_age", 215),
    ("nyfed_bankruptcy_total", 215),
    # Quarterly — balances from the same NY Fed workbook
    ("nyfed_mortgage", 215),
    ("nyfed_he_revolving", 215),
    ("nyfed_auto", 215),
    ("nyfed_credit_card", 215),
    ("nyfed_student", 215),
    ("nyfed_other", 215),
    ("nyfed_total", 215),
    # Monthly — USDA SNAP National Data Bank, refreshed roughly monthly with a
    # ~3-month lag, so ~140 days old just before a refresh. The collector once
    # sat on a superseded archive for months while still "succeeding"; this is
    # the check that catches that.
    ("snap_persons", 160),
    # Monthly — CMS Medicare and Medicaid/CHIP enrollment, published ~4-5 months
    # after the reference month
    ("medicare_total_enrollment", 200),
    ("medicaid_chip_enrollment", 200),
    # Annual — BLS Consumer Expenditure Survey, spending by age of reference
    # person. Data for calendar year Y is published in September of Y+1 and the
    # observation date is stored as Jan 1 of year Y (FRED annual convention), so
    # in the months just before a release the latest point is ~33 months old.
    # 1050 days covers that plus a buffer for a slipped release.
    ("ce_totalexp_all", 1050),
    ("ce_totalexp_lt25", 1050),
    ("ce_totalexp_25_34", 1050),
    ("ce_totalexp_35_44", 1050),
    ("ce_totalexp_45_54", 1050),
    ("ce_totalexp_55_64", 1050),
    ("ce_totalexp_65up", 1050),
    ("ce_totalexp_65_74", 1050),
    ("ce_totalexp_75up", 1050),
    # Annual — Census CPS ASEC income and poverty, released each September for
    # the prior calendar year and dated Jan 1 of the data year, so the latest
    # point is ~20 months old on release day and ~32 months just before the
    # next. Same 1050-day budget as the CE survey above.
    ("mehoinusa672n", 1050),
    ("census_poverty_rate", 1050),
    # Quarterly — Treasury total public debt via FRED. Observation date is the
    # quarter start but the value is the quarter-end level, and the release
    # follows quarter end by ~2.5 months, so the latest point is ~5.5 months old
    # on release day and ~8.5 months old just before the next one. 300 days
    # covers that with room for a slipped release.
    ("gfdebtn", 300),
    # Quarterly — Fed Z.1 household mortgages, same release and dating as gfdebtn
    ("hhmsdodns", 300),
    # Quarterly — Fed Distributional Financial Accounts, published alongside the
    # Z.1 release on the same lag and dating convention as gfdebtn above.
    ("fed_dfa_wealth_by_percentile", 300),
    # Daily — Treasury Debt to the Penny, published the next business day.
    # A long holiday weekend puts the latest point ~5 days back.
    ("treasury_national_debt", 10),
]

VIZ_SERVER = Path(__file__).parent.parent / "viz" / "src" / "routes" / "+page.server.js"


def _viz_series_lists() -> tuple[list[str], list[str]]:
    """Read every `const *_SERIES[_OPTIONAL] = [...]` list from the viz loader,
    so these tests can't drift from what the page actually loads."""
    src = VIZ_SERVER.read_text()
    raw, derived = [], []
    for name, body in re.findall(r"const (\w*SERIES\w*) = \[(.*?)\];", src, re.DOTALL):
        ids = re.findall(r"'([^']+)'", body)
        (derived if name.startswith("DERIVED") else raw).extend(ids)
    return raw, derived


VIZ_RAW_SERIES, VIZ_DERIVED_SERIES = _viz_series_lists()

# Suffixes Deriver appends; longest first so "_chg_3mo" isn't read as "_3mo"
DERIVED_SUFFIXES = ("_chg_3mo", "_chg", "_mom", "_yoy")


def _derived_source(name: str) -> str:
    for suffix in DERIVED_SUFFIXES:
        if name.endswith(suffix):
            return name[: -len(suffix)]
    raise ValueError(f"unrecognized derived series name: {name}")


DERIVED_FILES = sorted(p.stem for p in (DATA_DIR / "derived").glob("*.csv"))
ALL_CSVS = sorted(str(p.relative_to(DATA_DIR)) for p in DATA_DIR.glob("*/*.csv"))


def _latest(path: Path) -> str:
    return pl.read_csv(path)["date"].max()[:10]


@pytest.mark.parametrize("series_id,max_age_days", SERIES_MAX_AGE)
def test_raw_series_freshness(series_id, max_age_days):
    path = DATA_DIR / "raw" / f"{series_id}.csv"
    assert path.exists(), f"CSV missing: {path.name}"
    latest = date.fromisoformat(_latest(path))
    age = (datetime.now(UTC).date() - latest).days
    assert age <= max_age_days, (
        f"{series_id}: latest point {latest} is {age} days old (max allowed {max_age_days})"
    )


@pytest.mark.parametrize("series_id", VIZ_RAW_SERIES)
def test_viz_raw_series_present(series_id):
    path = DATA_DIR / "raw" / f"{series_id}.csv"
    assert path.exists(), f"viz raw series CSV missing: {path.name}"
    assert pl.read_csv(path).height > 0, f"{series_id} is empty"


@pytest.mark.parametrize("series_id", VIZ_DERIVED_SERIES)
def test_viz_derived_series_present(series_id):
    path = DATA_DIR / "derived" / f"{series_id}.csv"
    assert path.exists(), f"viz derived series CSV missing: {path.name}"
    assert pl.read_csv(path).height > 0, f"{series_id} is empty"


def test_viz_series_lists_parsed():
    """Guard the regex above: if the loader is restructured, fail loudly rather
    than silently parametrizing the presence tests over nothing."""
    assert len(VIZ_RAW_SERIES) > 30, VIZ_RAW_SERIES
    assert len(VIZ_DERIVED_SERIES) > 10, VIZ_DERIVED_SERIES


@pytest.mark.parametrize("name", DERIVED_FILES)
def test_derived_in_sync_with_source(name):
    source_id = _derived_source(name)
    raw_latest = _latest(DATA_DIR / "raw" / f"{source_id}.csv")
    derived_latest = _latest(DATA_DIR / "derived" / f"{name}.csv")
    assert derived_latest == raw_latest, (
        f"{name}: derived latest {derived_latest} does not match "
        f"raw latest {raw_latest} — re-run derivation"
    )


@pytest.mark.parametrize("rel_path", ALL_CSVS)
def test_dates_unique_and_sorted(rel_path):
    """Every reader (Deriver's row-based shifts, the viz's line paths, the
    README's latest-value lookup) assumes one row per date in ascending order."""
    dates = pl.read_csv(DATA_DIR / rel_path)["date"].str.slice(0, 10).to_list()
    dupes = sorted({d for d in dates if dates.count(d) > 1})
    assert not dupes, f"{rel_path}: duplicate dates {dupes[:5]}"
    assert dates == sorted(dates), f"{rel_path}: dates not in ascending order"


def test_brent_futures_curve_current():
    """The futures CSV is dated by contract month, not observation, so it has no
    age to check. A stale curve shows up as its front contract slipping into
    the past instead."""
    path = DATA_DIR / "raw" / "brent_futures_curve.csv"
    front = date.fromisoformat(pl.read_csv(path)["date"].min()[:10])
    cutoff = datetime.now(UTC).date() - timedelta(days=45)
    assert front >= cutoff, (
        f"brent_futures_curve: front contract {front} is in the past"
    )


def test_bankruptcy_bands_track_national_total():
    """The age bands and the national total come from two separately computed
    sheets of the same workbook, so they track each other without matching
    exactly: the bands omit filers with an unknown birth year, which puts them
    up to ~13% below the total in the early 2000s and within a fraction of a
    percent today. One quarter (2024:Q3) runs 1.4% the other way.

    The point of the bound is to catch a sheet layout shift or a unit error,
    which would throw the two orders of magnitude apart — not to police the
    publisher's own small inconsistencies.
    """
    bands = pl.read_csv(DATA_DIR / "raw" / "nyfed_bankruptcy_by_age.csv")
    total = pl.read_csv(DATA_DIR / "raw" / "nyfed_bankruptcy_total.csv")
    band_cols = [c for c in bands.columns if c != "date"]
    assert len(band_cols) == 6, f"expected 6 age bands, found {band_cols}"

    joined = (
        bands.select("date", pl.sum_horizontal(band_cols).alias("banded"))
        .join(total, on="date", how="inner")
        .with_columns((pl.col("banded") / pl.col("value")).alias("ratio"))
    )
    assert joined.height > 0, "no overlapping quarters between bands and total"

    stray = joined.filter((pl.col("ratio") < 0.80) | (pl.col("ratio") > 1.05))
    assert stray.height == 0, (
        f"band sum diverges from the national total in {stray.height} quarter(s): "
        f"{stray.select('date', 'banded', 'value').head(5).to_dicts()}"
    )
