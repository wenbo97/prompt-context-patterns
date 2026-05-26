---
layout: post
title: "Prompt Engineering Patterns for Claude Code Skills"
date: 2026-04-19
categories: [prompt-engineering, patterns]
---

A practical guide to writing stable, predictable skill prompts — grounded in how LLMs actually process tokens.

---

## Core Principle: Reduce Conditional Entropy

Every token an LLM generates is a probability distribution over candidates. **Your prompt's structure directly controls how sharp or diffuse that distribution is at each decision point.**

- Sharp distribution (low entropy) → deterministic behavior
- Diffuse distribution (high entropy) → unstable, unpredictable behavior

**Everything below is a technique for sharpening the distribution at the moments that matter.**

### What "conditional entropy" actually means

Every time the model generates a token, it faces a set of candidates, each with a probability. If probabilities are spread evenly (e.g., 10 candidates at 10% each), the model is "hesitating" — that's high entropy. If one candidate sits at 90% and the rest are negligible, the model is "certain" — that's low entropy.

**The way you write your prompt directly determines whether the model hesitates or commits at critical decision points.**

### Concrete example

Suppose your skill needs to decide whether to ask the user for input, based on the environment.

**Prose version:**

```
If running in CI with no arguments, use defaults.
If interactive with arguments, run directly.
If interactive without arguments, ask the user.
```

After reading this, the model needs to generate its next action. Here's what's happening inside attention:

```
"CI"              → line 1, beginning     ← attention must look back
"no arguments"    → line 1, middle        ← attention must look back
"use defaults"    → line 1, end           ← attention must look back
"interactive"     → line 2, beginning     ← also competing for attention
"ask the user"    → line 3, end           ← also competing for attention

5 conditions scattered across 3 lines — which should I attend to?
```

Attention is spread across multiple positions → no single condition gets enough weight → the model is uncertain about which path to take → **high entropy → unstable behavior**.

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

After the model determines "CI = YES" and "arguments = NO", its attention is here:

```
│     └─ NO  → use defaults, execute
              ↑
              attention is concentrated on this line
```

The tokens "use defaults, execute" are **right next to the cursor**. No need to look back anywhere. The model is nearly 100% certain what to do next → **very low entropy → deterministic behavior**.

### Feel it in numbers

Prose version — probability distribution at the decision point:

```
use arguments, execute:  35%
use defaults, execute:   30%
ask user:                25%
other:                   10%
```

Three options are close in probability. Run 10 times, roughly 3 may go wrong.

Tree version — at the correct branch leaf:

```
use defaults, execute:   92%
use arguments, execute:   5%
other:                    3%
```

One option dominates. Run 10 times, 0–1 deviations.

### Why indentation is information

```
└─ NO (interactive)
   └─ Has arguments?
      └─ NO  → ask user
```

The indentation (0 spaces, 3 spaces, 6 spaces) becomes whitespace tokens after tokenization. These whitespace tokens encode **hierarchy** — the model has seen massive amounts of indented structures (source code, YAML, directory trees) during training and has learned: deeper indent = child of parent condition.

Prose has no such spatial encoding. In "If interactive but arguments provided" — the subordination between "interactive" and "arguments provided" must be inferred from natural language grammar alone. That inference itself costs attention and introduces uncertainty.

### One-line summary

> A tree lets the model look at a few nearby tokens to know what to do. Prose forces it to scan an entire paragraph to piece together the answer. The smaller the search radius, the more certain the outcome.

---

## 1. Visual Decision Trees over Prose

Claude follows visual tree structures more reliably than prose descriptions of the same logic, because each branch terminates with an explicit action.

### Why it works

Prose scatters conditions across a sentence. The model must attend to multiple distant tokens simultaneously, diluting attention. A tree places the relevant condition and its action adjacent in the token sequence — the model only needs to look at nearby tokens to know what to do.

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

Indentation tokens encode hierarchy. Models have seen massive amounts of indented structures (code, YAML, directory trees) during training and have learned that deeper indent = child of parent condition. Prose has no such spatial encoding — the model must infer nesting from natural language grammar, which costs attention and introduces uncertainty.

---

## 2. Grounding (Anchoring)

Give the model a concrete starting point instead of letting it sample from an infinite space.

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

**Why:** Template tokens directly participate in attention — the model's output is "pulled toward" the template's distribution rather than sampling from the generic concept of "deployment script."

---

## 3. Cognitive Offloading

Externalize reasoning steps that the model would otherwise have to perform implicitly.

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

**Why:** LLMs have no true working memory. Each reasoning step consumes attention resources from the context window. Writing out intermediate steps provides "external memory" — each step only needs to attend to the previous step's output, not derive everything from scratch.

Decision trees = cognitive offloading for branching logic.
Chain-of-thought = cognitive offloading for reasoning.
Same principle, different applications.

---

## 4. Attention Locality

Related information should be close together in the token sequence. Closer tokens get higher attention weights in practice.

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

**Why:** Transformer attention is theoretically global but has positional bias — nearby tokens receive stronger attention scores. Place constraints next to the actions they constrain, not in a distant "general rules" section.

---

## 5. Token-Action Binding

Each instruction should map as directly as possible to one executable action.

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

**Why:** The model maps a single clear instruction sequence to a single tool call far more reliably than extracting multiple implied actions from a run-on sentence.

---

## 6. Schema Priming

Give the model an output "shape" and it fills in the content.

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

**Why:** Schema tokens act as "rails" during decoding. When generating each field value, the model's attention is strongly guided by the schema key names, drastically reducing drift.

---

## 7. Negative Space (Explicit Alternatives)

When telling the model what NOT to do, always provide what TO DO instead.

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

**Why:** "Don't do X" only suppresses certain token sequences but doesn't boost any alternative. The model knows where not to go but not where to go → unstable. Providing the alternative simultaneously suppresses the wrong path and boosts the right one.

---

## 8. XML Tags for Semantic Boundaries

Claude was trained with XML tags in its training data. Use them to delineate prompt sections.

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

**Why:** XML tags create hard semantic boundaries. The model treats content inside different tags as distinct sections, reducing cross-contamination between instructions, examples, and constraints.

---

## 9. Few-Shot with Embedded Reasoning

Show the model HOW to think, not just WHAT to output.

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

**Why:** The `<thinking>` pattern inside few-shot examples gets generalized into the model's own extended thinking blocks. It learns the reasoning pattern, not just the output pattern.

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
