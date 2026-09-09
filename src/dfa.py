"""
Household wealth by percentile collector (Federal Reserve DFA).

Data source: Federal Reserve Board, Distributional Financial Accounts.
https://www.federalreserve.gov/releases/z1/dataviz/dfa/

Downloads the DFA bulk archive and extracts `dfa-networth-levels.csv`, which
reports household net worth by wealth percentile group for every quarter since
1989:Q3. The Fed publishes five groups (top 0.1%, next 0.9%, next 9%, next 40%,
bottom 50%); this collector emits the four the dashboard charts, summing the
top two into a single top-1% column.

Unlike most collectors here this one writes a wide CSV — one column per
percentile group rather than a single `value` column — because the four groups
are only meaningful read together as a distribution.

Levels stay in the units the Fed publishes: millions of dollars.
"""

import io
import json
import zipfile
from datetime import UTC, datetime
from pathlib import Path

import polars as pl
import requests

ZIP_URL = "https://www.federalreserve.gov/releases/z1/dataviz/download/zips/dfa.zip"
LEVELS_FILE = "dfa-networth-levels.csv"

QUARTER_START_MONTH = {"Q1": 1, "Q2": 4, "Q3": 7, "Q4": 10}

# Output column -> source category / categories in dfa-networth-levels.csv
PERCENTILE_GROUPS = {
    "top_1pct": ("TopPt1", "RemainingTop1"),
    "pct_90_99": ("Next9",),
    "pct_50_90": ("Next40",),
    "bottom_50pct": ("Bottom50",),
}

METADATA = {
    "title": "Household Net Worth by Wealth Percentile (DFA)",
    "units": "Millions of U.S. Dollars",
    "frequency": "Quarterly",
    "seasonal_adjustment": "Not Seasonally Adjusted",
    "source": "Federal Reserve Board, Distributional Financial Accounts",
    "source_url": "https://www.federalreserve.gov/releases/z1/dataviz/dfa/",
}


def _quarter_to_iso(label: str) -> str:
    """Convert a DFA quarter label like '1989:Q3' to the first day of that quarter.

    FRED dates the equivalent WFRBL* series the same way, and it matches how
    quarterly series are stored elsewhere in this repo. The value itself is the
    level at the *end* of the quarter.
    """
    year, quarter = label.strip().split(":")
    return f"{int(year):04d}-{QUARTER_START_MONTH[quarter]:02d}-01"


class DfaCollector:
    """Collector for Federal Reserve DFA household net worth by wealth percentile."""

    def __init__(self, output_dir: str = "data/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.output_dir.parent / "metadata.json"

    def _download_levels(self) -> bytes:
        print(f"⬇️  Fetching {ZIP_URL} ...")
        r = requests.get(ZIP_URL, timeout=120)
        r.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(r.content)) as archive:
            names = archive.namelist()
            if LEVELS_FILE not in names:
                raise RuntimeError(
                    f"{LEVELS_FILE} not found in DFA archive (contains: {', '.join(sorted(names))})"
                )
            return archive.read(LEVELS_FILE)

    def save_metadata(self):
        if self.metadata_file.exists():
            with open(self.metadata_file) as f:
                all_meta = json.load(f)
        else:
            all_meta = {}
        entry = dict(METADATA)
        entry["last_updated"] = datetime.now(UTC).date().isoformat()
        all_meta["fed_dfa_wealth_by_percentile"] = entry
        with open(self.metadata_file, "w") as f:
            json.dump(all_meta, f, indent=2)
            f.write("\n")

    def collect_all(self):
        print("📊 Federal Reserve Distributional Financial Accounts")
        content = self._download_levels()

        df = pl.read_csv(io.BytesIO(content)).select("Date", "Category", "Net worth")

        missing = {c for group in PERCENTILE_GROUPS.values() for c in group} - set(
            df["Category"].unique().to_list()
        )
        if missing:
            raise RuntimeError(
                f"DFA net worth file is missing expected categories: {sorted(missing)}"
            )

        wide = df.pivot(on="Category", index="Date", values="Net worth").with_columns(
            pl.col("Date")
            .map_elements(_quarter_to_iso, return_dtype=pl.Utf8)
            .str.to_date()
            .alias("date")
        )
        wide = wide.with_columns(
            [
                pl.sum_horizontal(pl.col(c) for c in sources).alias(name)
                for name, sources in PERCENTILE_GROUPS.items()
            ]
        )

        out = (
            wide.select("date", *PERCENTILE_GROUPS)
            .drop_nulls()
            .unique(subset="date")
            .sort("date")
        )

        if out.is_empty():
            raise RuntimeError("No DFA net worth records parsed from the archive")

        filepath = self.output_dir / "fed_dfa_wealth_by_percentile.csv"
        out.write_csv(filepath)
        self.save_metadata()
        print(
            f"✅ Saved fed_dfa_wealth_by_percentile.csv ({len(out)} rows, "
            f"{out['date'].min()} to {out['date'].max()})"
        )
        return out
