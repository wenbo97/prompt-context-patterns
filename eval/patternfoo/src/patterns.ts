import fs from 'node:fs';
import path from 'node:path';
import yaml from 'js-yaml';

export interface LoadedPattern {
  caseId: string;
  patternIds: number[];
  name: string;
  category: string;
  hypothesis: string;
  status: 'ready' | 'todo';
  dir: string;
  absDir: string;
}

export function loadPatterns(rootDir: string): LoadedPattern[] {
  if (!fs.existsSync(rootDir)) return [];
  const out: LoadedPattern[] = [];
  for (const name of fs.readdirSync(rootDir)) {
    const absDir = path.join(rootDir, name);
    const metaPath = path.join(absDir, 'meta.yaml');
    if (!fs.statSync(absDir).isDirectory() || !fs.existsSync(metaPath)) continue;
    const meta = yaml.load(fs.readFileSync(metaPath, 'utf8')) as Record<string, unknown>;
    if (typeof meta?.case_id !== 'string' || !/^[a-z0-9-]+$/i.test(meta.case_id) || !Array.isArray(meta.pattern_ids) ||
      meta.pattern_ids.length === 0 || !meta.pattern_ids.every(id => Number.isInteger(id) && id > 0) ||
      typeof meta.name !== 'string' || typeof meta.category !== 'string' || typeof meta.hypothesis !== 'string' ||
      !['ready', 'todo'].includes(String(meta.status))) throw new Error(`Invalid case metadata: ${metaPath}`);
    out.push({ caseId: meta.case_id, patternIds: [...new Set(meta.pattern_ids as number[])],
      name: meta.name, category: meta.category, hypothesis: meta.hypothesis,
      status: meta.status as 'ready' | 'todo', dir: name, absDir });
  }
  if (new Set(out.map(p => p.caseId)).size !== out.length) throw new Error('Duplicate evaluation case identities');
  return out.sort((a, b) => a.caseId.localeCompare(b.caseId));
}

export function readyPatternIds(cases: LoadedPattern[]): Set<number> {
  return new Set(cases.filter(p => p.status === 'ready').flatMap(p => p.patternIds));
}

export function casesForPatterns(cases: LoadedPattern[], selected: number[]): LoadedPattern[] {
  const ids = new Set(selected);
  return cases.filter(p => p.status === 'ready' && p.patternIds.some(id => ids.has(id)));
}
