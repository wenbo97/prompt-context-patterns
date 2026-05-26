import { describe, it, expect } from 'vitest';
import { defaultConfig, mergeConfig, type UserConfig } from '../src/persistedConfig.js';

describe('persistedConfig', () => {
  it('default targets local endpoint with opus model', () => {
    expect(defaultConfig.providerId).toBe('anthropic:messages:claude-opus-4-7');
    expect(defaultConfig.apiBaseUrl).toBe('http://localhost:4141');
    expect(defaultConfig.judgeProviderId).toBe('anthropic:messages:claude-haiku-4-5');
    expect(defaultConfig.runs).toBe(10);
  });
  it('mergeConfig overrides only provided keys', () => {
    const u: Partial<UserConfig> = { runs: 5 };
    const m = mergeConfig(defaultConfig, u);
    expect(m.runs).toBe(5);
    expect(m.providerId).toBe(defaultConfig.providerId);
  });
});
