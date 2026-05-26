import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

export interface UserConfig {
  providerId: string;
  apiBaseUrl: string;
  apiKey: string;
  judgeProviderId: string;
  runs: number;
}

export const defaultConfig: UserConfig = {
  providerId: 'anthropic:messages:claude-opus-4-7',
  apiBaseUrl: 'http://localhost:4141',
  apiKey: 'dummy',
  judgeProviderId: 'anthropic:messages:claude-haiku-4-5',
  runs: 10,
};

const CONFIG_PATH = path.join(os.homedir(), '.patternfoo', 'config.json');

export function loadUserConfig(): UserConfig {
  if (!fs.existsSync(CONFIG_PATH)) return defaultConfig;
  const raw = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8')) as Partial<UserConfig>;
  return mergeConfig(defaultConfig, raw);
}

export function saveUserConfig(cfg: UserConfig): void {
  fs.mkdirSync(path.dirname(CONFIG_PATH), { recursive: true });
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(cfg, null, 2));
}

export function mergeConfig(base: UserConfig, over: Partial<UserConfig>): UserConfig {
  return { ...base, ...over };
}
