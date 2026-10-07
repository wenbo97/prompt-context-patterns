import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { readSiteConfig, legacySitePath } from '../scripts/catalog/site-config.mjs';

test('deployment overrides support an empty root prefix without replacing legacy defaults', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'pattern-site-config-'));
  try {
    fs.writeFileSync(path.join(root, '_config.yml'), 'url: https://wenbo97.github.io\nbaseurl: /prompt-context-patterns\ntheme: minima\n');
    fs.writeFileSync(path.join(root, '_config.cloudflare.yml'), 'url: https://patternnotes.dev\nbaseurl: ""\ndestination: .tools/cloudflare-site\naudit_report_directory: .tools/cloudflare-audit\n');
    const legacy = readSiteConfig({ root, configPaths: '_config.yml' });
    const cloudflare = readSiteConfig({ root, configPaths: '_config.yml,_config.cloudflare.yml' });
    assert.equal(legacy.origin + legacy.baseurl, 'https://wenbo97.github.io/prompt-context-patterns');
    assert.equal(cloudflare.origin + cloudflare.baseurl, 'https://patternnotes.dev');
    assert.equal(cloudflare.siteDirectory, path.join(root, '.tools/cloudflare-site'));
    assert.equal(cloudflare.reportDirectory, '.tools/cloudflare-audit');
    assert.equal(readSiteConfig({ root, configPaths: '_config.yml' }).baseurl, legacy.baseurl);
  } finally {
    assert.ok(path.resolve(root).startsWith(path.join(path.resolve(os.tmpdir()), 'pattern-site-config-')));
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('an unquoted empty YAML prefix does not consume the following setting', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'pattern-site-config-'));
  try {
    fs.writeFileSync(path.join(root, '_config.yml'), 'url: https://patternnotes.dev\nbaseurl:\ntheme: minima\n');
    assert.equal(readSiteConfig({ root, configPaths: '_config.yml' }).baseurl, '');
  } finally {
    assert.ok(path.resolve(root).startsWith(path.join(path.resolve(os.tmpdir()), 'pattern-site-config-')));
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('frozen old URLs resolve to the same route on a root-domain deployment', () => {
  const old = new URL('https://wenbo97.github.io/prompt-context-patterns/catalog/categories/patterns-execution-control/#pattern-8');
  const pathname = legacySitePath(old.pathname);
  assert.equal(pathname, '/catalog/categories/patterns-execution-control/');
  assert.equal(new URL(pathname + old.hash, 'https://patternnotes.dev').href, 'https://patternnotes.dev/catalog/categories/patterns-execution-control/#pattern-8');
  assert.equal(legacySitePath('/prompt-context-patterns/'), '/');
  assert.equal(legacySitePath('/prompt-context-patterns-other/page/'), '/prompt-context-patterns-other/page/');
});
