import fs from 'node:fs';
import path from 'node:path';
import { ROOT, readJson, writeText, validateCatalog, resolvePattern, sourceUrl, makeBrowserRecords, patternPath, CATEGORY_LABELS, CATEGORY_DESCRIPTIONS, CATEGORIES } from './lib.mjs';
import { readmeOutputs } from './readme.mjs';

const check = process.argv.includes('--check'); const changed = [];
function emit(file, content) {
  const normalized = content.replace(/\r?\n/g, '\r\n'); const full = path.join(ROOT, file);
  if (!fs.existsSync(full) || fs.readFileSync(full, 'utf8') !== normalized) {
    changed.push(file); if (!check) writeText(file, content);
  }
}
const json = (value) => JSON.stringify(value, null, 2) + '\n';
const fm = (props) => '---\n' + Object.entries(props).map(([k, v]) => `${k}: ${JSON.stringify(v)}`).join('\n') + '\n---\n\n';
const html = (value) => String(value).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
const link = (url, label) => `[${label}]({{ '${url}' | relative_url }})`;
const patterns = readJson('_data/patterns.json'); const errors = validateCatalog(patterns);
if (errors.length) throw new Error(errors.join('\n'));
const active = patterns.filter(p => p.status === 'active').sort((a, b) => a.id - b.id);
const stats = { active: active.length, traced: active.filter(p => p.trace_status === 'traceable').length,
  untraced: active.filter(p => p.trace_status === 'untraced').length,
  merged: patterns.filter(p => p.status === 'merged').length, removed: patterns.filter(p => p.status === 'removed').length,
  categories: Object.fromEntries(CATEGORIES.map(key => [key, active.filter(p => p.category === key).length])) };
emit('assets/patterns.json', JSON.stringify(makeBrowserRecords(patterns)) + '\n');
emit('_data/catalog_stats.json', json(stats));
for (const [file, content] of Object.entries(readmeOutputs(stats))) emit(file, content);
emit('_data/categories.json', json(CATEGORIES.map(key => ({ key, name_en: CATEGORY_LABELS[key][0], name_zh: CATEGORY_LABELS[key][1], count: stats.categories[key] }))));
const snapshot = readJson('docs/research/open-source-skills-top10.snapshot.json');
const inventory = readJson('docs/audit/source-inventory.json');
const sourceRecords = snapshot.selected.map(r => ({ repo: r.full_name, commit: r.commit_sha,
  url: r.html_url, stars: r.stargazers_count, stars_observed_at: snapshot.retrieved_at_utc,
  tracked_files: inventory.repositories.find(i => i.repo === r.full_name)?.files.length ?? 0,
  pattern_count: active.filter(p => p.sources.some(s => s.repo === r.full_name)).length }));
