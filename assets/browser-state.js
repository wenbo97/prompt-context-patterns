export function readState(href, rememberedLanguage = 'en') {
  const params = new URL(href).searchParams;
  const language = params.get('lang'); const requested = Number(params.get('limit'));
  return { q: params.get('q') ?? '', category: new Set(params.getAll('category')), repo: new Set(params.getAll('repo')),
    trace: new Set(params.getAll('trace')), lang: ['en', 'zh'].includes(language) ? language : rememberedLanguage === 'zh' ? 'zh' : 'en',
    limit: Number.isSafeInteger(requested) && requested >= 30 ? Math.floor(requested / 30) * 30 : 30 };
}
export function stateUrl(href, state) {
  const url = new URL(href); url.search = '';
  if (state.q) url.searchParams.set('q', state.q);
  for (const key of ['category', 'repo', 'trace']) for (const value of state[key]) url.searchParams.append(key, value);
  url.searchParams.set('lang', state.lang);
  if (state.limit > 30) url.searchParams.set('limit', String(state.limit));
  return url.href;
}
export function filterRows(rows, state, rankedRows = null) {
  const q = state.q.toLocaleLowerCase().trim();
  let matching = q && rankedRows ? rankedRows : [...rows].sort((a, b) => a.id - b.id);
  if (q && !rankedRows) matching = matching.filter(p => [p.name_en, p.name_zh, p.summary_en, p.summary_zh,
    p.scenario_en, p.scenario_zh, ...(p.tags ?? [])].some(text => String(text ?? '').toLocaleLowerCase().includes(q)));
  return matching.filter(p => (!state.category.size || state.category.has(p.category)) &&
    (!state.repo.size || (p.repos ?? []).some(repo => state.repo.has(repo))) && (!state.trace.size || state.trace.has(p.trace_status)));
}
