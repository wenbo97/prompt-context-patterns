import test from 'node:test';
import assert from 'node:assert/strict';
import { readPage, validateSite } from '../scripts/catalog/site-output.mjs';

const origin = 'https://example.test';
const baseurl = '/handbook';
const en = origin + baseurl + '/';
const zh = origin + baseurl + '/zh/';
function page(url, lang, alternate) {
  return readPage(url, `<html lang="${lang}"><title>Handbook</title><meta name="description" content="Read &amp; check">
    <link rel="canonical" href="${url}"><link rel="alternate" hreflang="${lang}" href="${url}">
    <link rel="alternate" hreflang="${lang === 'en' ? 'zh-CN' : 'en'}" href="${alternate}"><h1>Handbook</h1><h2 id="steps">Steps</h2><a href="#steps">Steps</a></html>`);
}
const sitemap = `<urlset><url><loc>${en}</loc></url><url><loc>${zh}</loc></url></urlset>`;

test('built bilingual pages have canonical, reciprocal language pairs and sitemap coverage', () => {
  const pages = [page(en, 'en', zh), page(zh, 'zh-CN', en)];
  assert.deepEqual(validateSite(pages, sitemap, origin, baseurl), []);
  assert.equal(pages[0].description, 'Read & check');
  assert.equal(pages[0].anchors[0].href, '#steps');
});

test('migration checks reject local canonicals, noindex discovery and missing reciprocal links', () => {
  const pages = [page(en, 'en', zh), page(zh, 'zh-CN', en)];
  pages[0].canonical = 'http://127.0.0.1:4000/handbook/';
  pages[1].alternates = [];
  const errors = validateSite(pages, sitemap, origin, baseurl);
  assert.ok(errors.some(error => error.startsWith('Indexable canonical differs')));
  assert.ok(errors.some(error => error.startsWith('Hreflang is not reciprocal')));
  pages[1].noindex = true;
  assert.ok(validateSite(pages, sitemap, origin, baseurl).some(error => error.startsWith('Noindex page in sitemap')));
});

test('discovery checks reject duplicated, omitted and out-of-prefix sitemap entries', () => {
  const pages = [page(en, 'en', zh), page(zh, 'zh-CN', en)];
  const bad = `<urlset><loc>${en}</loc><loc>${en}</loc><loc>${origin}/other/</loc></urlset>`;
  const errors = validateSite(pages, bad, origin, baseurl);
  assert.ok(errors.includes('Duplicate sitemap URLs'));
  assert.ok(errors.some(error => error.startsWith('Indexable page missing')));
  assert.ok(errors.some(error => error.startsWith('Unexpected sitemap origin/path')));
});
