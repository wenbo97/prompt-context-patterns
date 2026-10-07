export function contentDate(body) {
  const frontMatter = /^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/.exec(body)?.[1] ?? '';
  return /^last_modified_at:\s*["']?(\d{4}-\d{2}-\d{2})["']?\s*$/m.exec(frontMatter)?.[1] ?? null;
}

export function shanghaiDate(now = new Date()) {
  const parts = Object.fromEntries(new Intl.DateTimeFormat('en', {
    timeZone: 'Asia/Shanghai', year: 'numeric', month: '2-digit', day: '2-digit',
  }).formatToParts(now).map(part => [part.type, part.value]));
  return `${parts.year}-${parts.month}-${parts.day}`;
}

export function validateContentDate(body, today) {
  const date = contentDate(body);
  if (!date) return ['Missing or invalid last_modified_at date'];
  const parsed = new Date(date + 'T00:00:00Z');
  if (!Number.isFinite(parsed.getTime()) || parsed.toISOString().slice(0, 10) !== date)
    return ['Invalid calendar date in last_modified_at'];
  if (date > today) return ['last_modified_at is in the future'];
  return [];
}

export function sitemapDates(xml) {
  return new Map([...xml.matchAll(/<url>([\s\S]*?)<\/url>/g)].map(match => [
    /<loc>(.*?)<\/loc>/.exec(match[1])?.[1], /<lastmod>(.*?)<\/lastmod>/.exec(match[1])?.[1] ?? null,
  ]));
}

export function validatePatternDates(patterns, readBody, sitemap, prefix) {
  const dates = sitemapDates(sitemap);
  const errors = [];
  for (const pattern of patterns.filter(row => row.status === 'active')) for (const lang of ['en', 'zh']) {
    const expected = contentDate(readBody(pattern.id, lang));
    const url = `${prefix}/catalog/patterns/${pattern.id}${lang === 'zh' ? '-zh' : ''}/`;
    const actual = dates.get(url);
    if (!expected || !actual || actual.slice(0, 10) !== expected)
      errors.push(`Pattern content/sitemap date mismatch: P${pattern.id}/${lang}`);
  }
  return errors;
}
