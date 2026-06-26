# Adding a New Data Series

Four files to touch, in order.

---

## 1. Register in the collector

**FRED series**: add to `series_map` in `src/fred.py` `collect_all()`:

```python
"SERIES_ID": "Human-readable name",
```

**BLS or other source**: add a `collect_series()` call in the relevant collector (`src/bls.py`) or create a new collector class following the same pattern.

---

## 2. Collect the data

```bash
uv run python main.py --source fred --series SERIES_ID
# or for all at once:
uv run python main.py --source fred
```

This writes `data/raw/series_id.csv` and updates `data/metadata.json` automatically.

---

## 3. Add to freshness checks (`tests/test_freshness.py`)

Add a `(series_id_lowercase, max_age_days)` tuple to `SERIES_MAX_AGE`. Pick the threshold based on release frequency:

| Release cadence               | Threshold |
| ----------------------------- | --------- |
| Weekly (e.g. jobless claims)  | `21`      |
| Monthly, jobs report (BLS)    | `60`      |
| Monthly, lagged (CPI, JOLTS)  | `75`      |
| Quarterly (GDP)               | `215`     |

Then verify:

```bash
uv run pytest tests/test_freshness.py -v
```

---

## 4. Expose to the viz (`viz/src/routes/+page.server.js`)

Add the lowercase series ID to `RAW_SERIES` (or `DERIVED_SERIES` if it lives in `data/derived/`):

```js
const RAW_SERIES = [
  'unrate', ...,
  'new_series_id',   // ← add here
];
```

The series data and metadata will now be available to the Svelte page as `data.series.new_series_id` and `data.metadata.new_series_id`.

---

## Quick checklist

- [ ] Series ID added to collector
- [ ] `uv run python main.py --source fred --series SERIES_ID` succeeds
- [ ] CSV exists in `data/raw/`
- [ ] Entry added to `SERIES_MAX_AGE` in `tests/test_freshness.py`
- [ ] `uv run pytest tests/test_freshness.py -v` all green
- [ ] Series ID added to `RAW_SERIES` in `viz/src/routes/+page.server.js`
