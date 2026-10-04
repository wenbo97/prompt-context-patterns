import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';
import { ROOT, readJson } from './lib.mjs';

export const sourceRoot = () => path.resolve(process.env.SKILLS_ROOT || path.join(ROOT, '../open-skills'));
export function sourceLineCount(raw) {
  const text = raw.toString('utf8').replace(/\r\n/g, '\n');
  return text.length ? text.split('\n').length - (text.endsWith('\n') ? 1 : 0) : 0;
}
export function contentHash(raw, binary) {
  const value = binary ? raw : Buffer.from(raw.toString('utf8').replace(/\r\n/g, '\n'));
  return crypto.createHash('sha256').update(value).digest('hex');
}
function git(dir, args, input) {
  const result = spawnSync('git', ['-C', dir, ...args], { input, maxBuffer: 256 * 1024 * 1024 });
  if (result.status !== 0) throw new Error(`git ${args[0]} failed in ${dir}: ${result.stderr}`);
  return result.stdout;
}
export function verifyRepository(dir, repo) {
  if (git(dir, ['rev-parse', 'HEAD']).toString().trim() !== repo.commit) throw new Error(`${repo.repo}: frozen HEAD mismatch`);
  if (git(dir, ['status', '--porcelain']).length) throw new Error(`${repo.repo}: source worktree is dirty`);
  const tree = git(dir, ['ls-tree', '-r', '-z', repo.commit]).toString().split('\0').filter(Boolean);
  const expected = new Map(repo.files.map(f => [f.path, f]));
  if (tree.length !== expected.size) throw new Error(`${repo.repo}: tracked path count differs`);
  for (const row of tree) {
    const [meta, filename] = row.split('\t'); const [mode, type, blob] = meta.split(' ');
    const file = expected.get(filename);
    if (!file || file.mode !== mode || file.type !== type || file.blob !== blob) throw new Error(`${repo.repo}/${filename}: frozen tree differs`);
  }
  const files = repo.files.filter(f => f.type === 'blob');
  const oids = [...new Set(files.map(f => f.blob))];
  const data = git(dir, ['cat-file', '--batch'], oids.join('\n') + '\n');
  const blobs = new Map(); let offset = 0;
  for (const oid of oids) {
    const end = data.indexOf(10, offset); const header = data.subarray(offset, end).toString().split(' ');
    if (header[0] !== oid || header[1] !== 'blob') throw new Error(`${repo.repo}: invalid blob response`);
    const size = Number(header[2]); blobs.set(oid, data.subarray(end + 1, end + 1 + size)); offset = end + 2 + size;
  }
  for (const file of files) {
    const raw = blobs.get(file.blob);
    if (raw.length !== file.bytes || contentHash(raw, file.binary) !== file.hash) throw new Error(`${repo.repo}/${file.path}: frozen content differs`);
  }
  return { repo: repo.repo, commit: repo.commit, verified_files: repo.files.length };
}
function restoreRepository(dir, repo) {
  if (fs.existsSync(dir)) {
    // Existing evidence repositories are verified, never reset or overwritten.
    return verifyRepository(dir, repo);
  }
  fs.mkdirSync(dir, { recursive: true }); git(dir, ['init', '-q']);
  git(dir, ['remote', 'add', 'origin', `https://github.com/${repo.repo}.git`]);
  git(dir, ['fetch', '--quiet', '--depth=1', 'origin', repo.commit]);
  git(dir, ['-c', 'core.autocrlf=false', 'checkout', '--quiet', '--detach', 'FETCH_HEAD']);
  return verifyRepository(dir, repo);
}
if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  const inventory = readJson('docs/audit/source-inventory.json');
  if (inventory.repositories.length !== 10 || inventory.repositories.reduce((n, r) => n + r.files.length, 0) !== 9806) throw new Error('Frozen inventory must remain ten repositories / 9,806 files');
  for (const repo of inventory.repositories) {
    const dir = path.join(sourceRoot(), ...repo.repo.split('/'));
    console.log(JSON.stringify(process.argv.includes('--restore') ? restoreRepository(dir, repo) : verifyRepository(dir, repo)));
  }
}
