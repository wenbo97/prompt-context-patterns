import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { ROOT } from '../catalog/lib.mjs';
import { readSiteConfig } from '../catalog/site-config.mjs';

process.env.JEKYLL_CONFIG = '_config.yml,_config.cloudflare.yml';
const { siteDirectory } = readSiteConfig();
function run(file, args = []) {
  const result = spawnSync(process.execPath, [path.join(ROOT, file), ...args], { cwd: ROOT, env: process.env, stdio: 'inherit' });
  if (result.error) throw result.error;
  if (result.status !== 0) process.exit(result.status || 1);
}

if (process.argv[2] === 'check') {
  run('scripts/catalog/check-links.mjs');
  run('scripts/catalog/check-site.mjs');
  for (const file of ['_headers', '_redirects']) {
    if (!fs.existsSync(path.join(siteDirectory, file))) throw new Error(`Missing Cloudflare deployment policy: ${file}`);
  }
  const inspect = directory => {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      const file = path.join(directory, entry.name);
      if (entry.isDirectory()) inspect(file);
      else if (entry.name.endsWith('.html') && /<link\b[^>]*href="https:\/\/fonts\.(?:googleapis|gstatic)\.com/i.test(fs.readFileSync(file, 'utf8')))
        throw new Error(`Published page still depends on Google Fonts: ${path.relative(siteDirectory, file)}`);
    }
  };
  inspect(siteDirectory);
  console.log('Cloudflare policies are included; published HTML has no Google Fonts requests.');
} else if (process.argv[2] === 'e2e') {
  run('node_modules/@playwright/test/cli.js', ['test', ...process.argv.slice(3)]);
} else {
  throw new Error('Use cloudflare.mjs check or cloudflare.mjs e2e');
}
