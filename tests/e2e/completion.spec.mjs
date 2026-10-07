import { test, expect } from '@playwright/test';
import { baseurl } from './site-settings.mjs';

const messages = {
  en: { loading: 'Loading patterns…', error: 'Pattern data could not be loaded.', retry: 'Try again', html: 'en', index: '/catalog/catalog-index/' },
  zh: { loading: '正在加载…', error: '目录加载失败，请重试或打开完整目录。', retry: '重新加载', html: 'zh-CN', index: '/catalog/catalog-index-zh/' },
};

test('loading feedback follows language changes and history before data arrives', async ({ page }) => {
  let release;
  const pending = new Promise(resolve => { release = resolve; });
  await page.route('**/assets/patterns.json', async route => { await pending; await route.continue(); });
  try {
    await page.goto('catalog/browse/?lang=en', { waitUntil: 'domcontentloaded' });
    await expect(page.locator('#pb-count')).toHaveText(messages.en.loading);
    await page.locator('#pb-lang [data-lang=zh]').click();
    await expect(page.locator('#pb-count')).toHaveText(messages.zh.loading);
    await page.goBack();
    await expect(page.locator('#pb-count')).toHaveText(messages.en.loading);
    await page.goForward();
    await expect(page.locator('#pb-count')).toHaveText(messages.zh.loading);
    release();
    await expect(page.locator('#pb-list > li')).toHaveCount(30);
    await expect(page.locator('html')).toHaveAttribute('lang', messages.zh.html);
  } finally { release(); }
});

for (const initial of ['en', 'zh']) test(`failed data feedback switches from ${initial} and retries in the chosen language`, async ({ page }) => {
  let failing = true;
  await page.route('**/assets/patterns.json', route => failing ? route.abort('failed') : route.continue());
  await page.goto(`catalog/browse/?lang=${initial}&category=context&limit=60`);
  await expect(page.locator('#error-text')).toHaveText(messages[initial].error);
  const next = initial === 'en' ? 'zh' : 'en';
  await page.locator(`#pb-lang [data-lang=${next}]`).click();
  await expect(page.locator('#error-text')).toHaveText(messages[next].error);
  await expect(page.locator('#retry-load')).toHaveText(messages[next].retry);
  await expect(page.locator('#static-index')).toHaveAttribute('href', baseurl + messages[next].index);
  await page.goBack();
  await expect(page.locator('#error-text')).toHaveText(messages[initial].error);
  await page.goForward();
  await expect(page.locator('#error-text')).toHaveText(messages[next].error);
  failing = false;
  await page.locator('#retry-load').click();
  await expect(page.locator('#browser-error')).toBeHidden();
  await expect(page.locator('#pb-list > li').first()).toBeVisible();
  await expect(page.locator('html')).toHaveAttribute('lang', messages[next].html);
  await expect(page).toHaveURL(/category=context/);
  await expect(page).toHaveURL(/limit=60/);
});

for (const status of ['loading', 'error']) test(`Back restores remembered language from a URL without lang during ${status}`, async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('pcp-language', 'zh'));
  let release;
  const pending = new Promise(resolve => { release = resolve; });
  await page.route('**/assets/patterns.json', async route => {
    if (status === 'error') await route.abort();
    else { await pending; await route.continue(); }
  });
  try {
    await page.goto('catalog/browse/', { waitUntil: 'domcontentloaded' });
    const feedback = status === 'error' ? page.locator('#error-text') : page.locator('#pb-count');
    await expect(feedback).toHaveText(messages.zh[status === 'error' ? 'error' : 'loading']);
    await expect(page.locator('html')).toHaveAttribute('lang', messages.zh.html);
    await page.locator('#pb-lang [data-lang=en]').click();
    await expect(feedback).toHaveText(messages.en[status === 'error' ? 'error' : 'loading']);
    await page.goBack();
    await expect(page.locator('html')).toHaveAttribute('lang', messages.zh.html);
    await expect(feedback).toHaveText(messages.zh[status === 'error' ? 'error' : 'loading']);
    await expect(page.locator('#static-index')).toHaveAttribute('href', baseurl + messages.zh.index);
    await page.goForward();
    await expect(page.locator('html')).toHaveAttribute('lang', messages.en.html);
    await expect(feedback).toHaveText(messages.en[status === 'error' ? 'error' : 'loading']);
  } finally { release?.(); }
});

test('long plain technical strings wrap in the reading column without horizontal loss', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 900 });
  await page.goto('catalog/patterns/298/');
  await page.evaluate(() => document.fonts.ready);
  await page.locator('.pattern-content > p').first().evaluate(node => {
    node.textContent = 'namespace/' + 'long-reference-component/'.repeat(20);
  });
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBeTruthy();
});

for (const lang of ['en', 'zh']) test(`markup examples remain literal teaching text in ${lang}`, async ({ page }) => {
  const errors = []; page.on('pageerror', error => errors.push(error.message));
  await page.goto(`catalog/patterns/183${lang === 'zh' ? '-zh' : ''}/`);
  await expect(page.locator('.pattern-content script')).toHaveCount(0);
  await expect(page.locator('.pattern-content h2')).toHaveCount(7);
  const scenario = await page.locator('.pattern-content h2').first().evaluate(heading => heading.nextElementSibling.textContent);
  expect(scenario).toContain(lang === 'zh' ? '<script>' : '</script>');
  await page.goto(`catalog/patterns/4${lang === 'zh' ? '-zh' : ''}/`);
  await expect(page.locator('.pattern-content')).toContainText('catalog-check <path> [--json]');
  if (lang === 'en') {
    await page.goto('catalog/patterns/167/');
    await expect(page.locator('.pattern-content')).toContainText('clearLayers(layerIds:string[]):Promise<void>');
  }
  expect(errors).toEqual([]);
});
