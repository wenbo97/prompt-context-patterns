import fs from 'node:fs';
import path from 'node:path';
import { readJson, writeText } from './lib.mjs';
import { readSiteConfig } from './site-config.mjs';

const { origin, baseurl, siteDirectory: site, reportDirectory } = readSiteConfig();
const pages = [];
function walk(dir) { for (const item of fs.readdirSync(dir, { withFileTypes: true })) {
  const file = path.join(dir, item.name); if (item.isDirectory()) walk(file); else if (item.name.endsWith('.html')) pages.push(file);
} }
if (!fs.existsSync(site)) throw new Error('Build Jekyll before checking rendered links');
walk(site);
const ids = new Map(); const errors = [];
const decode = s => s.replace(/&amp;/g, '&').replace(/&#39;/g, "'").replace(/&quot;/g, '"');
for (const file of pages) {
  const html = fs.readFileSync(file, 'utf8'); const all = [...html.matchAll(/\bid="([^"]+)"/g)].map(m => decode(m[1]));
  const duplicates = all.filter((id, i) => all.indexOf(id) !== i);
  if (duplicates.length) errors.push(`${path.relative(site, file)}: duplicate IDs ${[...new Set(duplicates)].join(', ')}`);
  ids.set(file, new Set(all));
}
function targetFile(url) {
  let pathname = decodeURIComponent(url.pathname);
  if (baseurl && (pathname === baseurl || pathname.startsWith(baseurl + '/'))) pathname = pathname.slice(baseurl.length);
  const target = path.join(site, pathname.replace(/^\//, ''));
  const candidates = [target, path.join(target, 'index.html'), target + '.html'];
  return candidates.find(f => fs.existsSync(f) && fs.statSync(f).isFile());
}
let checked = 0;
for (const file of pages) {
  const relative = path.relative(site, file).replace(/\\/g, '/');
  const pagePath = '/' + relative.replace(/index\.html$/, '');
  const current = new URL(origin + baseurl + pagePath);
  const html = fs.readFileSync(file, 'utf8');
  for (const match of html.matchAll(/\b(?:href|src)="([^"]+)"/g)) {
    const href = decode(match[1]); if (!href || /^(?:mailto:|tel:|data:|javascript:)/i.test(href)) continue;
    let url; try { url = new URL(href, current); } catch { errors.push(`${relative}: invalid URL ${href}`); continue; }
    if (url.origin !== origin) continue;
    const target = targetFile(url); checked++;
    if (!target) { errors.push(`${relative}: missing ${url.pathname}`); continue; }
    if (url.hash && target.endsWith('.html') && !ids.get(target)?.has(decodeURIComponent(url.hash.slice(1)))) errors.push(`${relative}: missing fragment ${url.pathname}${url.hash}`);
  }
}
const legacy = readJson('docs/audit/legacy-routes.json');
for (const route of [...legacy.routes, ...(legacy.post_routes ?? [])]) {
  const url = new URL(origin + baseurl + route.url); const target = targetFile(url);
  if (!target) errors.push(`Legacy route missing: ${route.url}`);
  else for (const id of route.anchors) if (!ids.get(target)?.has(id)) errors.push(`Legacy anchor missing: ${route.url}#${id}`);
}
const report = { generated_at: new Date().toISOString(), html_pages: pages.length, rendered_links_checked: checked, errors };
writeText(path.join(reportDirectory, 'rendered-links.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify({ pages: pages.length, checked, errors: errors.length }));
if (errors.length) { console.error(errors.slice(0, 40).join('\n')); process.exitCode = 1; }
