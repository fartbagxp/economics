"""
NY Fed Household Debt and Credit collector.

Data source: Federal Reserve Bank of New York, Consumer Credit Panel (based on Equifax data).
Report: Household Debt and Credit — quarterly Excel workbook published at
https://www.newyorkfed.org/microeconomics/hhdc

The workbook sheet "Page 3 Data" contains total debt balances by category in
trillions of dollars going back to Q1 1999. Categories:
  Mortgage, HE Revolving (HELOC), Auto Loan, Credit Card, Student Loan, Other

"Other" is a catch-all that includes medical debt, personal loans, and retail
financing — it is the only publicly available proxy for medical debt at this
time granularity.

Output CSV files use millions of dollars (consistent with FRED series) so the
viz layer can treat all debt series uniformly.
"""

from datetime import date
from pathlib import Path
import json
import re

import polars as pl
import requests


BASE_URL = "https://www.newyorkfed.org/medialibrary/interactives/householdcredit/data/xls"
FILENAME_PATTERN = "HHD_C_Report_{year}Q{quarter}.xlsx"

SHEET_NAME = "Page 3 Data"

# Output CSV names → column name in the Excel sheet (case-insensitive prefix match)
SERIES = {
    "nyfed_mortgage":    "Mortgage",
    "nyfed_he_revolving": "HE Revolving",
    "nyfed_auto":        "Auto Loan",
    "nyfed_credit_card": "Credit Card",
    "nyfed_student":     "Student Loan",
    "nyfed_other":       "Other",
    "nyfed_total":       "Total",
}

METADATA = {
    "nyfed_mortgage":     {"title": "NY Fed: Mortgage Debt Balance",             "units": "Millions of U.S. Dollars", "frequency": "Quarterly", "seasonal_adjustment": "Not Seasonally Adjusted", "source": "NY Fed / Equifax Consumer Credit Panel", "source_url": "https://www.newyorkfed.org/microeconomics/hhdc"},
    "nyfed_he_revolving": {"title": "NY Fed: Home Equity Revolving (HELOC) Balance", "units": "Millions of U.S. Dollars", "frequency": "Quarterly", "seasonal_adjustment": "Not Seasonally Adjusted", "source": "NY Fed / Equifax Consumer Credit Panel", "source_url": "https://www.newyorkfed.org/microeconomics/hhdc"},
    "nyfed_auto":         {"title": "NY Fed: Auto Loan Balance",                 "units": "Millions of U.S. Dollars", "frequency": "Quarterly", "seasonal_adjustment": "Not Seasonally Adjusted", "source": "NY Fed / Equifax Consumer Credit Panel", "source_url": "https://www.newyorkfed.org/microeconomics/hhdc"},
    "nyfed_credit_card":  {"title": "NY Fed: Credit Card Balance",               "units": "Millions of U.S. Dollars", "frequency": "Quarterly", "seasonal_adjustment": "Not Seasonally Adjusted", "source": "NY Fed / Equifax Consumer Credit Panel", "source_url": "https://www.newyorkfed.org/microeconomics/hhdc"},
    "nyfed_student":      {"title": "NY Fed: Student Loan Balance",              "units": "Millions of U.S. Dollars", "frequency": "Quarterly", "seasonal_adjustment": "Not Seasonally Adjusted", "source": "NY Fed / Equifax Consumer Credit Panel", "source_url": "https://www.newyorkfed.org/microeconomics/hhdc"},
    "nyfed_other":        {"title": "NY Fed: Other Debt Balance (incl. medical)", "units": "Millions of U.S. Dollars", "frequency": "Quarterly", "seasonal_adjustment": "Not Seasonally Adjusted", "source": "NY Fed / Equifax Consumer Credit Panel", "source_url": "https://www.newyorkfed.org/microeconomics/hhdc"},
    "nyfed_total":        {"title": "NY Fed: Total Household Debt Balance",       "units": "Millions of U.S. Dollars", "frequency": "Quarterly", "seasonal_adjustment": "Not Seasonally Adjusted", "source": "NY Fed / Equifax Consumer Credit Panel", "source_url": "https://www.newyorkfed.org/microeconomics/hhdc"},
}


