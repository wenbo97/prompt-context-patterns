---
layout: post
title: "Prompt Engineering Patterns for Claude Code Skills"
date: 2026-04-19
categories: [prompt-engineering, patterns]
---

A hands-on guide to writing skill prompts that behave predictably — grounded in how LLMs actually process tokens.

---

## Core Principle: Reduce Conditional Entropy

Every token an LLM generates is really a probability distribution over candidates. **The structure of your prompt directly controls how sharp or diffuse that distribution is at each decision point.**

- Sharp distribution (low entropy) → deterministic behavior
- Diffuse distribution (high entropy) → unstable, unpredictable behavior

**Everything below is a way to sharpen the distribution at the moments that matter.**

### What "conditional entropy" actually means

Every time the model generates a token, it's choosing among candidates, each with its own probability. If those probabilities are spread evenly — say, 10 candidates at 10% each — the model is "hesitating," and that's high entropy. If one candidate sits at 90% and the rest barely register, the model is "certain," and that's low entropy.

**The way you write your prompt is what decides whether the model hesitates or commits at the critical decision points.**

### Concrete example

Say your skill has to decide whether to ask the user for input, depending on the environment.

**Prose version:**

```
If running in CI with no arguments, use defaults.
If interactive with arguments, run directly.
If interactive without arguments, ask the user.
```

Once it's read this, the model has to generate its next action. Here's what's going on inside attention:

```
"CI"              → line 1, beginning     ← attention must look back
"no arguments"    → line 1, middle        ← attention must look back
"use defaults"    → line 1, end           ← attention must look back
"interactive"     → line 2, beginning     ← also competing for attention
"ask the user"    → line 3, end           ← also competing for attention

5 conditions scattered across 3 lines — which should I attend to?
```

Attention is spread across several positions, so no single condition gets enough weight, and the model isn't sure which path to take → **high entropy → unstable behavior**.

**Tree version:**

```
## CI environment?
├─ YES
│  └─ Has arguments?
│     ├─ YES → use arguments, execute
│     └─ NO  → use defaults, execute
└─ NO (interactive)
   └─ Has arguments?
      ├─ YES → use arguments, execute
      └─ NO  → ask user
```

Once the model has worked out "CI = YES" and "arguments = NO," its attention lands right here:

```
│     └─ NO  → use defaults, execute
              ↑
              attention is concentrated on this line
```

The tokens "use defaults, execute" are **right next to the cursor** — there's nothing to look back for. The model is almost 100% sure what comes next → **very low entropy → deterministic behavior**.

### Feel it in numbers

Prose version — the probability distribution at the decision point:

```
use arguments, execute:  35%
use defaults, execute:   30%
ask user:                25%
other:                   10%
```

Three options are close in probability. Run it 10 times, and roughly 3 may go wrong.

Tree version — at the correct branch leaf:

```
use defaults, execute:   92%
use arguments, execute:   5%
other:                    3%
```

One option dominates. Run it 10 times, and you'll see 0–1 deviations.

### Why indentation is information

```
└─ NO (interactive)
   └─ Has arguments?
      └─ NO  → ask user
```

After tokenization, the indentation (0 spaces, 3 spaces, 6 spaces) turns into whitespace tokens, and those tokens carry **hierarchy**. The model has seen huge amounts of indented structure during training — source code, YAML, directory trees — and it has learned that a deeper indent means a child of the condition above it.

Prose gives it none of that spatial encoding. In "If interactive but arguments provided," the model has to work out how "interactive" and "arguments provided" relate using grammar alone — and that inference itself costs attention and adds uncertainty.

### One-line summary

> A tree lets the model glance at a few nearby tokens to know what to do. Prose makes it scan a whole paragraph and piece the answer together. The smaller the search radius, the more certain the outcome.

---

## 1. Visual Decision Trees over Prose

Claude follows a visual tree far more reliably than the same logic written as prose — because every branch ends with a clear, explicit action.

### Why it works

Prose spreads the conditions out across a sentence, so the model has to hold several far-apart tokens in mind at once, and its attention gets diluted. A tree keeps each condition right next to its action, so the model only has to glance at nearby tokens to know what to do.

### Bad: prose

```
If running in CI with no arguments, use defaults. If interactive with arguments,
run directly. If interactive without arguments, ask the user.
```

