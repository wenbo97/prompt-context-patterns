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

export function validateDecisions(candidates, decisions, idMap, patterns) {
  const errors = []; const keys = new Set(); const activeIds = new Set();
  for (const candidate of candidates) {
    const key = candidate.key;
    if (!key || keys.has(key)) errors.push(`Duplicate or missing candidate key: ${key}`);
    keys.add(key); const decision = decisions[key];
    if (!decision || !['active', 'merged', 'rejected'].includes(decision.status)) {
      errors.push(`Missing or invalid editorial decision: ${key}`); continue;
    }
    if (!decision.reason_en?.trim() || !decision.reason_zh?.trim()) errors.push(`Bilingual editorial rationale missing: ${key}`);
    if (decision.status === 'rejected') {
      if (idMap[key] !== undefined) errors.push(`Rejected candidate has an allocated identity: ${key}`);
      continue;
    }
    try {
      const pattern = resolveDecision(key, decisions, idMap, patterns);
      if (idMap[key] !== pattern.id) errors.push(`Candidate identity disagrees with its target: ${key}`);
      if (decision.status === 'active') {
        if (pattern.id < 207 || activeIds.has(pattern.id)) errors.push(`New candidate identity is invalid or reused: ${key}`);
        activeIds.add(pattern.id);
      }
    } catch (error) { errors.push(error.message); }
  }
  for (const key of Object.keys(decisions)) if (!keys.has(key)) errors.push(`Editorial decision has no candidate: ${key}`);
  for (const key of Object.keys(idMap)) if (!keys.has(key)) errors.push(`Allocated identity has no candidate: ${key}`);
  return errors;
}
