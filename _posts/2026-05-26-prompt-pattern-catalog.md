---
layout: post
title: "155 Prompt Patterns for AI Agent Development"
date: 2026-05-26
categories: [patterns, catalog]
---

This is a categorized catalog of 155 prompt engineering patterns, pulled from 500+ real-world AI agent plugins, open-source skill repositories, and the Claude Code system prompt. It's not theory — every pattern comes with a name, the problem it solves, and a concrete prompt snippet.

> **Updated 2026-05-26**: we harvested 13 new patterns (143–155) from `awesome-claude-skills`, `superpowers`, `andrej-karpathy-skills`, and `claude-plugins-official`, and refined 14 existing ones in place. See the [catalog index](/prompt-context-patterns/catalog/catalog-index) for the full list.

---

## Why This Exists

Most "awesome prompt" collections are aimed at ChatGPT users writing one-off queries. **This one is for developers building AI agents and multi-step plugins** — the setting where prompt stability, inter-skill coordination, and defensive patterns really matter.

To build it, we analyzed 500+ production plugins across DevOps automation, security analysis, code migration, incident response, deployment orchestration, and more. A pattern only made the cut if it showed up in at least 3 independent plugins.

---

## Catalog Structure

```
catalog/
├── catalog-index.md              ← Master index (all 155 patterns)
├── categories/                   ← Patterns grouped by function
│   ├── patterns-structural-scaffolding.md
│   ├── patterns-input-output-contracts.md
│   ├── patterns-execution-control.md
│   ├── patterns-knowledge-and-context.md
│   ├── patterns-agent-orchestration.md
│   ├── patterns-safety-and-trust.md
│   ├── patterns-quality-and-feedback.md
│   └── ... (18 files total)
├── techniques/                   ← Deep-dive guides
│   ├── token-level-techniques.md    ← 9 techniques grounded in entropy theory
│   ├── anti-laziness.md             ← 8 strategies to prevent agent shortcutting
│   ├── skill-architecture.md        ← Skill packaging and composition
│   ├── branching-stability.md       ← Branch logic reliability
│   ├── reference-skip-playbook.md   ← Force agents to read references
│   └── good-vs-bad-template.md      ← Side-by-side prompt comparison
└── standards/                    ← Review frameworks
    ├── quality-standards.md         ← P0/P1/P2 severity grading
    └── review-checklist.md          ← 9-dimension prompt review
```

---

## The 12 Pattern Categories

| # | Category | Patterns | What It Covers |
|---|----------|----------|----------------|
| 1 | Structural Scaffolding | 15 | Phase gates, decision trees, boundary tags |
| 2 | Input/Output Contracts | 12 | Schema enforcement, format locks, validation |
| 3 | Execution Control | 14 | Attempt limits, stop conditions, retry logic |
| 4 | Knowledge & Context | 12 | SSOT registries, on-demand loading, cache layers |
| 5 | Agent Orchestration | 11 | Sub-agent dispatch, parallel execution, handoffs |
| 6 | Safety & Trust | 10 | Guardrails, prohibited actions, escalation gates |
| 7 | Quality & Feedback | 9 | Self-review, evidence gates, confidence scoring |
| 8 | Advanced I/O & Domain | 10 | Domain routing, multi-modal, schema evolution |
| 9 | Advanced Orchestration | 8 | DAG execution, consensus, swarm patterns |
| 10 | Advanced Quality | 7 | Regression detection, drift monitoring |
| 11 | Advanced Safety | 8 | Data classification, audit trails, compliance |
| 12 | Advanced Workflow | 10 | Deployment gates, rollback, state machines |

There are also supplementary categories: Karpathy behavioral patterns, Claude Code platform patterns (121–142), open-source skill patterns, gap-fill patterns, and the **2026-05 harvest (143–155)** — which covers Iron-Law rule framing, HARD-GATE block tags, DOT-graph decision flows, marketplace polymorphism, plugin lifecycle state machines, and more.

---

## Example: Pattern 23 — Attempt-Capped Repair Loop

**Problem:** An AI agent fixing build errors can loop forever or give up too soon.

**Pattern:**

```markdown
## Stop Conditions (Exhaustive)

The repair loop stops ONLY when ONE of these is met:

| Condition | Action |
|-----------|--------|
| (a) Build succeeds | Return success |
| (b) Attempt counter reaches N | Return failed with remaining errors |
| (c) Session dies | Return session_dead |

No other condition justifies stopping. Not "too many errors",
not "beyond scope", not "unfixable."
```

**Why it works:** It takes away the agent's urge to talk itself into quitting early. The exhaustive table leaves no room for ambiguity, so the agent can't invent a 4th stop condition.

---

## Example: Pattern 45 — Directive-Based Pre-Write Review

**Problem:** An agent writes incorrect config changes that break production behavior.

**Pattern:**

```markdown
Before EVERY edit, evaluate each guardrail:

| # | Check | PASS | FAIL |
|---|-------|------|------|
| G1 | Is suppression scoped? | On specific item | Blanket scope |
| G2 | Is override needed? | Default insufficient | Default works fine |
| G3 | Is companion created? | Paired files exist | Orphaned condition |

If ANY guardrail returns FAIL → do NOT write. Revise first.
```

**Why it works:** It forces a real pause between deciding what to do and actually doing it. Because each check sits in its own table row, the agent has to evaluate them one by one — it can't just skip one by gliding past it in prose.

---

## Techniques Highlights

### Token-Level Techniques (9 techniques)

These are grounded in how LLMs actually process tokens, not in intuition. For instance, **decision trees beat prose for branching logic**: a tree focuses the model's attention on a single path, while prose spreads that attention across every condition at once.

### Anti-Laziness Strategies (8 strategies)

Agents skip reference reads, shrink multi-step procedures down to shortcuts, and "remember" instead of re-reading. The anti-laziness guide walks through 8 systematic defenses, from mandatory read gates to progressive disclosure.

### Prompt Review Framework

A structured review process built around 9 dimensions (clarity, determinism, safety, testability...) and P0/P1/P2 severity grading. It's meant for peer review of agent prompts, not just checking your own work.

---

## How to Use

1. **Building a new skill?** Scan the [catalog index](/prompt-context-patterns/catalog/) for patterns that match your problem
2. **Debugging unstable behavior?** Check [execution control](/prompt-context-patterns/catalog/categories/patterns-execution-control) and [anti-laziness](/prompt-context-patterns/catalog/techniques/anti-laziness)
3. **Reviewing someone's prompt?** Use the [review checklist](/prompt-context-patterns/catalog/standards/review-checklist)
4. **Learning prompt engineering?** Start with [token-level techniques](/prompt-context-patterns/catalog/techniques/token-level-techniques)

---

## License

MIT. Use these patterns in your own agents, plugins, and projects.