### Good: decision tree

```
## Is $ARGUMENTS non-empty?
├─ YES → parse arguments, execute directly, no interaction
└─ NO
   ## Is $CI or $CLAUDE_NONINTERACTIVE set?
   ├─ YES → use values from <defaults>, execute directly
   └─ NO  → ask user for missing parameters, then execute
```

### Why indentation matters

Those indentation tokens carry hierarchy. Models have seen enormous amounts of indented structure during training — code, YAML, directory trees — and learned that a deeper indent means a child of the parent condition. Prose gives them nothing like that, so the model has to infer the nesting from grammar alone, which costs attention and introduces uncertainty.

---

## 2. Grounding (Anchoring)

Give the model a concrete starting point instead of leaving it to sample from an infinite space.

### Bad: unanchored

```
Generate a deployment script.
```

### Good: anchored with template

```
Generate a deployment script based on this template:
<template>
#!/bin/bash
set -euo pipefail
ENV="${1:?Usage: deploy.sh <env>}"
# ... your steps here
</template>
```

**Why:** The template's tokens sit right in the attention window, so the output gets pulled toward the template's distribution instead of the generic idea of a "deployment script."

---

## 3. Cognitive Offloading

Move the reasoning steps out into the open, instead of leaving the model to work them out implicitly.

### Bad: implicit reasoning required

```
Analyze this code's performance issues and fix them.
```

### Good: explicit steps provided

```
<analysis_steps>
1. Identify all loops and recursion
2. Annotate each with time complexity
3. Flag anything O(n²) or higher
4. Propose optimization for each flagged section
</analysis_steps>
Execute these steps in order.
```

**Why:** LLMs have no real working memory, and every reasoning step eats into the attention available in the context window. Spelling the steps out gives the model "external memory" — each step only has to look at the output of the one before it, instead of deriving everything from scratch.

Decision trees = cognitive offloading for branching logic.
Chain-of-thought = cognitive offloading for reasoning.
Same principle, different applications.

---

## 4. Attention Locality

Keep related information close together in the token sequence — in practice, tokens that sit nearer each other get more attention.

### Bad: rule far from its target

```
<rules>Never delete production databases</rules>
... (500 tokens of other content) ...
<task>Clean up expired data</task>
```

### Good: rule adjacent to its target

```
<task>
Clean up expired data
<constraint>Never delete production databases</constraint>
</task>
```

**Why:** Transformer attention is global in theory, but it leans on position — nearby tokens score higher. So put each constraint right next to the action it governs, not off in some distant "general rules" section.

---

## 5. Token-Action Binding

Each instruction should point as directly as it can to one executable action.

### Bad: multiple implicit actions in one sentence

```
Check code style issues and fix them then run tests and make sure they pass.
```

### Good: one instruction = one action

```
1. Run: `eslint --fix src/`
2. Run: `npm test`
3. If tests fail → read error output, fix the issue, go to step 2
```

**Why:** The model turns one clear instruction into one tool call far more reliably than it pulls several implied actions out of a run-on sentence.

---

## 6. Schema Priming

Hand the model an output "shape" and let it fill in the content.

### Bad: open-ended

```
Analyze this PR's risk.
```

### Good: schema-constrained

```
<output_schema>
- risk_level: high | medium | low
- affected_files: [list]
- rollback_plan: [string]
- requires_review: true | false
</output_schema>
```

**Why:** The schema tokens work like rails during decoding. As the model fills in each field, the key names keep its attention on track, cutting drift sharply.

---

## 7. Negative Space (Explicit Alternatives)

Whenever you tell the model what NOT to do, always give it something TO DO instead.

### Bad: negation only

```
Don't modify the database directly.
Don't skip tests.
Don't use sudo.
```

### Good: negation + alternative path

```
<boundaries>
- Database changes → generate a migration file, never execute raw SQL
- Validation needed → run full test suite before continuing, never skip
- Elevated permissions → request user confirmation, never use sudo
</boundaries>
```

**Why:** "Don't do X" only holds down certain token sequences without lifting any alternative. The model learns where not to go, but not where to go — so it stays unstable. Give it the alternative and you suppress the wrong path and boost the right one at the same time.

---

## 8. XML Tags for Semantic Boundaries

Claude's training data was full of XML tags, so use them to mark off the sections of your prompt.

