import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readState, stateUrl, filterRows } from '../assets/browser-state.js';
const rows = [
  { id: 3, name_en: 'Routing', name_zh: '路由', summary_en: 'Choose a branch', summary_zh: '选择分支', scenario_zh: '客户请求', tags: ['dispatch'], category: 'workflow', repos: ['a/one'], trace_status: 'traceable' },
  { id: 1, name_en: 'Context', name_zh: '上下文', summary_en: 'Read evidence', summary_zh: '读取证据', tags: [], category: 'context', repos: ['b/two'], trace_status: 'untraced' },
];
test('shared links round-trip repeated facets, language and loaded count', () => {
  const href = 'https://example.test/catalog/browse/?q=证据&category=context&category=workflow&repo=b%2Ftwo&lang=zh&limit=60';
  const s = readState(href);
  const next = readState(stateUrl(href, s));
  assert.equal(next.q, '证据'); assert.deepEqual([...next.category], ['context', 'workflow']);
  assert.equal(next.lang, 'zh'); assert.equal(next.limit, 60); assert.deepEqual([...next.repo], ['b/two']);
});
test('facet union and intersection work independently of display language', () => {
  const s = readState('https://example.test/?category=context&category=workflow&repo=b%2Ftwo&trace=untraced');
  assert.deepEqual(filterRows(rows, s).map(r => r.id), [1]);
  s.q = '上下文'; s.lang = 'en'; assert.deepEqual(filterRows(rows, s).map(r => r.id), [1]);
  s.q = 'no match'; assert.deepEqual(filterRows(rows, s), []);
});
test('invalid load counts do not strand users or allocate unbounded arrays', () => {
  assert.equal(readState('https://example.test/?limit=-3').limit, 30);
  assert.equal(readState('https://example.test/?limit=wrong').limit, 30);
  assert.equal(readState('https://example.test/?limit=61').limit, 60);
});
