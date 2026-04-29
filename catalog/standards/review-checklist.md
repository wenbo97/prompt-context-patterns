# Prompt Engineering Review Checks

> **SSOT for review output format, severity criteria, and quality check procedures.**
> Referenced by: `commands/dev-prompt-review.md`.
> **Examples:** Read @../prompt-examples/template.md for good vs bad prompt comparison — review agents should reference this when evaluating prompt quality.

---

## Output Rules

**Every issue MUST include six parts — no exceptions:**

1. **Current Behavior** — What the prompt currently instructs agents to do. Describe the concrete agent behavior produced by the original text: which action the agent takes, which decision it makes, which output it produces. Include the verbatim quote (2-5 lines of surrounding context) so the reader can locate it. Never paraphrase — quote the actual text, then describe its behavioral effect.
2. **Changed Behavior** — What the prompt will instruct agents to do after the fix. Describe the concrete agent behavior the suggested text produces: how the action, decision, or output changes. Include the copy-pasteable replacement text. Never write vague suggestions like "clarify this" — write the actual improved text AND describe how agent behavior changes.
3. **Why** — A specific explanation of what failure, confusion, or risk the current behavior causes. Name the concrete failure mode: which agent gets confused, which phase breaks, which edge case is mishandled, which silent failure occurs. This answers: "What goes wrong today?"
4. **Benefit** — What concrete improvement the changed behavior provides. Name the specific outcome: "Prevents agent from applying wrong cached fix" or "Eliminates 50% false positive rate in P0 classification." This answers: "What gets better after the change?" Every fix must justify its existence — if you cannot state a concrete benefit, the issue is not worth reporting.
5. **Diff Summary** — A one-line statement of the behavioral delta: "Agent currently does X → after fix, agent does Y instead." This gives the reviewer an instant before/after comparison without reading the full details.
6. **Location** — File path and line number(s) where the issue exists. For cross-file issues, cite both files.

**Rationale:** The reviewer needs to see the current behavior vs. changed behavior side-by-side to evaluate whether each fix is correct and worthwhile. Without the current behavior description, they cannot understand what agents do today. Without the changed behavior, they cannot assess if the new behavior is actually better. Without the why, they cannot assess risk. Without the benefit, they cannot prioritize. Without the diff summary, they cannot quickly scan the report. Without the location, they cannot find the issue in the source files.

---

## Output Format

After all agents complete, synthesize a unified report:

```markdown
# Plugin Prompt Review Report

**Date**: {yyyy-MM-dd HH:mm}
**Files Reviewed**: {count}
**Total Issues**: {count}

## Summary

| Dimension | Issues | P0 | P1 | P2 |
|-----------|--------|----|----|-----|
| Semantic Conflicts | | | | |
| Stale Refs & Completeness | | | | |
| SSOT & Duplication | | | | |
| Workflow Integrity | | | | |
| Ambiguity | | | | |
| Sentence Precision | | | | |
| Edge Cases & Error Paths | | | | |
| Naming Consistency | | | | |
| Token-Level Quality | | | | |

## P0 — Must Fix (blocks correct execution)

### P0-{nn}: [{Dimension}] {short title}

**Location:** `{file}:{line}` (or `{file1}` vs `{file2}`)
**Verification:** {Verified | Downgraded from P{n} | False Positive}
**Diff Summary:** Agent currently {does X} → after fix, agent {does Y instead}.

**Current Behavior:**
> {Verbatim quote of the problematic text from the source file. Include enough surrounding context to locate it unambiguously.}

With this text, the agent {description of what the agent currently does — the concrete action, decision, or output this text produces}.

**Changed Behavior:**
> {The improved version — rewritten text that resolves the issue. Must be a concrete, copy-pasteable replacement, not a vague suggestion like "clarify this".}

With this text, the agent {description of what the agent will do instead — how the action, decision, or output changes}.

**Why:** {1-2 sentences explaining what goes wrong with the current behavior. Be specific — name the failure mode, the confused agent behavior, or the contradiction.}

**Benefit:** {What concrete improvement the changed behavior provides. Name the specific outcome: which failure is prevented, which agent behavior is corrected, which edge case is handled.}

---

## P1 — Should Fix (causes confusion or wrong behavior in edge cases)

### P1-{nn}: [{Dimension}] {short title}

**Location:** `{file}:{line}`
**Verification:** {Verified | Downgraded from P{n}}
**Diff Summary:** Agent currently {does X} → after fix, agent {does Y instead}.

**Current Behavior:**
> {Verbatim quote}

With this text, the agent {description of current behavior}.

**Changed Behavior:**
> {Improved version}

With this text, the agent {description of changed behavior}.

**Why:** {Explanation of the risk}

**Benefit:** {What concrete improvement the changed behavior provides}

---

## P2 — Nice to Fix (clarity improvement)

### P2-{nn}: [{Dimension}] {short title}

**Location:** `{file}:{line}`
**Diff Summary:** Agent currently {does X} → after fix, agent {does Y instead}.

**Current Behavior:**
> {Verbatim quote}

With this text, the agent {description of current behavior}.

**Changed Behavior:**
> {Improved version}

With this text, the agent {description of changed behavior}.

**Why:** {Explanation of the clarity improvement}

**Benefit:** {What concrete improvement the changed behavior provides}
```

