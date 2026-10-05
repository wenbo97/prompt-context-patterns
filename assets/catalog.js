import { readState, stateUrl, filterRows } from './browser-state.js';
const host = document.getElementById('pattern-browser');
if (host) {
  const base = host.dataset.baseurl || '';
  const el = id => document.getElementById(id);
  const text = {
    en: { title: 'Find a method', intro: 'Search use cases in either language. Filter methods by theme, source repository and provenance.', search: 'Search patterns and use cases', clear: 'Clear search', reset: 'Clear filters',
      category: 'Theme', repo: 'Source repository', trace: 'Source status', traceable: 'Source instance located', untraced: 'Source unconfirmed', loading: 'Loading patterns…',
      error: 'Pattern data could not be loaded.', retry: 'Try again', static: 'Open the static index', empty: 'No active patterns are available.', noResults: 'No methods match these conditions.',
      count: (n,total,shown) => `${n} matching · ${shown} shown · ${total} active patterns`, more: 'Load 30 more', scenario: 'Use case', detail: 'Read method', english: 'English', chinese: '中文' },
    zh: { title: '搜索方法', intro: '输入想解决的问题，或搜索中英文术语。', search: '搜索名称、用途或英文术语', clear: '清除', reset: '重置筛选',
      category: '分类', repo: '来源仓库', trace: '原文', traceable: '有原文链接', untraced: '来源未确认', loading: '正在加载…',
      error: '目录加载失败，请重试或打开完整目录。', retry: '重新加载', static: '查看完整目录', empty: '当前没有可浏览的方法。', noResults: '没有找到相关方法。试试其他关键词，或重置筛选。',
      count: (n,total,shown) => n === total ? `${total} 个方法，已显示 ${shown} 个` : `找到 ${n} 个方法，已显示 ${shown} 个`, more: '再显示 30 个', scenario: '适用场景', detail: '查看详情', english: 'English', chinese: '中文' },
  };
  let remembered = 'en'; try { remembered = localStorage.getItem('pcp-language') || 'en'; } catch (_) {}
  let state = readState(location.href, remembered); let rows = []; let fuse = null; let request = 0; let composing = false; let available = false;
  const element = (tag, value, className) => { const node = document.createElement(tag); if (value != null) node.textContent = value; if (className) node.className = className; return node; };
  const t = () => text[state.lang];
  function commit(push = true) {
    const url = stateUrl(location.href, state); if (url !== location.href) history[push ? 'pushState' : 'replaceState'](null, '', url);
    try { localStorage.setItem('pcp-language', state.lang); } catch (_) {}
  }
  function localize() {
    document.documentElement.lang = state.lang === 'zh' ? 'zh-CN' : 'en'; document.title = `${t().title} | Prompt & Context Patterns`;
    document.querySelector('.site-nav').setAttribute('aria-label', state.lang === 'zh' ? '主要导航' : 'Main navigation');
    el('pb-lang').setAttribute('aria-label', state.lang === 'zh' ? '语言' : 'Language');
    for (const node of document.querySelectorAll('[data-i18n-en]')) {
      node.textContent = node.getAttribute(`data-i18n-${state.lang}`);
    }
    for (const node of document.querySelectorAll('[data-url-en]')) node.setAttribute('href', node.getAttribute(`data-url-${state.lang}`));
    const localeLink = document.querySelector('.locale-link');
    if (localeLink) { const other = { ...state, lang: state.lang === 'en' ? 'zh' : 'en' }; localeLink.href = stateUrl(location.href, other); localeLink.textContent = state.lang === 'en' ? '中文' : 'English'; }
    el('browser-title').textContent = t().title; el('browser-intro').textContent = t().intro;
    el('search-label').textContent = t().search; el('pb-search').placeholder = t().search;
    el('clear-search').textContent = t().clear; el('clear-filters').textContent = t().reset;
    el('load-more').textContent = t().more; el('retry-load').textContent = t().retry;
    el('static-index').textContent = t().static; el('static-index').href = base + `/catalog/catalog-index${state.lang === 'zh' ? '-zh' : ''}/`;
    for (const button of el('pb-lang').querySelectorAll('button')) button.setAttribute('aria-pressed', String(button.dataset.lang === state.lang));
    for (const group of el('pb-facets').querySelectorAll('fieldset')) {
      const key = group.dataset.facet; group.querySelector('legend').textContent = t()[key];
      for (const button of group.querySelectorAll('button')) {
        button.setAttribute('aria-pressed', String(state[key].has(button.dataset.value)));
        button.textContent = (key === 'category' ? button.getAttribute(`data-label-${state.lang}`) : key === 'trace' ? t()[button.dataset.value] : button.dataset.value) + ` (${button.dataset.count})`;
      }
    }
  }
  function buildFacets() {
    el('pb-facets').replaceChildren();
    for (const key of ['category', 'repo', 'trace']) {
      const counts = new Map(); const labels = new Map();
      for (const p of rows) for (const value of key === 'repo' ? p.repos : [key === 'trace' ? p.trace_status : p.category]) {
        counts.set(value, (counts.get(value) || 0) + 1); labels.set(value, [p.category_en || value, p.category_zh || value]);
      }
      const group = element('fieldset', null, 'filter-group'); group.dataset.facet = key; group.append(element('legend', t()[key]));
      const buttons = element('div', null, 'filter-options');
      for (const value of [...counts.keys()].sort()) {
        const button = element('button', null, 'filter-chip'); button.type = 'button'; button.dataset.value = value; button.dataset.count = counts.get(value);
        button.setAttribute('data-label-en', labels.get(value)[0]); button.setAttribute('data-label-zh', labels.get(value)[1]);
        button.addEventListener('click', () => { state[key].has(value) ? state[key].delete(value) : state[key].add(value); state.limit = 30; commit(); render(); }); buttons.append(button);
      }
      group.append(buttons);
      if (key === 'repo') {
        const disclosure = element('details', null, 'repository-filter'); disclosure.open = state.repo.size > 0;
        const summary = element('summary'); summary.setAttribute('data-i18n-en', 'Filter by source repository'); summary.setAttribute('data-i18n-zh', '按来源仓库筛选');
        disclosure.append(summary, group); el('pb-facets').append(disclosure);
      } else el('pb-facets').append(group);
    }
  }
  function render() {
    localize(); if (!available) return;
    const ranked = state.q.trim() && fuse ? fuse.search(state.q.trim()).map(result => result.item) : null;
    const results = filterRows(rows, state, ranked); const shown = results.slice(0, state.limit);
    el('pb-count').textContent = t().count(results.length, rows.length, shown.length);
    el('pb-empty').hidden = results.length > 0; el('pb-empty').textContent = rows.length ? t().noResults : t().empty;
    el('pb-list').replaceChildren();
    for (const p of shown) {
      const item = element('li', null, 'pattern-card'); item.append(element('span', `P${p.id}`, 'record-id'));
      const heading = element('h2'); const anchor = element('a', p[`name_${state.lang}`]); anchor.href = base + `/catalog/patterns/${p.id}${state.lang === 'zh' ? '-zh' : ''}/`; heading.append(anchor); item.append(heading);
      if (state.lang === 'zh') { const english = element('p', p.name_en, 'english-name'); english.lang = 'en'; item.append(english); }
      const meta = element('div', null, 'meta-line'); const category = element('a', p[`category_${state.lang}`] || p.category);
      category.href = base + `/topics/${p.category}${state.lang === 'zh' ? '-zh' : ''}/`; meta.append(category);
      if (p.trace_status === 'untraced') meta.append(element('span', t().untraced, 'badge untraced')); item.append(meta);
      item.append(element('p', p[`summary_${state.lang}`]));
      const scenario = element('p', `${t().scenario}: ${p[`scenario_${state.lang}`]}`, 'scenario'); item.append(scenario); el('pb-list').append(item);
    }
    el('load-more').hidden = shown.length >= results.length;
  }
  async function load() {
    const seq = ++request; const controller = new AbortController(); const timeout = setTimeout(() => controller.abort(), 15000);
    el('browser-error').hidden = true; el('pb-count').textContent = t().loading; localize();
    try {
      const response = await fetch(base + '/assets/patterns.json', { signal: controller.signal }); if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json(); if (!Array.isArray(data) || data.some(p => !Number.isInteger(p.id) || !Array.isArray(p.repos))) throw new Error('Invalid catalog data');
      if (seq !== request) return; rows = data; available = true;
      fuse = typeof window.Fuse === 'function' ? new window.Fuse(rows, { includeScore: true, threshold: .35, ignoreLocation: true,
        keys: ['name_en', 'name_zh', 'summary_en', 'summary_zh', 'scenario_en', 'scenario_zh', 'tags'] }) : null;
      buildFacets(); commit(false); render();
    } catch (_) {
      if (seq !== request) return; available = false; el('pb-count').textContent = ''; el('browser-error').hidden = false; el('error-text').textContent = t().error; localize();
    } finally { clearTimeout(timeout); }
  }
  el('pb-search').value = state.q;
  const search = () => { state.q = el('pb-search').value; state.limit = 30; commit(false); render(); };
  el('pb-search').addEventListener('compositionstart', () => { composing = true; });
  el('pb-search').addEventListener('compositionend', () => { composing = false; search(); });
  el('pb-search').addEventListener('input', () => { if (!composing) search(); });
  el('clear-search').addEventListener('click', () => { el('pb-search').value = ''; search(); el('pb-search').focus(); });
  el('clear-filters').addEventListener('click', () => { state.category.clear(); state.repo.clear(); state.trace.clear(); state.limit = 30; commit(); render(); });
  el('load-more').addEventListener('click', () => { state.limit += 30; commit(); render(); });
  el('retry-load').addEventListener('click', load);
  for (const button of el('pb-lang').querySelectorAll('button')) button.addEventListener('click', () => { state.lang = button.dataset.lang; commit(); render(); });
  window.addEventListener('popstate', () => { state = readState(location.href); el('pb-search').value = state.q; render(); });
  load();
}
