# Setup

## Data Collection

Collect all data from FRED:

```bash
uv run python main.py --source fred
```

Collect from all sources:

```bash
uv run python main.py --source all
```

Collect a specific series:

```bash
uv run python main.py --source fred --series CPIAUCSL
```

## Visualization

Plot a single series:

```bash
uv run python main.py --plot unrate
```

Plot multiple series on the same chart:

```bash
uv run python main.py --plot unrate civpart
```

Custom chart options:

```bash
uv run python main.py --plot unrate --plot-output unemployment.png --plot-title "US Unemployment Rate"
```

### Unemployment Charts

Plot alternative unemployment measures (U1-U6):

```bash
uv run python main.py --plot U1RATE U2RATE UNRATE U4RATE U5RATE U6RATE \
  --plot-output unemployment_measures.png \
  --plot-title "Alternative Unemployment Measures (U1-U6)"
```

Plot unemployment by age group:

```bash
uv run python main.py --plot LNS14000012 LNS14000036 LNS14000089 LNS14024230 \
  --plot-output unemployment_by_age.png \
  --plot-title "Unemployment Rate by Age Group"
```

Compare official rate with U6 (broadest measure):

```bash
uv run python main.py --plot UNRATE U6RATE --plot-output unrate_vs_u6.png
```

## README Dashboard

Regenerate the economic dashboard in `README.md`:

```bash
uv run python -m src.readme_updater
```

This is also run automatically by the GitHub Actions workflow on each data update.