emit('_data/sources.json', json(sourceRecords));
const legacy = readJson('docs/audit/legacy-routes.json');
const headingTargets = new Map(readJson('docs/audit/legacy-heading-targets.json').routes.map(route => [route.url, route.targets]));
const kRecords = readJson('docs/audit/legacy-review.json').patterns.filter(p => p.legacy_id);
const idMap = fs.existsSync(path.join(ROOT, 'docs/audit/new-id-map.json')) ? readJson('docs/audit/new-id-map.json') : {};
for (const lang of ['en', 'zh']) {
  const zh = lang === 'zh';
  const indexUrl = zh ? '/catalog/catalog-index-zh/' : '/catalog/catalog-index/';
  const title = zh ? '方法总目录' : 'Complete pattern index';
  const oldIndexAnchors = legacy.routes.find(r => r.url === indexUrl)?.anchors ?? [];
  const indexAliases = oldIndexAnchors.filter(id => !['nav-trigger', 'main', 'quick-reference-table'].includes(id))
    .map(id => `<span id="${html(id)}"></span>`).join('\n');
  const table = ['| ID | ' + (zh ? '方法' : 'Pattern') + ' | ' + (zh ? '分类' : 'Theme') + ' | ' + (zh ? '来源状态' : 'Source status') + ' |', '| --- | --- | --- | --- |',
    ...active.map(p => `| ${p.id} | ${link(patternPath(p.id, lang), p[`name_${lang}`])}${zh ? `<br><span class="english-name" lang="en">${html(p.name_en)}</span>` : ''} | ${link(`/topics/${p.category}${zh ? '-zh' : ''}/`, CATEGORY_LABELS[p.category][zh ? 1 : 0])} | ${p.trace_status === 'traceable' ? (zh ? '可查看原文' : 'Located source instance') : (zh ? '来源未确认' : 'Source unconfirmed')} |`)];
  emit(`catalog/catalog-index${zh ? '-zh' : ''}.md`, fm({ layout: 'catalog-index', lang, title,
    description: zh ? `按稳定编号浏览 ${active.length} 个方法，查看双语详情、分类和原文状态。` : `Browse ${active.length} methods by stable ID, with bilingual details, themes and source status.`,
    permalink: indexUrl, alternate_url: zh ? '/catalog/catalog-index/' : '/catalog/catalog-index-zh/' }) +
    `# ${title}\n\n${active.length} ${zh ? '个方法，按编号排列。点击分类可查看同类方法。' : 'editorially reviewed methods.'}\n\n` +
    link(`/catalog/browse/${zh ? '?lang=zh' : ''}`, zh ? '搜索与筛选' : 'Search and filter') + '\n\n<a id="quick-reference-table"></a>\n\n' + table.join('\n') + '\n\n' + indexAliases + '\n');
  emit(`catalog/index${zh ? '-zh' : ''}.md`, fm({ layout: 'catalog', lang, title: zh ? '按分类查找方法' : 'Find a method by theme',
    description: zh ? '从提示词、上下文、任务流程、工具和评估等分类，查找适合当前问题的方法。' : 'Find methods for your task through themes including prompts, context, workflows, tools and evaluation.',
    permalink: zh ? '/catalog/index-zh/' : '/catalog/', alternate_url: zh ? '/catalog/' : '/catalog/index-zh/' }));
  for (const category of CATEGORIES) emit(`topics/${category}${zh ? '-zh' : ''}.md`, fm({ layout: 'topic', lang, category_key: category,
    title: CATEGORY_LABELS[category][zh ? 1 : 0], description: CATEGORY_DESCRIPTIONS[category][zh ? 1 : 0],
    permalink: `/topics/${category}${zh ? '-zh' : ''}/`, alternate_url: `/topics/${category}${zh ? '' : '-zh'}/` }));
  emit(`sources/index${zh ? '-zh' : ''}.md`, fm({ layout: 'sources', lang, title: zh ? '来源与固定版本' : 'Sources and frozen revisions',
    description: zh ? '查看十个冻结来源仓库、固定版本和对应方法；原文实例不等于最早出处。' : 'Inspect ten frozen source repositories, pinned revisions and related methods; occurrence is distinct from earliest provenance.',
    permalink: `/sources${zh ? '-zh' : ''}/`, alternate_url: `/sources${zh ? '' : '-zh'}/` }));
  emit(`blog${zh ? '-zh' : ''}.md`, fm({ layout: 'blog', lang, title: zh ? '文章与历史实验' : 'Articles and historical experiments',
    description: zh ? '阅读提示词、决策树和技能研究的历史文章，区分原始样例、已知结果与证据限制。' : 'Read historical articles on prompts, decision trees and skill research, with their original fixtures and evidence limits.',
    permalink: `/blog${zh ? '-zh' : ''}/`, alternate_url: `/blog${zh ? '' : '-zh'}/` }));
}
for (const p of patterns.filter(p => p.status !== 'active')) {
  for (const lang of ['en', 'zh']) emit(`_patterns/${p.id}.${lang}.md`, fm({ layout: 'retired-pattern', lang, pattern_id: p.id,
    permalink: patternPath(p.id, lang), alternate_url: patternPath(p.id, lang === 'en' ? 'zh' : 'en'), sitemap: false, robots: 'noindex,follow' }));
}
const current = new Set(['/catalog/', '/catalog/browse/', '/catalog/catalog-index/', '/catalog/catalog-index-zh/']);
const oldByPath = new Map();
for (const p of legacy.original_patterns) for (const lang of ['en', 'zh']) {
  const url = p[`detail_${lang}`].replace(/^\/prompt-context-patterns/, '');
  const [pathname, anchor] = url.split('#'); if (!oldByPath.has(pathname)) oldByPath.set(pathname, new Map());
  oldByPath.get(pathname).set(anchor, p.id);
}
for (const route of legacy.routes) {
  if (current.has(route.url)) continue;
  const lang = /-zh\/?$/.test(route.url) || /README-zh$/.test(route.url) ? 'zh' : 'en';
  let currentId = null;
  const guide = /anti-laziness|reference-skip-playbook/.test(route.url) ? 'reference-reading' : /good-vs-bad-template/.test(route.url) ? 'teaching-examples' : null;
  const fallback = guide ? `/guides/${guide}${lang === 'zh' ? '-zh' : ''}/` : (lang === 'zh' ? '/catalog/index-zh/' : '/catalog/');
  // Preserve both rendered legacy headings and IDs used by historical detail links.
  const detailAnchors = [...(oldByPath.get(route.url.replace(/\/$/, ''))?.keys() ?? [])];
  const entries = [...new Set([...route.anchors, ...detailAnchors])].filter(anchor => !['nav-trigger', 'main'].includes(anchor)).map(anchor => {
    const explicit = oldByPath.get(route.url.replace(/\/$/, ''))?.get(anchor);
    const numeric = /^pattern-(\d+)(?:-|$)/.exec(anchor);
    const k = /pattern-k([1-6])/.exec(anchor);
    if (explicit || numeric) currentId = explicit ?? Number(numeric[1]);
    if (k) { const old = kRecords.find(p => p.legacy_id === `K${k[1]}`); currentId = old?.merged_into ?? idMap[old?.candidate_key] ?? null; }
    const hierarchy = headingTargets.get(route.url);
    if (!explicit && !numeric && !k && hierarchy && Object.hasOwn(hierarchy, anchor)) {
      const owner = hierarchy[anchor];
      if (typeof owner === 'number' || owner === null) currentId = owner;
      else { const old = kRecords.find(p => p.legacy_id === owner); currentId = old?.merged_into ?? idMap[old?.candidate_key] ?? null; }
    }
    const target = currentId && patterns.some(p => p.id === currentId) ? resolvePattern(currentId, patterns) : null;
    const url = target ? patternPath(target.id, lang) : fallback;
    return `<li id="${html(anchor)}" data-target="{{ '${url}' | relative_url }}"><a href="{{ '${url}' | relative_url }}">${html(anchor)} → ${html(target?.[`name_${lang}`] ?? (lang === 'zh' ? '当前目录' : 'Current catalog'))}</a></li>`;
  });
  const file = 'catalog/compat/' + route.file.replace(/^catalog\//, '').replace(/\/index\.html$/, '').replace(/\.html$/, '') + '.md';
  emit(file, fm({ layout: 'default', lang, title: lang === 'zh' ? '内容迁移入口' : 'Content migration entry', permalink: route.url,
    sitemap: false, robots: 'noindex,follow', canonical_url: lang === 'zh' ? '/catalog/index-zh/' : '/catalog/' }) +
    `<div data-compat><h1>${lang === 'zh' ? '内容已迁移' : 'Content has moved'}</h1><p>${lang === 'zh' ? '原有地址和小节仍可定位；使用下列链接访问审核后的内容。' : 'Old addresses and sections still resolve. Follow a link to the reviewed content.'}</p><ul class="compat-list">\n${entries.join('\n')}\n</ul></div>\n<script src="{{ '/assets/compat.js' | relative_url }}"></script>\n`);
}
if (check && changed.length) { console.error('Generated files differ:\n' + changed.join('\n')); process.exitCode = 1; }
else console.log(`${check ? 'Checked' : 'Updated'} catalog outputs (${changed.length} changes; ${active.length} active patterns).`);
