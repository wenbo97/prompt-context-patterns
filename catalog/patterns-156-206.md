---
layout: default
title: "Patterns 156–206 · 2026-07 Harvest"
permalink: /catalog/patterns-156-206/
---

# Patterns 156–206 · 2026-07 Harvest

The 51 patterns added in the 2026-07 harvest — from
[superpowers](https://github.com/obra/superpowers),
[claude-plugins-official](https://github.com/anthropics/claude-plugins-official),
and [mattpocock/skills](https://github.com/mattpocock/skills), including the new
**Skill Authoring** category. Full write-ups are in progress; this page is the
static, searchable index of names and problems.

Interactive version: [pattern browser]({{ site.baseurl }}/catalog/browse/) ·
Patterns 1–155: [catalog-index]({{ site.baseurl }}/catalog/catalog-index) ·
中文版：[模式 156–206]({{ site.baseurl }}/catalog/patterns-156-206-zh)

{% assign harvest = site.data.patterns | where_exp: "p", "p.id >= 156" %}
{% for p in harvest %}
## {{ p.id }}. {{ p.name_en }}

{{ p.problem_en }}

*Category: {{ p.category }} · Source: {{ p.source }} · Confidence: {{ p.confidence }}*
{% endfor %}
