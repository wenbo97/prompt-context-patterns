import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';
import { loadPatterns } from '../src/patterns.ts';
import { generatePromptfooConfig } from '../src/configGen.ts';
import { defaultConfig } from '../src/persistedConfig.ts';
import { runPromptfoo, summarizeOutput, writeRunArtifacts } from '../src/runner.ts';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, '..', 'patterns');
const resultsRoot = path.join(__dirname, '..', 'results');
const picked = loadPatterns(root).filter((p) => p.id === 145);
const yamlStr = generatePromptfooConfig({
  patterns: picked,
  config: { ...defaultConfig, runs: 1 },
});
const { yamlPath, outPath, dir } = writeRunArtifacts(resultsRoot, yamlStr);
console.log('wrote', yamlPath);
try {
  const out = await runPromptfoo({
    configYamlPath: yamlPath,
    outputJsonPath: outPath,
    onStdout: (c) => process.stdout.write(c),
  });
  const s = summarizeOutput(out);
  console.log('\n=== SUMMARY ===');
  for (const [k, v] of s) console.log(k, v);
} catch (e) {
  console.error('eval failed:', e);
  process.exit(2);
}