class NyFedCollector:
    def __init__(self, output_dir: str = "data/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.output_dir.parent / "metadata.json"

    def _latest_report_url(self) -> tuple[str, str]:
        """Return (url, label) for the most recent available quarterly report."""
        today = date.today()
        # Current quarter — NY Fed publishes ~5–6 weeks after quarter-end,
        # so subtract one quarter as the most likely published quarter.
        current_q = (today.month - 1) // 3 + 1
        current_year = today.year

        # Build candidates starting one quarter back from today
        candidates = []
        y, q = current_year, current_q - 1
        if q == 0:
            y -= 1
            q = 4
        for _ in range(8):  # check up to 8 quarters back
            candidates.append((y, q))
            q -= 1
            if q == 0:
                y -= 1
                q = 4

        for year, quarter in candidates:
            filename = FILENAME_PATTERN.format(year=year, quarter=quarter)
            url = f"{BASE_URL}/{filename}"
            try:
                r = requests.head(url, timeout=10, allow_redirects=True,
                                  headers={"User-Agent": "Mozilla/5.0"})
                ct = r.headers.get("Content-Type", "")
                # xlsx files are application/vnd.openxmlformats... or application/zip/octet-stream
                if r.status_code == 200 and ("spreadsheet" in ct or "zip" in ct or "octet" in ct or "excel" in ct):
                    return url, f"{year}Q{quarter}"
            except requests.RequestException:
                continue

        # Fall back: try downloading each candidate and check magic bytes
        for year, quarter in candidates:
            filename = FILENAME_PATTERN.format(year=year, quarter=quarter)
            url = f"{BASE_URL}/{filename}"
            try:
                r = requests.get(url, timeout=30, stream=True,
                                 headers={"User-Agent": "Mozilla/5.0"})
                first_bytes = next(r.iter_content(4), b"")
                r.close()
                # xlsx (zip) magic: PK\x03\x04
                if first_bytes[:2] == b"PK":
                    return url, f"{year}Q{quarter}"
            except requests.RequestException:
                continue

        raise RuntimeError("Could not find a valid NY Fed report. Try: python main.py --source nyfed --nyfed-quarter 2025Q1")

    def _download_workbook(self, url: str):
        """Download the Excel workbook and return as bytes."""
        print(f"⬇️  Downloading {url} ...")
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        return r.content

    def _parse_workbook(self, content: bytes) -> pl.DataFrame:
        """Parse the 'Page 3 Data' sheet and return a tidy DataFrame."""
        import io
        from openpyxl import load_workbook

        wb = load_workbook(io.BytesIO(content), data_only=True)

        # Find the right sheet — name varies slightly across report vintages
        sheet = None
        for name in wb.sheetnames:
            if re.search(r"page.?3", name, re.IGNORECASE) or re.search(r"total.?balance", name, re.IGNORECASE):
                sheet = wb[name]
                break
        if sheet is None:
            # Fall back: first sheet that has "Mortgage" in any cell of row 1–5
            for name in wb.sheetnames:
                ws = wb[name]
                header_text = " ".join(
                    str(ws.cell(r, c).value or "")
                    for r in range(1, 6)
                    for c in range(1, 15)
                )
                if "Mortgage" in header_text:
                    sheet = ws
                    break
        if sheet is None:
            available = ", ".join(wb.sheetnames)
            raise RuntimeError(f"Could not locate debt-balance sheet. Available sheets: {available}")

        # Read all rows into a list-of-lists
        rows = [[cell.value for cell in row] for row in sheet.iter_rows()]

        # Locate header row (contains "Mortgage")
        header_idx = None
        for i, row in enumerate(rows):
            row_text = " ".join(str(v or "") for v in row)
            if "Mortgage" in row_text and "Total" in row_text:
                header_idx = i
                break
        if header_idx is None:
            raise RuntimeError("Could not find header row with 'Mortgage' and 'Total'")

        headers = [str(v or "").strip() for v in rows[header_idx]]

        # Map column names → indices
        col_map = {}
        for series_key, col_label in SERIES.items():
            for idx, h in enumerate(headers):
                if col_label.lower() in h.lower():
                    col_map[series_key] = idx
                    break

        # Find date column (first column that looks like a quarter label e.g. "99:Q1")
        date_col = 0  # usually column 0

        records = []
        for row in rows[header_idx + 1:]:
            if not row or row[date_col] is None:
                continue
            raw_date = str(row[date_col]).strip()
            # Parse formats: "99:Q1", "2003:Q1", "Q1 1999", "1999Q1"
            parsed = _parse_quarter_date(raw_date)
            if parsed is None:
                continue
            record = {"date": parsed}
            for series_key, col_idx in col_map.items():
                try:
                    val = row[col_idx]
                    if val is not None:
                        # Values are in trillions → convert to millions (*1e6)
                        record[series_key] = float(val) * 1_000_000
                except (TypeError, ValueError):
                    pass
            records.append(record)

        return pl.DataFrame(records)

    def save_metadata(self, series_id: str, extra: dict = None):
        if self.metadata_file.exists():
            with open(self.metadata_file) as f:
                all_meta = json.load(f)
        else:
            all_meta = {}
        entry = dict(METADATA[series_id])
        entry["last_updated"] = date.today().isoformat()
        if extra:
            entry.update(extra)
        all_meta[series_id] = entry
        with open(self.metadata_file, "w") as f:
            json.dump(all_meta, f, indent=2)

    def collect_all(self, quarter: str = None):
        if quarter:
            m = re.match(r"(\d{4})Q(\d)", quarter.upper())
            if not m:
                raise ValueError(f"Invalid quarter format '{quarter}'. Use e.g. 2024Q4")
            year, q = int(m.group(1)), int(m.group(2))
            filename = FILENAME_PATTERN.format(year=year, quarter=q)
            url = f"{BASE_URL}/{filename}"
            label = quarter.upper()
        else:
            url, label = self._latest_report_url()

        print(f"📊 NY Fed Household Debt Report — {label}")
        content = self._download_workbook(url)
        df = self._parse_workbook(content)

        if df.is_empty():
            print("❌ Parsed DataFrame is empty — check sheet structure")
            return

        for series_key in SERIES:
            if series_key not in df.columns:
                print(f"⚠️  Column missing for {series_key}, skipping")
                continue
            out = df.select(["date", series_key]).rename({series_key: "value"}).drop_nulls()
            filepath = self.output_dir / f"{series_key}.csv"
            out.write_csv(filepath)
            self.save_metadata(series_key)
            print(f"✅ Saved {series_key}.csv ({len(out)} rows, {out['date'].min()} to {out['date'].max()})")


def _parse_quarter_date(raw: str) -> str | None:
    """Convert quarter labels like '99:Q1', '2003:Q1', 'Q1 2003' to ISO date strings."""
    raw = raw.strip()
    # "YY:Q#" or "YYYY:Q#"
    m = re.match(r"(\d{2,4}):Q(\d)", raw)
    if m:
        year, quarter = int(m.group(1)), int(m.group(2))
        if year < 100:
            year += 1900 if year >= 99 else 2000
        return _quarter_to_date(year, quarter)
    # "Q# YYYY" or "Q#YYYY"
    m = re.match(r"Q(\d)\s*(\d{4})", raw, re.IGNORECASE)
    if m:
        return _quarter_to_date(int(m.group(2)), int(m.group(1)))
    # "YYYYQ#"
    m = re.match(r"(\d{4})Q(\d)", raw, re.IGNORECASE)
    if m:
        return _quarter_to_date(int(m.group(1)), int(m.group(2)))
    return None


def _quarter_to_date(year: int, quarter: int) -> str:
    """Return the last month of the quarter as ISO YYYY-MM-01."""
    month = quarter * 3
    return f"{year}-{month:02d}-01"