---

## Severity Criteria

| Severity | Definition |
|----------|------------|
| **P0** | Two files give opposite instructions for the same operation; a reference points to a nonexistent file that is read at runtime; a required parameter is undocumented; an SSOT concept is contradicted by a copy in another file; a workflow handoff passes fields the receiver does not handle; a newer rule silently breaks or overrides an existing working feature without explicit deprecation |
| **P1** | Ambiguous rule that could cause an agent to take the wrong action; hardcoded value that drifts from config; missing error handling for a likely failure mode; a rule is restated (non-contradictory copy) instead of referencing the SSOT; verbatim content duplicated across files; a dangling condition with no else/otherwise clause for a failure path |
| **P2** | Minor wording ambiguity; style inconsistency; redundant statement; weak imperative that should be stronger; semantic duplication (same idea, different words); unanchored pronoun that is resolvable from nearby context |

---

## Quality Check Categories

Checks are grouped by the **model behavior** they address. For each check, the agent must evaluate: (1) does this prompt correctly exploit or account for this behavior? (2) what specific failure occurs if the check fails?

Read @prompt-engineering-standards.md for the full principles behind each check category.

**Category A: Clarity & Directness** (Claude follows explicit instructions; infers poorly from vague ones)

| Check | What to Flag | Why It Fails (Model Behavior) | Severity |
|-------|-------------|-------------------------------|----------|
| **Weak imperatives** | "Consider...", "Try to...", "You might want to...", "It may be helpful to..." | Claude treats hedged language as optional guidance, not instructions. Under context pressure (long conversations), optional guidance is the first thing skipped. | P2 |
| **Missing context/motivation** | Rules stated without explaining WHY (e.g., "NEVER use git amend" without explaining the retry safety reason) | Claude generalizes better from explained rules. Without the "why," agents apply rules mechanically and miss edge cases where the rule should/shouldn't apply. Per Anthropic: "Providing context or motivation behind your instructions helps Claude better understand your goals." | P2 |
| **Unanchored pronouns** | "it", "this", "that", "these" where the referent is ambiguous | Claude resolves ambiguous pronouns using the nearest plausible referent, which may not be the intended one. In multi-step instructions, "update it" after discussing both a csproj and a cs file is genuinely ambiguous. | P1 |
| **Over-prompting for Claude 4.6** | "CRITICAL: You MUST use this tool when...", "ALWAYS be thorough", "If in doubt, use [tool]" | Claude 4.6 is significantly more proactive than previous models. Anti-laziness prompting that was needed for Claude 3.5 now causes overtriggering — tools fire on every turn, exploration reads 50+ files, subagents spawn for simple tasks. Per Anthropic: "These models may now overtrigger. The fix is to dial back any aggressive language." | P1 |

**Category B: Examples & Demonstration** (few-shot is the most reliable steering mechanism)

| Check | What to Flag | Why It Fails (Model Behavior) | Severity |
|-------|-------------|-------------------------------|----------|
| **Missing few-shot examples** | Critical operations (tool calls, output JSON, csproj transformations, classification decisions) without concrete input/output examples | Without examples, Claude improvises format. Anthropic: "Examples are one of the most reliable ways to steer Claude's output format, tone, and structure. A few well-crafted examples can dramatically improve accuracy and consistency." For this plugin, missing examples on skill output format means the consumer agent guesses field names. | P1 |
| **Abstract examples** | Examples that describe the pattern in prose instead of showing exact XML/JSON/commands | Claude copies the structure of examples literally. An abstract description ("add the package to the right group") produces abstract output. Only concrete examples (`<PackageReference Include="X" NoWarn="NU1701" />`) produce concrete output. | P2 |
| **Non-diverse examples** | All examples show the same branch of a multi-branch decision (e.g., only REPLACE mapping examples, no KEEP_DUAL) | Claude picks up patterns from example sets. If all examples show one branch, Claude defaults to that branch for ambiguous cases. Per Anthropic: "Cover edge cases and vary enough that Claude doesn't pick up unintended patterns." | P2 |

**Category C: Structure & Sequencing** (Claude follows numbered sequences; skips prose-embedded steps)

