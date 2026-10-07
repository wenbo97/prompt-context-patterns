import { describe, it, expect } from 'vitest';
import { loadPatterns } from '../src/patterns.js';
import path from 'node:path';

describe('loadPatterns', () => {
  it('reads meta.yaml from each subdir', () => {
    const root = path.join(__dirname, 'fixtures/patterns');
    const list = loadPatterns(root);
    expect(list).toHaveLength(1);
    expect(list[0]).toMatchObject({ caseId: 'fake-fixture', patternIds: [999], name: 'Fake Pattern', status: 'ready', dir: '999-fake' });
  });
  it('all shipped cases have explicit identities and method links', () => {
    const cases = loadPatterns(path.join(__dirname, '../patterns'));
    expect(cases).toHaveLength(10);
    expect(cases.find(p => p.caseId === '008-decision-tree')?.patternIds).not.toContain(8);
    expect(cases.find(p => p.caseId === '017-schema-lock')?.patternIds).not.toContain(17);
  });
});
