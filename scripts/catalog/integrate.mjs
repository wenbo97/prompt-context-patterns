// One-time editorial migration. Regular generation never overwrites authored bodies.
import fs from 'node:fs';
import path from 'node:path';
import { ROOT, readJson, writeText, sourceUrl, validateCatalog, resolvePattern, patternPath, protectLiquid } from './lib.mjs';
import { resolveDecision } from './decisions.mjs';

const legacyOnly = process.argv.includes('--legacy-only');
const review = readJson('docs/audit/legacy-review.json');
const fields = ['description', 'scenario', 'mechanism', 'bad', 'good', 'why', 'expected', 'boundaries'];
const normalizeSource = (s) => {
  const value = { ...s, start_line: s.start_line ?? s.line_start, end_line: s.end_line ?? s.line_end,
    role: s.role ?? 'observed-example', license: s.license ?? 'no-explicit-license' };
  if (value.repo) value.url = sourceUrl(value);
  return value;
};
const patterns = review.patterns.filter(p => Number.isInteger(p.id)).map(p => ({
  id: p.id, name_en: p.name_en, name_zh: p.name_zh, status: p.status, category: p.category,
  summary_en: p.content?.en?.description ?? '', summary_zh: p.content?.zh?.description ?? '',
  tags: p.tags ?? [], trace_status: p.sources?.length ? 'traceable' : 'untraced', origin_status: p.origin_status ?? 'unknown',
  sources: (p.sources ?? []).map(normalizeSource), related_ids: p.related_ids ?? [],
  reason_en: p.reason_en, reason_zh: p.reason_zh, ...(p.merged_into ? { merged_into: p.merged_into } : {}),
  review: { scores: p.scores, decision: p.status, reason_en: p.reason_en, reason_zh: p.reason_zh, reviewed_at: p.reviewed_at ?? '2026-10-03' },
  example_origin: 'teaching-construction', validation_status: 'editorial-review-only',
}));
const content = new Map(review.patterns.filter(p => p.status === 'active' && Number.isInteger(p.id)).map(p => [p.id, p.content]));
if (!legacyOnly) {
  const decisions = readJson('docs/audit/integration-decisions.json');
  const idMap = fs.existsSync(path.join(ROOT, 'docs/audit/new-id-map.json')) ? readJson('docs/audit/new-id-map.json') : {};
  let nextId = Math.max(206, ...Object.values(idMap)) + 1;
  const reports = ['harvest-composio.json', 'harvest-ecc.json', 'harvest-ecc-variants.json', 'harvest-core.json', 'harvest-gstack.json'];
  const candidates = reports.flatMap(file => readJson(`docs/audit/${file}`).candidates);
  if (new Set(candidates.map(c => c.key)).size !== candidates.length) throw new Error('Candidate keys must be unique across reports');
  for (const c of candidates) {
    const decision = decisions[c.key];
    if (!decision) throw new Error(`No integration decision for ${c.key}`);
    if (!decision.reason_en?.trim() || !decision.reason_zh?.trim()) throw new Error(`Bilingual integration rationale missing: ${c.key}`);
    if (!['active', 'merged', 'rejected'].includes(decision.status)) throw new Error(`Invalid integration status: ${c.key}`);
    if (decision.status !== 'active') continue;
    const sources = c.sources.map(normalizeSource);
    if (!idMap[c.key]) idMap[c.key] = nextId++;
    const id = idMap[c.key]; const name = c.name ?? {};
    patterns.push({ id, key: c.key, status: 'active', name_en: c.name_en ?? name.en, name_zh: c.name_zh ?? name.zh,
      summary_en: c.content.en.description, summary_zh: c.content.zh.description, category: c.category, tags: c.tags,
      trace_status: 'traceable', origin_status: 'unknown', sources, related_ids: decision.related_ids ?? [],
      review: { scores: c.scores, decision: 'active', reason_en: decision.reason_en, reason_zh: decision.reason_zh, reviewed_at: decision.reviewed_at },
      example_origin: 'teaching-construction', validation_status: 'editorial-review-only' });
    content.set(id, c.content);
  }
  for (const c of candidates) {
    if (decisions[c.key].status !== 'merged') continue;
    const p = resolveDecision(c.key, decisions, idMap, patterns);
    p.sources = [...p.sources, ...c.sources.map(normalizeSource)].filter((s, i, all) => all.findIndex(t => t.url === s.url) === i);
    p.trace_status = p.sources.length ? 'traceable' : 'untraced';
    idMap[c.key] = p.id;
  }
  writeText('docs/audit/new-id-map.json', JSON.stringify(idMap, null, 2) + '\n');
}
for (const p of patterns) {
  if (p.status === 'merged') p.merged_into = resolvePattern(p.id, patterns).id;
  p.related_ids = [...new Set(p.related_ids.filter(id => patterns.some(x => x.id === id)).map(id => resolvePattern(id, patterns)).filter(x => x.status === 'active' && x.id !== p.id).map(x => x.id))];
  if (p.status !== 'active') continue;
  p.tags = [...new Set(p.tags.filter(tag => tag !== 'source-unconfirmed' && tag !== 'source-instance-located')),
    p.trace_status === 'untraced' ? 'source-unconfirmed' : 'source-instance-located'];
  for (const lang of ['en', 'zh']) for (const field of fields) {
    if (!content.get(p.id)?.[lang]?.[field]?.trim()) throw new Error(`Incomplete authored content: ${p.id}/${lang}/${field}`);
  }
}
const errors = validateCatalog(patterns); if (errors.length) throw new Error(errors.join('\n'));
writeText('_data/patterns.json', JSON.stringify(patterns.sort((a, b) => a.id - b.id), null, 2) + '\n');
const titles = {
  en: ['Use case', 'Mechanism', 'Bad example', 'Good example', 'Why the change matters', 'Observable expectation', 'Limits'],
  zh: ['使用场景', '机制', 'Bad example', 'Good example', '差异说明', '可检查的结果', '适用边界'],
};
for (const p of patterns.filter(p => p.status === 'active')) for (const lang of ['en', 'zh']) {
  const c = content.get(p.id)[lang]; const heads = titles[lang];
  const header = `---\nlayout: pattern\npattern_id: ${p.id}\nlang: ${lang}\npermalink: ${patternPath(p.id, lang)}\nalternate_url: ${patternPath(p.id, lang === 'en' ? 'zh' : 'en')}\n---\n\n`;
  const teaching = lang === 'zh' ? '> 以下为独立教学构造，未声称是实际模型输出或已测得的性能。' : '> Independent teaching constructions, not observed model outputs or measured performance.';
  const body = `${teaching}\n\n## ${heads[0]}\n\n${c.scenario}\n\n## ${heads[1]}\n\n${c.mechanism}\n\n## ${heads[2]}\n\n\`\`\`text\n${c.bad}\n\`\`\`\n\n## ${heads[3]}\n\n\`\`\`text\n${c.good}\n\`\`\`\n\n## ${heads[4]}\n\n${c.why}\n\n## ${heads[5]}\n\n${c.expected}\n\n## ${heads[6]}\n\n${c.boundaries}\n`;
  writeText(`_patterns/${p.id}.${lang}.md`, header + protectLiquid('\n' + body) + '\n');
}
console.log(`Migrated ${patterns.length} identities, ${content.size} active authored bilingual methods${legacyOnly ? ' (legacy staging only)' : ''}.`);
