# Category 6: Knowledge and Context

How information is managed — reference files, domain knowledge, examples, and evidence requirements.

**Related foundational techniques:** Grounding/Anchoring, Few-Shot with Embedded Reasoning, Attention Locality (see [prompt-engineering-for-skills.md](../techniques/token-level-techniques))

---

## Pattern 23: Reference File / Knowledge Base Injection

**Prevalence:** ~17% of skills (390 files)
**Related patterns:** [Domain Knowledge Embedding](#pattern-24), [Few-Shot Examples](#pattern-25), [Tool Routing Tables](#pattern-21)

**What it is:** Pointing the agent to external reference files (JSON, markdown, KQL templates, lookup tables) that contain domain knowledge the skill needs at runtime. Rather than embedding all knowledge inline, the skill instructs the agent to read specific files before proceeding.

**When to use:**
- When domain knowledge is large enough to be maintained as separate files
- When knowledge is shared across multiple skills (DRY)
- When knowledge updates independently of the skill logic
- When lookup tables would make the skill file unwieldy

### Positive Example
```markdown
## Routing Tables

All team routing data is in **`references/team-routing-tables.md`**. Read that file before
attempting any match. It contains three lookup tables:

- **Table 1 — Team Descriptions**: Match team names or problem descriptions against the
  incident management path and Description columns.
- **Table 2 — InternalService to Incident Team**: Match InternalService service or application names
  to their owning incident team.
- **Table 3 — Process to Incident Team**: Match crashing process names to their owning incident team.

## Steps

### Step 1 — Match input to incident management path

Read `references/team-routing-tables.md` and apply the appropriate lookup:

1. If the user provides a **team name** → match directly against Table 1 incident management path column
2. If the user describes a **problem** → match keywords against Table 1 Description column
3. If the user names an **InternalService service** → look up in Table 2
4. If the user names a **crashing process** → look up in Table 3

If the input is ambiguous, present the top candidate matches and ask the user to confirm.
```
```markdown
## Reference Files

All in `references/` relative to this skill:

| Reference | Contents |
|-----------|----------|
| `mas-standards.json` | 16 MAS standards — _DID, _DetectionPatterns, _FixPrinciples, _CommonPatterns |
| `01-perceivable.md` | Code examples for alt text, semantic HTML, contrast, color |
| `02-operable.md` | Code examples for keyboard, focus, tab order, target size |
| `03-understandable.md` | Code examples for labels, errors, language, predictability |
| `04-robust.md` | Code examples for ARIA, roles, states, live regions |
```

**Why this works:** The file path is exact — the model doesn't search for it. The content summary tells the model what's in each file so it can decide which to read. The routing logic in Step 1 maps input types to specific tables, preventing the model from scanning all tables for every query. The a11y example uses a reference index pattern: one JSON file for structured data and separate markdown files for code examples, organized by WCAG category.

### Negative Example

```markdown
Look up the correct team routing information. There should be some reference
data available somewhere in the project. Check if there are any tables you can use.
```

**Why this fails:** "Somewhere in the project" forces the model to search the directory tree. "Some reference data" doesn't identify the file or its format. "Check if there are tables" makes the knowledge base optional — the model might skip it. No mapping from input type to table means the model uses brute-force matching across all data. Each run might read different files or skip the lookup entirely.

---

## Pattern 24: Domain Knowledge Embedding

**Prevalence:** ~22% of skills (500+ files)
**Related patterns:** [Reference File Injection](#pattern-23), [Few-Shot Examples](#pattern-25), [Scoring Rubrics](#pattern-27)

**What it is:** Embedding detailed domain-specific knowledge directly in the prompt — schema definitions, API field mappings, query syntax, classification rules, or command references. Unlike Pattern 23, the knowledge is inline rather than in external files.

**When to use:**
- When the knowledge is compact enough to embed (under ~100 lines)
- When the knowledge is tightly coupled to the skill logic (not reusable)
- When the model needs the knowledge in its immediate attention window
- When external file reads would add latency for small reference data

### Positive Example
```markdown
## Key Schema Fields

| Field | Description |
|-------|-------------|
| `DeploymentConfigurationItemType` | Type of override — determines its effect |
| `StartVersion` | Build version the override starts applying from |
| `EndVersion` | Build version the override stops applying (inclusive) |
| `TargetFilterExpression` | Scope: which machines/rings/roles it applies to |
| `IsDeleted` | `false` = currently active |
| `WhenCreated` | When the override was created |
| `CreatedBy` | Who created it |
| `Reason` | Why it was created |

## Blocking Override Types

These types are checked by the deployment gate system `DeploymentBlockRule`:

| DeploymentConfigurationItemType value | Effect |
|---------------------------------------|--------|
| `BlockAll` | Blocks all deployment to matching machines |
| `BlockProvisionedMachines` | Blocks deployment to provisioned machines |
| `Halt` | Halts deployment of specific version range |
| `HaltAndStop` | Halts and stops any in-progress deployment |
| `Purge` | Rolls back to previous version |
| `PurgePreferSxSRollback` | Rolls back using side-by-side method |

## Common Filters

| Filter | KQL |
|--------|-----|
| Active only | `where IsDeleted == false` |
| Blocking types only | `where DeploymentConfigurationItemType in ("BlockAll",...)` |
| By start version | `where StartVersion == "1.2.3456.007"` |
| By ring | `where TargetFilterExpression has "global"` |
```

**Why this works:** Schema fields are documented with types and descriptions — the model can construct valid queries. The blocking override types are exhaustively listed with effects — no guessing which types are "blocking." Common filters provide ready-to-use KQL fragments that the model can compose. The knowledge is structured as tables, which the model can scan efficiently. Every field name is the exact string used in the data source — no mapping needed.

### Negative Example

```markdown
Query the deployment overrides table in Kusto to find blocking overrides.
The table has various fields for tracking deployments.
Use appropriate filters to find what you need.
```

**Why this fails:** No field names — the model invents plausible but wrong column names. No enumeration of blocking types — the model might filter on `Type == "Block"` instead of the actual values. No query patterns — each run generates different KQL syntax. "Appropriate filters" delegates the entire query design to the model, which doesn't know the schema.

---

## Pattern 25: Few-Shot Examples

**Prevalence:** ~21% of skills (482 files)
**Related patterns:** [Structured Output Templates](#pattern-14), [Scoring Rubrics](#pattern-27), [Domain Knowledge Embedding](#pattern-24)

**What it is:** Including complete input/output examples within the skill to demonstrate expected behavior. The best examples include both a happy path and a failure path, with complete output showing the exact format.

**When to use:**
- When the output format is complex (multi-section reports, scorecards, JSON)
- When showing the model "what good looks like" is more effective than describing it
- When the skill has non-obvious behaviors that are best demonstrated
- When before/after code transformations need to be shown

### Positive Example
```markdown
### Input

Review this pitch for "CodePilot" (3 minutes):

Slide 1: "CodePilot — AI Pair Programming"
Slide 2: "Problem: Code reviews take 2-3 days on average"
Slide 3: Demo — shows GPT-4 suggesting refactors in VS Code
Slide 4: "Architecture: VS Code extension → GPT-4 API → GitHub PR comments"
Slide 5: "Thank you!"

### Output

# Pitch Review — CodePilot

**Format:** 5 slides, ~3 minutes | **Overall:** 16/25 (Adequate)

## Scorecard

| Criterion | Score | Feedback |
|-----------|-------|----------|
| Hook | 2/5 | Title slide alone is not a hook. Start with a pain point: "Your PR has been waiting 3 days. Sound familiar?" |
| Problem / Solution | 4/5 | Problem is clear and quantified. Add one metric: "reduces review time by 60%." |
| Demo Flow | 4/5 | Live demo is strong. Add a before/after comparison to make impact visible. |
| Technical Clarity | 4/5 | Architecture diagram is clear. Mention latency and cost for credibility. |
| Call to Action | 2/5 | "Thank you" is not a CTA. End with: "Try it today — install from marketplace." |
```
```markdown
Output for each fix:

### MAS XX.XX.XX — Criterion Name

**File:** `path/to/file.ext` (line N)
**Standard:** [_Requirement text]

**Before:**
[offending code]

**After:**
[fixed code]

**Fix applied:** [from _FixPrinciples — issue type + principle]
```

**Why this works:** The pitch reviewer example shows a complete input/output pair — the model sees the exact transformation from 5-slide input to scored output. Scores are specific (2/5, 4/5) with actionable feedback, not generic praise. The a11y example shows a before/after code template that teaches the model the expected structure for each fix. Both examples are specific enough to imitate but general enough to adapt.

### Negative Example

```markdown
Here's an example: if someone gives you a pitch about a coding tool,
review it and give it a score. Make sure to provide helpful feedback.
```

**Why this fails:** No actual output shown — the model doesn't see the output token sequence. "Give it a score" doesn't show the scoring table format. "Helpful feedback" could be a paragraph, a bullet list, or a single sentence. The model has no template to imitate, so each run produces a different structure. Without seeing a scored example, the model doesn't know the expected score distribution (is 16/25 common?).

---

## Pattern 26: Evidence Chain / Proof-of-Work

**Prevalence:** ~5% of skills (100-150 files)
**Related patterns:** [Persona/Role Assignment](#pattern-5), [Negative Constraints](#pattern-6), [Self-Critique](#pattern-28)

**What it is:** Requiring the agent to show its work — cite sources, provide evidence for conclusions, and maintain audit trails. Prevents the model from generating plausible-sounding conclusions without having actually investigated.

**When to use:**
- Root cause analysis where conclusions must be traceable
- Any skill that produces recommendations that others will act on
- Incident response where the investigation record matters for post-mortems
- Skills that analyze data where the model might confabulate findings

### Positive Example
```markdown
| **R3 — Evidence chain** | All phases | Every root cause must cite:
`[Conclusion] <- [Query/Log evidence] <- [Code path]`. Missing link → investigate first |
```
```markdown
## PROOF OF WORK — Mandatory Checkpoint Before Any Hypothesis

After completing Phase 1, you MUST output a **Download & Analysis Manifest** listing:

1. **Every attachment URL** from the bug's relations array — with download status
   (SUCCESS / FAILED + reason)
2. **Every file extracted** from archives — with file type and size
3. **Every CDB command run** on every `.dmp` / `.mdmp` file — with the output file path
4. **Every ETL converted** — with the output file path
5. **Key findings per file** — 1-2 lines summarizing what each file revealed

**If the manifest shows ZERO dumps analyzed and the bug has dump attachments → your
investigation is INVALID. Go back to Phase 1.**

**If you formed a hypothesis before completing this manifest → STOP. Delete the hypothesis.
Complete Phase 1 first.**
```

**Why this works:** R3 defines the exact format of an evidence chain: `Conclusion ← Evidence ← Code path`. Each link must be present — a "missing link" triggers investigation, not assumption. The Athena manifest is even stronger: the model must prove it analyzed every attachment before forming any hypothesis. The "delete the hypothesis" instruction prevents confirmation bias — if the model already has an idea, it might selectively look for evidence to confirm it.

### Negative Example

```markdown
Make sure your analysis is thorough and well-supported. Include evidence for your
conclusions. Don't make assumptions.
```

**Why this fails:** "Well-supported" is subjective — the model might cite one log line and consider it "supported." No required evidence format means some runs produce traced evidence chains and others produce unsupported assertions. "Don't make assumptions" is impossible for the model to self-verify without a mandatory checkpoint. The model might genuinely believe it has evidence when it's actually confabulating.
