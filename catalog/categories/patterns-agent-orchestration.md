# Category 5: Agent Orchestration

How multiple agents coordinate — topologies, skill composition, intent routing, tool mapping, and consensus.

**Related foundational techniques:** Cognitive Offloading, Token-Action Binding (see [prompt-engineering-for-skills.md](../techniques/token-level-techniques))

---

## Pattern 18: Multi-Agent Orchestration / Agent Topologies

**Prevalence:** ~2% of skills (30-50 true orchestrations out of 857 agent-referencing files)
**Related patterns:** [Skill Composition](#pattern-19), [Deduplication/Consensus](#pattern-22), [Tool Routing Tables](#pattern-21)

**What it is:** Defining how multiple AI agents coordinate — spawning subagents, routing between agents, establishing communication protocols, and merging results. The topology defines the shape of the agent graph.

**When to use:**
- When a single agent can't produce reliable results (use cross-model consensus)
- When the task has independent dimensions that benefit from parallel analysis
- When adversarial validation improves output quality (one agent challenges another)
- When scale requires it (reviewing 100+ files in parallel)

### Positive Example
```markdown
## Architecture Overview

This skill uses a **multi-agent ensemble architecture** that combines cross-model
diversity (Tier 3) with adversarial validation (Tier 2):

Orchestrator (this agent — Opus)
  |
  +- Phase 0: Setup & Context Gathering
  |
  +- Phase 1: Spawn 8 parallel dimension pipelines
  |    |
  |    +- Per dimension (x8 in parallel):
  |         +- 2 Context Builders (Sonnet + Gemini) — gather relevant code, union merge
  |         +- 3 Analyzers in parallel:
  |         |    +- Model A: Claude Opus
  |         |    +- Model B: GPT-5.2-Codex
  |         |    +- Model C: Gemini Pro
  |         +- Validator (Opus) — adversarial consensus judge
  |
  +- Phase 2: Synthesis Ensemble
  |    +- 3 Synthesizers in parallel (Opus, GPT-5.2-Codex, Gemini Pro)
  |    +- Synthesizer Validator (Opus) — consensus merge & dedup
  |
  +- Phase 3: Report Writer (Opus) — final Markdown report
  |
  +- Phase 4: Action Mode (if mode="act") — fix, commit, push

**Total agents per review: ~55**

### Consensus Scoring

| Agreement | Action |
|-----------|--------|
| 3/3 models | `[high]` confidence — almost certainly real |
| 2/3 models | Accept — verify specifics, `[medium]`+ confidence |
| 1/3 models | Adversarially challenge — keep only if it survives scrutiny |
```

**Why this works:** The topology is visualized as a tree diagram — the orchestrator can see the full shape of the agent graph. Each node specifies which model runs it, creating cross-model diversity (Claude, GPT, Gemini). The consensus scoring table gives deterministic rules for merging disagreements. Agent counts are stated so the orchestrator knows the expected scale. The phased structure prevents agents from conflicting — context building completes before analysis begins.

### Negative Example

```markdown
Use multiple agents to review the code. Have them analyze different aspects and then
combine the results. Make sure they don't duplicate findings.
```

**Why this fails:** No topology defined — the model doesn't know how many agents, what roles, or what models. "Different aspects" doesn't enumerate dimensions. "Combine the results" has no merge strategy. "Don't duplicate" has no dedup algorithm. The orchestrator will spawn an arbitrary number of agents with overlapping scopes and no consensus mechanism. Each run produces a different agent graph.

---

## Pattern 19: Skill Composition / Cross-Skill Invocation

**Prevalence:** ~4% of skills (100+ files)
**Related patterns:** [Multi-Agent Orchestration](#pattern-18), [Intent Classification](#pattern-20), [Activation Scope](#pattern-13)

**What it is:** One skill explicitly invoking or delegating to another skill, creating a workflow pipeline where each skill handles a specific phase of a larger task.

**When to use:**
- When functionality already exists in another skill (DRY principle)
- When a workflow has phases that different skills specialize in
- When you want a routing skill that dispatches to specialist skills
- When combining skills from different plugins into a pipeline

### Positive Example
```markdown
## Execution Workflow

### PHASE 1: THREAT MODELING (Automatic)

**Action:** Invoke the `security-threat-modeler` skill from ai-starter-pack plugin

**Instructions:**
1. Change working directory to the repository path provided
2. Invoke the skill: `security-threat-modeler`
3. The ai-starter-pack's security-threat-modeler will:
   - Analyze codebase architecture
   - Generate comprehensive STRIDE threat model
   - Identify trust boundaries and data flows
   - Output threat model to `{repo_name}_Threats.csv`
4. Read the generated threat model CSV into memory for Phase 2

**Expected Output from security-threat-modeler:**
- Threat model CSV file with all identified threats
- Each threat includes: Title, Category, Priority, Description, Affected Component,
  Mitigation, CVSS Score, Location

**Important:** DO NOT duplicate the security-threat-modeler functionality. Always invoke
the existing skill from ai-starter-pack.
```

**Why this works:** The delegation is explicit — names the exact skill and plugin. Expected outputs are documented so this skill knows what to consume. The "DO NOT duplicate" instruction prevents the model from re-implementing the threat modeler inline. Working directory setup ensures the invoked skill has the right context. The output file path is specified so Phase 2 knows where to read from.

### Negative Example

```markdown
First do threat modeling, then do security review. You might want to use some
existing tools for the threat modeling part.
```

**Why this fails:** "Might want to use existing tools" is not a delegation — the model will attempt to do threat modeling itself. No skill name, no plugin name, no expected output format. The model either re-implements threat modeling (poorly) or skips it. No output handoff mechanism means the security review phase doesn't know what data is available from the threat modeling phase.

---

## Pattern 20: Intent Classification / Smart Routing

**Prevalence:** ~6% of skills (100-150 files)
**Related patterns:** [Workflow Mode Branching](#pattern-3), [Activation Scope](#pattern-13), [$ARGUMENTS Pattern](#pattern-4)

**What it is:** Analyzing the user's input and routing to the appropriate sub-skill, workflow mode, or pipeline based on keyword matching, URL parsing, content analysis, or language detection.

**When to use:**
- When a single skill entry point serves multiple sub-workflows
- When the routing depends on analyzing the input (not just flags)
- When different programming languages need different analysis pipelines
- When the skill needs to parse URLs to determine the target platform (ADO vs GitHub)

### Positive Example
```markdown
# Enhanced SAST Security Review V2 Command

This command auto-detects the project's primary language and routes to the appropriate
workflow:

- **C# projects** → Agent-driven taint analysis with CodeQL verification + critic re-triage
- **PowerShell projects** → Parallel security analysis with critic re-triage

## Phase 0: Language Detection

**Goal**: Determine the project's primary language to route to the correct pipeline

**Actions**:
1. Invoke `detect-project-language` skill
2. Read `.shield_security/detect_project_language/language_detection.json`
3. If `primaryLanguage == "csharp"` → proceed to **C# Pipeline**
4. If `primaryLanguage == "powershell"` → proceed to **PowerShell Pipeline**
5. If `primaryLanguage == "unknown"` → stop and report to user
```

**Why this works:** The routing is deterministic — read a JSON file, check a field, branch to a named pipeline. The "unknown" case is handled (stop and report, not guess). The routing happens in Phase 0 before any analysis begins, so no work is wasted. Each pipeline is a fully specified workflow (C# has 8 phases, PowerShell has its own). The detection is delegated to a dedicated skill rather than using heuristics.

### Negative Example

```markdown
Figure out what kind of project this is and analyze it appropriately.
Use the right tools for the language.
```

**Why this fails:** "Figure out what kind" requires the model to implement language detection from scratch. "Appropriately" is undefined per language. No branching structure means the model might apply C# analysis to PowerShell code. No handling for unrecognized languages means the model either guesses or silently produces garbage results.

---

## Pattern 21: Tool Routing Tables

**Prevalence:** ~16% of skills (358 files reference `allowed-tools`; 200+ have internal routing)
**Related patterns:** [Negative Constraints](#pattern-6), [YAML Frontmatter](#pattern-1), [Multi-Agent Orchestration](#pattern-18)

**What it is:** A lookup table mapping tasks to specific tools, with an explicit "NOT these" column listing prohibited alternatives. Prevents the agent from using the wrong tool for a given operation.

**When to use:**
- When multiple tools could superficially handle the same task but with different reliability
- When general-purpose Q&A tools exist alongside precise query tools
- When past failures were caused by using the wrong tool
- When the skill interacts with many MCP servers

### Positive Example
```markdown
## Tool Routing — MANDATORY

Use ONLY the tools listed below for each task. Do NOT use `mcp__workiq__ask_work_iq`,
`es_chat`, or any general-purpose Q&A tool as a substitute — they return unreliable,
unstructured results.

| Task | Tool(s) | NOT these |
|------|---------|-----------|
| **Search code by keyword** | `mcp__bluebird__search_file_content` | workiq, es_chat, WebSearch |
| **Read source files** | `mcp__bluebird__get_file_content` | workiq |
| **Find files by path** | `mcp__bluebird__search_file_paths` | workiq |
| **Search commits** | `mcp__ado__repo_search_commits` | workiq |
| **Fetch PRs** | `mcp__ado__repo_list_pull_requests_by_repo_or_project` | workiq |
| **Fetch bug data** | `mcp__ado__wit_get_work_item` | workiq |
| **Download attachments** | `Bash` (curl with ADO bearer token) | workiq |
| **Analyze crash dumps** | `Bash` (CDB — see Phase 1c) | workiq |
| **View screenshots** | `Read` (supports PNG, JPG) | workiq |
```

**Why this works:** The three-column table (Task / Tool / NOT these) makes the routing unambiguous. The "NOT these" column explicitly blocks the model's tendency to use general-purpose tools (workiq, es_chat) that return unreliable results. The rationale is stated upfront ("unreliable, unstructured results"). Tool names use exact MCP identifiers, not descriptions. Even non-obvious tools are included (screenshots → `Read`, crash dumps → `Bash` with CDB).

### Negative Example

```markdown
Use the appropriate tools to investigate the bug. You have access to code search,
work item tracking, and various other tools. Pick the best one for each task.
```

**Why this fails:** "Appropriate" and "best" require the model to evaluate tool quality — it will default to familiar general-purpose tools (workiq) even when precision tools exist. No prohibited tools means the model freely uses unreliable Q&A endpoints for structured queries. No mapping means the model might use a work item search tool to search code, or a code search tool to find PRs.

---

## Pattern 22: Deduplication / Consensus Algorithms

**Prevalence:** ~1% of skills (20-30 files)
**Related patterns:** [Multi-Agent Orchestration](#pattern-18), [Scoring Rubrics](#pattern-27)

**What it is:** Defining explicit algorithms for deduplicating findings across multiple agents or analysis passes, typically using weighted similarity scoring with defined thresholds.

**When to use:**
- Multi-agent reviews where agents may report the same issue
- Cross-batch analysis where findings need merging
- Comparison against existing comments/findings to avoid duplicates
- Any workflow producing findings that need de-duplication

### Positive Example
```markdown
### Dedup Algorithm (Multi-Signal Fingerprinting)

Used wherever two findings are compared. Compute a match score:

| Signal | Weight | Match Criteria |
|--------|--------|---------------|
| File + Line proximity | 0.35 | Same file AND line within +/-5 lines |
| Code symbol reference | 0.25 | Both reference the same function/variable/class name |
| Issue category | 0.25 | Both address the same concern type (null-handling, security, perf) |
| Text similarity | 0.15 | Jaccard similarity on significant words (exclude stop words) |

**Thresholds (consistent everywhere):**
- **>= 0.7:** DUPLICATE — skip / do not post
- **0.5 – 0.7:** RELATED — reply to existing thread, or merge findings
- **< 0.5:** NEW — distinct finding

**Precedence:** Micy self-dedup (exact file+line within +/-3 lines + same severity + same
category) is a **HARD DUPLICATE** regardless of text similarity score. This deterministic
check runs FIRST, before the weighted scoring.

**Dedup execution order** (deterministic):
1. **Cross-batch dedup** (Step 5.3) — after all batches, MERGE duplicates across batches
2. **Cross-agent dedup** (Step 6) — MERGE duplicates across the 5 agents
3. **Vs-existing-comments dedup** (Step 6.75) — classify against existing PR threads
```

**Why this works:** The algorithm is fully specified: signals, weights, match criteria, thresholds, and execution order. The model can compute the score deterministically — no "use your judgment." Hard duplicate precedence prevents the weighted algorithm from keeping obvious duplicates. The execution order prevents order-dependent results (cross-batch before cross-agent before vs-existing). Threshold meanings are defined (skip vs merge vs keep).

### Negative Example

```markdown
Remove duplicate findings. If two agents report the same issue, only include it once.
Make sure related findings are grouped together.
```

**Why this fails:** "Same issue" is undefined — same file? Same category? Same wording? "Related" has no threshold. No algorithm means each run deduplicates differently. Some runs will aggressively merge distinct findings; others will keep near-duplicates. No execution order means dedup results depend on which agent's findings are processed first. No distinction between "duplicate" (skip) and "related" (merge).
