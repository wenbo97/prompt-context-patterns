import { describe, it, expect } from 'vitest';
import { catalog, TOP10 } from '../src/catalog.js';

describe('catalog', () => {
  it('contains exactly 155 patterns', () => {
    expect(catalog.length).toBe(155);
  });
  it('ids are unique and 1..155', () => {
    const ids = catalog.map(p => p.id).sort((a, b) => a - b);
    expect(ids[0]).toBe(1);
    expect(ids[ids.length - 1]).toBe(155);
    expect(new Set(ids).size).toBe(155);
  });
  it('TOP10 lists the 10 MVP-runnable pattern ids', () => {
    expect(TOP10).toEqual([6, 8, 17, 100, 103, 145, 146, 148, 151, 152]);
  });
});
