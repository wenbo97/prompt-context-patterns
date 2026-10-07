import test from 'node:test';
import assert from 'node:assert/strict';
import { REVIEW_KINDS, validateFileOutcome } from '../scripts/catalog/review-coverage.mjs';

const outcome = { disposition:'excluded', hash:'frozen-hash', reason:'HTTP adapter implementation; its imported review contract was analyzed separately.', review_kind:'scoped-relevance', review_evidence:{ reference:'per-path role ledger', observed:'request parser and adapter declarations' } };

test('scoped implementation exclusion can complete file accounting without a full audit', () => {
  assert.deepEqual(validateFileOutcome(outcome, 'frozen-hash', 'repo/adapter.ts'), []);
  for (const kind of REVIEW_KINDS) assert.deepEqual(validateFileOutcome({...outcome,review_kind:kind}, 'frozen-hash', 'repo/file'), []);
});
test('a disposition alone cannot establish honest review completion', () => {
  const errors=validateFileOutcome({disposition:'analyzed',hash:'frozen-hash',reason:'Reviewed'}, 'frozen-hash', 'repo/file');
  assert.ok(errors.some(e=>e.includes('review kind')));
  assert.ok(errors.some(e=>e.includes('evidence missing')));
});
test('pending, changed-source and empty-evidence outcomes stay invalid', () => {
  assert.match(validateFileOutcome({...outcome,disposition:'pending'}, 'frozen-hash', 'repo/file')[0], /Unreviewed/);
  assert.ok(validateFileOutcome(outcome, 'changed-hash', 'repo/file').some(e=>e.includes('hash mismatch')));
  for (const evidence of ['', [], {}, null]) assert.ok(validateFileOutcome({...outcome,review_evidence:evidence}, 'frozen-hash', 'repo/file').some(e=>e.includes('evidence missing')));
});

test('a terminal label cannot hide an explicitly unfinished evidence refresh', () => {
  const row = { ...outcome, review_evidence: { ...outcome.review_evidence, refresh_required: 'Inspect actual source content before final delivery.' } };
  assert.ok(validateFileOutcome(row, 'frozen-hash', 'repo/file').some(e => e.includes('refresh incomplete')));
});
