# Economics

US economic data collection and analysis project using FRED and BLS data sources.

## Data Sources

- **FRED (Federal Reserve Economic Data)**: CPI, GDP, Consumer Confidence, Unemployment
- **BLS (Bureau of Labor Statistics)**: Additional labor and economic statistics

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Create `.env` file with API keys:

```bash
FRED_API_TOKEN=your_fred_api_key
```

## Usage

### Data Collection

Collect all data from FRED:

```bash
python main.py --source fred
```

Collect from all sources:

```bash
python main.py --source all
```

Collect specific series:

```bash
python main.py --source fred --series CPIAUCSL
```

### Visualization

Plot a single series:

```bash
python main.py --plot unrate
```

Plot multiple series on the same chart:

```bash
python main.py --plot unrate civpart
```

Custom chart options:

```bash
python main.py --plot unrate --plot-output unemployment.png --plot-title "US Unemployment Rate"
```

#### Unemployment Charts

Plot alternative unemployment measures (U1-U6):

```bash
python main.py --plot U1RATE U2RATE UNRATE U4RATE U5RATE U6RATE \
  --plot-output unemployment_measures.png \
  --plot-title "Alternative Unemployment Measures (U1-U6)"
```

Plot unemployment by age group:

```bash
python main.py --plot LNS14000012 LNS14000036 LNS14000089 LNS14024230 \
  --plot-output unemployment_by_age.png \
  --plot-title "Unemployment Rate by Age Group"
```

Compare official rate with U6 (broadest measure):

```bash
python main.py --plot UNRATE U6RATE --plot-output unrate_vs_u6.png
```

## Data Collected

### Core Economic Indicators

- **CPIAUCSL**: CPI - All Urban Consumers
- **GDP**: Gross Domestic Product
- **UMCSENT**: Consumer Confidence (U. Michigan)
- **UNRATE**: Unemployment Rate (U-3, official rate)
- **CIVPART**: Labor Force Participation Rate

### Alternative Unemployment Measures

- **U1RATE**: Persons unemployed 15 weeks or longer
- **U2RATE**: Job losers and persons who completed temporary jobs
- **U4RATE**: Total unemployed plus discouraged workers
- **U5RATE**: U-4 plus all other marginally attached to labor force
- **U6RATE**: U-5 plus employed part time for economic reasons (broadest measure)

### Unemployment by Age

- **LNS14000012**: Unemployment Rate - Ages 16-19
- **LNS14000036**: Unemployment Rate - Ages 20-24
- **LNS14000089**: Unemployment Rate - Ages 25-54
- **LNS14024230**: Unemployment Rate - Ages 55 and over

Raw data is saved to `data/raw/` as CSV files, with metadata stored in `data/metadata.json`.
