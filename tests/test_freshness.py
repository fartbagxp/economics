"""
Sanity checks for data freshness and viz coverage.

Freshness thresholds are based on typical release lags per frequency:
  - Weekly (ICSA, CCSA): released every Thursday, expect data within 21 days
  - Monthly (labor): observation date is the 1st of the month; released the first
    Friday of the following month. Worst case is two adjacent 31-day months plus
    a release as late as the 7th, e.g. Jul 1 -> Aug 1 (31) -> Sep 1 (31) -> Sep 7
    release (7) = 69 days just before the next release (70-day threshold)
  - Monthly (CPI/PPI): BLS releases ~2-3 weeks after month end; 75-day threshold
  - Monthly (PCE/PI/Michigan): BEA/UMich releases at end of following month;
    worst-case age just before next release is ~88 days (90-day threshold)
  - Monthly (JOLTS): BLS releases ~5-6 weeks after month end; worst-case ~93 days
    (95-day threshold)
  - Quarterly (GDP): advance estimate ~30 days after quarter end; observation date
    is the quarter start, so the threshold is wider (215 days covers the full
    quarter + release lag + one additional quarter of buffer before next release)
"""

from datetime import date
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
    ("cpiaucsl", 75),
    ("cpilfesl", 75),
    ("umcsent", 90),
    ("pcepi", 90),
    ("pcepilfe", 90),
    ("ppifid", 75),
    ("ppifes", 75),
    # Quarterly — observation date is quarter start, not release date
    ("gdp", 215),
    # Monthly — personal income & outlays (released end of following month)
    ("pi", 90),
    ("dspi", 90),
    ("pce", 90),
    ("psave", 215),
    ("psavert", 90),
    ("mich", 90),
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
]

# Must match RAW_SERIES in viz/src/routes/+page.server.js
VIZ_RAW_SERIES = [
    "unrate",
    "u6rate",
    "civpart",
    "icsa",
    "cpiaucsl",
    "gdp",
    "umcsent",
    "mortgage30us",
    "mortgage15us",
]

# Must match DERIVED_SERIES in viz/src/routes/+page.server.js
VIZ_DERIVED_SERIES = [
    "cpiaucsl_mom",
    "cpiaucsl_yoy",
    "cpilfesl_mom",
    "cpilfesl_yoy",
    "pcepi_mom",
    "pcepi_yoy",
    "pcepilfe_mom",
    "pcepilfe_yoy",
    "ppifid_mom",
    "ppifid_yoy",
    "ppifes_mom",
    "ppifes_yoy",
]

DERIVED_SOURCES = sorted({s.rsplit("_", 1)[0] for s in VIZ_DERIVED_SERIES})


def _latest(path: Path) -> str:
    return pl.read_csv(path)["date"].max()[:10]


@pytest.mark.parametrize("series_id,max_age_days", SERIES_MAX_AGE)
def test_raw_series_freshness(series_id, max_age_days):
    path = DATA_DIR / "raw" / f"{series_id}.csv"
    assert path.exists(), f"CSV missing: {path.name}"
    latest = date.fromisoformat(_latest(path))
    age = (date.today() - latest).days
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


@pytest.mark.parametrize("source_id", DERIVED_SOURCES)
def test_derived_in_sync_with_source(source_id):
    raw_latest = _latest(DATA_DIR / "raw" / f"{source_id}.csv")
    for suffix in ("_mom", "_yoy"):
        derived_path = DATA_DIR / "derived" / f"{source_id}{suffix}.csv"
        if not derived_path.exists():
            continue
        derived_latest = _latest(derived_path)
        assert derived_latest == raw_latest, (
            f"{source_id}{suffix}: derived latest {derived_latest} does not match "
            f"raw latest {raw_latest} — re-run derivation"
        )
