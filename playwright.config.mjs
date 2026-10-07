import { defineConfig } from '@playwright/test';
import { base, port, settings } from './tests/e2e/site-settings.mjs';
export default defineConfig({
  testDir: './tests/e2e', timeout: 45000, expect: { timeout: 10000 }, fullyParallel: false,
  use: { baseURL: base, trace: 'retain-on-failure', channel: process.env.PLAYWRIGHT_CHANNEL || undefined },
  reporter: [['list'], ['json', { outputFile: 'test-results/browser-report.json' }]],
  webServer: { command: `bundle exec jekyll serve --config ${settings.configPaths} --host 127.0.0.1 --port ${port} --no-watch`,
    env: { JEKYLL_ENV: 'production' }, url: base, reuseExistingServer: Boolean(settings.baseurl) && !process.env.CI, timeout: 120000 },
});
