# Gap Patterns: Onboarding, Productivity, Migration & Creative

Eight patterns missed by the initial research sweep — covering DAG-based onboarding, self-learning migration, personal productivity, executive communication review, and accessibility post-processing.

**Source research:** Extracted from analysis of 500+ production AI agent plugins across DevOps, security, migration, and incident response domains.

---

## Pattern 92: DAG Journey with Typed Gates

**Prevalence:** <1% of plugins
**Related patterns:** [Phased Execution](#pattern-2), [Deployment State Machine](#pattern-73), [State File Continuity](#pattern-70)

**What it is:** A DAG-based (not linear) onboarding/migration journey where steps have prerequisite dependencies, each step has an automation-level annotation (auto/approval/manual/decision), and the agent can resume days later from a persisted journey state. Unlike phased execution (linear) or state machines (transitions), this is a full dependency graph with parallel paths, optional steps, and backfill logic.

### Positive Example

```markdown
## Step Dependency Graph (topological ordering)
Step A → Step B → Step D
Step A → Step C → Step D
Step E (optional, activates on user opt-in)

## Automation Levels per Step
- `auto` — agent can complete without user input
- `approval` — agent prepares, user confirms
- `manual` — user must do this externally (e.g., order hardware)
- `saw` — user must complete a secure workstation (privileged access) step
- `decision` — user must make a choice between alternatives
- `tbd` — automation not yet determined

## Journey State File (JSON)
Each step tracks: not-started / in-progress / pending / completed / failed

## Auto-Detection with Backfill
At initialization, scan existing repo artifacts to detect which steps are
already done. Backfill implied prerequisites. But distinguish:
- "repo-level" artifacts (can infer from files) vs.
- "machine-state" steps (must always be runtime-verified)

## Manual Gate Resumption
User returns days later: "my secure workstation device is ready"
→ Agent reads journey state, marks secure workstation step completed, unlocks dependents

## Critical Path Visualization
Show the longest dependency chain to production readiness.
```

**Why this works:** The DAG handles parallel paths that phased execution can't. Automation-level typing prevents the agent from attempting manual steps. Backfill logic avoids making users repeat work they've already done. Manual gate resumption enables multi-day journeys.

### Negative Example

```markdown
## Onboarding Steps (linear)
1. Order hardware
2. Set up dev environment
3. Configure SAW device
4. Clone repo
5. Run first build
Complete steps in order. If a step fails, retry until it succeeds.
```

**Why this fails:** Linear ordering forces serial execution of independent steps (hardware and repo clone can happen in parallel). No automation-level typing means the agent will attempt manual-only steps like ordering hardware. No state persistence means a multi-day journey restarts from scratch if the session ends.



---

## Pattern 93: Multi-Source Evidence Harvest with Goal-Aligned Synthesis

**Prevalence:** <1% of plugins
**Related patterns:** [Audience-Purpose Calibration](#pattern-83), [Reference File Injection](#pattern-23)

**What it is:** Harvesting evidence from 6+ heterogeneous sources in parallel (GitHub PRs, ADO work items, Claude sessions, emails, Teams, calendar), mapping each evidence item to a user-defined goal/OKR, then generating audience-stratified reports from the same evidence.

### Positive Example

```markdown
## Evidence Sources (parallel harvest)
1. GitHub PRs — merged, reviewed, authored
2. ADO work items — state changes, comments
3. Claude sessions — conversation summaries
4. M365 emails — sent threads with action items
5. Teams — meeting actions, chat commitments
6. Calendar — meeting attendance and patterns

## Goal Alignment
Map each evidence item to goals from user's goals.md file.
Unaligned evidence gets flagged for user attention.

## Audience-Stratified Reports (same evidence, different framing)
- Manager report: tactical, what was delivered, blockers
- Skip-level report: strategic, themes and trajectory
- Executive report: business outcomes, metrics impact
- Team report: recognition, shared context
```

**Why this works:** The same evidence serves four audiences at different abstraction levels. Goal alignment prevents "I was busy but not productive" reports. Parallel harvest from diverse sources gives a complete picture.

### Negative Example

```markdown
## Weekly Report
Collect all PRs merged this week and list them.
Format as bullet points for the manager.
If the manager wants more detail, they can ask.
```

**Why this fails:** Single-source evidence (PRs only) misses meetings, commitments, and cross-functional work. No goal alignment means the report is an activity log, not a productivity narrative. Single-audience formatting forces the user to manually rewrite for skip-level or executive audiences.

---

## Pattern 94: Promise Detection and Knowledge Base Sync

**Prevalence:** <1% of plugins
**Related patterns:** [Configuration Persistence](#pattern-16), [Intent Classification](#pattern-20)

**What it is:** Scanning natural language conversations (Teams chats, emails) for implicit commitments ("I'll follow up", "let me check", "will do"), extracting them as structured promises, deduplicating against an existing personal knowledge base, and proposing write-back of new commitments.

### Positive Example

```markdown
## Commitment Extraction
Scan Teams chats and WorkIQ for commitment phrases:
- "I'll follow up on..."
- "Let me check..."
- "Will do"
- "I'll send you..."
- "I can take that"

## Deduplication
Compare extracted commitments against existing personal KB file.
Skip duplicates. Flag commitments that are overdue.

## Write-Back
Propose adding new commitments to the KB file.
User approves before write.
```

**Why this works:** The LLM's language understanding catches implicit commitments that keyword matching would miss. Dedup against existing KB prevents duplicate tracking. Write-back creates a persistent accountability system.

### Negative Example

```markdown
## Track Commitments
Search messages for "I will" and "I'll" keywords.
Add all matches to a TODO list.
```

**Why this fails:** Keyword matching misses implicit commitments like "let me check" or "I can take that" while also catching false positives like "I'll be in the meeting" (not a commitment). No deduplication means the same promise gets added every time the scan runs. No approval gate before write-back means the user's KB accumulates noise.

---

## Pattern 95: Mandatory Self-Learning After Failure Resolution

**Prevalence:** <1% of plugins
**Related patterns:** [Rule-Catalog Review](#pattern-48), [Error Handling](#pattern-15)

**What it is:** After diagnosing and fixing a build failure, the agent MUST update its knowledge base file with the new error pattern, root cause, and fix — making the knowledge base grow with every execution. Future runs consult the expanded KB.

### Positive Example

```markdown
After each build failure resolution:
1. Diagnose error:
   - Tier 1: Match against known patterns in known-errors.md
   - Tier 2: Novel investigation if no pattern matches
2. Apply fix
3. MANDATORY: Update known-errors.md with:
   - Error signature (regex pattern)
   - Root cause explanation
   - Fix applied
   - Files affected
4. Update shared rules files so future sub-skill runs handle it automatically

New Boost types encountered in the wild → categorize and record for
incorporation into the skill.
```

**Why this works:** The knowledge base is a living document that grows smarter with every failure. Tier 1/Tier 2 distinction ensures known patterns are handled instantly while novel errors still get investigated. Mandatory update prevents the "fix it but don't document it" failure mode.

### Negative Example

```markdown
After a build failure:
1. Diagnose the error
2. Apply a fix
3. If the fix works, move on to the next task
```

**Why this fails:** The fix is applied but never recorded. The next session encountering the same error will re-investigate from scratch, wasting identical diagnostic effort. Without a mandatory write-back step, the agent's knowledge never compounds across runs.

---

## Pattern 96: Risk-Ordered Batch Migration with Build-Verify Loops

**Prevalence:** <1% of plugins
**Related patterns:** [Deployment State Machine](#pattern-73), [Loop Prevention](#pattern-41)

**What it is:** Splitting a large migration into risk-ordered batches, where each batch goes through: migrate → commit → remote build → auto-monitor → auto-diagnose → auto-fix → resubmit. Only proceed to next batch after green build. Same-error-signature detection triggers revert.

### Positive Example

```markdown
## Batch Ordering
Order by risk: lowest-dependency files first, highest-risk last.

## Per-Batch Loop
1. Migrate code in batch
2. Commit changes
3. Submit remote build
4. Auto-monitor via CronCreate polling
5. On failure: auto-diagnose → auto-fix → resubmit
6. If same error signature repeats → STOP, revert batch
7. On green build → proceed to next batch

## No-Progress Detection
If the same error signature appears 2x after fix attempts:
→ Revert entire batch
→ Report failure with error details
→ Move to next batch (skip problematic files)
```

**Why this works:** Risk ordering minimizes blast radius of early failures. Same-error-signature detection prevents infinite retry loops. Batch-level revert preserves previously successful migrations.

### Negative Example

```markdown
## Migration
1. Migrate all files at once
2. Submit build
3. If build fails, fix errors and resubmit
4. Repeat until green
```

**Why this fails:** Migrating everything at once means a single failure contaminates the entire changeset with no way to isolate which files caused it. No same-error detection means the agent can retry the same unfixable error indefinitely. Without batch-level revert, a problematic file blocks all other files from progressing.

---

## Pattern 97: PII-Motivated Delivery Restriction

**Prevalence:** <1% of plugins
**Related patterns:** [Sensitive Data Redaction](#pattern-11), [Read-Only Boundary](#pattern-12)

**What it is:** The output contains personal data aggregated from multiple sources. Delivery is restricted to ONLY the user's own accounts (Outlook/Teams). Even if the user explicitly asks to send it to someone else, the agent refuses. PII protection overrides user consent.

### Positive Example

```markdown
## Delivery Restriction (ABSOLUTE)
Briefing delivery: ONLY to the user's own Outlook inbox or Teams chat.

Even if user explicitly asks to send to someone else → REFUSE.
"This briefing contains your personal activity data from multiple sources.
I can only deliver it to your own accounts."

This is not a confirmation gate — there is no override.
```

**Why this works:** Unlike data redaction (which removes sensitive bits from output), this restricts the entire delivery channel regardless of content. The absolute nature prevents social engineering ("just send it to my manager, it's fine").

### Negative Example

```markdown
## Delivery
Send the briefing to the user's preferred channel.
If user asks to forward it to someone, confirm before sending.
"Are you sure you want to share this with [person]?"
```

**Why this fails:** A confirmation gate is not a restriction — users will always confirm when they believe the request is reasonable. PII-aggregated reports from multiple sources should never leave the user's own accounts, regardless of consent. The social engineering path ("my manager asked for it") trivially bypasses a confirmation prompt.

---

## Pattern 98: Audience-Register Translation Review with Matched Frameworks

**Prevalence:** <1% of plugins
**Related patterns:** [Scoring Rubrics](#pattern-27), [Audience-Purpose Calibration](#pattern-83)

**What it is:** A review methodology structured around the *translation problem* — technical authors writing for executive audiences. Includes document-type classification, matched content frameworks per type, and an anti-pattern catalog specific to engineer-to-executive communication.

### Positive Example

```markdown
## Six Executive Fundamentals (scoring rubric)
1. Unambiguous Ask — what exactly do you want the executive to DO?
2. Quantified Business Impact — numbers, not adjectives
3. Strategic Framing — connect to company priorities
4. Executive Tone — confident, concise, no hedging
5. Decision-Enabling Structure — reader can decide from this alone
6. Self-Contained — no required pre-reading

## Document Type → Content Framework
| Type | Recommended Framework |
| Strategy Brief | SCR (Situation, Complication, Resolution) |
| Investment Ask | What / So What / Now What |
| Post-Mortem | Finding / Implication / Recommendation |
| Decision Record | Evidence-First Decision |

## Engineer-to-Executive Anti-Patterns (14 named)
- "The Architecture Astronaut" — leading with system design, not business value
- "The Hedge Fund" — "we might potentially consider possibly..."
- "The Kitchen Sink" — every detail included, no hierarchy of importance

## Verdict: SEND-READY / NEEDS REVISION / DO NOT SEND
```

**Why this works:** The review is calibrated to the specific failure mode (technical expert → executive audience), not generic document quality. Matched frameworks per document type give the writer a structural starting point. Named anti-patterns are memorable and specific.

### Negative Example

```markdown
## Document Review Checklist
- Is the writing clear?
- Is the grammar correct?
- Is the document well-structured?
- Are there any typos?
Rate overall quality: 1-5
```

**Why this fails:** Generic quality criteria miss the core translation problem — a technically accurate document can score 5/5 on clarity and grammar while completely failing to communicate business value to an executive. No document-type matching means a post-mortem gets the same review framework as a strategy brief. No named anti-patterns means feedback is vague ("could be more concise") rather than actionable ("you're leading with architecture, not business impact").

---

## Pattern 99: Automated Accessibility Post-Processing Pipeline

**Prevalence:** <1% of plugins
**Related patterns:** [Schema Validation Gate](#pattern-51), [Test Scaffolding](#pattern-54)

**What it is:** After generating output (e.g., a PPTX presentation), a dedicated accessibility post-processor runs automatically to transform the output for compliance with accessibility standards. A separate eval script runs assertions.

### Positive Example

```markdown
## A11y Post-Processing (automatic, after PPTX generation)
1. Mark decorative shapes as decorative
2. Inject slide titles (for screen reader navigation)
3. Fix reading order (logical, not visual)
4. Group elements for screen readers
5. Set alt text on images

## A11y Evaluation (25 assertions)
Run accessibility eval script that checks:
- Every slide has a title
- Every image has alt text
- Reading order matches visual order
- No decorative elements are in the tab sequence
- Color contrast meets WCAG AA
```

**Why this works:** Accessibility is handled as a post-processing pipeline, not embedded in the generation logic. This separation of concerns means the creative generation can focus on content while a dedicated pipeline ensures compliance. The 25-assertion eval provides measurable quality.

### Negative Example

```markdown
## Presentation Generation
When creating slides, make sure to:
- Add alt text to images
- Use readable fonts
- Keep good contrast
Generate the PPTX with these guidelines in mind.
```

**Why this fails:** Embedding accessibility as guidelines within the generation prompt means compliance depends on the LLM remembering every rule during creative work. There is no verification step, so violations are silently shipped. Without a separate eval with concrete assertions, "make sure to add alt text" produces inconsistent results that cannot be measured or enforced.
