import { test } from 'node:test';
import assert from 'node:assert/strict';
import { resolveDecision } from '../scripts/catalog/decisions.mjs';

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
