---
layout: post
title: "Pattern: Decision Trees Beat Prose in AI Prompts"
date: 2026-04-19
categories: [patterns, decision-tree]
---

Tell an AI what to do in plain paragraphs and it usually gets it right. But the moment the logic branches — "if X then Y, otherwise Z" — those prose prompts start giving you **different outputs on every run**, even when you feed in exactly the same input.

**Decision trees fix this.** Swap the prose branching for a visual tree, and the model follows it the same way every time.

---

## The Problem

Take an incident response system. The AI has to triage incidents, assign responders, choose mitigation actions, and hand back a structured plan. The rules get complicated fast: 4 severity levels, 6 root cause categories, tier-based responder assignment, escalation conditions, and communication deadlines.

We wrote two prompts for the same job — one as prose paragraphs (~140 lines), one as decision trees (~260 lines) — and ran each one **20 times** on identical input with `claude -p`.

## Results (20 Runs Each)

### Primary Mitigation Action

| Prose | Decision Tree |
|-------|--------------|
| **15 unique phrasings** out of 20 runs | **1 phrasing** out of 20 runs |

Here's what the prose produced — a different answer every time:

```
Run 1:  "Enable graceful degradation on Cosmos DB (cached responses, reduced functionality) while investigating root cause"
Run 2:  "Enable graceful degradation on Cosmos DB (cached responses, reduced functionality for non-critical read paths)"
Run 3:  "Enable graceful degradation mode on Cosmos DB East US 2"
Run 4:  "Enable graceful degradation on Cosmos DB East US 2 to serve cached/reduced-functionality responses while..."
...15 unique variants total
```

And the decision tree — the same answer, all 20 times:

```
Run 1-20:  "enable_graceful_degradation"
```

### Secondary Action

| Prose | Decision Tree |
|-------|--------------|
| **20 unique phrasings** (zero repeats) | **2 variants** (19× `hotfix`, 1× `failover_to_secondary`) |

Prose managed **0% reproducibility** on secondary actions. Every single run came back with a unique sentence.

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

Both approaches actually made the **same correct decisions** — SEV2, enable graceful degradation, assign 4 responders. What sets them apart is **output determinism**.

Say your downstream code does this:

```python
if response["mitigation_plan"]["primary_action"]["action"] == "enable_graceful_degradation":
    execute_graceful_degradation()
```

- **Decision tree prompt**: works all 20 times
- **Prose prompt**: works **0 times out of 20** — the action is a free-form sentence, so it never matches

And this isn't some theoretical worry. Any system that parses AI output — automation pipelines, agent orchestration, tool calling — breaks the moment the output format stops being predictable.

## The Pattern

Here's the core idea. Take something like this:

```
If the root cause is a bad deployment and the service supports instant 
rollback, always prefer rollback over other mitigations because it restores 
the last known good state with minimal risk. If the root cause is a bad 
deployment but rollback is not available, then consider feature flag 
disablement if the change is behind a feature flag. If no feature flag 
exists, proceed with hotfix.
```

And turn it into this:

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

Same logic, either way. But the tree hands the model an **exact string to output** at each leaf, and the indentation lays out the decision path visually.

## Why It Works

1. **It narrows attention at each step.** The model works through one condition at a time instead of juggling every rule at once.
2. **It hands over the exact output text.** Each leaf holds the literal action string, so the model just copies it rather than writing a fresh sentence.
3. **It encodes the hierarchy spatially.** The whitespace indentation carries the parent-child relationships — a pattern LLMs picked up from millions of code files, YAML configs, and directory trees while training.

## When to Use / When Not To

**Reach for decision trees when:**
- Your prompt has branching logic (if/else, switch/case)
- Code parses the output (JSON fields, action names, status values)
- You need the same result across multiple runs
- You're building agent orchestration or automation pipelines

**Skip them when:**
- The task is open-ended creative work, where variety is the point
- There's no branching logic to begin with
- Only humans read the output, so different phrasing doesn't matter

## Try It Yourself

Clone the repo and run:

```bash
cd eval/decision-tree-ab
bash run.sh 20           # 20 runs, default model
bash run.sh 10 haiku     # 10 runs, haiku model
python3 analyze.py       # analyze results
```

It comes with three scenarios: simple (deployment controller), ambiguous (unknown server status), and complex (incident response with 200+ line prompts).

## Further Reading

- [Anthropic: Prompt Engineering Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)
- [Anthropic: Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
