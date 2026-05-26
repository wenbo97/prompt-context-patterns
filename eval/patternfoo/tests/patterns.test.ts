import { describe, it, expect } from 'vitest';
import { loadPatterns } from '../src/patterns.js';
import path from 'node:path';

describe('loadPatterns', () => {
  it('reads meta.yaml from each subdir', () => {
    const root = path.join(__dirname, 'fixtures/patterns');
    const list = loadPatterns(root);
    expect(list).toHaveLength(1);
    expect(list[0]).toMatchObject({ id: 999, name: 'Fake Pattern', status: 'ready', dir: '999-fake' });
  });
});