| Check | What to Flag | Why It Fails (Model Behavior) | Severity |
|-------|-------------|-------------------------------|----------|
| **Missing chain-of-thought structure** | Multi-step decisions described as prose paragraphs instead of numbered steps | Claude processes numbered sequences step-by-step. Prose-embedded sequences are processed as a single chunk — steps may be reordered or skipped. Per Prompt Engineering Guide: chain-of-thought with explicit steps outperforms implicit reasoning on complex tasks. | P2 |
| **Missing else/otherwise** | `if/when` clauses without explicit fallback for the negative case | Claude invents fallback behavior when no branch is specified. The invented behavior may be reasonable but is unpredictable across runs — a silent source of inconsistency. This is the #1 ambiguity pattern in autonomous agents. | P1 |
| **Long data below query** | Reference data (package maps, error tables) placed AFTER the decision logic that uses it | Anthropic testing: queries at the end of long-context prompts improve response quality by up to 30%. For skills loading package-map.md or project-map-list.md, placing the data above the decision steps improves classification accuracy. | P2 |

**Category D: Contracts & Boundaries** (agents at context boundaries share nothing implicitly)

| Check | What to Flag | Why It Fails (Model Behavior) | Severity |
|-------|-------------|-------------------------------|----------|
| **Undocumented output schemas** | Agents or skills without an Output section listing field names, types, and possible values | The consuming agent/phase must know exact field names to read them. Without a contract, field name mismatches are silent — `buildStatus` vs `LocalBuildStatus` produces a null value, not an error. | P0 |
| **Missing Input parameters** | Agent or skill definition without a formal Input table (parameter name, type, required/optional, source) | The calling agent must know what to pass. Without a contract, missing parameters cause the child agent to fail or improvise. Test: can the agent work with ONLY its Input table and no parent context? | P0 |
| **Implicit context inheritance** | Instructions assuming a forked agent or subagent can see parent variables without them being passed as parameters | Forked agents start fresh. Per Claude Code System Prompts: workers "execute a directive directly" with only what they receive. Per Claude Code Best Practices: "Subagents run in separate context windows and report back summaries." Any value not in the Input table is invisible. | P0 |
| **Broken phase contract** | Output field name/type in Phase N doesn't match Input field name/type in Phase N+1 | Silent null/undefined when the consumer reads a field that the producer named differently. Check against `rules/phase-data-contract.md` — the SSOT for inter-phase variable naming. | P0 |

**Category E: Verification & Grounding** (agents rationalize success without executable checks)

| Check | What to Flag | Why It Fails (Model Behavior) | Severity |
|-------|-------------|-------------------------------|----------|
| **Self-check without commands** | `<self-check>` items that say "verify X works" without specifying the command to run and expected output | Per Claude Code Best Practices: "Claude performs dramatically better when it can verify its own work." A check without a command is not a PASS — it's a skip. Claude will rationalize: "the code looks correct" and proceed. Per Claude Code System Prompts: the verification specialist is a separate agent that issues PASS/FAIL verdicts based on running builds, tests, and linters. | P1 |
| **Missing verification steps** | Operations without explicit "check the result" instructions (e.g., "create PR" without "verify PR URL from API response") | Without verification, silent failures propagate. The agent reports success because no error was thrown — but the PR wasn't actually created, or the csproj is corrupt XML. | P1 |
| **Indirect value references** | Instructions that say "Per @file for format" without inlining the critical value at the point of use | Claude must follow 2+ hops to reach the value. Under context pressure, the hop is skipped and the agent improvises. Fix: inline the value AND cite the source: `NoWarn="NU1701" PrivateAssets="all" (per @nu1701-handling.md)`. | P1 |

