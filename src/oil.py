import logging
from pathlib import Path
from datetime import date, timedelta

import polars as pl
import yfinance as yf

# Suppress yfinance's "possibly delisted" / "Failed to get ticker" noise
logging.getLogger('yfinance').setLevel(logging.CRITICAL)

MONTH_CODES = ['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V', 'X', 'Z']

# Yahoo Finance doesn't expose individual Brent (BZ) monthly contracts.
# We use the WTI term structure (CL*.NYM) shifted by the live Brent-WTI
# spread (BZ=F minus CL=F) to produce an estimated Brent futures curve.


class OilCollector:
    """Collects Brent crude oil futures curve from Yahoo Finance (ICE/NYMEX)."""

    def __init__(self, output_dir: str = "data/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _fetch_price(self, ticker: str) -> float | None:
        """Fetch latest close for a ticker; returns None if no recent data."""
        try:
            hist = yf.Ticker(ticker).history(period="5d")
            if hist.empty:
                return None
            last_date = hist.index[-1].date()
            # Skip stale prices from contracts near or past expiry
            if (date.today() - last_date) > timedelta(days=4):
                return None
            return float(hist["Close"].dropna().iloc[-1])
        except Exception:
            return None

    def _wti_contract_tickers(self, months_ahead: int = 18) -> list[tuple[str, int, int]]:
        """Return (ticker, year, month) for WTI monthly contracts going forward.

        Starts 2 months out — skips the nearest-month contract which is often
        in its expiry window (NYMEX WTI expires ~3 business days before the
        25th of the month preceding delivery).
        """
        today = date.today()
        result = []
        for i in range(2, months_ahead + 2):
            total = today.month + i - 1
            month = total % 12 + 1
            year = today.year + total // 12
            code = MONTH_CODES[month - 1]
            result.append((f"CL{code}{str(year)[-2:]}.NYM", year, month))
        return result

    def collect_futures_curve(self) -> bool:
        """
        Fetch an estimated Brent crude futures curve.

        WTI monthly contracts (CL*.NYM) are shifted by the live Brent-WTI
        spread (BZ=F − CL=F) to produce Brent-equivalent prices.
        Returns True if at least some contracts were retrieved.
        """
        print("📊 Fetching Brent crude futures curve (WTI curve + Brent-WTI spread)...")

        brent_spot = self._fetch_price("BZ=F")
        wti_spot   = self._fetch_price("CL=F")
        if brent_spot is None or wti_spot is None:
            print("⚠️  Could not fetch Brent or WTI spot price")
            return False

        spread = brent_spot - wti_spot
        print(f"  Brent spot: ${brent_spot:.2f}  WTI spot: ${wti_spot:.2f}  spread: ${spread:+.2f}")

        rows = []
        for ticker, year, month in self._wti_contract_tickers():
            wti_price = self._fetch_price(ticker)
            if wti_price is not None:
                brent_est = wti_price + spread
                rows.append({"date": f"{year}-{month:02d}-01", "value": round(brent_est, 2)})

        if not rows:
            print("⚠️  Could not fetch any WTI futures contracts")
            return False

        df = pl.DataFrame(rows)
        filepath = self.output_dir / "brent_futures_curve.csv"
        df.write_csv(filepath)
        print(f"✅ Saved brent_futures_curve.csv ({len(df)} contracts, "
              f"{rows[0]['date'][:7]} → {rows[-1]['date'][:7]})")
        return True

    def collect_all(self) -> None:
        self.collect_futures_curve()
