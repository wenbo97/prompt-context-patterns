import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { readJson, writeText } from './lib.mjs';

const sourcesRoot = process.env.SKILLS_ROOT || 'D:/Projects/open-skills';
const selected = readJson('docs/research/open-source-skills-top10.snapshot.json').selected;
function git(dir, args, binary = false) {
  const result = spawnSync('git', ['-C', dir, ...args], { encoding: binary ? undefined : 'utf8', maxBuffer: 256 * 1024 * 1024 });
  if (result.status !== 0) throw new Error(String(result.stderr));
  return result.stdout;
}
const all = [];
for (const repo of selected) {
  const dir = path.join(sourcesRoot, ...repo.full_name.split('/'));
  const commit = git(dir, ['rev-parse', 'HEAD']).trim();
  if (commit !== repo.commit_sha) throw new Error(`${repo.full_name}: source HEAD changed since collection`);
  const tree = git(dir, ['ls-tree', '-r', '-z', commit]).split('\0').filter(Boolean).map((line) => {
    const [meta, filename] = line.split('\t'); const [mode, type, blob] = meta.split(' ');
    return { path: filename, mode, type, blob };
  });
  const requests = [...new Set(tree.filter((f) => f.type === 'blob').map((f) => f.blob))];
  const proc = spawnSync('git', ['-C', dir, 'cat-file', '--batch'], {
    input: requests.join('\n') + '\n', maxBuffer: 256 * 1024 * 1024,
  });
  if (proc.status !== 0) throw new Error(String(proc.stderr));
  const blobs = new Map(); let offset = 0;
  for (const hash of requests) {
    const end = proc.stdout.indexOf(10, offset); const header = proc.stdout.subarray(offset, end).toString().split(' ');
    const size = Number(header[2]); const content = proc.stdout.subarray(end + 1, end + 1 + size);
    const binary = content.includes(0);
    const normalized = binary ? content : Buffer.from(content.toString('utf8').replace(/\r\n/g, '\n'));
    blobs.set(hash, { bytes: size, hash: crypto.createHash('sha256').update(normalized).digest('hex'), binary,
      lines: binary ? null : normalized.toString().split('\n').length });
    offset = end + 1 + size + 1;
  }
  const files = tree.map((f) => {
    const value = blobs.get(f.blob) ?? { hash: f.blob, binary: true, lines: null, bytes: 0 };
    const ext = path.extname(f.path).toLowerCase();
    const classification = f.mode === '120000' ? 'symlink' : /^skill\.md$/i.test(path.basename(f.path)) ? 'skill' :
      /\.(md|mdx|txt)$/i.test(ext) ? 'prose' : ['.js', '.mjs', '.cjs', '.ts', '.tsx', '.jsx', '.py', '.sh', '.rb', '.yml', '.yaml', '.json'].includes(ext) ? 'supporting-code-or-data' : 'other';
    return { ...f, ...value, classification, review_status: 'pending' };
  });
  all.push({ repo: repo.full_name, commit, files });
  console.log(`${repo.full_name}: ${files.length} tracked paths, ${files.filter((f) => f.classification === 'skill').length} skills`);
}
writeText('docs/audit/source-inventory.json', JSON.stringify({ frozen_at: '2026-10-03', repositories: all }, null, 2) + '\n');
console.log('Inventory records identity and scope only; semantic review comes from harvest reports.');
