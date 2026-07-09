// One-off: normalize working-tree text files to CRLF (repo enforces `* text=auto eol=crlf`).
// Converts every changed/untracked text file except the local launcher, so `git add`
// won't trip safecrlf. Run: node eval/tools/to-crlf.mjs
import { execSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';

const exts = /\.(md|markdown|js|mjs|json|scss|css|html|yml|yaml|txt)$/i;
const skip = new Set(['blog-cc-dev.cmd']);
const list = execSync('git status --porcelain -uall', { encoding: 'utf8' });

let n = 0;
const skipped = [];
for (const line of list.split(/\r?\n/)) {
  if (!line.trim()) continue;
  const f = line.slice(3).trim();
  if (skip.has(f) || !exts.test(f)) continue;
  const buf = readFileSync(f);
  if (buf.includes(0)) { skipped.push(f + ' (binary)'); continue; }
  const crlf = buf.toString('utf8').replace(/\r\n/g, '\n').replace(/\n/g, '\r\n');
  writeFileSync(f, crlf);
  n++;
}
console.log('converted to CRLF:', n, 'files');
if (skipped.length) console.log('skipped:', skipped.join(', '));
