// Fix cross-language catalog links so each doc links within its own language.
// A -zh doc's link to an EN catalog page gets `-zh` inserted before the anchor;
// an EN doc's link to a -zh page gets `-zh` removed. Skips the bilingual landing
// (catalog/index.md). Verifies the retargeted page exists before rewriting — no
// dead links. Run: node eval/tools/fix-lang-links.mjs
import { readFileSync, writeFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, relative } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const BASE = '/prompt-context-patterns';

function walk(dir, out = []) {
  for (const n of readdirSync(dir)) {
    const p = join(dir, n);
    statSync(p).isDirectory() ? walk(p, out) : n.endsWith('.md') && out.push(p);
  }
  return out;
}
const isNeutral = (p) => /\/catalog\/?$/.test(p) || /\/catalog\/(browse|index)\/?$/.test(p);
const tLang = (p) => (/-zh$/.test(p) ? 'zh' : 'en');

// URL path (root-relative, no baseurl) -> repo file, to confirm the target exists
function pageExists(path) {
  const rel = path.startsWith(BASE) ? path.slice(BASE.length) : path;
  return existsSync(join(ROOT, rel.replace(/^\//, '') + '.md'));
}

let fixed = 0, skippedDead = [];
for (const f of walk(join(ROOT, 'catalog')).concat(walk(join(ROOT, '_posts')))) {
  const rel = relative(ROOT, f).replace(/\\/g, '/');
  if (rel === 'catalog/index.md') continue;
  const fileLang = /-zh\.md$/.test(f) ? 'zh' : 'en';
  let n = 0;
  const out = readFileSync(f, 'utf8').replace(/\]\(([^)]+)\)/g, (m, url) => {
    if (!url.includes('/catalog/')) return m;
    const [path, anchor] = url.split('#');
    const clean = path.replace(/\/$/, '');
    if (isNeutral(clean)) return m;
    // a link to this file's own counterpart (X <-> X-zh) is a deliberate language switcher — leave it
    const fileBase = rel.split('/').pop().replace(/\.md$/, '');
    const counterpart = /-zh$/.test(fileBase) ? fileBase.replace(/-zh$/, '') : fileBase + '-zh';
    if (clean.split('/').pop() === counterpart) return m;
    if (tLang(clean) === fileLang) return m;
    const newPath = fileLang === 'zh' ? clean + '-zh' : clean.replace(/-zh$/, '');
    if (!pageExists(newPath)) { skippedDead.push(`${rel}: ${newPath} (missing)`); return m; }
    n++;
    return '](' + newPath + (anchor ? '#' + anchor : '') + ')';
  });
  if (n) { writeFileSync(f, out); fixed += n; console.log(`${rel}: ${n} fixed`); }
}
console.log(`\ntotal fixed: ${fixed}`);
if (skippedDead.length) console.log('skipped (target page missing):\n  ' + skippedDead.join('\n  '));
