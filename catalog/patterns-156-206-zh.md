---
layout: default
title: "模式 156–206 · 2026-07 收割"
permalink: /catalog/patterns-156-206-zh/
lang: zh
---

# 模式 156–206 · 2026-07 收割

2026-07 收割新增的 51 个模式 —— 来自
[superpowers](https://github.com/obra/superpowers)、
[claude-plugins-official](https://github.com/anthropics/claude-plugins-official)、
[mattpocock/skills](https://github.com/mattpocock/skills)，含新增的**技能创作**分类。
完整长写法进行中；本页是名称与问题的静态可搜索索引。

交互版：[模式浏览器]({{ site.baseurl }}/catalog/browse/) ·
模式 1–155：[目录索引]({{ site.baseurl }}/catalog/catalog-index-zh) ·
English: [Patterns 156–206]({{ site.baseurl }}/catalog/patterns-156-206)

{% assign harvest = site.data.patterns | where_exp: "p", "p.id >= 156" %}
{% for p in harvest %}
## {{ p.id }}. {{ p.name_zh }}

{{ p.problem_zh }}

*分类：{{ p.category }} · 来源：{{ p.source }} · 置信度：{{ p.confidence }}*
{% endfor %}
