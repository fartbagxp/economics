"""
Sanity checks for data freshness and viz coverage.

Freshness thresholds are based on typical release lags per frequency:
  - Weekly (ICSA, CCSA): released every Thursday, expect data within 21 days
  - Monthly: observation date is the 1st of the month; data released up to ~6 weeks
    later, so worst-case age just before the next release is ~66 days (75-day threshold)
  - PCE: released last Friday of following month, same lag profile (75 days)
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
    ("unrate", 60),
    ("civpart", 60),
    ("u1rate", 60),
    ("u2rate", 60),
    ("u4rate", 60),
    ("u5rate", 60),
    ("u6rate", 60),
    ("lns14000012", 60),
    ("lns14000036", 60),
    ("lns14000089", 60),
    ("lns14024230", 60),
    ("uemp27ov", 60),
    ("lns13008397", 60),
    ("lns11300001", 60),
    ("lns11300002", 60),
    ("lns11327659", 60),
    ("lns11327660", 60),
    ("lns11327689", 60),
    ("lns11327662", 60),
    ("jtshir", 75),
    ("cpiaucsl", 75),
    ("cpilfesl", 75),
    ("umcsent", 75),
    ("pcepi", 75),
    ("pcepilfe", 75),
    ("ppifid", 75),
    ("ppifes", 75),
    # Quarterly — observation date is quarter start, not release date
    ("gdp", 215),
    # Monthly — personal income & outlays (released ~30 days after month end)
    ("pi", 75),
    ("dspi", 75),
    ("pce", 75),
    ("psave", 215),
    ("psavert", 75),
    ("mich", 75),
    # Daily — TIPS-based breakeven rates
    ("t5yie", 21),
    ("t10yie", 21),
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
