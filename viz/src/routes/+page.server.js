import { readFileSync, existsSync } from 'fs';
import { join } from 'path';

const RAW_SERIES = [
  'unrate', 'u6rate', 'lns13008397', 'uemp27ov',
  'civpart', 'lns11300001', 'lns11300002',
  'lns11327659', 'lns11327660', 'lns11327689', 'lns11327662',
  'icsa',
  'cpiaucsl',
  'gdp', 'umcsent',
  'pi', 'w875rx1', 'dspi', 'pce', 'psave', 'psavert',
  'mich', 't5yie', 't10yie',
  'hhmsdodns', 'revolsl', 'sloas', 'mvloas', 'nonrevsl',
  'dcoilbrenteu',
  'gs2', 'gs10', 'gs20', 'gs30', 'fedfunds',
  'dfedtaru', 'dfedtarl',
];

// NY Fed series are optional — charts degrade gracefully if not yet collected
const NYFED_SERIES = [
  'nyfed_mortgage', 'nyfed_he_revolving', 'nyfed_auto',
  'nyfed_credit_card', 'nyfed_student', 'nyfed_other', 'nyfed_total',
];

// Oil futures curve is optional — populated by: python main.py --source oil
const OIL_SERIES = ['brent_futures_curve'];

const DERIVED_SERIES = [
  'cpiaucsl_mom', 'cpiaucsl_yoy',
  'cpilfesl_mom', 'cpilfesl_yoy',
  'pcepi_mom',    'pcepi_yoy',
  'pcepilfe_mom', 'pcepilfe_yoy',
  'ppifid_mom',   'ppifid_yoy',
  'ppifes_mom',   'ppifes_yoy',
  'w875rx1_yoy',
];

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
  const derived = Object.fromEntries(
    DERIVED_SERIES.map((id) => [id, loadCsv(join(process.cwd(), '..', 'data', 'derived', `${id}.csv`))])
  );
  return { series: { ...raw, ...nyfed, ...oil, ...derived }, metadata };
}
