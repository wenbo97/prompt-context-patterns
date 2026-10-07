const decode = value => value.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;|&apos;/g, "'")
  .replace(/&#(\d+);/g, (_, number) => String.fromCodePoint(Number(number)))
  .replace(/&#x([\da-f]+);/gi, (_, number) => String.fromCodePoint(parseInt(number, 16)));

function attributes(tag) {
  return Object.fromEntries([...tag.matchAll(/([\w:-]+)\s*=\s*(?:"([^"]*)"|'([^']*)')/g)]
    .map(match => [match[1].toLowerCase(), decode(match[2] ?? match[3])]));
}

export function readPage(url, html) {
  const links = [...html.matchAll(/<link\b[^>]*>/gi)].map(match => attributes(match[0]));
  const meta = [...html.matchAll(/<meta\b[^>]*>/gi)].map(match => attributes(match[0]));
  const text = value => decode(value.replace(/<[^>]*>/g, '').trim());
  return {
    url, lang: attributes(/<html\b[^>]*>/i.exec(html)?.[0] ?? '').lang,
    title: text(/<title>([\s\S]*?)<\/title>/i.exec(html)?.[1] ?? ''),
    heading: text(/<h1\b[^>]*>([\s\S]*?)<\/h1>/i.exec(html)?.[1] ?? ''),
    noindex: meta.some(row => row.name === 'robots' && /\bnoindex\b/i.test(row.content)),
    canonical: links.find(row => row.rel === 'canonical')?.href,
    alternates: links.filter(row => row.rel === 'alternate' && row.hreflang),
    description: meta.find(row => row.name === 'description')?.content,
    ids: [...html.matchAll(/\bid\s*=\s*(?:"([^"]*)"|'([^']*)')/g)].map(match => decode(match[1] ?? match[2])),
    migration_targets: Object.fromEntries([...html.matchAll(/<li\b[^>]*>/gi)].map(match => attributes(match[0]))
      .filter(row => row.id && row['data-target']).map(row => [row.id, row['data-target']])),
    anchors: [...html.matchAll(/<a\b[^>]*>[\s\S]*?<\/a>/gi)].map((match, index) => ({
      index, ...attributes(match[0].slice(0, match[0].indexOf('>') + 1)), label: text(match[0])
    })).filter(row => row.href !== undefined)
  };
}

export function validateSite(pages, sitemap, origin, baseurl) {
  const errors = [];
  const urls = [...sitemap.matchAll(/<loc>([\s\S]*?)<\/loc>/g)].map(match => decode(match[1].trim()));
  const sitemapSet = new Set(urls);
  const byUrl = new Map(pages.map(page => [page.url, page]));
  for (const url of urls) {
    let parsed;
    try { parsed = new URL(url); } catch { errors.push(`Invalid sitemap URL: ${url}`); continue; }
    if (parsed.origin !== origin || !(parsed.pathname === baseurl || parsed.pathname.startsWith(baseurl + '/')) || parsed.search || parsed.hash)
      errors.push(`Unexpected sitemap origin/path: ${url}`);
    const page = byUrl.get(url);
    if (!page) errors.push(`Sitemap URL has no built page: ${url}`);
    else if (page.noindex) errors.push(`Noindex page in sitemap: ${url}`);
  }
  if (sitemapSet.size !== urls.length) errors.push('Duplicate sitemap URLs');
  for (const page of pages) {
    if (!page.title || !page.heading || !page.description) errors.push(`Missing title, heading or description: ${page.url}`);
    if (new Set(page.ids).size !== page.ids.length) errors.push(`Duplicate anchors: ${page.url}`);
    if (!page.noindex && !sitemapSet.has(page.url)) errors.push(`Indexable page missing from sitemap: ${page.url}`);
    if (!page.noindex && page.canonical !== page.url) errors.push(`Indexable canonical differs: ${page.url}`);
    if (!page.canonical || !byUrl.has(page.canonical)) errors.push(`Canonical target absent: ${page.url}`);
    if (page.noindex) continue;
    for (const alternate of page.alternates) {
      const other = byUrl.get(alternate.href);
      if (!other || other.noindex || other.lang !== alternate.hreflang) {
        errors.push(`Invalid hreflang target: ${page.url} -> ${alternate.href}`); continue;
      }
      if (!other.alternates.some(row => row.href === page.url && row.hreflang === page.lang))
        errors.push(`Hreflang is not reciprocal: ${page.url} -> ${alternate.href}`);
    }
  }
  return errors;
}