**Category F: Composition & Scale** (context window is the #1 constraint)

| Check | What to Flag | Why It Fails (Model Behavior) | Severity |
|-------|-------------|-------------------------------|----------|
| **Oversized prompt file** | Agent/command >260 lines, skill >300 lines (per @prompt-engineering-standards.md Prompt Size Discipline) | Per Claude Code Best Practices: "If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise." Same applies to any prompt file. Agents prioritize early content and skim late content — rules in the bottom third are applied inconsistently. | P1 |
| **Single-sentence skill/agent description** | Frontmatter description lacks trigger phrases, usage examples, and when-NOT-to-use guidance | Per Claude Code Sub-Agents: trigger-rich descriptions (3-5 trigger scenarios) outperform single-sentence summaries for agent routing. Claude uses the description to decide whether to invoke the skill — vague descriptions cause mis-routing or non-invocation. | P1 |
| **Tool invocation by name only** | Instructions say "use search_code" without showing exact parameters and expected response | Claude guesses parameters. In this plugin, `search_code` requires `project: ["O365 Core"]` (not `"ControlPlane"`) — a guess would use the wrong value. | P1 |
| **Guardrails as prose paragraphs** | Constraints embedded in paragraphs instead of lists/tables with one rule per row | Per Claude Code System Prompts: behavioral guardrails average 16-102 tokens, stated as individual micro-rules. Tables and lists are parsed row-by-row; prose paragraphs are processed as chunks where individual rules blur together. | P2 |
| **Verbose guardrails (>60 tokens)** | Single guardrail rule exceeding 60 tokens | Per Claude Code System Prompts: the average guardrail is 47 tokens. Long rules dilute impact. If a rule needs >60 tokens, it may be two rules or include unnecessary explanation. | P2 |
| **Intentional redundancy not labeled** | Duplicated values at point-of-use without `(per @SSOT-file)` attribution | Reviewers cannot distinguish intentional reliability redundancy from accidental SSOT violation. Add `(per @file)` after every intentionally duplicated value so drift can be detected. | P1 |

**Category G: Backward Compatibility** (existing features must not break)

| Check | What to Flag | Why It Fails (Model Behavior) | Severity |
|-------|-------------|-------------------------------|----------|
| **Backward compatibility violation** | A newer rule, mapping, or feature that silently overrides or invalidates an existing working behavior without explicit acknowledgment or deprecation | Agents follow the newest instruction they encounter. If a new rule contradicts an existing one without explicit supersession, agents may flip-flop between behaviors depending on which file is loaded first. Per Claude Code Best Practices: "Treat CLAUDE.md like code: review it when things go wrong." Same applies to all prompt files. | P0 |

**Category H: Token-Level Quality Patterns** (per @../prompt-examples/prompt-engineering-for-skills.md — reduces conditional entropy at decision points)

| Check | What to Flag | Why It Fails (Model Behavior) | Severity |
|-------|-------------|-------------------------------|----------|
| **Prose branching instead of decision tree** | Multi-path decisions described as "if X then Y, if Z then W" prose instead of visual `├─ YES →` / `└─ NO →` trees | Prose scatters conditions across a sentence — attention dilutes across multiple positions. A tree places condition and action adjacent in the token sequence, concentrating attention and producing deterministic behavior. Run 10 times: prose ~30% deviation, tree ~5%. | P2 |
| **Missing output schema** | Skill/agent/command produces structured output but has no `<output_schema>` or output table with enumerated field names and value types | Schema tokens act as "rails" during decoding — each field value is guided by the schema key. Without a schema, the model invents format, producing inconsistent output across runs that downstream consumers cannot parse. | P1 |
| **Distant constraints** | Constraints placed in a "general rules" section far from the actions they govern | Transformer attention has positional bias — nearby tokens get higher attention scores. A constraint 500 tokens from its action is applied inconsistently. Move constraints adjacent to actions: `<constraint>` inside `<task>`, or bullet directly below the step. | P2 |
| **Missing grounding template** | Agent must produce structured output (reports, code blocks, XML) but no filled-in template/example is provided | Without a template, the model samples from its generic distribution of "what a report looks like." A concrete template pulls output toward the template's distribution, reducing variance dramatically. | P1 |
| **Multi-action instructions** | Single sentence maps to multiple implicit actions ("check and fix issues then run tests") | The model maps one clear instruction to one tool call reliably. Multi-action sentences cause action merging, skipping, or reordering. Split: "1. Run X. 2. Run Y. 3. If fail → Z." | P2 |
| **Negation without alternative** | "Don't modify the database" / "Never use sudo" without specifying what TO do instead | "Don't do X" suppresses tokens but doesn't boost alternatives — model knows where not to go but not where to go. Unstable. Fix: "Database changes → generate migration file, never raw SQL." | P2 |
| **Missing XML semantic boundaries** | Skill/agent/command file uses only markdown headers to separate sections — no `<context>`, `<steps>`, `<boundaries>`, `<output_schema>` tags | XML tags create hard semantic boundaries. Content inside different tags is treated as distinct sections, reducing cross-contamination. Markdown headers are softer boundaries — content bleeds between adjacent sections under context pressure. | P2 |
| **Few-shot without reasoning** | `<example>` blocks show input→output only, no `<thinking>` step showing HOW the model should reason | The `<thinking>` pattern inside examples gets generalized into the model's own reasoning. Without it, the model learns the output pattern but not the decision process — brittle on edge cases. | P1 |
| **No cognitive offloading** | Multi-step reasoning left implicit ("analyze the error and fix it") instead of explicit numbered steps | LLMs have no working memory. Each reasoning step consumes attention from the full context. Writing out steps provides "external memory" — each step attends only to the previous step's output. Decision trees = cognitive offloading for branching. Chain-of-thought = cognitive offloading for reasoning. | P2 |
