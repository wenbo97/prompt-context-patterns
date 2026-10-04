import { describe, it, expect } from 'vitest';
import { casesForPatterns, readyPatternIds } from '../src/patterns.js';
import type { LoadedPattern } from '../src/patterns.js';

const caseFixture = (caseId: string, patternIds: number[]): LoadedPattern => ({
  caseId, patternIds, name: caseId, category: 'test', hypothesis: 'Fixture', status: 'ready', dir: caseId, absDir: '/tmp/fixture',
});
describe('explicit evaluation case mappings', () => {
  it('never equates the historic008 case number with catalog pattern8', () => {
    const fixtures = [caseFixture('008-decision-tree', [3, 20])];
    expect(casesForPatterns(fixtures, [8])).toEqual([]);
    expect(casesForPatterns(fixtures, [3])).toHaveLength(1);
  });
  it('deduplicates one case linked to multiple selected patterns', () => {
    const fixtures = [caseFixture('decision-tree', [3, 20]), caseFixture('schema-lock', [14])];
    expect(casesForPatterns(fixtures, [3, 20]).map(p => p.caseId)).toEqual(['decision-tree']);
    expect(readyPatternIds(fixtures)).toEqual(new Set([3, 20, 14]));
  });
});
