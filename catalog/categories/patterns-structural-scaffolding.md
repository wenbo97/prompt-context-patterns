# Category 1: Structural Scaffolding

How a skill prompt is organized — the skeleton that holds everything together.

**Related foundational techniques:** Schema Priming, XML Tags for Semantic Boundaries (see [prompt-engineering-for-skills.md](prompt-engineering-for-skills.md))

---

## Pattern 1: YAML Frontmatter Metadata Block

**Prevalence:** ~100% of skills (2,290+ files)
**Related patterns:** [Activation Scope](#pattern-13), [Tool Routing Tables](#pattern-21)

**What it is:** A structured YAML block at the top of every SKILL.md that declares the skill's identity, trigger conditions, tool permissions, arguments, and (in advanced cases) input/output schemas. The frontmatter is parsed by the platform, not by the LLM — it controls what the skill CAN do before the model even sees the body.

**When to use:**
- Every skill must have frontmatter — it is the entry point
- Use `allowed-tools` to restrict tool access (least-privilege)
- Use `description` to tell the platform WHEN to activate this skill
- Add `input_schema` / `output_schema` for complex skills that need contract enforcement

### Positive Example
```yaml
---
name: specification-writing
description: "Use when writing a product spec, feature spec, API contract, agent task spec, or any other specification where a zero-question document is required. Encodes outcome-first methodology, acceptance criteria taxonomy, scope boundary protocol, executor context model, and ambiguity resolution framework."
version: "1.3.0"
type: "codex"
tags: ["Problem Shaping", "Execution"]
created: "2026-02-19"
valid_until: "2026-08-19"
derived_from: "shared/toolkits/skills/specification_writing.md"
tested_with: ["Claude Sonnet 4.6", "Claude Opus 4.6"]
license: "MIT"
capability_summary: "Produces a Zero-Question Specification where every assumption is surfaced, every ambiguity is resolved or explicitly marked TBD, every acceptance criterion is binary-testable, and every scope boundary names the adjacent capability it excludes."
input_schema:
  feature_or_capability: "string — what is being specified"
  spec_type: "enum[product_feature, api_contract, agent_task, process_workflow, infrastructure_migration, research_discovery]"
  outcome: "string — the desired user or business outcome"
  executor: "string — optional, who will build this"
  constraints: "string — optional, technical constraints, dependencies, timeline"
  prior_context: "string — optional, existing docs, prior specs, stakeholder decisions"
output_schema:
  outcome_definition: "What success looks like, with binary-testable criteria"
  scope: "In-scope items with explicit out-of-scope boundaries"
  acceptance_criteria: "Binary-testable criteria per requirement, tagged by confidence"
  dependencies: "External dependencies, blocking decisions, TBD items with owners"
  failure_conditions: "What happens when things go wrong, with mitigation strategies"
  assumption_registry: "Load-bearing assumptions with confidence annotations"
  zero_question_score: "Computed completeness score after Step 6 audit"
  self_critique: ">=3 genuine weaknesses in this specification"
---
```

**Why this works:** Every field serves a purpose. The `description` tells the platform exactly when to trigger. `input_schema` and `output_schema` create a contract — the model knows what it receives and what it must produce. Version tracking, test coverage (`tested_with`), and expiration (`valid_until`) support operational hygiene. The schema fields use typed definitions (`enum[...]`, `string — description`) that double as documentation.

### Negative Example

```yaml
---
name: spec-writer
description: Writes specs
---

Write a specification for whatever the user asks about. Make it detailed and comprehensive.
```

**Why this fails:** The `description` is too vague — the platform can't distinguish this from any other writing skill, leading to false activations. No input/output schema means the model invents different structures each run. No version, no expiration, no test record — impossible to track regressions. The body is a single vague sentence that gives the model no structure to follow.

---

## Pattern 2: Phased/Stepped Execution Flow

**Prevalence:** ~54% of skills (1,245 files)
**Related patterns:** [Confirmation Gates](#pattern-8), [Progress Feedback](#pattern-9), [Workflow Mode Branching](#pattern-3)

**What it is:** Breaking the skill into numbered, sequential phases or steps that must be executed in order. Each phase has a clear goal, specific actions, and defined outputs. This is the most dominant structural pattern for anything beyond trivial skills.

**When to use:**
- Any workflow with 3+ distinct stages
- When later stages depend on outputs from earlier stages
- When you need different error handling per stage
- When human checkpoints are needed between stages

### Positive Example
```markdown
## Phase 0: Language Detection

**Goal**: Determine the project's primary language to route to the correct pipeline

**Actions**:
1. Invoke `detect-project-language` skill
2. Read `.analysis/detect_project_language/language_detection.json`
3. If `primaryLanguage == "csharp"` → proceed to **C# Pipeline**
4. If `primaryLanguage == "powershell"` → proceed to **PowerShell Pipeline**
5. If `primaryLanguage == "unknown"` → stop and report to user

---

## C# Phase 1: Discovery

**Goal**: Understand file(s) that need to be reviewed

**Actions**:
1. Create todo list with all C# phases
2. Find .cs files under the target folder or belonging to the project

---

## C# Phase 2: Understand Codebase Architectures

**Goal**: Determine if the project is an internal infrastructure service and generate architecture context

**Actions**:
1. Check if INPUT's directory contains **src/sources** — if yes, it is internal infrastructure code
2. Use `understand-codebase-architecture` skill to understand the high-level architecture
3. Write a `architecture_{INPUT}.md` file to `.analysis/architecture/`

---

## C# Phase 3: Taint Analysis

**Goal**: Analyze each file for taint analysis and write security reports in parallel

**Actions**:
1. Launch taint-analyzer agents in parallel based on number of files, up to 64 agents
```

**Why this works:** Each phase has a named **Goal** (what), numbered **Actions** (how), and clear transition logic (when to proceed, when to stop). The Goal/Actions split means the model understands intent even if it needs to adapt the specific commands. Phase numbering creates a progress tracker the model can reference.

### Negative Example

```markdown
Analyze the code for security issues. First figure out what language it is, then look for
vulnerabilities. Check for taint analysis issues and also understand the architecture.
Write reports for everything you find. Make sure to be thorough and check all the files.
```

**Why this fails:** All actions are compressed into a single paragraph with no sequencing. The model can't tell what depends on what — does architecture understanding come before or after taint analysis? There's no stopping condition for language detection failure. "Be thorough" is not an executable instruction. Each run will execute steps in a different order with different thoroughness.

---

## Pattern 3: Workflow Mode Branching

**Prevalence:** ~5% of skills (100-150 files)
**Related patterns:** [Phased Execution](#pattern-2), [Intent Classification](#pattern-20), [$ARGUMENTS Pattern](#pattern-4)

**What it is:** Defining multiple execution modes within a single skill, each with different phase flows, guardrails, and output depth. The mode is selected based on the user's role, arguments, or context.

**When to use:**
- When the same skill serves different audiences (internal vs external)
- When you need a "quick" and "deep" mode
- When different roles need different guardrails (e.g., OCE gets gates, partners run uninterrupted)

### Positive Example
```markdown
## Mode: Partner vs OCE

| | **Partner mode** (default) | **OCE mode** |
|---|---|---|
| **User** | Customer/partner team | Cosmic App Deployment OCE |
| **Phases** | 0 → 1 → 2(a,b,c,f Step 1, Step 4) → 4 → 8 | 0 → 1 → 2 → 3 → 4 → 4.5 → 5 → 6 → 7 → 8 |
| **Gates** | None — runs end-to-end uninterrupted | G1, G2, G3, G4 |
| **ICM correlation** | Mandatory — runs automatically | Mandatory — runs automatically |
| **Phase 4.5 (deep dive)** | Skipped | On demand |
| **Phase 5 (mitigations)** | Skipped (platform-internal) | Full |
| **Phase 6/7 (PRs/TSGs)** | Skipped | On demand |
| **Report content** | Partner-friendly: error summary, TSG links, customer actions only | Full: all buckets, platform analysis, code traces |
| **R8/R9 rules** | Disabled — no hypothesis prompts | Enabled |
```

**Why this works:** A comparison table makes mode differences instantly scannable. Each dimension (phases, gates, report content, rule activation) is explicitly specified for both modes — no ambiguity about what's included or excluded. The default mode is marked, so the model doesn't need to guess when no mode is specified.

### Negative Example

```markdown
If the user is a partner, make the output simpler and skip the technical details.
If the user is an OCE engineer, include everything. Use your judgment about what
to include based on who you think the user is.
```

**Why this fails:** "Simpler" and "everything" are undefined. "Use your judgment" creates non-deterministic behavior — each run will include/exclude different sections. There's no way to verify which mode was selected or whether the right phases executed. The model must infer the user's role rather than having it declared.

---

## Pattern 4: $ARGUMENTS Variable Pattern

**Prevalence:** ~7% of skills (169 files)
**Related patterns:** [Configuration Persistence](#pattern-16), [Intent Classification](#pattern-20)

**What it is:** Using the platform-injected `$ARGUMENTS` placeholder to receive user input at invocation time, then parsing it for structured data, flags, and options.

**When to use:**
- When the skill accepts command-line-style arguments
- When you need flags to toggle behavior (e.g., `--json`, `--force`)
- When the skill needs a target (URL, file path, identifier) passed inline

### Positive Example
```markdown
## Arguments
$ARGUMENTS

Parse the arguments. Also check for these flags:
- `--json` — generate structured JSON output (see Step 7.8)
- `--force` — force a full review, ignoring cache and skipping early returns
- `--api-only` — skip local repo detection, use ADO API for everything
```

**Why this works:** The flags are enumerated with exact names and clear effects. Each flag maps to a specific behavioral change referenced later in the skill (Step 7.8 for JSON output). The model knows exactly what to look for in the arguments string and what each flag means.

### Negative Example

```markdown
The user will provide some arguments. Parse them and figure out what they want.
Handle any options they might pass.
```

**Why this fails:** No flag names are defined, so the model invents its own argument syntax. "Figure out what they want" is an open-ended NLU task, not argument parsing. There's no connection between parsed flags and skill behavior — even if the model parses correctly, it doesn't know what to do with the results.
