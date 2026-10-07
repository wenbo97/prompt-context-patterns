import test from 'node:test';
import assert from 'node:assert/strict';
import { contentDate, shanghaiDate, validateContentDate, validatePatternDates } from '../scripts/catalog/content-metadata.mjs';

const body = date => `---\nlang: en\nlast_modified_at: ${date}\n---\n\n## Use case\n\nRead the inputs.`;

test('content dates come from front matter rather than teaching material', () => {
  assert.equal(contentDate(body('2026-10-06')), '2026-10-06');
  assert.equal(contentDate('---\nlang: en\n---\n\nlast_modified_at: 2026-10-06'), null);
  assert.deepEqual(validateContentDate(body('2026-10-06'), '2026-10-06'), []);
  assert.ok(validateContentDate(body('2026-02-30'), '2026-10-06').length);
  assert.ok(validateContentDate(body('2026-10-07'), '2026-10-06').length);
  assert.ok(validateContentDate(body('2026-10-06T12:00:00Z'), '2026-10-06').length);
  assert.equal(shanghaiDate(new Date('2026-10-06T16:01:00Z')), '2026-10-07');
});

test('sitemap dates match each authored language and reject build-time fallback', () => {
  const prefix = 'https://example.test/handbook';
  const patterns = [{ id: 1, status: 'active' }, { id: 2, status: 'merged' }];
  const readBody = (_, lang) => body(lang === 'en' ? '2026-10-05' : '2026-10-06');
  const xml = `<urlset><url><loc>${prefix}/catalog/patterns/1/</loc><lastmod>2026-10-05T00:00:00+08:00</lastmod></url>
    <url><loc>${prefix}/catalog/patterns/1-zh/</loc><lastmod>2026-10-06T00:00:00+08:00</lastmod></url></urlset>`;
  assert.deepEqual(validatePatternDates(patterns, readBody, xml, prefix), []);
  assert.equal(validatePatternDates(patterns, readBody, xml.replace('2026-10-05T', '2026-10-07T'), prefix).length, 1);
  assert.equal(validatePatternDates(patterns, readBody, xml.replace(/<lastmod>.*?<\/lastmod>/g, ''), prefix).length, 2);
});
