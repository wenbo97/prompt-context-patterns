// Full scan for cross-language links: an EN doc must not link to a -zh catalog
// page, and a -zh doc must not link to an EN catalog page. Deterministic, 100%
// coverage. Reports every mismatch. Run: node eval/tools/scan-lang-links.mjs
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, relative } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', '..');

function walk(dir, out = []) {
  for (const n of readdirSync(dir)) {
    const p = join(dir, n);
    const s = statSync(p);
    if (s.isDirectory()) walk(p, out);
    else if (n.endsWith('.md')) out.push(p);
  }
  return out;
}

const files = [...walk(join(ROOT, 'catalog')), ...walk(join(ROOT, '_posts'))];
const LINK = /\]\(([^)]+)\)/g;

// language-neutral catalog targets (bilingual pages) — never a mismatch
function isNeutral(path) {
  return /\/catalog\/?$/.test(path) || /\/catalog\/(browse|index)\/?$/.test(path);
}
function targetLang(path) {
  return /-zh$/.test(path) ? 'zh' : 'en';
}

let total = 0;
const byFile = {};
for (const f of files) {
  const rel0 = relative(ROOT, f).replace(/\\/g, '/');
  if (rel0 === 'catalog/index.md') continue; // bilingual landing page — links to BOTH langs by design
  const fileLang = /-zh\.md$/.test(f) ? 'zh' : 'en';
  const src = readFileSync(f, 'utf8');
  let m;
  while ((m = LINK.exec(src))) {
    let url = m[1].trim();
    if (!url.includes('/catalog/')) continue;         // only internal catalog links
    const path = url.split('#')[0].replace(/\/$/, ''); // strip anchor + trailing slash
    if (isNeutral(path)) continue;
    // a link to this page's own counterpart (X <-> X-zh) is a deliberate language switcher — allowed
    const fileBase = f.split(/[\\/]/).pop().replace(/\.md$/, '');
    const counterpart = /-zh$/.test(fileBase) ? fileBase.replace(/-zh$/, '') : fileBase + '-zh';
    if (path.split('/').pop() === counterpart) continue;
    const tl = targetLang(path);
    if (tl !== fileLang) {
      total++;
      const rel = relative(ROOT, f).replace(/\\/g, '/');
      (byFile[rel] ||= []).push(`${fileLang}→${tl}: ${url}`);
    }
  }
}

console.log('cross-language link mismatches:', total);
for (const [file, hits] of Object.entries(byFile)) {
  console.log(`\n${file}  (${hits.length})`);
  for (const h of hits.slice(0, 6)) console.log('  ' + h);
  if (hits.length > 6) console.log(`  … +${hits.length - 6} more`);
}
