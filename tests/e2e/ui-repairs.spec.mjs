import { test, expect } from '@playwright/test';
import fs from 'node:fs';

const patterns = JSON.parse(fs.readFileSync('_data/patterns.json', 'utf8'));
const active = patterns.filter(pattern => pattern.status === 'active');
const base = 'http://127.0.0.1:4000/prompt-context-patterns/';
const titleOf = file => /^title:\s*(.+)$/m.exec(fs.readFileSync(file, 'utf8'))[1].trim().replace(/^["']|["']$/g, '');
const center = async locator => {
  await locator.scrollIntoViewIfNeeded();
  const box = await locator.boundingBox();
  return { x: box.x + box.width / 2, y: box.y + box.height / 2 };
};

test('ordinary pages retain their own titles and metadata instead of P1', async ({ page, request }) => {
  const pages = [
    ['', 'index.md'], ['index-zh/', 'index-zh.md'],
    ['catalog/', 'catalog/index.md'], ['catalog/index-zh/', 'catalog/index-zh.md'],
    ['topics/prompt/', 'topics/prompt.md'], ['topics/prompt-zh/', 'topics/prompt-zh.md'],
    ['sources/', 'sources/index.md'], ['sources-zh/', 'sources/index-zh.md'],
    ['methodology/', 'methodology/index.md'], ['methodology-zh/', 'methodology/index-zh.md'],
    ['blog/', 'blog.md'], ['blog-zh/', 'blog-zh.md'],
    ['catalog/catalog-index/', 'catalog/catalog-index.md'], ['catalog/catalog-index-zh/', 'catalog/catalog-index-zh.md'],
    ['guides/reference-reading/', 'guides/reference-reading.md'], ['guides/reference-reading-zh/', 'guides/reference-reading-zh.md'],
  ];
  for (const file of fs.readdirSync('_posts').filter(file => file.endsWith('.md'))) {
    const [year, month, day, ...slug] = file.replace(/\.md$/, '').split('-');
    pages.push([`${year}/${month}/${day}/${slug.join('-')}/`, `_posts/${file}`]);
  }
  for (const [route, file] of pages) {
    await page.goto(route);
    const title = titleOf(file);
    await expect(page).toHaveTitle(`${title} | Prompt & Context Patterns`);
    await expect(page.locator('meta[property="og:title"]')).toHaveAttribute('content', title);
    const description = await page.locator('meta[name="description"]').getAttribute('content');
    expect(description).not.toBe(patterns[0].summary_en);
    expect(description).not.toBe(patterns[0].summary_zh);
    await expect(page.locator('meta[property="og:description"]')).toHaveAttribute('content', description);
  }
  const html = await (await request.get(`${base}catalog/browse/`)).text();
  expect(html).toContain('<title>Browse patterns | Prompt &amp; Context Patterns</title>');
  for (const lang of ['en', 'zh']) {
    const p = active.find(pattern => pattern.id === 25);
    await page.goto(`catalog/patterns/25${lang === 'zh' ? '-zh' : ''}/`);
    await expect(page).toHaveTitle(`${p[`name_${lang}`]} | Prompt & Context Patterns`);
    await expect(page.locator('meta[name="description"]')).toHaveAttribute('content', p[`summary_${lang}`]);
  }
});

test('all English index titles have continuous hit areas at 768px', async ({ page }) => {
  await page.setViewportSize({ width: 768, height: 900 });
  await page.goto('catalog/catalog-index/');
  await page.evaluate(() => document.fonts.ready);
  const titles = page.locator('.complete-index tbody tr td:nth-child(2) > a');
  await expect(titles).toHaveCount(active.length);
  const misses = await titles.evaluateAll(anchors => anchors.flatMap(anchor => {
    anchor.scrollIntoView({ block: 'center' });
    const box = anchor.getBoundingClientRect();
    const hit = document.elementFromPoint(box.x + box.width / 2, box.y + box.height / 2);
    return hit?.closest('a') === anchor ? [] : [{ title: anchor.textContent, hit: hit?.tagName }];
  }));
  expect(misses).toEqual([]);
  const p60 = titles.filter({ hasText: 'Tiered Permission Model (RED/DEFER/GREEN)' });
  const point = await center(p60);
  await page.mouse.click(point.x, point.y);
  await expect(page).toHaveURL(/catalog\/patterns\/60\//);
});

test('wrapped guide references open by their center and by keyboard', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 900 });
  for (const keyboard of [false, true]) {
    await page.goto('guides/reference-reading-zh/');
    const link = page.getByRole('link', { name: '用证据支撑结论', exact: true });
    if (keyboard) { await link.focus(); await page.keyboard.press('Enter'); }
    else { const point = await center(link); await page.mouse.click(point.x, point.y); }
    await expect(page).toHaveURL(/catalog\/patterns\/26-zh\//);
  }
});

test('current topic tags are inert while mixed-list category links navigate', async ({ page }) => {
  await page.goto('topics/prompt-zh/');
  await expect(page.locator('.pattern-card .category-tag')).toHaveCount(active.filter(pattern => pattern.category === 'prompt').length);
  await expect(page.locator('.pattern-card .meta-line a')).toHaveCount(0);
  const tag = page.locator('.category-tag').first();
  const point = await center(tag);
  await page.mouse.click(point.x, point.y);
  await expect(page).toHaveURL(/topics\/prompt-zh\//);
  await expect(tag).not.toHaveAttribute('tabindex');
  await page.goto('index-zh/');
  await page.locator('.pattern-card .meta-line a').first().click();
  await expect(page).toHaveURL(/topics\/skill-authoring-zh\//);
  await page.goto('catalog/browse/?lang=zh');
  await page.locator('#pb-list .meta-line a').first().click();
  await expect(page).toHaveURL(/topics\/skill-authoring-zh\//);
});

test('source titles and pinned evidence open new tabs without replacing the reading page', async ({ page, context }) => {
  await context.route('https://github.com/**', route => route.fulfill({ contentType: 'text/html', body: '<title>Reference target</title>' }));
  await page.setViewportSize({ width: 768, height: 900 });
  for (const repo of ['multica-ai/andrej-karpathy-skills', 'nextlevelbuilder/ui-ux-pro-max-skill']) {
    await page.goto('sources-zh/');
    const link = page.locator('.source-card h2 a').filter({ hasText: repo });
    const href = await link.getAttribute('href');
    const point = await center(link);
    const popupPromise = page.waitForEvent('popup');
    await page.mouse.click(point.x, point.y);
    const popup = await popupPromise;
    await expect(popup).toHaveURL(href);
    await expect(page).toHaveURL(/sources-zh\//);
    await popup.close();
  }
  await page.goto('catalog/patterns/1-zh/');
  for (const link of await page.locator('.evidence-panel li a').all()) {
    const href = await link.getAttribute('href');
    const popupPromise = page.waitForEvent('popup');
    await link.focus(); await page.keyboard.press('Enter');
    const popup = await popupPromise;
    await expect(popup).toHaveURL(href);
    await expect(page).toHaveURL(/catalog\/patterns\/1-zh\//);
    await expect(link).toHaveAttribute('rel', 'noopener noreferrer');
    await popup.close();
  }
});

test('source display labels remove Markdown without losing literal section names', async ({ page }) => {
  for (const id of [14, 25]) for (const suffix of ['', '-zh']) {
    await page.goto(`catalog/patterns/${id}${suffix}/`);
    const labels = await page.locator('.evidence-panel li > a:first-child').allTextContents();
    expect(labels.some(label => label.includes('Defining output formats'))).toBeTruthy();
    expect(labels.some(label => label.includes('**'))).toBeFalsy();
  }
  for (const suffix of ['', '-zh']) {
    await page.goto(`catalog/patterns/112${suffix}/`);
    await page.locator('.button').click();
    await expect(page).toHaveURL(new RegExp(`catalog/patterns/25${suffix}/`));
    await expect(page.locator('.evidence-panel li > a:first-child').first()).toContainText('Defining output formats');
  }
  await page.goto('catalog/patterns/8-zh/');
  await expect(page.locator('.evidence-panel li > a:first-child').first()).toContainText('<HARD-GATE>');
});

test('bad and good examples have explicit red and green markers without JavaScript', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 375, height: 900 } });
  const page = await context.newPage();
  for (const route of ['catalog/patterns/8-zh/', 'catalog/patterns/1/']) {
    await page.goto(base + route);
    for (const [kind, color] of [['bad', 'rgb(185, 28, 28)'], ['good', 'rgb(21, 128, 61)']]) {
      const block = page.locator(`pre.example--${kind}, .example--${kind} pre`);
      await expect(block).toHaveCount(1);
      await expect(block).toHaveCSS('border-left-color', color);
    }
    const external = page.locator('.evidence-panel li a').first();
    await expect(external).toHaveAttribute('target', '_blank');
    for (const link of await page.locator('.evidence-panel li a').all()) {
      await link.scrollIntoViewIfNeeded();
      expect(await link.evaluate(anchor => {
        const box = anchor.getBoundingClientRect();
        return document.elementFromPoint(box.x + box.width / 2, box.y + box.height / 2)?.closest('a') === anchor;
      })).toBeTruthy();
    }
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBeTruthy();
  }
  await context.close();
});

test('built pages preserve external-link policy and every bilingual example marker', () => {
  const siteOrigin = 'https://wenbo97.github.io';
  const misses = [];
  const inspect = directory => {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      const file = `${directory}/${entry.name}`;
      if (entry.isDirectory()) { inspect(file); continue; }
      if (!file.endsWith('.html')) continue;
      const html = fs.readFileSync(file, 'utf8');
      for (const match of html.matchAll(/<a\b([^>]*?)>/gi)) {
        const attributes = match[1];
        const href = /\bhref="([^"]+)"/i.exec(attributes)?.[1].replace(/&amp;/g, '&');
        if (!href) continue;
        const url = new URL(href, siteOrigin);
        if (!['http:', 'https:'].includes(url.protocol) || url.origin === siteOrigin) continue;
        const target = /\btarget="([^"]*)"/i.exec(attributes)?.[1];
        const rel = /\brel="([^"]*)"/i.exec(attributes)?.[1].split(/\s+/) || [];
        if (target !== '_blank' || !rel.includes('noopener') || !rel.includes('noreferrer')) misses.push({ file, href });
      }
    }
  };
  inspect('_site');
  expect(misses).toEqual([]);
  for (const p of active) for (const suffix of ['', '-zh']) {
    const html = fs.readFileSync(`_site/catalog/patterns/${p.id}${suffix}/index.html`, 'utf8');
    const classes = [...html.matchAll(/<(?:pre|div)\b[^>]*class="([^"]*)"/g)].flatMap(match => match[1].split(/\s+/));
    expect(classes, `P${p.id}${suffix} examples`).toContain('example--bad');
    expect(classes, `P${p.id}${suffix} examples`).toContain('example--good');
  }
});
