import { resolvePattern } from './lib.mjs';

// Resolve candidate aliases before attaching evidence; report order is irrelevant.
export function resolveDecision(key, decisions, idMap, patterns, seen = new Set()) {
  if (seen.has(key)) throw new Error(`Candidate merge cycle at ${key}`);
  const decision = decisions[key];
  if (!decision) throw new Error(`No integration decision for ${key}`);
  if (decision.status === 'rejected') throw new Error(`Rejected candidate cannot be a merge target: ${key}`);
  if (decision.status === 'active') {
    const pattern = patterns.find(p => p.id === idMap[key] && p.key === key);
    if (!pattern) throw new Error(`Active candidate has no identity: ${key}`);
    return pattern;
  }
  if (decision.status !== 'merged') throw new Error(`Invalid decision for ${key}`);
  if (decision.target_key) {
    return resolveDecision(decision.target_key, decisions, idMap, patterns, new Set([...seen, key]));
  }
  const pattern = resolvePattern(decision.target_id, patterns);
  if (pattern.status !== 'active') throw new Error(`Candidate ${key} merges into inactive ${pattern.id}`);
  return pattern;
}
