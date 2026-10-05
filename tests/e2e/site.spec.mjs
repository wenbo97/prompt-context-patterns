import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import fs from 'node:fs';

// Exercise integrated content as well as the established reference page.
const additions = JSON.parse(fs.readFileSync('_data/patterns.json', 'utf8'))
  .filter(pattern => pattern.status === 'active' && pattern.id >= 207);
const longestAddition = additions.reduce((selected, pattern) => {
  const length = ['en', 'zh'].reduce((total, lang) => total + fs.statSync(`_patterns/${pattern.id}.${lang}.md`).size, 0);
  return !selected || length > selected.length ? { id: pattern.id, length } : selected;
}, null);
const integratedReadingRoutes = longestAddition
  ? [`catalog/patterns/${longestAddition.id}/`, `catalog/patterns/${longestAddition.id}-zh/`] : [];

test('search, facets, language and loaded results survive detail navigation and Back', async ({ page }) => {
  const errors = []; page.on('pageerror', error => errors.push(error.message));
  await page.goto('catalog/browse/');
  await expect(page.locator('#pb-list > li')).toHaveCount(30);
  await page.getByRole('button', { name: 'Load 30 more' }).click();
  await expect(page.locator('#pb-list > li')).toHaveCount(60);
  await expect(page).toHaveURL(/limit=60/);
  await page.locator('#pb-lang [data-lang=zh]').click();
  await expect(page.locator('html')).toHaveAttribute('lang', 'zh-CN');
  await expect(page.locator('.brand')).toHaveAttribute('href', /index-zh\//);
  await expect(page.locator('.site-nav')).toHaveAttribute('aria-label', '主要导航');
  await expect(page.locator('.skip-link')).toHaveText('跳到正文');
  await page.locator('#pb-list h2 a').first().click();
  await expect(page.locator('html')).toHaveAttribute('lang', 'zh-CN');
  await page.goBack(); await expect(page.locator('#pb-list > li')).toHaveCount(60);
  await page.locator('#pb-search').fill('a request which cannot match this collection zzz999');
  await expect(page.locator('#pb-empty')).toBeVisible();
  await page.locator('#clear-search').click();
  await expect(page.locator('#pb-list > li')).toHaveCount(30);
  await page.locator('[data-facet=trace] [data-value=untraced]').click();
  await expect(page.locator('[data-facet=trace] [data-value=untraced]')).toBeFocused();
  for (const item of await page.locator('#pb-list > li').all()) await expect(item.locator('.untraced')).toBeVisible();
  expect(errors).toEqual([]);
});

test('keyboard controls and reduced motion work under 200% equivalent reflow', async ({ page, context }) => {
  // A 1280px display at 200% zoom exposes a 640 CSS-pixel layout viewport.
  // Emulation checks that reflow; it does not claim to test browser chrome zoom UI.
  const session = await context.newCDPSession(page);
  await session.send('Emulation.setDeviceMetricsOverride', { width: 640, height: 450, deviceScaleFactor: 2, mobile: false, screenWidth: 1280, screenHeight: 900 });
  await page.emulateMedia({ reducedMotion: 'reduce' });
  for (const route of ['', 'catalog/browse/?lang=zh', 'catalog/patterns/23-zh/', 'sources-zh/', ...integratedReadingRoutes]) {
    await page.goto(route);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBeTruthy();
    expect(await page.evaluate(() => getComputedStyle(document.documentElement).scrollbarColor)).not.toBe('auto');
    expect(await page.evaluate(() => getComputedStyle(document.documentElement).scrollBehavior)).toBe('auto');
  }
  await page.goto('catalog/browse/?lang=zh');
  await expect(page.locator('#pb-list > li')).toHaveCount(30);
  await page.locator('#pb-search').focus(); await page.keyboard.type('zzzz999999');
  await expect(page.locator('#pb-empty')).toBeVisible();
  await page.keyboard.press('Tab'); await expect(page.locator('#clear-search')).toBeFocused();
  await page.keyboard.press('Enter'); await expect(page.locator('#pb-search')).toBeFocused();
  await expect(page.locator('#pb-list > li')).toHaveCount(30);
  const more = page.locator('#load-more'); await more.focus(); await page.keyboard.press('Enter');
  await expect(page.locator('#pb-list > li')).toHaveCount(60); await expect(more).toBeFocused();
});

test('data failure provides retry and a usable static index', async ({ page }) => {
  let failing = true;
  await page.route('**/assets/patterns.json', route => failing ? route.abort() : route.continue());
  await page.goto('catalog/browse/'); await expect(page.locator('#browser-error')).toBeVisible();
  await expect(page.locator('#static-index')).toHaveAttribute('href', /catalog-index/);
  failing = false; await page.locator('#retry-load').click();
  await expect(page.locator('#pb-list > li')).toHaveCount(30); await expect(page.locator('#browser-error')).toBeHidden();
});

test('an empty catalog is localized and distinct from no search matches', async ({ page }) => {
  await page.route('**/assets/patterns.json', route => route.fulfill({ contentType: 'application/json', body: '[]' }));
  await page.goto('catalog/browse/?lang=zh');
  await expect(page.locator('#pb-empty')).toHaveText('当前没有可浏览的方法。');
  await expect(page.locator('#browser-error')).toBeHidden();
  await expect(page.locator('#pb-list > li')).toHaveCount(0);
  await expect(page.locator('#load-more')).toBeHidden();
  await expect(page.locator('#static-index')).toHaveAttribute('href', /catalog-index-zh/);
});

test('Chinese composition does not commit incomplete search text', async ({ page }) => {
  await page.goto('catalog/browse/'); await expect(page.locator('#pb-list > li')).toHaveCount(30);
  await page.locator('#pb-search').evaluate(input => {
    input.dispatchEvent(new CompositionEvent('compositionstart', { bubbles: true }));
    input.value = '上下文'; input.dispatchEvent(new InputEvent('input', { bubbles: true, isComposing: true }));
  });
  await expect(page).not.toHaveURL(/q=/);
  await page.locator('#pb-search').evaluate(input => input.dispatchEvent(new CompositionEvent('compositionend', { bubbles: true })));
  await expect(page).toHaveURL(/q=/);
});

test('static fallback and old fragment entry remain usable without JavaScript', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false }); const page = await context.newPage();
  await page.goto('http://127.0.0.1:4000/prompt-context-patterns/catalog/browse/');
  await expect(page.locator('noscript a').first()).toHaveAttribute('href', /catalog-index/);
  await page.goto('http://127.0.0.1:4000/prompt-context-patterns/catalog/categories/patterns-execution-control/#pattern-8-confirmation-gates--human-in-the-loop');
  await expect(page.locator('[id="pattern-8-confirmation-gates--human-in-the-loop"] a')).toHaveAttribute('href', /patterns\/8/);
  await context.close();
});

