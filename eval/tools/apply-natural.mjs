// Extract the "版本 3 · 更自然流畅版" (Natural & fluent) section from each
// docs/polish/<slug>-polish.md and write it back over the corresponding _posts file.
//
// Run: node eval/tools/apply-natural.mjs

import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', '..');

const MAP = [
  ['decision-tree-pattern-polish.md',          '_posts/2026-04-19-decision-tree-pattern.md'],
  ['decision-tree-pattern-zh-polish.md',       '_posts/2026-04-19-decision-tree-pattern-zh.md'],
  ['prompt-engineering-patterns-polish.md',    '_posts/2026-04-19-prompt-engineering-patterns.md'],
  ['prompt-engineering-patterns-zh-polish.md', '_posts/2026-04-19-prompt-engineering-patterns-zh.md'],
  ['prompt-pattern-catalog-polish.md',         '_posts/2026-05-26-prompt-pattern-catalog.md'],
  ['prompt-pattern-catalog-zh-polish.md',      '_posts/2026-05-26-prompt-pattern-catalog-zh.md'],
  ['harvest-2026-07-polish.md',                '_posts/2026-07-08-harvest-2026-07.md'],
  ['harvest-2026-07-zh-polish.md',             '_posts/2026-07-08-harvest-2026-07-zh.md'],
];

const startRe = /^##\s*版本\s*3\b.*$/m;   // "## 版本 3 · 更自然流畅版 ..."
const endRe   = /^##\s*主要修改点.*$/m;    // "## 主要修改点 ..."

let ok = 0;
for (const [polish, post] of MAP) {
  const src = readFileSync(join(ROOT, 'docs', 'polish', polish), 'utf8');
  const s = startRe.exec(src);
  if (!s) { console.error('NO version-3 heading in', polish); continue; }
  const afterHeading = s.index + s[0].length;
  const e = endRe.exec(src.slice(afterHeading));
  const endIdx = e ? afterHeading + e.index : src.length;
  let body = src.slice(afterHeading, endIdx).trim() + '\n';
  if (!body.startsWith('---')) { console.error('extracted body does not start with front matter for', polish, '\n  head:', JSON.stringify(body.slice(0, 40))); continue; }
  writeFileSync(join(ROOT, post), body);
  ok++;
  console.log('wrote', post, '(' + body.length + ' bytes)');
}
console.log(`\napplied ${ok}/${MAP.length}`);
