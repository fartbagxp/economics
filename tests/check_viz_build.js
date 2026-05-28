#!/usr/bin/env node
/**
 * Post-build sanity check: verifies that viz/build/__data.json contains the
 * latest dates from the key viz CSV series.  Run from project root after
 * `pnpm build` inside viz/.
 */

'use strict';

const { readFileSync } = require('fs');
const { join } = require('path');

const ROOT = join(__dirname, '..');

function latestCsvDate(relPath) {
  const lines = readFileSync(join(ROOT, relPath), 'utf-8').trim().split('\n');
  return lines[lines.length - 1].split(',')[0].slice(0, 10);
}

// Key viz raw series — most-recently-updated first so failures are obvious
const CHECKS = [
  { id: 'icsa',     csv: 'data/raw/icsa.csv' },
  { id: 'unrate',   csv: 'data/raw/unrate.csv' },
  { id: 'gdp',      csv: 'data/raw/gdp.csv' },
  { id: 'umcsent',  csv: 'data/raw/umcsent.csv' },
  { id: 'cpiaucsl', csv: 'data/raw/cpiaucsl.csv' },
];

let buildData;
try {
  buildData = JSON.parse(readFileSync(join(ROOT, 'viz/build/__data.json'), 'utf-8'));
} catch (e) {
  console.error('❌ Could not read viz/build/__data.json — was the build run?');
  process.exit(1);
}

const payload = buildData?.nodes?.[1]?.data;
if (!Array.isArray(payload)) {
  console.error('❌ Unexpected __data.json structure — SvelteKit format may have changed');
  process.exit(1);
}

const builtDates = new Set(
  payload.filter((x) => typeof x === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(x))
);

let failed = false;
for (const { id, csv } of CHECKS) {
  const latest = latestCsvDate(csv);
  if (builtDates.has(latest)) {
    console.log(`✅ ${id}: ${latest} present in viz build`);
  } else {
    console.error(`❌ ${id}: latest date ${latest} not found in viz/build/__data.json`);
    failed = true;
  }
}

if (failed) {
  console.error('\nThe viz build does not reflect the latest CSV data.');
  process.exit(1);
}
