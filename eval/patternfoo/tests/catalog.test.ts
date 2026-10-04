import { describe, it, expect } from 'vitest';
import { catalog, catalogFromRecords } from '../src/catalog.js';

describe('catalog', () => {
  it('reads active records and real names without assuming a fixed catalog length', () => {
    expect(catalogFromRecords([
      { id: 207, status: 'active', name_en: 'Bounded retry' },
      { id: 8, status: 'active', name_en: 'Confirmation gates' },
      { id: 17, status: 'removed', name_en: 'Retired' },
    ])).toEqual([{ id: 8, name: 'Confirmation gates' }, { id: 207, name: 'Bounded retry' }]);
  });
  it('has unique canonical identities', () => {
    expect(new Set(catalog.map(p => p.id)).size).toBe(catalog.length);
  });
});
