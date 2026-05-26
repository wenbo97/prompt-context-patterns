import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadPatterns } from '../src/patterns.ts';
import { generatePromptfooConfig } from '../src/configGen.ts';
import { defaultConfig } from '../src/persistedConfig.ts';
import yaml from 'js-yaml';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, '..', 'patterns');
const all = loadPatterns(root);
const picked = all.filter((p) => p.id === 145 || p.id === 151);
if (picked.length !== 2) {
  console.error('expected patterns 145 and 151, got', picked.map((p) => p.id));
  process.exit(1);
}
const yamlStr = generatePromptfooConfig({
  patterns: picked,
  config: { ...defaultConfig, runs: 2 },
});
const parsed = yaml.load(yamlStr) as any;
if (!Array.isArray(parsed.prompts) || parsed.prompts.length !== 4) {
  console.error('expected 4 prompts, got', parsed.prompts);
  process.exit(1);
}
if (parsed.defaultTest.options.repeat !== 2) {
  console.error('repeat mismatch');
  process.exit(1);
}
console.log('YAML smoke OK');
console.log('---');
console.log(yamlStr);
