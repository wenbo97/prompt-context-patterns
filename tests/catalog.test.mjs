import { test } from 'node:test';
import assert from 'node:assert/strict';
import { validateCatalog, resolvePattern, sourceUrl, makeBrowserRecords, scenarioText } from '../scripts/catalog/lib.mjs';

test('search scenarios retain the opening task without leaking Markdown teaching fixtures', () => {
  const section = 'Route the `billing-api` review to its **owner** using [the table](owners.md).\n\nReference material:\n\n```text\nbilling-api | payments\n```';
  assert.equal(scenarioText(section), 'Route the billing-api review to its owner using the table.');
  assert.equal(scenarioText(''), '');
});

const active = (id = 1) => ({ id, status: 'active', name_en: 'Bounded retrieval', name_zh: '有界检索',
  summary_en: 'Fill the evidence gap before acting.', summary_zh: '行动前补齐证据缺口。',
  category: 'context', tags: ['retrieval'], trace_status: 'untraced', origin_status: 'unknown',
  sources: [], related_ids: [], review: { scores: { scenario: 2, mechanism: 2, contrast: 2, observable: 1, boundaries: 1 },
    decision: 'active', reason_en: 'A concrete retrieval constraint.', reason_zh: '可操作的检索约束。', reviewed_at: '2026-10-03' } });

test('source uncertainty does not disqualify a reviewed useful method', () => {
  assert.deepEqual(validateCatalog([active()]), []);
});
test('a traceable label requires a pinned, located source', () => {
  const p = { ...active(), trace_status: 'traceable' };
  assert.match(validateCatalog([p]).join('\n'), /source/);
  p.sources = [{ repo: 'obra/superpowers', commit: 'a'.repeat(40), path: 'skills/writing-skills/SKILL.md',
    start_line: 1, end_line: 8, role: 'observed-example', license: 'MIT' }];
  assert.deepEqual(validateCatalog([p]), []);
});
test('quality admission rejects weak contrasts even when total reaches eight', () => {
  const p = active(); p.review.scores = { scenario: 2, mechanism: 2, contrast: 1, observable: 2, boundaries: 2 };
  assert.match(validateCatalog([p]).join('\n'), /contrast/);
});
test('merged and removed records preserve identities without appearing in search', () => {
  const records = [active(), { id: 2, status: 'merged', merged_into: 1, reason_en: 'Same mechanism.', reason_zh: '同一机制。' },
    { id: 3, status: 'removed', reason_en: 'Unsupported claim.', reason_zh: '缺少依据。' }];
  assert.equal(resolvePattern(2, records).id, 1);
  assert.equal(resolvePattern(3, records).status, 'removed');
  assert.equal(makeBrowserRecords(records, () => 'Example scenario').length, 1);
});
test('migration cannot hide cycles, dangling references or reused IDs', () => {
  const cyclic = [{ id: 1, status: 'merged', merged_into: 2 }, { id: 2, status: 'merged', merged_into: 1 }];
  assert.throws(() => resolvePattern(1, cyclic), /cycle/);
  assert.match(validateCatalog([active(), active()]).join('\n'), /duplicate/);
  const dangling = active(); dangling.related_ids = [999];
  assert.match(validateCatalog([dangling]).join('\n'), /related/);
});
test('GitHub sources bind to a commit and encode paths and line locations', () => {
  assert.equal(sourceUrl({ repo: 'owner/repo', commit: 'b'.repeat(40), path: 'rules/a b.md', start_line: 9, end_line: 12 }),
    `https://github.com/owner/repo/blob/${'b'.repeat(40)}/rules/a%20b.md#L9-L12`);
});
