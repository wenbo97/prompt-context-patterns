import fs from 'node:fs';
import path from 'node:path';
import yaml from 'js-yaml';

export interface LoadedPattern {
  id: number;
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
    const meta = yaml.load(fs.readFileSync(metaPath, 'utf8')) as Omit<LoadedPattern, 'dir' | 'absDir'>;
    out.push({ ...meta, dir: name, absDir });
  }
  return out.sort((a, b) => a.id - b.id);
}
