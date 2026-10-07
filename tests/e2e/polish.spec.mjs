import { test, expect } from '@playwright/test';
import fs from 'node:fs';
import { base } from './site-settings.mjs';

test('stable three-digit IDs remain readable on both complete indexes at all widths', async ({ page }) => {
  for (const width of [375, 768, 1280]) {
    await page.setViewportSize({ width, height: 900 });
    for (const suffix of ['', '-zh']) {
      await page.goto(`catalog/catalog-index${suffix}/`);
      const wrapped = await page.locator('.complete-index tbody td:first-child').evaluateAll(cells => cells.filter(cell => {
        const range = document.createRange(); range.selectNodeContents(cell);
        return range.getBoundingClientRect().height > parseFloat(getComputedStyle(cell).lineHeight) + 1 || cell.scrollWidth > cell.clientWidth;
      }).map(cell => cell.textContent));
      expect(wrapped).toEqual([]);
    }
  }
});

test('wrapped native links include their line gaps in the hit area across reading and migration pages', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 900 });
  const cases = [
    ['blog-zh/', '.post-list h2 a'],
    ['catalog/catalog-index/', 'td:nth-child(3) a'],
    ['catalog/categories/patterns-open-source-skills-zh/', '.compat-list a'],
    ['2026/04/19/prompt-engineering-patterns/', '.lang-switch a']
  ];
  for (const [route, selector] of cases) {
    await page.goto(route, { waitUntil: 'domcontentloaded' });
    await page.evaluate(() => document.fonts.ready);
    const candidates = page.locator(selector);
    const longest = await candidates.evaluateAll(nodes => nodes.map((a, index) => ({ index, length: a.textContent.length })).sort((a, b) => b.length - a.length)[0].index);
    const anchor = candidates.nth(longest);
    await anchor.scrollIntoViewIfNeeded();
    const rect = await anchor.boundingBox();
    const href = await anchor.getAttribute('href');
    expect(await anchor.evaluate(a => { const b = a.getBoundingClientRect(); return document.elementFromPoint(b.x + b.width / 2, b.y + b.height / 2)?.closest('a') === a; })).toBeTruthy();
    const target = new URL(href, page.url()).href;
    await anchor.click({ position: { x: rect.width / 2, y: rect.height / 2 } });
    await expect(page).toHaveURL(target);
  }
});

test('Forward restores the same detail and combined filters keep their URL state', async ({ page }) => {
  await page.goto('catalog/browse/?lang=zh&limit=60');
  await expect(page.locator('#pb-list > li')).toHaveCount(60);
  await page.locator('#pb-list h2 a').first().click();
  const detail = page.url();
  await page.goBack();
  await expect(page.locator('#pb-list > li')).toHaveCount(60);
  await expect(page).toHaveURL(/limit=60/);
  await page.goForward();
  await expect(page).toHaveURL(detail);
  await page.goBack();
  await page.locator('[data-facet=category] [data-value=context]').click();
  await page.locator('.repository-filter summary').click();
  await page.locator('[data-facet=repo] [data-value="anthropics/skills"]').click();
  const matches = JSON.parse(fs.readFileSync('_data/patterns.json', 'utf8')).filter(p => p.status === 'active' && p.category === 'context' && p.sources.some(s => s.repo === 'anthropics/skills'));
  await expect(page.locator('#pb-list > li')).toHaveCount(matches.length);
  await expect(page).toHaveURL(/category=context/);
  await expect(page).toHaveURL(/repo=anthropics%2Fskills/);
  await page.locator('#clear-filters').click();
  await expect(page.locator('#pb-list > li')).toHaveCount(30);
  await expect(page).not.toHaveURL(/category=|repo=/);
});

test('legacy numbered subheadings retain their parent method and global headings return to the index', async ({ page, browser }) => {
  const route = 'catalog/categories/patterns-open-source-skills-zh/';
  await page.goto(route + '#5-步-eval-流程');
  await expect(page).toHaveURL(/\/catalog\/patterns\/119-zh\/$/);
  await page.goto(route + '#跨领域观察');
  await expect(page).toHaveURL(/\/catalog\/index-zh\/$/);
  const context = await browser.newContext({ javaScriptEnabled: false });
  const staticPage = await context.newPage();
  await staticPage.goto(base + route);
  await expect(staticPage.locator('[id="5-步-eval-流程"] a')).toHaveAttribute('href', /\/patterns\/119-zh\/$/);
  await expect(staticPage.locator('[id="跨领域观察"] a')).toHaveAttribute('href', /\/catalog\/index-zh\/$/);
  await context.close();
});

test('detail navigation uses existing bilingual anchors and stays usable on narrow screens', async ({ page }) => {
  for (const width of [375, 768, 1280]) {
    await page.setViewportSize({ width, height: 900 });
    for (const lang of ['en', 'zh']) {
      await page.goto(`catalog/patterns/224${lang === 'zh' ? '-zh' : ''}/`);
      const navigation = page.getByRole('navigation', { name: lang === 'zh' ? '本页导航' : 'On this page' });
      await expect(navigation.getByRole('link')).toHaveCount(7);
      for (const link of await navigation.getByRole('link').all()) {
        const href = await link.getAttribute('href');
        await link.click();
        expect(decodeURIComponent(new URL(page.url()).hash)).toBe(href);
        await expect(page.locator(`[id="${href.slice(1)}"]`)).toBeInViewport();
      }
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBeTruthy();
    }
  }
});

test('detail navigation remains native when JavaScript is disabled', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 375, height: 900 } });
  const page = await context.newPage();
  await page.goto(base + 'catalog/patterns/23-zh/');
  await page.getByRole('navigation', { name: '本页导航' }).getByRole('link', { name: '验证', exact: true }).press('Enter');
  await expect(page.locator('[id="如何验证"]')).toBeInViewport();
  await context.close();
});
