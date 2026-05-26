import { describe, it, expect } from 'vitest';
import { summarizeOutput } from '../src/runner.js';

describe('summarizeOutput', () => {
  it('counts pass/fail per prompt label', () => {
    const out = {
      results: {
        results: [
          { promptId: 'A', success: true },
          { promptId: 'A', success: false },
          { promptId: 'B', success: true },
          { promptId: 'B', success: true },
        ],
      },
    };
    const s = summarizeOutput(out as any);
    expect(s.get('A')).toEqual({ pass: 1, fail: 1 });
    expect(s.get('B')).toEqual({ pass: 2, fail: 0 });
  });
});
