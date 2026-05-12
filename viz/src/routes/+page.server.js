import { readFileSync } from 'fs';
import { join } from 'path';

const SERIES = ['unrate', 'cpiaucsl', 'gdp', 'umcsent', 'civpart', 'u6rate', 'icsa'];

function loadSeries(id) {
  const csvPath = join(process.cwd(), '..', 'data', 'raw', `${id}.csv`);
  const raw = readFileSync(csvPath, 'utf-8');
  const lines = raw.trim().split('\n').slice(1);
  return lines
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
  const series = Object.fromEntries(SERIES.map((id) => [id, loadSeries(id)]));
  return { series, metadata };
}