for (const width of [375, 768, 1280]) test(`reading surfaces are accessible at${width}px`, async ({ page }) => {
  await page.setViewportSize({ width, height: 900 });
  for (const route of ['', 'catalog/browse/', 'catalog/patterns/23/', 'sources/', ...integratedReadingRoutes]) {
    await page.goto(route); if (route.includes('browse')) await expect(page.locator('#pb-list > li')).toHaveCount(30);
    const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']).analyze();
    expect(results.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.map(n => n.target) }))).toEqual([]);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBeTruthy();
  }
  fs.mkdirSync('.tools/qa', { recursive: true });
  await page.goto(''); await page.screenshot({ path: `.tools/qa/home-${width}.png`, fullPage: true });
});


test('localized category navigation and source versions lead to their exact targets', async ({ page }) => {
  const catalog = JSON.parse(fs.readFileSync('_data/patterns.json', 'utf8'));
  const first = catalog.find(pattern => pattern.id === 1);
  await page.goto('catalog/catalog-index-zh/');
  const row = page.locator('tbody tr').first();
  await expect(row.locator('.english-name')).toHaveText(first.name_en);
  const category = row.locator('td').nth(2).getByRole('link');
  await expect(category).toHaveAttribute('href', `/prompt-context-patterns/topics/${first.category}-zh/`);
  await category.click();
  await expect(page).toHaveURL(new RegExp(`topics/${first.category}-zh/`));
  await page.goto('catalog/patterns/1-zh/');
  await expect(page.locator('.pattern-heading .english-name')).toHaveText(first.name_en);
  await expect(page.locator('.source-version')).toHaveCount(first.sources.filter(source => source.commit).length);
  for (const [index, source] of first.sources.filter(source => source.commit).entries()) {
    const version = page.locator('.source-version').nth(index);
    await expect(version).toHaveAttribute('href', source.url);
    await expect(version.locator('code')).toHaveText(source.commit.slice(0, 12));
    expect(source.url).toContain(`/blob/${source.commit}/`);
  }
  await expect(page.getByRole('heading', { name: '反例', exact: true })).toBeVisible();
  await expect(page.getByRole('heading', { name: '改进写法', exact: true })).toBeVisible();
  await page.goto('catalog/browse/?lang=zh');
  await expect(page.locator('#pb-list > li')).toHaveCount(30);
  await expect(page.locator('#pb-list .english-name').first()).toHaveText(first.name_en);
  await expect(page.locator('.repository-filter')).not.toHaveAttribute('open');
  await page.locator('.repository-filter summary').click();
  await expect(page.locator('[data-facet=repo]')).toBeVisible();
  await page.locator('[data-facet=repo] button').first().click();
  await expect(page).toHaveURL(/repo=/);
  await expect(page.locator('[data-facet=repo] button').first()).toHaveAttribute('aria-pressed', 'true');
});
