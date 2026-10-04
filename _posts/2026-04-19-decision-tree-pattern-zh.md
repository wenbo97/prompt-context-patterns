---
layout: post
title: "决策树提示词：历史样例与实验边界"
date: 2026-04-19
categories: [patterns, decision-tree]
lang: zh
last_modified_at: 2026-10-03
---

<span id="问题"></span>
<span id="结果各-20-次运行"></span>
<span id="主要缓解措施"></span>
<span id="次要措施"></span>
<span id="完整对比"></span>
<span id="这意味着什么"></span>
<span id="模式"></span>
<span id="为什么有效"></span>
<span id="什么时候用--什么时候不用"></span>
<span id="自己试试"></span>
<span id="延伸阅读"></span>

## 历史修订说明

保留本文2026-04-19的实验语境。旧报告描述了重复运行的 prose/tree 对比，但当前仓库没有原始输出，无法重新计算当时的数字；这些结论不作为当前效果证据。

两组提示词的输出词汇也不同：树形版本给出固定 action 字符串，散文版本允许自由句子。这混合了分支表示与输出契约两个变量。决策树本身不保证模型决策稳定或正确。

## 教学对照

任务：为失败部署选择一个已获授权的行动。

Bad：

```text
选择最好的缓解措施并解释。
```

Good：

```text
支持且授权回滚时，提出 action=rollback。
否则，如果授权的 feature flag 能禁用变更，提出 action=disable_flag。
否则，报告 action=investigate 及缺失的事实。
返回含 action 与 evidence 的 JSON，不执行缓解操作。
```

这个构造让分支、未知状态和输出枚举可检查。输出 schema 与语义判断准确性仍应分别验证。

## 复现受控实验

旧样例保留在 `eval/decision-tree-ab/`，运行器需要 Claude Code CLI。Patternfoo 是当前可配置的评测工具。运行模型实验须显式选择，不属于网站静态检查。

新的对比应固定事实、模型配置、输出枚举与预算，只改变分支表示方式。报告每次结果和失败，并保存原始输出后再提出数值主张。

[工作流分支]({{ '/catalog/patterns/3-zh/' | relative_url }}) · [意图路由]({{ '/catalog/patterns/20-zh/' | relative_url }}) · [输出契约]({{ '/catalog/patterns/14-zh/' | relative_url }})
