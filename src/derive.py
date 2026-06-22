from pathlib import Path

import polars as pl


INFLATION_SERIES = ["cpiaucsl", "cpilfesl", "pcepi", "pcepilfe", "ppifid", "ppifes"]
INCOME_YOY_SERIES = ["w875rx1"]


class Deriver:
    def __init__(self, raw_dir="data/raw", derived_dir="data/derived"):
        self.raw_dir = Path(raw_dir)
        self.derived_dir = Path(derived_dir)
        self.derived_dir.mkdir(parents=True, exist_ok=True)

    def _load(self, series_id):
        path = self.raw_dir / f"{series_id}.csv"
        return (
            pl.read_csv(path)
            .with_columns(pl.col("date").str.to_datetime())
            .sort("date")
        )

    def _save(self, df, name):
        path = self.derived_dir / f"{name}.csv"
        df.write_csv(path)
        print(f"✅ Derived {name}.csv ({len(df)} rows)")

    def _pct_change(self, df, periods):
        return (
            df.with_columns(
                (
                    (pl.col("value") - pl.col("value").shift(periods))
                    / pl.col("value").shift(periods)
                    * 100
                ).alias("value")
            )
            .slice(periods)
            .drop_nulls("value")
        )

    def derive_series(self, series_id):
        df = self._load(series_id)
        self._save(self._pct_change(df, 1), f"{series_id}_mom")
        self._save(self._pct_change(df, 12), f"{series_id}_yoy")

    def derive_all(self):
        for series_id in INFLATION_SERIES:
            try:
                self.derive_series(series_id)
            except Exception as e:
                print(f"❌ Error deriving {series_id}: {e}")
        for series_id in INCOME_YOY_SERIES:
            try:
                df = self._load(series_id)
                self._save(self._pct_change(df, 12), f"{series_id}_yoy")
            except Exception as e:
                print(f"❌ Error deriving {series_id}: {e}")
