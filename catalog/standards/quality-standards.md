# Prompt Engineering Quality Standards

> **SSOT for prompt writing techniques, anti-patterns, and style guide.**
> Referenced by: `commands/dev-prompt.md`, `commands/dev-prompt-review.md`.
> **Examples:** Read @../prompt-examples/template.md for a detailed good vs bad prompt comparison with line-by-line analysis — study this before writing or reviewing any prompt.

These standards operationalize research-backed prompt engineering techniques for this plugin's autonomous migration agents. Each principle includes the **why** (the model behavior it exploits or avoids), **when** (the specific plugin context where it applies), and **how** (the concrete pattern to use).

> **Sources (read for deep understanding before writing or reviewing prompts):**
>
> | Source | What to Learn From It |
> |--------|----------------------|
> | [Claude Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) | **Primary reference.** Clarity principles, XML structuring, few-shot design, role prompting, long-context ordering, adaptive thinking, subagent orchestration, parallel tool calling, and Claude 4.6-specific migration guidance (reduced anti-laziness prompting, overtrigger avoidance). |
> | [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices) | CLAUDE.md design (what to include/exclude, conciseness rules), verification-first development, context window management (the #1 constraint), subagent delegation for context isolation, session management, and parallel scaling. |
> | [Prompt Engineering Guide](https://www.promptingguide.ai/techniques) | 18 techniques catalog. Most relevant to this plugin: few-shot, chain-of-thought, prompt chaining, ReAct (reason+act loops), reflexion (learning from past failures), self-consistency (multiple reasoning paths). |
> | [Claude Code System Prompts](https://github.com/Piebald-AI/claude-code-system-prompts) | 110+ modular micro-prompts (16–102 tokens each), adversarial verification specialist pattern, two-layer security (evaluator + policy engine), fork-safe delegation (workers cannot spawn workers), conditional prompt assembly by agent role. |
> | [Claude Code Sub-Agents](https://github.com/dl-ezo/claude-code-sub-agents) | Trigger-rich descriptions (3–5 trigger scenarios per agent), narrowly-scoped single-concern agents, explicit output contracts, master coordinator pattern (orchestrate but never do specialist work). |
> | [Anthropic Prompt Engineering Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) | Few-shot exemplar selection, chain-of-thought elicitation, structured output enforcement, hallucination reduction via grounding. |

---

## Principle 1: Be Clear and Direct — Eliminate Inference

**Why it works:** Claude responds to explicit instructions. Vague prompts force the model to infer intent, producing inconsistent behavior across runs. The golden rule from Anthropic: "Show your prompt to a colleague with minimal context on the task and ask them to follow it. If they'd be confused, Claude will be too."

**When to apply:** Every instruction in every file.

**How to apply:**

| Pattern | Bad (agent infers) | Good (agent follows) |
|---------|-------------------|---------------------|
| Imperative mood | "You might want to check the csproj" | "Read the target csproj. If `<TargetFrameworks>` is absent, stop — this is a legacy CoreXT project." |
| Specific format | "Add the package" | "Add `<PackageReference Include=\"System.Configuration.ConfigurationManager\" />` to the .NET Core conditioned ItemGroup (`!= '{conditionTFM}'`)." |
| Explicit fallback | "If the build fails, handle it" | "If `build` returns `Build FAILED`, extract all CS*/MSB*/NU* error codes from the output. If no error codes found, classify as `infra_error`." |
| Context/motivation | "NEVER use git amend" | "NEVER use git amend — the build-repair loop may fail and retry, so amending would destroy the previous commit's safe state." |

**Claude 4.6 note:** Claude 4.6 is more responsive to system prompts than previous models. If your prompts were designed to reduce undertriggering on tools or skills, dial back aggressive language. Where you might have said "CRITICAL: You MUST use this tool when...", use normal prompting: "Use this tool when..."

---

## Principle 2: Few-Shot Examples — Show, Don't Describe

**Why it works:** Examples are the most reliable way to steer output format, tone, and structure. 3–5 well-crafted examples dramatically improve accuracy and consistency. Wrap examples in `<example>` tags so Claude distinguishes them from instructions.

**When to apply:** Critical operations — tool calls with specific parameters, output JSON format, complex classification decisions, csproj XML transformations.

**How to construct examples:**

1. **Relevant** — mirror actual migration scenarios (not hypothetical). Use real package names, real csproj structures, real error messages from this plugin.
2. **Diverse** — cover the happy path AND at least one edge case. If the decision has 3 branches, show 2–3 examples covering different branches.
3. **Structural** — show the exact XML/JSON/command, not a prose description of it.

**Example of a good few-shot (for NU1701 handling):**

```xml
<examples>
<example>
<scenario>OrchestrationSDK triggers NU1701 — no REPLACE mapping exists</scenario>
<before>
<ItemGroup>
  <PackageReference Include="OrchestrationSDK" />
</ItemGroup>
</before>
<after>
<ItemGroup Condition="'$(TargetFramework)' == 'net472'">
  <PackageReference Include="OrchestrationSDK" />
</ItemGroup>
<ItemGroup Condition="'$(TargetFramework)' != 'net472'">
  <!-- NU1701: OrchestrationSDK targets net472 only; suppress fallback warning -->
  <PackageReference Include="OrchestrationSDK" NoWarn="NU1701" PrivateAssets="all" />
</ItemGroup>
</after>
</example>
</examples>
```

**Target:** 100–300 tokens per example. Show exact input/output, not abstract patterns.

---

## Principle 3: Chain of Thought — Structure Multi-Step Decisions

**Why it works:** Multi-step decisions described as prose are unreliable — agents may skip steps or reorder them. Numbered sequences with explicit if/else at each decision point force sequential execution.

**When to apply:** Error classification, dependency resolution, tier selection, status routing.

**How to apply:** Structure as numbered steps where each step has a concrete check and explicit branches:

```
1. Read the error code from build output.
2. If error code matches SUPPRESSIBLE (PackageReference) list per @../skills/error-handling-rules.md → add NoWarn at PackageReference level.
3. If error code matches SUPPRESSIBLE (PropertyGroup) list per @../skills/error-handling-rules.md → add <NoWarn> in .NET Core PropertyGroup.
4. If error code is CS* (except CS8981) → classify as MUST FIX. Proceed to Tier selection.
5. Otherwise → log "Unknown error code: {code}" and continue to next error.
```

**Never:** "Classify the error and apply the appropriate fix." (agent must infer the classification logic)

---

## Principle 4: Prompt Chaining — Explicit Phase Contracts

**Why it works:** Each phase produces outputs that the next phase consumes. Undocumented handoffs cause silent field-name mismatches. Document the output schema at the END of each phase and the input table at the START of the next.

**When to apply:** Phase transitions (0→1→2→3→4), agent boundaries (orchestrator→dotnet-migrator→build-repair-agent→ado-agent), skill sequence handoffs.

**How to apply:**

- End every phase/agent/skill with an **Output** section: field name, type, possible values
- Start every phase/agent/skill with an **Input** section: parameter name, type, required/optional, source (which phase/agent produces it)
- Use the contract defined in `rules/phase-data-contract.md` — never invent ad-hoc variable names

**Self-test:** For every Output field, grep the downstream consumer. If the consumer does not reference that exact field name, the contract is broken.

---

## Principle 5: Grounding — Force Reading Over Remembering

**Why it works:** Claude's context window degrades with length. Agents that "remember" rules from earlier in the conversation may misremember. Forcing a read of the authoritative file at the point of decision ensures accuracy.

**When to apply:** Error resolution, package mapping, dependency classification, status routing.

**How to apply:**

- "Read @../rules/nu1701-handling.md before adding NoWarn to any PackageReference."
- "Check @../issue-and-solution/runtime-solution/issue-map-index.md for this error code BEFORE searching ADO."
- Inline the critical value AND reference the SSOT: `NoWarn="NU1701" PrivateAssets="all" (per @nu1701-handling.md)`

**Anti-pattern:** "Per @file for details" without inlining the key value. Agent must follow 2+ hops and may skip or improvise. Always inline the action, then cite the source.

---

## Principle 6: Long-Context Ordering — Put Data First, Instructions Last

**Why it works:** Anthropic testing shows queries at the end of long-context prompts improve response quality by up to 30%. For this plugin, putting reference data (package maps, project maps, error tables) at the top and decision logic at the bottom produces more accurate classifications.

**When to apply:** Skills that load large reference files (package-map.md, project-map-list.md, issue-solutions.md).

**How to apply:**

1. Load reference data via `@` references early in the file
2. Place the decision logic (numbered steps) after the data
3. For skills with 200+ lines: split data into a separate file, compose via `@` reference

---

## Principle 7: Self-Verification — Every Check Needs a Command

**Why it works:** Without executable verification, agents rationalize success: "the code looks correct" is not a check — it's a skip. Claude Code best practices: "Claude performs dramatically better when it can verify its own work."

**When to apply:** After every build, every git operation, every PR creation, every csproj modification.

**How to apply:**

Every `<self-check>` item must specify:
1. A **command** to run (or tool to invoke)
2. The **expected output** that constitutes PASS
3. The **failure action** if the output doesn't match

```
<self-check>
- [ ] Run `git status --porcelain` with pathspec from @git-exclusions.md — output shows modified files → PASS. Empty → exit with Aborted_NoChanges.
- [ ] Read the target csproj — contains `<TargetFrameworks>` with both `{previousTFM}` and `{netCoreTargets}` → PASS. Missing either → FAIL, stop and report.
</self-check>
```

**Never:** "- [ ] Verify the csproj is valid" (no command, no expected output — agent will skip)

---

## Principle 8: Role Prompting — One Sentence, First Position

**Why it works:** A role statement in the first sentence focuses Claude's behavior and tone. Even a single sentence makes a difference (per Anthropic docs).

**When to apply:** Agent definitions (frontmatter + opening line). Not needed in skills (skills are tools, not personas).

**How to apply:** "You are a {role} that {primary responsibility}." Keep it to one sentence. The role frames all subsequent instructions.

```
You are a diagnostic build engineer responsible for analyzing .NET build failures and applying fixes within 7 attempts.
```

**Never:** Multi-paragraph backstory or motivational text. The role is a framing device, not a character sheet.

---

## Principle 9: Fork-Safe Delegation — Pass Everything, Assume Nothing

**Why it works:** Subagents and forked agents start with zero parent context. Claude Code's system prompts enforce a strict delegation hierarchy: Main Agent → Coordinator → Worker (terminal, no further forks). Workers receive all required values as explicit parameters.

**When to apply:** Every orchestrator→agent boundary (Phase 1 → dotnet-migrator, Phase 3 → build-repair-agent, Phase 4 → ado-agent).

**How to apply:**

- Pass ALL required values as explicit parameters — never reference "the value from Phase 0" without passing it
- Show the exact tool invocation with actual parameter values at the point of use
- "Terse, command-style prompts produce shallow, generic work" — brief subagents thoroughly with context, constraints, and expected output format

**Test:** Remove the parent conversation from context. Can the child agent still execute correctly with only its Input parameters? If not, a parameter is missing.

---

## Principle 10: Behavioral Guardrails — Short, Tiered, Negative+Positive

**Why it works:** Claude Code's internal guardrails average 47 tokens each — precise and surgical. Long prose paragraphs are skimmed under context pressure. Tables and lists are parsed reliably.

**When to apply:** Constraining agent scope, preventing common mistakes, enforcing "do no harm" rules.

**How to apply:**

1. State what the agent MUST NOT do alongside what it should do
2. Keep each guardrail to 30–60 tokens
3. Group by severity tier: MUST > SHOULD > PREFER (per `rules/never-always-rules.md`)
4. Use a table or bullet list, one rule per row

**Claude 4.6 note:** Claude 4.6 has a tendency to overengineer — creating extra files, adding unnecessary abstractions. Counter with explicit scope constraints: "Only make changes that are directly requested. Do not add features, refactor code, or make 'improvements' beyond what was asked."

---

## Principle 11: Adaptive Subagent Orchestration

**Why it works:** Claude 4.6 has significantly improved native subagent orchestration — it proactively delegates work without explicit instruction. But it may spawn subagents when a direct grep/read is faster.

**When to apply:** When writing orchestrator-level prompts (CLAUDE.md, agent definitions).

**How to apply:**

- Let Claude orchestrate naturally for genuinely parallel tasks
- Add explicit guidance to prevent over-delegation: "For simple file reads, single-file edits, or sequential operations, work directly rather than delegating to subagents."
- Use subagents for context isolation (build investigation, codebase exploration) — keeps main conversation clean
- Each subagent should own exactly one concern (per Claude Code Sub-Agents pattern)

---

## Principle 12: ReAct Pattern — Reason Then Act Then Observe

**Why it works:** The build-repair-agent already uses this pattern implicitly: think about the error → apply a fix → observe the build result → repeat. Making it explicit prevents agents from applying fixes without diagnosis or skipping observation.

**When to apply:** Build-repair loops, error investigation, search-first resolution.

**How to apply:**

```
For each build error:
1. REASON: What is the root cause? Check issue-map-index.md, then ADO search.
2. ACT: Apply the specific fix (Tier 1/2/3/4 per code-fix-tiers.md).
3. OBSERVE: Rebuild. Parse the output for the same error code.
4. If error persists with same code → the fix was wrong. Try a different approach.
5. If error is gone but new errors appeared → continue to next error.
```

---

## Principle 13: Reflexion — Learn From Past Session Failures

**Why it works:** The `issue-map-index.md` cache IS a reflexion loop — it stores fixes from previous migration sessions so future sessions don't repeat the same investigation. Making this pattern explicit ensures new fixes are always recorded.

**When to apply:** Phase 3 build-repair — checking the cache before ADO search, recording new fixes after the loop.

**How to apply:**

- Step 0 in search-first-strategy.md: check the cache FIRST
- After the build loop completes: record new error/fix pairs per issue-format-guide.md
- Supersede ineffective cached fixes with new entries (per issue-format-guide.md Rule 4)

---

## Anti-Patterns — What Causes Agents to Fail

| Anti-Pattern | Model Behavior It Exploits | Concrete Failure in This Plugin | Fix |
|--------------|---------------------------|--------------------------------|-----|
| **Vague imperatives** ("Consider...", "Try to...", "You might...") | Claude treats hedged language as optional; skips under context pressure | Agent skips NU1701 suppression because instruction said "consider adding NoWarn" | Direct command: "Add `NoWarn=\"NU1701\"` to the PackageReference in the .NET Core group." |
| **Missing else/otherwise** | Claude invents fallback behavior when no branch is specified | Agent encounters unknown error code, invents a fix because no "otherwise" clause exists | Every `if/when` must have explicit `else/otherwise`: "Otherwise, log the error and continue." |
| **Undocumented output schema** | Next consumer guesses field names and types; silent mismatches | Phase 3 returns `buildStatus` but Phase 4 expects `LocalBuildStatus` — field is silently null | Formal Output table at end of every agent/skill with field name, type, possible values. |
| **Reference hop without inline value** ("Per @file for details") | Agent must follow 2+ hops; may skip under context pressure | Agent skips reading nu1701-handling.md and improvises NU1701 placement in common group | Inline the critical value at point of use AND cite the source: `NoWarn="NU1701" PrivateAssets="all" (per @nu1701-handling.md)` |
| **Context inheritance assumption** | Forked agents start fresh with zero parent context | Build-repair-agent doesn't know `netCoreTargets` because orchestrator assumed it inherited from Phase 0 | Pass all values as explicit Input parameters. Test: can the agent work with only its Input table? |
| **Monolithic prompt (>300 lines)** | Agent prioritizes early content, skims or ignores late sections (context dilution) | Rules in the bottom third of a 400-line skill file are applied inconsistently | Split into focused files composed via `@` references. One file = one concern. Target: <200 lines per file. |
| **Tool name without parameters** ("use search_code") | Agent guesses parameters; uses wrong project name or missing filters | Agent calls `search_code` with `project: "ControlPlane"` instead of `project: "O365 Core"` | Show the exact tool invocation: `search_code(searchText: "WorkflowSDK AND TargetFrameworks ext:csproj", project: ["O365 Core"], repository: ["ControlPlane"], top: 15)` |
| **Guardrails as prose paragraphs** | Agents extract rules from tables/lists reliably; they skim prose | Agent misses the "do not add packages to common group" rule buried in a paragraph | One rule per table row or bullet. 30–60 tokens each. |
| **Skipped verification** ("the code looks correct") | Agent rationalizes success without running a check | Agent declares csproj valid without parsing it — corrupt XML propagates to PR | Every self-check: command + expected output + failure action. No "verify it works" without a command. |
| **Over-prompting for thoroughness** (Claude 4.6 specific) | Claude 4.6 is significantly more proactive than predecessors; anti-laziness prompting causes overtriggering | Agent reads 50+ files during Phase 0 analysis because prompt says "be thorough" | Remove "If in doubt, use [tool]" language. Replace blanket "Default to using [tool]" with "Use [tool] when it would enhance your understanding of the problem." |

---

## Redundancy for Reliability

Certain instructions benefit from **intentional duplication** across files to ensure agents follow them even when the SSOT file isn't loaded in context. This is distinct from SSOT violations (unintentional duplication of **rules** that drift apart).

**What to duplicate (values at point of use):**
- Critical format strings (PR titles, commit messages) — inline the exact format AND reference the SSOT
- Tool call patterns (which tool, which parameters) — show the exact invocation at the point of use
- Error handling defaults ("log and continue", "stop and report") — restate at each decision point

**How to mark intentional redundancy:** Add `(per @SSOT-file)` attribution after the inlined value. This signals to reviewers that the duplication is intentional and which file is authoritative if they diverge.

---

## Prompt Style Guide

### Structure Rules

| Rule | Why (model behavior) | How |
|------|---------------------|-----|
| **One file, one concern** | Multi-concern files force irrelevant content into context; agents load files on demand | `rules/nu1701-handling.md` handles NU1701 only — not all package warnings |
| **Lead with the action, not the context** | Claude extracts the first imperative and may skim background. Putting "why" before "what" buries the instruction. | "Add `NoWarn="NU1701"` to the PackageReference. This suppresses..." — not the reverse |
| **Tables over prose for decisions** | Tables are parsed row-by-row reliably; prose paragraphs with embedded conditions are fragile under context pressure | Status handlers, error categories, package mappings — all use tables. Continue this pattern. |
| **Numbered steps for sequences** | Claude follows numbered sequences more reliably than paragraph-embedded sequences | "1. Read the csproj. 2. Find the ItemGroup. 3. Add the PackageReference." |
| **Bullets for unordered constraints** | Numbered lists imply sequence; bullets imply "all of these, in any order" | Use bullets for guardrails, exclusion lists, "any of these" conditions |
| **Long data at the top, query at the bottom** | Queries at the end of long-context prompts improve response quality by up to 30% (Anthropic testing) | Put package maps, project maps, error tables near the top; put decision logic after |

### Prompt Size Discipline

| File Type | Target | Hard Max | If Over Limit |
|-----------|--------|----------|---------------|
| Agent definition (`agents/*.md`) | ≤200 lines | 260 lines | Extract reference content into `rules/` or skill resource files; `@` reference from agent |
| Command definition (`commands/*.md`) | ≤200 lines | 260 lines | Extract reference content into `rules/` or `skills/` resource files; `@` reference from command |
| Skill definition (`skills/*/SKILL.md`) | ≤200 lines | 300 lines | Extract data tables, examples, or mappings into sibling resource files within the skill folder; `@` reference from SKILL.md |
| Rule file (`rules/*.md`) | ≤200 lines | 300 lines | Split into focused files by sub-topic; `@` reference from parent |

**Extraction pattern:** When a file exceeds its limit, identify the largest self-contained section (reference tables, examples, quality standards, output templates). Create a new file in the natural home directory (`rules/` for shared content, skill folder for skill-specific data). Replace the section with a concise `@` reference (1–3 lines) that states what the referenced file contains and when to read it.

### Token Economy

Claude Code's behavioral guardrails average **47 tokens each**. This plugin should follow the same economy:

| Component | Target Length | Why |
|-----------|-------------|-----|
| Single guardrail rule | 30–60 tokens | Precise enough to be unambiguous, short enough to survive context pressure |
| Skill description (frontmatter) | 50–150 tokens | Must include trigger phrases, when-NOT-to-use, and one usage example |
| Input/Output parameter row | 20–40 tokens per row | Name, type, required, source — no prose |
| Self-check item | 20–50 tokens | Command + expected output + failure action |
| Few-shot example | 100–300 tokens per example | Exact input/output, not abstract patterns |
| Agent role statement | 15–30 tokens | One sentence. "You are a {role} that {responsibility}." |

### Agent Definition Pattern

```
1. Role statement (1 sentence — "You are a [role] that [primary responsibility].")
2. Context block (environment variables, @references, configuration)
3. Input block (parameters table — name, type, required, source)
4. Constraints block (guardrails as bullets/table, tiered MUST > SHOULD > PREFER)
5. Steps block (numbered instructions, decision tables with if/else at every branch)
6. Self-check block (postcondition checklist — command + expected output per item)
7. Output block (field table — name, type, possible values)
```

### Skill Definition Pattern

```
1. Frontmatter (name, description with 3-5 trigger phrases and when-NOT-to-use)
2. Purpose (1-2 sentences — what this skill does and when it's a NO-OP)
3. Input parameters table (name, type, required/optional, source)
4. Steps (numbered, with explicit if/else at each decision point)
5. Examples (1-2 before/after — happy path + one edge case, using real package/project names)
6. Verification (command + expected output + failure action)
7. Output table (field name, type, possible values)
```

### Writing Checklist

Before finalizing any prompt file, verify these minimum quality bars:

- [ ] Every `if/when` has an explicit `else/otherwise` — no dangling conditions
- [ ] Every agent/skill has formal Input and Output tables — no guessing
- [ ] Every critical operation has at least one few-shot example with real values — not abstract
- [ ] Every multi-step decision uses numbered steps — not prose paragraphs
- [ ] Every guardrail is ≤60 tokens and uses imperative mood — not "consider" or "try to"
- [ ] Every `@` reference is verified to point to an existing file — use Glob to check
- [ ] Every tool invocation shows exact parameters (tool name + every required param + expected response shape)
- [ ] File stays within size limits (per Prompt Size Discipline table above)
- [ ] Description frontmatter includes 3–5 trigger phrases and 1–2 when-NOT-to-use phrases
- [ ] Every self-check item has a command to run and expected output — no "verify it works"
- [ ] No over-prompting for thoroughness — replace "MUST use this tool" with natural guidance for Claude 4.6
