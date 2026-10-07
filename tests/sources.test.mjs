import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { contentHash, sourceLineCount, verifyRepository } from '../scripts/catalog/sources.mjs';

test('frozen evidence normalizes text line endings and preserves binary bytes', () => {
  assert.equal(contentHash(Buffer.from('a\r\nb\r\n'), false), contentHash(Buffer.from('a\nb\n'), false));
  assert.notEqual(contentHash(Buffer.from('a\r\nb\0'), true), contentHash(Buffer.from('a\nb\0'), true));
});
test('source locators cannot point beyond the real last line of a newline-terminated blob', () => {
  assert.equal(sourceLineCount(Buffer.from('only line\n')), 1);
  assert.equal(sourceLineCount(Buffer.from('first\r\nsecond\r\n')), 2);
  assert.equal(sourceLineCount(Buffer.from('first\n\n')), 2);
  assert.equal(sourceLineCount(Buffer.from('unterminated')), 1);
  assert.equal(sourceLineCount(Buffer.alloc(0)), 0);
});
test('source verification rejects changed content, revisions and dirty evidence worktrees', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'pattern-source-'));
  const git = args => execFileSync('git', ['-C', dir, ...args], { encoding: 'utf8' }).trim();
  try {
    git(['init', '-q']); fs.writeFileSync(path.join(dir, 'fixture.md'), 'fixed source\n');
    git(['-c', 'core.autocrlf=false', 'add', 'fixture.md']);
    git(['-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'Fixture']);
    const commit = git(['rev-parse', 'HEAD']); const blob = git(['rev-parse', 'HEAD:fixture.md']);
    const file = { path: 'fixture.md', mode: '100644', type: 'blob', blob, binary: false, bytes: 13, hash: contentHash(Buffer.from('fixed source\n'), false) };
    const repo = { repo: 'test/fixture', commit, files: [file] };
    assert.equal(verifyRepository(dir, repo).verified_files, 1);
    assert.throws(() => verifyRepository(dir, { ...repo, commit: '0'.repeat(40) }), /HEAD mismatch/);
    assert.throws(() => verifyRepository(dir, { ...repo, files: [{ ...file, hash: '0'.repeat(64) }] }), /content differs/);
    fs.appendFileSync(path.join(dir, 'fixture.md'), 'local change\n');
    assert.throws(() => verifyRepository(dir, repo), /dirty/);
  } finally { fs.rmSync(dir, { recursive: true, force: true }); }
});
