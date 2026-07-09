// Fix broken related-pattern links in catalog/categories/*.md
//
// Rewrites bare `](#pattern-N)` anchors — which never resolve because the real
// kramdown heading id is the full slug (#pattern-N-<name>) and often lives on a
// DIFFERENT category page — into the correct full detail URL from patterns.json.
// EN files use detail_en; `*-zh.md` files use detail_zh.
//
// Run:  node eval/tools/fix-related-links.mjs

import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const CATS = join(ROOT, 'catalog', 'categories');
const data = JSON.parse(readFileSync(join(ROOT, 'assets', 'patterns.json'), 'utf8'));

const map = new Map();
for (const p of data) map.set(p.id, p);

let files = 0, fixed = 0, missing = new Set();

for (const name of readdirSync(CATS)) {
  if (!name.endsWith('.md')) continue;
  const zh = name.endsWith('-zh.md');
  const path = join(CATS, name);
  let src = readFileSync(path, 'utf8');
  let n = 0;
  const out = src.replace(/\]\(#pattern-(\d+)\)/g, function (m, idStr) {
    const p = map.get(Number(idStr));
    const url = p ? (zh ? p.detail_zh : p.detail_en) : null;
    if (!url) { missing.add(idStr); return m; }
    n++;
    return '](' + url + ')';
  });
  if (n > 0) { writeFileSync(path, out); files++; fixed += n; }
}

console.log('files changed:', files, ' links fixed:', fixed);
if (missing.size) console.log('unmapped pattern ids (left as-is):', [...missing].join(','));