### Recommended structure for skill prompts

```markdown
<context>
Background information the model needs to understand the domain.
</context>

<parameters>
Inputs with types, defaults, and sources.
</parameters>

<decision_tree>
Visual branching logic with explicit leaf actions.
</decision_tree>

<examples>
<example>
<input>...</input>
<thinking>Step-by-step reasoning the model should follow</thinking>
<output>...</output>
</example>
</examples>

<boundaries>
What not to do + what to do instead.
</boundaries>

<output_schema>
Expected output shape.
</output_schema>
```

**Why:** XML tags draw firm boundaries. The model reads content in different tags as separate sections, which keeps instructions, examples, and constraints from bleeding into each other.

---

## 9. Few-Shot with Embedded Reasoning

Show the model how to think, not just what to output.

### Bad: input/output pairs only

```
<example>
<input>deploy staging</input>
<output>Deployed to staging.</output>
</example>
```

### Good: input + thinking + output

```
<example>
<input>deploy staging</input>
<thinking>
1. Arguments provided: "staging" → non-empty → skip user interaction
2. Environment "staging" is valid (matches staging|production)
3. No CI variable detected → but args present → proceed silently
4. Execute deployment to staging
</thinking>
<output>Deployed to staging successfully.</output>
</example>
```

**Why:** The `<thinking>` block in your examples carries over into the model's own extended thinking. It picks up the reasoning pattern, not just the output pattern.

---

## Putting It All Together: Skill Prompt Template

```markdown
---
name: my-skill
description: One line that tells Claude WHEN to activate this skill
context: default
allowed-tools: Bash(specific-commands*), Write, Edit
---

<context>
What this skill does and why it exists.
Domain-specific background if needed.
</context>

<parameters>
- target: from $ARGUMENTS, or ask user
- env_mode: from $CI or $CLAUDE_NONINTERACTIVE, default "interactive"
</parameters>

<decision_tree>
## Has $ARGUMENTS?
├─ YES → parse into `target`, skip interaction
└─ NO
   ## Is env_mode non-interactive?
   ├─ YES → use defaults from <defaults>, proceed
   └─ NO  → ask user for `target`, then proceed
</decision_tree>

<defaults>
- target: "staging"
</defaults>

<steps>
1. Validate `target` against allowed values (staging | production)
2. Run preflight checks: `npm test`
3. If tests fail → stop, report error, do NOT proceed
4. Execute deployment to `target`
5. Verify deployment health
</steps>

<examples>
<example>
<input>/my-skill production</input>
<thinking>
1. $ARGUMENTS = "production" → non-empty → use directly
2. target = "production" → valid
3. Run tests → pass
4. Deploy to production
</thinking>
<output>Deployed to production. Health check passed.</output>
</example>
</examples>

<boundaries>
- Never deploy without passing tests → run `npm test` first, abort on failure
- Never modify .env files → read config from environment variables only
- Never run with sudo → request user confirmation for elevated actions
</boundaries>
```

---

## Summary of Relationships

```
Behavioral Stability
      ↑
Low Conditional Entropy at Decision Points
      ↑
Sharp Attention Distribution
      ↑
Token Spatial Arrangement in Prompt
      ↑
┌─────────────┬──────────────┬───────────────┬──────────────┐
│ Decision    │ Attention    │ Cognitive     │ Schema       │
│ Trees       │ Locality     │ Offloading    │ Priming      │
├─────────────┼──────────────┼───────────────┼──────────────┤
│ Grounding   │ Token-Action │ Negative      │ XML          │
│ (Anchoring) │ Binding      │ Space         │ Boundaries   │
├─────────────┼──────────────┼───────────────┼──────────────┤
│ Few-Shot w/ │              │               │              │
│ Reasoning   │              │               │              │
└─────────────┴──────────────┴───────────────┴──────────────┘

All techniques manipulate the same thing:
how attention is distributed across tokens at generation time.
```

---

## References

- [Anthropic Prompting Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)
- [Anthropic Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [XML Tags Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags)
- [Claude Code Skills Docs](https://code.claude.com/docs/en/skills)
- [Claude Code System Prompts (community)](https://github.com/Piebald-AI/claude-code-system-prompts)
- [Awesome Claude Skills](https://github.com/travisvn/awesome-claude-skills)
