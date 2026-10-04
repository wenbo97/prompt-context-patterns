import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests/e2e', timeout: 45000, expect: { timeout: 10000 }, fullyParallel: false,
  use: { baseURL: 'http://127.0.0.1:4000/prompt-context-patterns/', trace: 'retain-on-failure' },
  reporter: [['list'], ['json', { outputFile: 'test-results/browser-report.json' }]],
  webServer: { command: 'bundle exec jekyll serve --host 127.0.0.1 --port 4000 --no-watch',
    url: 'http://127.0.0.1:4000/prompt-context-patterns/', reuseExistingServer: !process.env.CI, timeout: 120000 },
});
