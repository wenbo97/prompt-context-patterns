// Wire browser cards for patterns 156-206 to their static list-page anchors.
// Extracts the REAL kramdown <h2 id="..."> from the built pages (no slug guessing),
// maps them positionally (pages render in id order), and writes detail_en/detail_zh
// into patterns-harvest.json so build-patterns.mjs carries them into patterns.json.
//
// Requires a fresh `jekyll build` first. Run: node eval/tools/wire-harvest-detail.mjs
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const BASE = '/prompt-context-patterns';

function h2ids(rel) {
  const html = readFileSync(join(ROOT, rel), 'utf8');
  const out = [];
  const re = /<h2 id="([^"]+)"/g;
  let m;
  while ((m = re.exec(html))) out.push(m[1]);
  return out;
}

const en = h2ids('_site/catalog/patterns-156-206/index.html');
const zh = h2ids('_site/catalog/patterns-156-206-zh/index.html');
if (en.length !== 51 || zh.length !== 51) {
  console.error(`expected 51 anchors each, got en=${en.length} zh=${zh.length} — rebuild the site first`);
  process.exit(1);
}

const path = join(ROOT, 'eval/tools/patterns-harvest.json');
const harvest = JSON.parse(readFileSync(path, 'utf8')).sort((a, b) => a.id - b.id);

harvest.forEach((p, i) => {
  // safety: heading is "## <id>. <name>" so the anchor must start with "<id>-"
  if (!en[i].startsWith(p.id + '-') || !zh[i].startsWith(p.id + '-')) {
    throw new Error(`anchor/id misalignment at ${p.id}: en=${en[i]} zh=${zh[i]}`);
  }
  p.detail_en = `${BASE}/catalog/patterns-156-206#${en[i]}`;
  p.detail_zh = `${BASE}/catalog/patterns-156-206-zh#${zh[i]}`;
});

writeFileSync(path, JSON.stringify(harvest, null, 2) + '\n');
console.log(`wired ${harvest.length} detail links`);
console.log('first:', harvest[0].id, harvest[0].detail_en);
console.log('       ', harvest[0].detail_zh);
