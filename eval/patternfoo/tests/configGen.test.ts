import { describe, it, expect } from 'vitest';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import yaml from 'js-yaml';
import { generatePromptfooConfig } from '../src/configGen.js';
import { defaultConfig } from '../src/persistedConfig.js';

describe('generatePromptfooConfig', () => {
  it('emits one prompt pair per pattern and shared defaultTest with repeat=N', () => {
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'pf-'));
    const patDir = path.join(tmp, '145-iron-law');
    fs.mkdirSync(patDir, { recursive: true });
    fs.writeFileSync(path.join(patDir, 'rubric.md'), 'PASS if X. FAIL if Y.');
    fs.writeFileSync(
      path.join(patDir, 'scenarios.yaml'),
      "- vars: { task: 'do thing' }\n  assert: [{ type: llm-rubric, value: file://rubric.md }]\n",
    );
    const yamlStr = generatePromptfooConfig({
      patterns: [
        { id: 145, dir: '145-iron-law', absDir: patDir, name: '', category: '', hypothesis: '', status: 'ready' },
      ],
      config: { ...defaultConfig, runs: 7 },
    });
    const parsed = yaml.load(yamlStr) as any;
    expect(parsed.providers[0].id).toBe(defaultConfig.providerId);
    expect(parsed.providers[0].config.apiBaseUrl).toBe(defaultConfig.apiBaseUrl);
    expect(parsed.prompts).toHaveLength(2);
    expect(parsed.prompts[0]).toContain('145-iron-law/prompt-a.md');
    expect(parsed.prompts[1]).toContain('145-iron-law/prompt-b.md');
    expect(parsed.tests[0].vars.task).toBe('do thing');
    expect(parsed.tests[0].assert[0].value).toContain('PASS if X');
    expect(parsed.defaultTest.assert[0].type).toBe('llm-rubric');
    expect(parsed.defaultTest.assert[0].value).toContain('PASS if X');
    expect(parsed.defaultTest.options.repeat).toBe(7);
    expect(parsed.defaultTest.options.provider.id).toBe(defaultConfig.judgeProviderId);
  });
});
