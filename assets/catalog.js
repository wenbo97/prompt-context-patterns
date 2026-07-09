/* Catalog pattern browser — vanilla JS + Fuse.js. Data: /assets/patterns.json */
(function () {
  'use strict';

  var BASE = window.PB_BASEURL || '';
  var LANG_KEY = 'pcp-lang';

  // --- label maps -----------------------------------------------------------
  var CAT = {
    'structural-scaffolding': ['Structural Scaffolding', '结构脚手架'],
    'execution-control': ['Execution Control', '执行控制'],
    'safety-and-trust': ['Safety & Trust', '安全与信任'],
    'input-output-contracts': ['I/O Contracts', '输入输出契约'],
    'agent-orchestration': ['Agent Orchestration', 'Agent 编排'],
    'knowledge-and-context': ['Knowledge & Context', '知识与上下文'],
    'quality-and-feedback': ['Quality & Feedback', '质量与反馈'],
    'advanced-orchestration': ['Advanced Orchestration', '高级编排'],
    'advanced-quality': ['Advanced Quality', '高级质量'],
    'advanced-safety': ['Advanced Safety', '高级安全'],
    'advanced-workflow': ['Advanced Workflow', '高级工作流'],
    'advanced-io-domain': ['Advanced I/O & Domain', '高级 I/O'],
    'gap-fills': ['Gap Fills', '补充模式'],
    'open-source-skills': ['Open-Source Skills', '开源技能'],
    'claude-code-platform': ['Claude Code Platform', 'Claude Code 平台'],
    'skill-authoring': ['Skill Authoring', '技能创作']
  };
  var SRC = {
    '500plus': ['500+ plugins', '500+ 插件'],
    'open-source': ['Open-source skills', '开源技能'],
    'claude-code': ['Claude Code', 'Claude Code'],
    'superpowers': ['superpowers', 'superpowers'],
    'claude-plugins-official': ['claude-plugins-official', 'claude-plugins-official'],
    'mattpocock': ['mattpocock/skills', 'mattpocock/skills']
  };
  var CONF = { high: ['High', '高'], medium: ['Medium', '中'], low: ['Low', '低'] };

  var T = {
    en: { search: 'Search patterns…', category: 'Category', source: 'Source', confidence: 'Confidence',
          count: function (s, t) { return s + ' of ' + t + ' patterns'; }, empty: 'No patterns match.',
          detail: 'detail →', pending: 'write-up pending', clear: 'clear' },
    zh: { search: '搜索模式…', category: '分类', source: '来源', confidence: '置信度',
          count: function (s, t) { return t + ' 个模式 · 显示 ' + s + ' 个'; }, empty: '没有匹配的模式。',
          detail: '详情 →', pending: '正文待补', clear: '清除' }
  };

  // --- state -----------------------------------------------------------------
  var lang = localStorage.getItem(LANG_KEY) === 'zh' ? 'zh' : 'en';
  var data = [], fuse = null;
  var sel = { category: new Set(), source: new Set(), confidence: new Set() };
  var query = '';

  var $search = document.getElementById('pb-search');
  var $facets = document.getElementById('pb-facets');
  var $count = document.getElementById('pb-count');
  var $list = document.getElementById('pb-list');
  var $empty = document.getElementById('pb-empty');
  var $lang = document.getElementById('pb-lang');

  function label(map, key) { var e = map[key]; return e ? e[lang === 'zh' ? 1 : 0] : key; }
  function nameOf(p) { return lang === 'zh' ? p.name_zh : p.name_en; }
  function problemOf(p) { return lang === 'zh' ? p.problem_zh : p.problem_en; }
  function detailOf(p) { return lang === 'zh' ? p.detail_zh : p.detail_en; }

  // --- data load -------------------------------------------------------------
  fetch(BASE + '/assets/patterns.json')
    .then(function (r) { return r.json(); })
    .then(function (rows) {
      data = rows;
      fuse = new Fuse(rows, {
        keys: [
          { name: 'name_en', weight: 2 }, { name: 'name_zh', weight: 2 },
          'problem_en', 'problem_zh'
        ],
        threshold: 0.35, ignoreLocation: true, minMatchCharLength: 2
      });
      applyStaticText();
      renderFacets();
      render();
    })
    .catch(function () { $empty.hidden = false; $empty.textContent = 'Failed to load patterns.json'; });

  // --- facets ----------------------------------------------------------------
  function counts(field) {
    var m = {};
    data.forEach(function (p) { if (p[field]) m[p[field]] = (m[p[field]] || 0) + 1; });
    return m;
  }
  // desired display order for categories = the map's insertion order
  function orderedKeys(map, present) {
    return Object.keys(map).filter(function (k) { return present[k]; });
  }

  function renderFacets() {
    $facets.innerHTML = '';
    groupEl('category', CAT, orderedKeys(CAT, counts('category')), counts('category'));
    groupEl('source', SRC, orderedKeys(SRC, counts('source')), counts('source'));
    groupEl('confidence', CONF, ['high', 'medium'], counts('confidence'));
  }

  function groupEl(field, labelMap, keys, cnt) {
    var wrap = document.createElement('div');
    wrap.className = 'pb-facet-group';
    var h = document.createElement('span');
    h.className = 'pb-facet-label';
    h.textContent = T[lang][field];
    wrap.appendChild(h);
    keys.forEach(function (k) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'pb-chip' + (sel[field].has(k) ? ' is-on' : '');
      b.dataset.field = field; b.dataset.key = k;
      b.innerHTML = '<span>' + escapeHtml(label(labelMap, k)) + '</span><i>' + (cnt[k] || 0) + '</i>';
      b.addEventListener('click', function () {
        sel[field].has(k) ? sel[field].delete(k) : sel[field].add(k);
        b.classList.toggle('is-on');
        render();
      });
      wrap.appendChild(b);
    });
    $facets.appendChild(wrap);
  }

  // --- filter + search + render ---------------------------------------------
  function passesFacets(p) {
    for (var f in sel) {
      if (sel[f].size && !sel[f].has(p[f])) return false;
    }
    return true;
  }

  function render() {
    var rows;
    if (query && fuse) {
      rows = fuse.search(query).map(function (r) { return r.item; }).filter(passesFacets);
    } else {
      rows = data.filter(passesFacets);
    }
    $count.textContent = T[lang].count(rows.length, data.length);
    $list.innerHTML = '';
    $empty.hidden = rows.length > 0;
    if (!rows.length) { $empty.textContent = T[lang].empty; return; }

    var frag = document.createDocumentFragment();
    rows.forEach(function (p) { frag.appendChild(card(p)); });
    $list.appendChild(frag);
  }

  function card(p) {
    var li = document.createElement('li');
    var det = detailOf(p);
    li.className = 'pb-card' + (det ? ' pb-card--link' : '');
    if (det) li.dataset.detail = det;
    var detHtml = det
      ? '<a class="pb-detail" href="' + escapeAttr(det) + '">' + T[lang].detail + '</a>'
      : '<span class="pb-detail pb-pending">' + T[lang].pending + '</span>';
    li.innerHTML =
      '<div class="pb-card-head"><span class="pb-id">#' + p.id + '</span>' +
      '<span class="pb-name">' + escapeHtml(nameOf(p)) + '</span></div>' +
      '<div class="pb-meta">' +
        '<span class="pb-tag pb-cat">' + escapeHtml(label(CAT, p.category)) + '</span>' +
        '<span class="pb-tag pb-src">' + escapeHtml(label(SRC, p.source)) + '</span>' +
        (p.confidence ? '<span class="pb-tag pb-conf pb-conf-' + p.confidence + '">' +
          escapeHtml(label(CONF, p.confidence)) + '</span>' : '') +
      '</div>' +
      '<p class="pb-problem">' + escapeHtml(problemOf(p) || '') + '</p>' +
      detHtml;
    return li;
  }

  // --- static text + language toggle ----------------------------------------
  function applyStaticText() {
    $search.placeholder = T[lang].search;
    document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';
  }

  $search.addEventListener('input', function () { query = this.value.trim(); render(); });

  // Whole card is clickable → jump to its detail page (patterns without a
  // write-up have no data-detail and stay inert). Real inner links keep working.
  $list.addEventListener('click', function (e) {
    if (e.target.closest('a')) return;
    var c = e.target.closest('.pb-card');
    if (c && c.dataset.detail) window.location.href = c.dataset.detail;
  });

  $lang.addEventListener('click', function (e) {
    var btn = e.target.closest('button[data-lang]');
    if (!btn) return;
    lang = btn.dataset.lang;
    localStorage.setItem(LANG_KEY, lang);
    Array.prototype.forEach.call($lang.children, function (b) {
      b.classList.toggle('is-active', b.dataset.lang === lang);
    });
    applyStaticText();
    renderFacets();
    render();
  });

  // init lang button state from storage
  Array.prototype.forEach.call($lang.children, function (b) {
    b.classList.toggle('is-active', b.dataset.lang === lang);
  });

  // --- helpers ---------------------------------------------------------------
  function escapeHtml(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
  function escapeAttr(s) { return escapeHtml(s).replace(/'/g, '&#39;'); }
})();
