---
layout: post
title: "Decision-tree prompts: historical fixtures and limits"
date: 2026-04-19
categories: [patterns, decision-tree]
lang: en
last_modified_at: 2026-10-06
description: "Read the historical decision-tree instruction fixture and its known experimental evidence limits."
---

<span id="the-problem"></span>
<span id="results-20-runs-each"></span>
<span id="primary-mitigation-action"></span>
<span id="secondary-action"></span>
<span id="full-comparison-table"></span>
<span id="what-this-means-in-practice"></span>
<span id="the-pattern"></span>
<span id="why-it-works"></span>
<span id="when-to-use--when-not-to"></span>
<span id="try-it-yourself"></span>
<span id="further-reading"></span>

## Historical revision

This article retains its 2026-04-19 experiment context. The earlier report described repeated prose/tree runs, but the raw outputs are absent from this checkout. Its numerical reproducibility claims cannot be recomputed here and are not current evidence.

The two prompt forms also differed in their output vocabulary: the tree supplied fixed action strings while prose allowed free-form sentences. That confounds branch presentation with output-contract enforcement. A tree alone does not guarantee stable or correct model decisions.

## A teaching comparison

Task: choose an authorized action for a failed deployment.

Bad:

```text
Choose the best mitigation and explain it.
```

Good:

```text
If rollback is supported and authorized, propose action=rollback.
Otherwise, if an authorized feature flag disables the change, propose action=disable_flag.
Otherwise report action=investigate and the missing fact.
Return JSON with action and evidence. Do not execute a mitigation.
```

This construction makes the branches, unknown state and allowed output values inspectable. Check schema compliance separately from semantic decision accuracy.

## Reproduce a controlled experiment

The retained fixtures are in `eval/decision-tree-ab/`; its runner requires Claude Code CLI. Patternfoo is the maintained configurable evaluation tool. Running either tool is an explicit model experiment, not part of the static site checks.

A new comparison should hold facts, model configuration, output enums and budget constant; change only the branch representation. Report individual outcomes and failures, and retain raw outputs before making numerical claims.

[Workflow branching]({{ '/catalog/patterns/3/' | relative_url }}) · [Intent routing]({{ '/catalog/patterns/20/' | relative_url }}) · [Output contracts]({{ '/catalog/patterns/14/' | relative_url }})
