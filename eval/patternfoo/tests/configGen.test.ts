import { describe, it, expect } from 'vitest';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import yaml from 'js-yaml';
import { generatePromptfooConfig, generateCaseConfigs } from '../src/configGen.js';
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
        { caseId: '145-iron-law', patternIds: [145], dir: '145-iron-law', absDir: patDir, name: '', category: '', hypothesis: '', status: 'ready' },
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
    expect(parsed.defaultTest.assert).toEqual([]);
    expect(parsed.tests[0].assert.filter((a: any) => a.type === 'llm-rubric')).toHaveLength(1);
    expect(parsed.defaultTest.options.repeat).toBe(7);
    expect(parsed.defaultTest.options.provider.id).toBe(defaultConfig.judgeProviderId);
  });
  it('isolates each case prompt pair from other cases scenarios', () => {
    const root = fs.mkdtempSync(path.join(os.tmpdir(), 'pf-isolated-'));
    const patterns = ['one', 'two'].map(caseId => {
      const absDir = path.join(root, caseId); fs.mkdirSync(absDir);
      fs.writeFileSync(path.join(absDir, 'rubric.md'), `Grade ${caseId}`);
      fs.writeFileSync(path.join(absDir, 'scenarios.yaml'), `- vars: { task: '${caseId} input' }\n`);
      return { caseId, patternIds: [1], dir: caseId, absDir, name: caseId, category: 'test', hypothesis: '', status: 'ready' as const };
    });
    const configs = generateCaseConfigs(patterns, defaultConfig);
    expect(configs).toHaveLength(2);
    for (const run of configs) {
      const config = yaml.load(run.yaml) as any;
      expect(config.prompts).toHaveLength(2);
      expect(config.prompts.every((p: string) => p.includes(`/${run.caseId}/`))).toBeTruthy();
      expect(config.tests.map((t: any) => t.vars.task)).toEqual([`${run.caseId} input`]);
      expect(config.tests[0].assert[0].type).toBe('llm-rubric');
    }
    expect(() => generatePromptfooConfig({ patterns, config: defaultConfig })).toThrow(/one evaluation case/);
  });
});
