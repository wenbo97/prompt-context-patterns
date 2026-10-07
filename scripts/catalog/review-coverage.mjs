export const REVIEW_KINDS = ['full-semantic', 'verified-equivalence', 'difference-review', 'scoped-relevance'];

function hasEvidence(value) {
  if (typeof value === 'string') return value.trim().length > 0;
  if (Array.isArray(value)) return value.length > 0;
  return value !== null && typeof value === 'object' && Object.keys(value).length > 0;
}

// Validate honest accounting, not equal-depth upstream implementation audits.
// Evidence quality and the selected depth remain independent-review questions.
export function validateFileOutcome(row, expectedHash, label) {
  if (!row || !['analyzed', 'duplicate', 'excluded'].includes(row.disposition)) return [`Unreviewed source: ${label}`];
  const errors = [];
  if (typeof row.reason !== 'string' || !row.reason.trim()) errors.push(`Unexplained source decision: ${label}`);
  if (row.hash !== expectedHash) errors.push(`Source hash mismatch: ${label}`);
  if (!REVIEW_KINDS.includes(row.review_kind)) errors.push(`Missing or invalid review kind: ${label}`);
  if (!hasEvidence(row.review_evidence)) errors.push(`Review evidence missing: ${label}`);
  if (row.review_evidence?.refresh_required) errors.push(`Review evidence refresh incomplete: ${label}`);
  return errors;
}
