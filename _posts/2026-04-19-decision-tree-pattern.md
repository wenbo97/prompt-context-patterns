---
layout: post
title: "Pattern: Decision Trees Beat Prose in AI Prompts"
date: 2026-04-19
categories: [patterns, decision-tree]
---

When you tell an AI what to do using natural language paragraphs, it works — most of the time. But when the logic has branches ("if X then Y, otherwise Z"), prose prompts produce **inconsistent outputs across runs** — even when the input is identical.

**Decision trees fix this.** Replace prose branching logic with a visual tree structure, and the model follows it deterministically.

---

## The Problem

Consider an incident response system. The AI must triage incidents, assign responders, choose mitigation actions, and produce a structured plan. The rules are complex: 4 severity levels, 6 root cause categories, tier-based responder assignment, escalation conditions, communication deadlines.

We wrote two prompts for the same task — one as prose paragraphs (~140 lines), one as decision trees (~260 lines) — and ran each **20 times** with identical input using `claude -p`.

## Results (20 Runs Each)

### Primary Mitigation Action

| Prose | Decision Tree |
|-------|--------------|
| **15 unique phrasings** out of 20 runs | **1 phrasing** out of 20 runs |

Prose outputs looked like this — every run different:

```
Run 1:  "Enable graceful degradation on Cosmos DB (cached responses, reduced functionality) while investigating root cause"
Run 2:  "Enable graceful degradation on Cosmos DB (cached responses, reduced functionality for non-critical read paths)"
Run 3:  "Enable graceful degradation mode on Cosmos DB East US 2"
Run 4:  "Enable graceful degradation on Cosmos DB East US 2 to serve cached/reduced-functionality responses while..."
...15 unique variants total
```

Decision tree — every run identical:

```
Run 1-20:  "enable_graceful_degradation"
```

### Secondary Action

| Prose | Decision Tree |
|-------|--------------|
| **20 unique phrasings** (zero repeats) | **2 variants** (19× `hotfix`, 1× `failover_to_secondary`) |

Prose achieved **0% reproducibility** on secondary actions. Every single run produced a unique sentence.

### Full Comparison Table

| Dimension | Prose (20 runs) | Decision Tree (20 runs) |
|-----------|----------------|------------------------|
| Severity classification | 20/20 SEV2 | 20/20 SEV2 |
| Primary action (unique values) | **15** | **1** |
| Secondary action (unique values) | **20** | **2** |
| Responder role sets | 2 variants (capitalization: `on-call` vs `On-Call`) | 1 (consistent) |
| Actions-to-avoid count | inconsistent (16× two items, 4× three items) | consistent (20× two items) |
| Escalation triggers | 3/3 consistent | 3/3 consistent |

## What This Means in Practice

Both approaches made the **same correct decisions** — SEV2, enable graceful degradation, assign 4 responders. The difference is **output determinism**.

If your downstream code does:

```python
if response["mitigation_plan"]["primary_action"]["action"] == "enable_graceful_degradation":
    execute_graceful_degradation()
```

- **Decision tree prompt**: works 20/20 times
- **Prose prompt**: works **0/20 times** (action is a free-form sentence, never matches)

This isn't a theoretical problem. Any system that parses AI output — automation pipelines, agent orchestration, tool calling — breaks when the output format is unpredictable.

## The Pattern

Here's the core idea. Replace this:

```
If the root cause is a bad deployment and the service supports instant 
rollback, always prefer rollback over other mitigations because it restores 
the last known good state with minimal risk. If the root cause is a bad 
deployment but rollback is not available, then consider feature flag 
disablement if the change is behind a feature flag. If no feature flag 
exists, proceed with hotfix.
```

With this:

```
Root cause category?
├─ Bad deployment
│   └─ Service supports instant rollback?
│       ├─ YES → action: "rollback"
│       └─ NO
│           └─ Change behind feature flag?
│               ├─ YES → action: "disable_feature_flag"
│               └─ NO  → action: "hotfix"
```

Same logic. The tree version gives the model an **exact string to output** at each leaf node, and the indentation encodes the decision path spatially.

## Why It Works

1. **Narrows attention at each step.** The model evaluates one condition at a time instead of holding all rules in attention simultaneously.
2. **Provides exact output text.** Leaf nodes contain the literal action string — the model copies it rather than composing a new sentence.
3. **Encodes hierarchy spatially.** Indentation tokens (whitespace) encode parent-child relationships. LLMs learned this pattern from millions of code files, YAML configs, and directory trees during training.

## When to Use / When Not To

**Use decision trees when:**
- Your prompt has branching logic (if/else, switch/case)
- Output is parsed by code (JSON fields, action names, status values)
- You need consistency across multiple runs
- You're building agent orchestration or automation pipelines

**Skip decision trees when:**
- The task is open-ended creative work (variation is desirable)
- There's no branching logic
- Output is read by humans only (phrasing variation doesn't matter)

## Try It Yourself

Clone the repo and run:

```bash
cd eval/decision-tree-ab
bash run.sh 20           # 20 runs, default model
bash run.sh 10 haiku     # 10 runs, haiku model
python3 analyze.py       # analyze results
```

Three scenarios are included: simple (deployment controller), ambiguous (unknown server status), and complex (incident response with 200+ line prompts).

## Further Reading

- [Anthropic: Prompt Engineering Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)
- [Anthropic: Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
