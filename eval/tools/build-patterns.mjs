// Build _data/patterns.json — the catalog browser's single data source.
//
// 1–155: parsed from catalog/catalog-index.md (+ -zh) table rows (name, category, detail link).
// 156+:  read from eval/tools/patterns-harvest.json (hand-authored 2026-07 harvest metadata).
//
// Run:  node eval/tools/build-patterns.mjs
// Node 18+ (ESM, no deps).

import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const EN = join(ROOT, 'catalog', 'catalog-index.md');
const ZH = join(ROOT, 'catalog', 'catalog-index-zh.md');
const HARVEST = join(ROOT, 'eval', 'tools', 'patterns-harvest.json');
const NAMES_ZH = join(ROOT, 'eval', 'tools', 'names-zh.json'); // Chinese names for 1-155 (source index only has English)
const OUT = join(ROOT, '_data', 'patterns.json');
const OUT_ASSET = join(ROOT, 'assets', 'patterns.json'); // served statically for the browser fetch

// A catalog row: | <id> | [<name>](<url>) | ... |   (url encodes category slug + detail anchor)
const ROW = /^\|\s*(\d+)\s*\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|/;
// category slug lives in the url:  .../categories/patterns-<slug>#pattern-...
const CAT = /categories\/patterns-([a-z0-9-]+?)(?:-zh)?#/;

// slug → canonical category key used for filtering
function catKey(slug) {
  // platform-extended folds into claude-code-platform for the filter facet
  if (slug === 'claude-code-platform-extended') return 'claude-code-platform';
  return slug;
}

function parseIndex(file) {
  const map = new Map(); // id -> { name, url, category }
  for (const line of readFileSync(file, 'utf8').split(/\r?\n/)) {
    const m = ROW.exec(line);
    if (!m) continue;
    const id = Number(m[1]);
    const name = m[2].trim();
    const url = m[3].trim();
    const cm = CAT.exec(url);
    if (!cm) continue; // skip rows whose link isn't a category detail (e.g. cross-ref tables)
    if (!map.has(id)) map.set(id, { name, url, category: catKey(cm[1]) });
  }
  return map;
}

const en = parseIndex(EN);
const zh = parseIndex(ZH);

const base = [];
for (const [id, e] of [...en.entries()].sort((a, b) => a[0] - b[0])) {
  const z = zh.get(id);
  base.push({
    id,
    name_en: e.name,
    name_zh: z ? z.name : e.name,
    category: e.category,
    source: id <= 99 ? '500plus' : id <= 120 ? 'open-source' : 'claude-code',
    detail_en: e.url,
    detail_zh: z ? z.url : e.url,
  });
}

const harvest = existsSync(HARVEST) ? JSON.parse(readFileSync(HARVEST, 'utf8')) : [];

// Override name_zh for 1-155 (the source catalog-index-zh keeps English names)
const namesZh = existsSync(NAMES_ZH) ? JSON.parse(readFileSync(NAMES_ZH, 'utf8')) : {};
for (const p of base) if (namesZh[p.id]) p.name_zh = namesZh[p.id];

const all = [...base, ...harvest].sort((a, b) => a.id - b.id);

writeFileSync(OUT, JSON.stringify(all, null, 2) + '\n');
writeFileSync(OUT_ASSET, JSON.stringify(all) + '\n');

const ids = all.map((p) => p.id);
const dupes = ids.filter((x, i) => ids.indexOf(x) !== i);
console.log(`base(1-155)=${base.length}  harvest=${harvest.length}  total=${all.length}`);
console.log(`id range ${Math.min(...ids)}..${Math.max(...ids)}  dupes=[${[...new Set(dupes)]}]`);
const byCat = {};
for (const p of all) byCat[p.category] = (byCat[p.category] || 0) + 1;
console.log('by category:', byCat);
