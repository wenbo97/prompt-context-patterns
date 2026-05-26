import fs from 'node:fs';
import path from 'node:path';
import yaml from 'js-yaml';
import type { LoadedPattern } from './patterns.js';
import type { UserConfig } from './persistedConfig.js';

export interface GenInput {
  patterns: LoadedPattern[];
  config: UserConfig;
}

export function generatePromptfooConfig({ patterns, config }: GenInput): string {
  const prompts: string[] = [];
  const tests: any[] = [];
  for (const p of patterns) {
    prompts.push(`file://${p.absDir}/prompt-a.md`);
    prompts.push(`file://${p.absDir}/prompt-b.md`);
    const rubric = fs.readFileSync(path.join(p.absDir, 'rubric.md'), 'utf8');
    const scenarios = yaml.load(fs.readFileSync(path.join(p.absDir, 'scenarios.yaml'), 'utf8')) as any[];
    for (const s of scenarios) {
      const assert = (s.assert ?? []).map((a: any) =>
        a && typeof a.value === 'string' && a.value.startsWith('file://') && a.value.endsWith('rubric.md')
          ? { ...a, value: rubric }
          : a,
      );
      tests.push({ ...s, assert });
    }
  }
  const doc = {
    providers: [
      {
        id: config.providerId,
        config: { apiBaseUrl: config.apiBaseUrl, apiKey: config.apiKey, apiKeyRequired: false },
      },
    ],
    prompts,
    tests,
    defaultTest: {
      assert: patterns.length === 1
        ? [{ type: 'llm-rubric', value: fs.readFileSync(path.join(patterns[0].absDir, 'rubric.md'), 'utf8') }]
        : [],
      options: {
        repeat: config.runs,
        provider: {
          id: config.judgeProviderId,
          config: { apiBaseUrl: config.apiBaseUrl, apiKey: config.apiKey, apiKeyRequired: false },
        },
      },
    },
  };
  return yaml.dump(doc, { lineWidth: 200 });
}
