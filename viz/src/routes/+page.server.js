import { readFileSync, existsSync } from 'fs';
import { join } from 'path';

const RAW_SERIES = [
  'unrate', 'u6rate', 'lns13025703', 'uemp27ov',
  'civpart', 'lns11300001', 'lns11300002',
  'lns11327659', 'lns11327660', 'lns11327689', 'lns11327662',
  'icsa',
  'cpiaucsl',
  'gdp', 'umcsent',
  'pi', 'w875rx1', 'dspi', 'pce', 'psave', 'psavert',
  'mich', 't5yie', 't10yie',
  'hhmsdodns', 'revolsl', 'sloas', 'mvloas', 'nonrevsl',
  'dcoilbrenteu', 'gasregw', 'gasdesw',
  'gs2', 'gs10', 'gs20', 'gs30', 'fedfunds',
  'dfedtaru', 'dfedtarl',
  'mortgage30us', 'mortgage15us',
  'gfdebtn',
];

// NY Fed series are optional — charts degrade gracefully if not yet collected
const NYFED_SERIES = [
  'nyfed_mortgage', 'nyfed_he_revolving', 'nyfed_auto',
  'nyfed_credit_card', 'nyfed_student', 'nyfed_other', 'nyfed_total',
  'nyfed_delinq_mortgage', 'nyfed_delinq_he_revolving', 'nyfed_delinq_auto',
  'nyfed_delinq_credit_card', 'nyfed_delinq_student', 'nyfed_delinq_other',
  'nyfed_delinq_total',
  'nyfed_bankruptcy_total',
];

// Oil futures curve is optional — populated by: python main.py --source oil
const OIL_SERIES = ['brent_futures_curve'];

// Supply chain pressure is optional — populated by: python main.py --source gscpi
const GSCPI_SERIES = ['gscpi'];

// Regional Fed manufacturing surveys (ISM PMI proxies) are optional —
// populated by: python main.py --source fred
const MANUFACTURING_SERIES = ['gacdfsa066msfrbphi', 'gacdisa066msfrbny', 'bactsamfrbdal'];

// Payrolls are optional — populated by: python main.py --source bls
const BLS_SERIES = ['ces0000000001'];

// Social program enrollment is optional — populated by:
// python main.py --source snap / --source medicare / --source medicaid
const SOCIAL_SERIES = ['snap_persons', 'medicare_total_enrollment', 'medicaid_chip_enrollment'];

// Consumer Expenditure Survey spending by age is optional — populated by:
// python main.py --source ce
const CE_SERIES = [
  'ce_totalexp_all',
  'ce_totalexp_lt25', 'ce_totalexp_25_34', 'ce_totalexp_35_44',
  'ce_totalexp_45_54', 'ce_totalexp_55_64', 'ce_totalexp_65up',
  'ce_totalexp_65_74', 'ce_totalexp_75up',
];

// Household wealth by percentile (Fed DFA) is optional and wide-format — one
// column per percentile group rather than the usual date,value pair.
// Populated by: python main.py --source dfa
const WEALTH_COLUMNS = ['top_1pct', 'pct_90_99', 'pct_50_90', 'bottom_50pct'];

const BANKRUPTCY_AGE_COLUMNS = [
  'age_18_29', 'age_30_39', 'age_40_49', 'age_50_59', 'age_60_69', 'age_70up',
];

const DERIVED_SERIES = [
  'cpiaucsl_mom', 'cpiaucsl_yoy',
  'cpilfesl_mom', 'cpilfesl_yoy',
  'pcepi_mom',    'pcepi_yoy',
  'pcepilfe_mom', 'pcepilfe_yoy',
  'ppifid_mom',   'ppifid_yoy',
  'ppifes_mom',   'ppifes_yoy',
  'w875rx1_yoy',
];

// Payroll change is optional, same as BLS_SERIES above
const DERIVED_SERIES_OPTIONAL = ['ces0000000001_chg', 'ces0000000001_chg_3mo', 'ces0500000003_yoy'];

function loadCsv(path) {
  const raw = readFileSync(path, 'utf-8');
  return raw.trim().split('\n').slice(1)
    .map((line) => {
      const [dateStr, val] = line.split(',');
      const value = parseFloat(val);
      return isNaN(value) ? null : { date: dateStr.slice(0, 10), value };
    })
    .filter(Boolean);
}

function loadCsvOptional(path) {
  if (!existsSync(path)) return [];
  return loadCsv(path);
}

