from pathlib import Path
import json
import polars as pl

SPARK_CHARS = "▁▂▃▄▅▆▇█"


def _to_spark_char(value, min_val, max_val):
    if max_val == min_val:
        return SPARK_CHARS[3]
    idx = int((value - min_val) / (max_val - min_val) * (len(SPARK_CHARS) - 1))
    return SPARK_CHARS[max(0, min(len(SPARK_CHARS) - 1, idx))]


def build_sparkline(values: list[float], width: int = 24) -> str:
    if not values:
        return ""
    window = values[-width:]
    lo, hi = min(window), max(window)
    return "".join(_to_spark_char(v, lo, hi) for v in window)


def load_series(series_id: str, data_dir: Path) -> pl.DataFrame:
    path = data_dir / f"{series_id.lower()}.csv"
    df = pl.read_csv(path)
    df = df.with_columns(pl.col("date").str.to_datetime(strict=False))
    df = df.filter(pl.col("value").is_not_nan() & pl.col("value").is_not_null())
    return df.sort("date")


def compute_stats(df: pl.DataFrame, frequency: str) -> dict:
    values = df["value"].to_list()
    dates = df["date"].to_list()

    if not values:
        return {}

    latest = values[-1]
    latest_date = dates[-1].strftime("%Y-%m-%d") if dates else ""

    prev_val = values[-2] if len(values) >= 2 else None
    change_prev = latest - prev_val if prev_val is not None else None

    freq = (frequency or "").lower()
    if "weekly" in freq:
        lookback = 52
    elif "quarterly" in freq:
        lookback = 4
    else:
        lookback = 12

    yoy_val = values[-(lookback + 1)] if len(values) > lookback else None
    change_yoy = latest - yoy_val if yoy_val is not None else None

    sparkline = build_sparkline(values)

    return {
        "latest": latest,
        "latest_date": latest_date,
        "change_prev": change_prev,
        "change_yoy": change_yoy,
        "sparkline": sparkline,
    }


def _fmt_change(val, units: str) -> str:
    if val is None:
        return "—"
    sign = "+" if val >= 0 else ""
    if "percent" in units.lower() or units.lower() == "percent":
        return f"{sign}{val:.1f}pp"
    if "billion" in units.lower():
        return f"{sign}{val:.1f}B"
    if "number" in units.lower():
        return f"{sign}{val:,.0f}"
    return f"{sign}{val:.2f}"


def _fmt_value(val, units: str) -> str:
    if "percent" in units.lower() or units.lower() == "percent":
        return f"{val:.1f}%"
    if "billion" in units.lower():
        return f"${val:,.1f}B"
    if "number" in units.lower():
        return f"{val:,.0f}"
    return f"{val:.2f}"


def _row_cells(label: str, stats: dict, meta: dict) -> list[str]:
    units = meta.get("units", "Value")
    return [
        label,
        f"`{stats['sparkline']}`",
        _fmt_value(stats["latest"], units),
        _fmt_change(stats.get("change_prev"), units),
        _fmt_change(stats.get("change_yoy"), units),
        stats["latest_date"],
    ]


def _format_table(header: list[str], rows: list[list[str]]) -> str:
    all_rows = [header] + rows
    col_widths = [max(len(row[c]) for row in all_rows) for c in range(len(header))]

    def pad_row(cells):
        return "| " + " | ".join(c.ljust(w) for c, w in zip(cells, col_widths)) + " |"

    separator = "| " + " | ".join("-" * w for w in col_widths) + " |"

    table_lines = [pad_row(header), separator]
    table_lines += [pad_row(r) for r in rows]
    return "\n".join(table_lines)


def build_dashboard(data_dir: str = "data/raw") -> str:
    data_path = Path(data_dir)
    metadata_file = data_path.parent / "metadata.json"
    with open(metadata_file) as f:
        metadata = json.load(f)

    sections = [
        (
            "Labor Market Overview",
            [
                ("unrate", "Unemployment Rate (U-3)"),
                ("civpart", "Labor Force Participation"),
                ("icsa", "Initial Jobless Claims"),
                ("ccsa", "Continued Claims"),
            ],
        ),
        (
            "Unemployment Measures (U1–U6)",
            [
                ("u1rate", "U-1: 15+ Weeks Unemployed"),
                ("u2rate", "U-2: Job Losers"),
                ("unrate", "U-3: Official Rate"),
                ("u4rate", "U-4: + Discouraged Workers"),
                ("u5rate", "U-5: + Marginally Attached"),
                ("u6rate", "U-6: + Part-Time Economic"),
            ],
        ),
        (
            "Unemployment by Age",
            [
                ("lns14000012", "Ages 16–19"),
                ("lns14000036", "Ages 20–24"),
                ("lns14000089", "Ages 25–54"),
                ("lns14024230", "Ages 55+"),
            ],
        ),
        (
            "Economy",
            [
                ("gdp", "GDP"),
                ("cpiaucsl", "CPI (All Urban)"),
                ("umcsent", "Consumer Sentiment (U. Mich.)"),
            ],
        ),
    ]

    lines = []
    lines.append(
        "_Sparklines show the last 24 data points (monthly), "
        "52 points (weekly), or 8 points (quarterly)._\n"
    )

    for section_title, series_list in sections:
        lines.append(f"### {section_title}\n")

        freqs = {
            metadata.get(sid, {}).get("frequency", "Monthly").split(",")[0].lower()
            for sid, _ in series_list
        }
        if len(freqs) > 1:
            period_col, yoy_col = "Chg (prev)", "Chg (1Y)"
        elif "weekly" in next(iter(freqs)):
            period_col, yoy_col = "WoW", "YoY (52w)"
        elif "quarterly" in next(iter(freqs)):
            period_col, yoy_col = "QoQ", "YoY (4q)"
        else:
            period_col, yoy_col = "MoM", "YoY (12m)"

        header = [
            "Indicator",
            "Trend (sparkline)",
            "Latest",
            period_col,
            yoy_col,
            "As of",
        ]
        rows = []
        for series_id, label in series_list:
            try:
                df = load_series(series_id, data_path)
                meta = metadata.get(series_id, {})
                freq = meta.get("frequency", "Monthly")
                stats = compute_stats(df, freq)
                rows.append(_row_cells(label, stats, meta))
            except Exception as e:
                rows.append([label, f"_(error: {e})_", "—", "—", "—", "—"])

        lines.append(_format_table(header, rows))
        lines.append("")

    return "\n".join(lines)
