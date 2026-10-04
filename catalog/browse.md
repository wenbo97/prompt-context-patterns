---
layout: default
title: Browse patterns
permalink: /catalog/browse/
alternate_url: /catalog/browse/?lang=zh
---
<div id="pattern-browser" data-baseurl="{{ site.baseurl }}">
  <span class="eyebrow" data-i18n-en="PATTERN CATALOG" data-i18n-zh="模式目录">PATTERN CATALOG</span><h1 id="browser-title">Find a method</h1><p id="browser-intro" class="lead">Search use cases in either language.</p>
  <div class="catalog-toolbar"><label class="search-label" id="search-label" for="pb-search">Search patterns and use cases</label><div class="search-row"><input id="pb-search" type="search" autocomplete="off" spellcheck="false"><button class="button secondary" id="clear-search" type="button">Clear search</button></div>
    <div class="meta-line" id="pb-lang" role="group" aria-label="Language"><button class="lang-button" type="button" data-lang="en" aria-pressed="true">English</button><button class="lang-button" type="button" data-lang="zh" aria-pressed="false">中文</button></div>
    <div id="pb-facets"></div>
  </div>
  <p id="pb-count" class="browser-status" role="status" aria-live="polite">Loading patterns…</p>
  <div class="browser-error" id="browser-error" hidden><p id="error-text"></p><button class="button" id="retry-load" type="button">Try again</button> <a id="static-index" href="{{ '/catalog/catalog-index/' | relative_url }}">Open the static index</a></div>
  <p id="pb-empty" class="browser-empty" hidden></p><ul class="browser-results" id="pb-list"></ul>
  <div class="browser-actions"><button class="button secondary" id="clear-filters" type="button">Clear filters</button><button class="button" id="load-more" type="button" hidden>Load30 more</button></div>
  <noscript><p>This interactive view needs JavaScript. <a href="{{ '/catalog/catalog-index/' | relative_url }}">Read the full static index</a> · <a href="{{ '/catalog/catalog-index-zh/' | relative_url }}">阅读中文静态总索引</a>。</p></noscript>
</div>
<script src="{{ '/assets/fuse.min.js' | relative_url }}"></script>
<script type="module" src="{{ '/assets/catalog.js' | relative_url }}"></script>
