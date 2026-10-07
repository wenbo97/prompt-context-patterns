import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { ROOT, readJson, writeText, patternPath, resolvePattern } from './lib.mjs';
import { readPage, validateSite } from './site-output.mjs';
import { validatePatternDates } from './content-metadata.mjs';

const site = path.join(ROOT, '_site');
const config = fs.readFileSync(path.join(ROOT, '_config.yml'), 'utf8');
const baseurl = /^baseurl:\s*(.*)$/m.exec(config)[1].trim();
const origin = /^url:\s*(.*)$/m.exec(config)[1].trim();
const files = [];
function walk(dir) {
  for (const item of fs.readdirSync(dir, { withFileTypes: true })) {
    const file = path.join(dir, item.name);
    if (item.isDirectory()) walk(file); else files.push(file);
  }
}
walk(site);
const pages = files.filter(file => file.endsWith('.html')).map(file => {
  const relative = path.relative(site, file).replace(/\\/g, '/');
  const html = fs.readFileSync(file, 'utf8');
  return { ...readPage(origin + baseurl + '/' + relative.replace(/index\.html$/, ''), html),
    file: relative, content_hash: crypto.createHash('sha256').update(html).digest('hex') };
});
const sitemap = fs.readFileSync(path.join(site, 'sitemap.xml'), 'utf8');
const errors = validateSite(pages, sitemap, origin, baseurl);
const catalog = readJson('_data/patterns.json');
errors.push(...validatePatternDates(catalog, (id, lang) => fs.readFileSync(path.join(ROOT, '_patterns', `${id}.${lang}.md`), 'utf8'), sitemap, origin + baseurl));
const byUrl = new Map(pages.map(page => [page.url, page]));
for (const pattern of catalog.filter(row => row.status === 'active')) for (const lang of ['en', 'zh']) {
  const url = origin + baseurl + patternPath(pattern.id, lang);
  const page = byUrl.get(url);
  if (!page || page.noindex || page.heading !== pattern[`name_${lang}`] || page.description !== pattern[`summary_${lang}`])
    errors.push(`Active pattern metadata/route mismatch: P${pattern.id}/${lang}`);
  if (page && (!page.alternates.some(row => row.href === url && row.hreflang === (lang === 'zh' ? 'zh-CN' : 'en')) ||
    !page.alternates.some(row => row.href === origin + baseurl + patternPath(pattern.id, lang === 'en' ? 'zh' : 'en'))))
    errors.push(`Active pattern language pair absent: P${pattern.id}/${lang}`);
}
const legacy = readJson('docs/audit/legacy-routes.json');
let headingMappingsChecked = 0;
for (const route of readJson('docs/audit/legacy-heading-targets.json').routes) {
  const page = byUrl.get(origin + baseurl + route.url);
  if (!page || !Object.keys(page.migration_targets).length) continue;
  const lang = /-zh\/?$/.test(route.url) || /README-zh$/.test(route.url) ? 'zh' : 'en';
  for (const [anchor, owner] of Object.entries(route.targets)) {
    const href = page.migration_targets[anchor];
    if (!href) continue;
    headingMappingsChecked++;
    if (typeof owner === 'number') {
      const expected = origin + baseurl + patternPath(resolvePattern(owner, catalog).id, lang);
      if (new URL(href, page.url).href !== expected) errors.push(`Legacy subheading has wrong owner: ${page.url}#${anchor}`);
    } else if (owner === null && /\/catalog\/patterns\//.test(href)) errors.push(`Legacy global heading points to unrelated pattern: ${page.url}#${anchor}`);
  }
}
const migrations = legacy.original_patterns.flatMap(old => ['en', 'zh'].map(lang => {
  const oldUrl = new URL(old[`detail_${lang}`], origin);
  const target = resolvePattern(old.id, catalog);
  const targetUrl = origin + baseurl + patternPath(target.id, lang);
  const oldPageUrl = oldUrl.origin + oldUrl.pathname;
  const page = byUrl.get(oldPageUrl) ?? byUrl.get(oldPageUrl + '/');
  const anchor = decodeURIComponent(oldUrl.hash.slice(1));
  if (!page || !page.ids.includes(anchor)) errors.push(`Legacy pattern anchor missing: ${oldUrl.href}`);
  if (page && !page.anchors.some(link => new URL(link.href, page.url).href === targetUrl))
    errors.push(`Legacy pattern target missing: ${oldUrl.href} -> ${targetUrl}`);
  return { id: old.id, lang, old_url: oldUrl.href, target_url: targetUrl };
}));
const robots = fs.readFileSync(path.join(site, 'robots.txt'), 'utf8');
if (!robots.includes(`Sitemap: ${origin}${baseurl}/sitemap.xml`)) errors.push('Robots sitemap reference differs');
if (/Disallow:\s*\//.test(robots)) errors.push('Robots blocks site content');
for (const file of files) {
  const relative = path.relative(site, file).replace(/\\/g, '/');
  if (/^(?:docs\/|tests\/|scripts\/|\.tools\/)|(?:^|\/)premium-audit\.json$/.test(relative))
    errors.push(`Non-site artifact published: ${relative}`);
}
const assets = files.filter(file => /\.(?:css|js|json)$/.test(file)).sort();
const assetHash = crypto.createHash('sha256');
for (const file of assets) assetHash.update(path.relative(site, file)).update(fs.readFileSync(file));
const report = { generated_at: new Date().toISOString(), html_pages: pages.length,
  indexable_pages: pages.filter(page => !page.noindex).length, noindex_pages: pages.filter(page => page.noindex).length,
  rendered_anchor_instances: pages.reduce((sum, page) => sum + page.anchors.length, 0),
  legacy_pattern_mappings: migrations.length, legacy_pages: legacy.routes.length,
  legacy_post_routes: legacy.post_routes.length, errors };
report.robots_check = { scope: 'Built project artifact text only; not live host-root enforcement',
  host_root_url: `${origin}/robots.txt`, published_artifact_url: `${origin}${baseurl}/robots.txt`,
  host_root_verified: false, notes: baseurl ? ['Subdirectory robots.txt is not the host robots file; verify the host root after release or submit the sitemap through existing properties.'] : [] };
report.legacy_heading_mappings_checked = headingMappingsChecked;
writeText('docs/audit/site-output-2026-10-06.json', JSON.stringify(report, null, 2) + '\n');
writeText('.tools/polish-2026-10-06/site-manifest.json', JSON.stringify({ ...report, origin, baseurl,
  shared_asset_hash: assetHash.digest('hex'), pages, migrations }, null, 2) + '\n');
console.log(JSON.stringify({ ...report, errors: errors.slice(0, 20), error_count: errors.length }));
if (errors.length) process.exitCode = 1;
