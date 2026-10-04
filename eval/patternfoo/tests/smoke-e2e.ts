import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadPatterns } from '../src/patterns.ts';
import { generateCaseConfigs } from '../src/configGen.ts';
import { defaultConfig } from '../src/persistedConfig.ts';
import yaml from 'js-yaml';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, '..', 'patterns');
const all = loadPatterns(root);
const picked = all.filter((p) => p.caseId === '145-iron-law' || p.caseId === '151-hard-gate');
if (picked.length !== 2) {
  console.error('expected cases 145-iron-law and 151-hard-gate, got', picked.map((p) => p.caseId));
  process.exit(1);
}
const configs = generateCaseConfigs(picked, { ...defaultConfig, runs: 2 });
for (const run of configs) {
  const parsed = yaml.load(run.yaml) as any;
  if (!Array.isArray(parsed.prompts) || parsed.prompts.length !== 2 || parsed.defaultTest.options.repeat !== 2) {
    console.error('isolated case contract mismatch', run.caseId); process.exit(1);
  }
}
console.log('Two isolated case YAML contracts passed. No provider calls were made.');
