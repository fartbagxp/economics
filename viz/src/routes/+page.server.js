import { readFileSync } from 'fs';
import { join } from 'path';

const RAW_SERIES = [
  'unrate', 'u6rate', 'civpart', 'icsa',
  'cpiaucsl',
  'gdp', 'umcsent',
];

const DERIVED_SERIES = [
  'cpiaucsl_mom', 'cpiaucsl_yoy',
  'cpilfesl_mom', 'cpilfesl_yoy',
  'pcepi_mom',    'pcepi_yoy',
  'pcepilfe_mom', 'pcepilfe_yoy',
  'ppifid_mom',   'ppifid_yoy',
  'ppifes_mom',   'ppifes_yoy',
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

function loadMetadata() {
  const p = join(process.cwd(), '..', 'data', 'metadata.json');
  return JSON.parse(readFileSync(p, 'utf-8'));
}

export function load() {
  const metadata = loadMetadata();
  const raw = Object.fromEntries(
    RAW_SERIES.map((id) => [id, loadCsv(join(process.cwd(), '..', 'data', 'raw', `${id}.csv`))])
  );
  const derived = Object.fromEntries(
    DERIVED_SERIES.map((id) => [id, loadCsv(join(process.cwd(), '..', 'data', 'derived', `${id}.csv`))])
  );
  return { series: { ...raw, ...derived }, metadata };
}
