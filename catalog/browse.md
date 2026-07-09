---
layout: default
title: "Browse Patterns · 模式浏览器"
permalink: /catalog/browse/
---

<div class="pb" id="pattern-browser" aria-live="polite">
  <div class="pb-topbar">
    <input type="search" id="pb-search" class="pb-search" autocomplete="off" spellcheck="false">
    <div class="pb-lang" id="pb-lang" role="group" aria-label="language">
      <button type="button" data-lang="en" class="is-active">EN</button>
      <button type="button" data-lang="zh">中文</button>
    </div>
  </div>
  <div class="pb-facets" id="pb-facets"></div>
  <div class="pb-count" id="pb-count"></div>
  <ul class="pb-list" id="pb-list"></ul>
  <p class="pb-empty" id="pb-empty" hidden></p>
  <noscript>
    JavaScript is required for the interactive browser.
    See the <a href="{{ '/catalog/catalog-index' | relative_url }}">full index</a>
    （中文：<a href="{{ '/catalog/catalog-index-zh' | relative_url }}">总索引</a>）.
  </noscript>
</div>

<script src="{{ '/assets/fuse.min.js' | relative_url }}"></script>
<script>window.PB_BASEURL = "{{ site.baseurl }}";</script>
<script src="{{ '/assets/catalog.js' | relative_url }}"></script>
