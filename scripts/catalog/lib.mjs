import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
export const CATEGORIES = ['prompt', 'context', 'workflow', 'orchestration', 'tools', 'output', 'evaluation', 'safety', 'skill-authoring'];
export const CRITERIA = ['scenario', 'mechanism', 'contrast', 'observable', 'boundaries'];
export const CATEGORY_LABELS = {
  prompt: ['Prompt design', '提示词设计'], context: ['Context management', '上下文管理'],
  workflow: ['Workflow control', '任务流程'], orchestration: ['Agent orchestration', '多 Agent 协作'],
  tools: ['Tool use', '工具调用'], output: ['Output contracts', '输出格式与约束'],
  evaluation: ['Evaluation & feedback', '测试与评估'], safety: ['Safety & trust', '安全与权限'],
  'skill-authoring': ['Skill authoring', 'Skill 编写'],
};
export const CATEGORY_DESCRIPTIONS = {
  prompt: ['Write instructions with explicit goals, useful constraints and same-task examples.', '通过明确目标、必要约束和同任务示例，写出可执行的提示词。'],
  context: ['Select, retrieve and preserve the information needed to carry out a task.', '选择、读取和保存执行任务所需的资料，处理缺失信息与上下文续接。'],
  workflow: ['Organize work into concrete steps, decisions, completion conditions and handoffs.', '把任务拆成具体步骤、判断和完成条件，说明未完成工作如何续接。'],
  orchestration: ['Coordinate agents through clear responsibilities, inputs, boundaries and shared results.', '明确各个 Agent 的职责、输入、工作边界和结果交接方式。'],
  tools: ['Choose and use tools with explicit inputs, inspectable results and failure handling.', '说明工具的选择条件、调用输入、结果检查和失败处理。'],
  output: ['Specify output structures, required fields and checks that make results usable.', '约定结果的结构、必要字段和检查方式，让输出可读取、可使用。'],
  evaluation: ['Design checks, compare results and use evidence to revise instructions or systems.', '设计检查与对照，根据可核对的结果改进指令或系统。'],
  safety: ['Set permission, evidence and trust boundaries before consequential actions.', '在关键操作前明确授权范围、证据要求与不可信输入的处理边界。'],
  'skill-authoring': ['Author discoverable skills with clear triggers, reusable instructions and maintainable references.', '写清 Skill 的触发条件、执行指令和参考资料，支持发现、复用与维护。'],
};
export const readJson = (rel) => JSON.parse(fs.readFileSync(path.join(ROOT, rel), 'utf8'));
export function protectLiquid(text) {
  return '{% raw %}' + text.replace(/{%-?\s*endraw\s*-?%}/g,
    token => '{{% endraw %}{{ ' + JSON.stringify(token.slice(1, -1)) + ' }}{% raw %}}') + '{% endraw %}';
}
export function writeText(rel, text) {
  const dest = path.join(ROOT, rel); fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.writeFileSync(dest, text.replace(/\r?\n/g, '\r\n'), 'utf8');
}
export function sourceUrl(source) {
  if (!source.repo) return source.url;
  const encoded = source.path.split('/').map(encodeURIComponent).join('/');
  const lines = source.start_line ? `#L${source.start_line}${source.end_line > source.start_line ? `-L${source.end_line}` : ''}` : '';
  return `https://github.com/${source.repo}/blob/${source.commit}/${encoded}${lines}`;
}
export function resolvePattern(id, patterns) {
  const byId = new Map(patterns.map((p) => [p.id, p])); const seen = new Set();
  let current = byId.get(id);
  while (current?.status === 'merged') {
    if (seen.has(current.id)) throw new Error(`merge cycle at ${current.id}`);
    seen.add(current.id);
    current = byId.get(current.merged_into);
    if (!current) throw new Error(`missing merge target for ${id}`);
  }
  if (!current) throw new Error(`missing pattern ${id}`);
  return current;
}
export function validateCatalog(patterns) {
  const errors = []; const ids = new Set();
  if (!Array.isArray(patterns) || !patterns.length) return ['catalog must be a non-empty array'];
  for (const p of patterns) {
    const prefix = `pattern ${p.id}`;
    if (!Number.isInteger(p.id) || p.id < 1) errors.push(`${prefix}: invalid id`);
    if (ids.has(p.id)) errors.push(`${prefix}: duplicate id`); ids.add(p.id);
    if (!['active', 'merged', 'removed'].includes(p.status)) errors.push(`${prefix}: invalid status`);
    if (p.status !== 'active') {
      if (!p.reason_en?.trim() || !p.reason_zh?.trim()) errors.push(`${prefix}: retirement needs bilingual reasons`);
      continue;
    }
    for (const key of ['name_en', 'name_zh', 'summary_en', 'summary_zh']) {
      if (typeof p[key] !== 'string' || !p[key].trim()) errors.push(`${prefix}: missing ${key}`);
    }
    if (!CATEGORIES.includes(p.category)) errors.push(`${prefix}: invalid category`);
    if (!Array.isArray(p.tags) || !Array.isArray(p.related_ids) || !Array.isArray(p.sources)) errors.push(`${prefix}: lists are required`);
    if (!['traceable', 'untraced'].includes(p.trace_status)) errors.push(`${prefix}: invalid trace status`);
    if (!['confirmed', 'unknown'].includes(p.origin_status)) errors.push(`${prefix}: invalid origin status`);
    const scores = p.review?.scores ?? {};
    for (const key of CRITERIA) if (!Number.isInteger(scores[key]) || scores[key] < 0 || scores[key] > 2) errors.push(`${prefix}: invalid ${key} score`);
    if (CRITERIA.reduce((sum, k) => sum + (scores[k] ?? 0), 0) < 8) errors.push(`${prefix}: quality below eight`);
    for (const key of ['scenario', 'mechanism', 'contrast']) if (scores[key] !== 2) errors.push(`${prefix}: ${key} admission gate failed`);
    if (p.trace_status === 'traceable' && !p.sources?.length) errors.push(`${prefix}: traceable label needs a source`);
    if (p.trace_status === 'untraced' && p.sources?.length) errors.push(`${prefix}: source/status conflict`);
    for (const s of p.sources ?? []) {
      if (s.repo) {
        if (!/^[\w.-]+\/[\w.-]+$/.test(s.repo) || !/^[a-f0-9]{40}$/i.test(s.commit ?? '') ||
          !s.path || s.path.split('/').includes('..') || !Number.isInteger(s.start_line) || s.start_line < 1 ||
          !Number.isInteger(s.end_line) || s.end_line < s.start_line) errors.push(`${prefix}: source needs immutable file and line evidence`);
      } else if (!/^https:\/\//.test(s.url ?? '') || !s.locator) errors.push(`${prefix}: external source needs a primary locator`);
      if (!s.license || !s.role) errors.push(`${prefix}: source attribution is incomplete`);
      if (s.url && s.repo && s.url !== sourceUrl(s)) errors.push(`${prefix}: source URL disagrees with evidence`);
    }
  }
  for (const p of patterns) {
    try {
      const target = resolvePattern(p.id, patterns);
      if (p.status === 'merged' && target.status !== 'active') errors.push(`pattern ${p.id}: merge target is not active`);
    } catch (error) { errors.push(error.message); }
    for (const id of p.related_ids ?? []) {
      if (id === p.id || !ids.has(id)) errors.push(`pattern ${p.id}: invalid related id ${id}`);
    }
  }
  return errors;
}
export function patternPath(id, lang = 'en') { return `/catalog/patterns/${id}${lang === 'zh' ? '-zh' : ''}/`; }
export function scenarioText(section) {
  // Search cards show the opening task, not supporting tables and fenced fixtures.
  return section.trim().split(/\n\s*\n/)[0].replace(/`([^`]+)`/g, '$1')
    .replace(/\[([^\]]+)\]\([^\)]+\)/g, '$1').replace(/\*\*([^*]+)\*\*/g, '$1').trim();
}
export function scenarioFromBody(id, lang) {
  const file = path.join(ROOT, '_patterns', `${id}.${lang}.md`);
  if (!fs.existsSync(file)) return '';
  const body = fs.readFileSync(file, 'utf8').replace(/\r\n/g, '\n');
  const heading = lang === 'zh' ? '使用场景' : 'Use case';
  return scenarioText(body.match(new RegExp(`^## ${heading}\\n+([\\s\\S]*?)(?=^## |(?![\\s\\S]))`, 'm'))?.[1] ?? '');
}
export function makeBrowserRecords(patterns, getScenario = scenarioFromBody) {
  return patterns.filter((p) => p.status === 'active').sort((a, b) => a.id - b.id).map((p) => ({
    id: p.id, name_en: p.name_en, name_zh: p.name_zh, summary_en: p.summary_en, summary_zh: p.summary_zh,
    scenario_en: getScenario(p.id, 'en'), scenario_zh: getScenario(p.id, 'zh'), category: p.category,
    category_en: CATEGORY_LABELS[p.category][0], category_zh: CATEGORY_LABELS[p.category][1], tags: p.tags,
    trace_status: p.trace_status, origin_status: p.origin_status,
    repos: [...new Set(p.sources.map((s) => s.repo).filter(Boolean))],
    detail_en: patternPath(p.id), detail_zh: patternPath(p.id, 'zh'),
  }));
}
