import { test } from 'node:test';
import assert from 'node:assert/strict';
import { resolveDecision, validateDecisions } from '../scripts/catalog/decisions.mjs';

test('candidate aliases resolve across report order and legacy aliases', () => {
  const patterns = [{ id: 25, status: 'active' }, { id: 80, status: 'merged', merged_into: 25 }, { id: 207, key: 'new', status: 'active' }];
  const decisions = { earlier: { status: 'merged', target_key: 'later' }, later: { status: 'merged', target_key: 'new' }, new: { status: 'active' }, old: { status: 'merged', target_id: 80 } };
  assert.equal(resolveDecision('earlier', decisions, { new: 207 }, patterns).id, 207);
  assert.equal(resolveDecision('old', decisions, {}, patterns).id, 25);
});

test('candidate integration rejects cycles, rejected targets and withdrawals', () => {
  assert.throws(() => resolveDecision('a', { a: { status: 'merged', target_key: 'b' }, b: { status: 'merged', target_key: 'a' } }, {}, []), /cycle/);
  assert.throws(() => resolveDecision('a', { a: { status: 'merged', target_key: 'b' }, b: { status: 'rejected' } }, {}, []), /Rejected/);
  assert.throws(() => resolveDecision('a', { a: { status: 'merged', target_id: 9 } }, {}, [{ id: 9, status: 'removed' }]), /inactive/);
});

test('editorial delivery accounts for every candidate and binds aliases to stable identities', () => {
  const candidates = ['new', 'alias', 'rejected'].map(key => ({ key }));
  const patterns = [{ id: 207, key: 'new', status: 'active' }];
  const rationale = { reason_en: 'Mechanism reviewed', reason_zh: '已审核机制' };
  const decisions = { new: { ...rationale, status: 'active' }, alias: { ...rationale, status: 'merged', target_key: 'new' }, rejected: { ...rationale, status: 'rejected' } };
  assert.deepEqual(validateDecisions(candidates, decisions, { new: 207, alias: 207 }, patterns), []);
  assert.match(validateDecisions([...candidates, { key: 'missing' }], decisions, { new: 207, alias: 25 }, patterns).join('\n'), /decision: missing/);
  assert.match(validateDecisions(candidates, decisions, { new: 207, alias: 25, rejected: 208 }, patterns).join('\n'), /disagrees|Rejected candidate/);
  assert.match(validateDecisions(candidates, { ...decisions, extra: decisions.new }, { new: 207, alias: 207 }, patterns).join('\n'), /no candidate/);
});