// Reads a CSV with several data columns into one row object per date.
// Rows with a missing or unparseable cell in any requested column are dropped.
function loadWideCsvOptional(path, columns) {
  if (!existsSync(path)) return [];
  const lines = readFileSync(path, 'utf-8').trim().split('\n');
  const header = lines[0].split(',');
  const indexes = columns.map((c) => header.indexOf(c));
  if (indexes.some((i) => i < 0)) return [];
  return lines.slice(1)
    .map((line) => {
      const cells = line.split(',');
      const row = { date: cells[0].slice(0, 10) };
      columns.forEach((c, i) => {
        const value = parseFloat(cells[indexes[i]]);
        row[c] = isNaN(value) ? null : value;
      });
      return row;
    })
    .filter((row) => columns.every((c) => row[c] !== null));
}

// The daily Treasury debt file is ~8k rows and only its latest reading is shown,
// so read the last line rather than shipping the whole series to the client.
// Populated by: python main.py --source treasury
function loadLatestOptional(path) {
  if (!existsSync(path)) return null;
  const lines = readFileSync(path, 'utf-8').trim().split('\n');
  if (lines.length < 2) return null;
  const [dateStr, val] = lines[lines.length - 1].split(',');
  const value = parseFloat(val);
  return isNaN(value) ? null : { date: dateStr.slice(0, 10), value };
}

function loadMetadata() {
  const p = join(process.cwd(), '..', 'data', 'metadata.json');
  return JSON.parse(readFileSync(p, 'utf-8'));
}

export function load() {
  const metadata = loadMetadata();
  const raw = Object.fromEntries(
    RAW_SERIES.map((id) => [id, loadCsv(join(process.cwd(), '..', 'data', 'raw', `${id}.csv`))])
  );
  const nyfed = Object.fromEntries(
    NYFED_SERIES.map((id) => [id, loadCsvOptional(join(process.cwd(), '..', 'data', 'raw', `${id}.csv`))])
  );
  const oil = Object.fromEntries(
    OIL_SERIES.map((id) => [id, loadCsvOptional(join(process.cwd(), '..', 'data', 'raw', `${id}.csv`))])
  );
  const bls = Object.fromEntries(
    BLS_SERIES.map((id) => [id, loadCsvOptional(join(process.cwd(), '..', 'data', 'raw', `${id}.csv`))])
  );
  const gscpi = Object.fromEntries(
    GSCPI_SERIES.map((id) => [id, loadCsvOptional(join(process.cwd(), '..', 'data', 'raw', `${id}.csv`))])
  );
  const manufacturing = Object.fromEntries(
    MANUFACTURING_SERIES.map((id) => [id, loadCsvOptional(join(process.cwd(), '..', 'data', 'raw', `${id}.csv`))])
  );
  const social = Object.fromEntries(
    SOCIAL_SERIES.map((id) => [id, loadCsvOptional(join(process.cwd(), '..', 'data', 'raw', `${id}.csv`))])
  );
  const ce = Object.fromEntries(
    CE_SERIES.map((id) => [id, loadCsvOptional(join(process.cwd(), '..', 'data', 'raw', `${id}.csv`))])
  );
  const wealth = loadWideCsvOptional(
    join(process.cwd(), '..', 'data', 'raw', 'fed_dfa_wealth_by_percentile.csv'),
    WEALTH_COLUMNS
  );
  const bankruptcyByAge = loadWideCsvOptional(
    join(process.cwd(), '..', 'data', 'raw', 'nyfed_bankruptcy_by_age.csv'),
    BANKRUPTCY_AGE_COLUMNS
  );
  const treasuryDebtLatest = loadLatestOptional(
    join(process.cwd(), '..', 'data', 'raw', 'treasury_national_debt.csv')
  );
  const derived = Object.fromEntries(
    DERIVED_SERIES.map((id) => [id, loadCsv(join(process.cwd(), '..', 'data', 'derived', `${id}.csv`))])
  );
  const derivedOptional = Object.fromEntries(
    DERIVED_SERIES_OPTIONAL.map((id) => [id, loadCsvOptional(join(process.cwd(), '..', 'data', 'derived', `${id}.csv`))])
  );
  return {
    series: { ...raw, ...nyfed, ...oil, ...bls, ...gscpi, ...manufacturing, ...social, ...ce, ...derived, ...derivedOptional },
    wealth,
    bankruptcyByAge,
    treasuryDebtLatest,
    metadata,
  };
}
