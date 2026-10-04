import fs from 'node:fs';

export interface PatternMeta { id: number; name: string; }
interface CatalogRecord { id: number; status: string; name_en: string; }

export function catalogFromRecords(records: CatalogRecord[]): PatternMeta[] {
  return records.filter(p => p.status === 'active').map(p => ({ id: p.id, name: p.name_en })).sort((a, b) => a.id - b.id);
}

const file = new URL('../../../_data/patterns.json', import.meta.url);
export const catalog = catalogFromRecords(JSON.parse(fs.readFileSync(file, 'utf8')) as CatalogRecord[]);
