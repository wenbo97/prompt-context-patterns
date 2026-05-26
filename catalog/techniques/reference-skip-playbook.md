# The Reference-Skip Problem: A Playbook

When a Claude Code skill references external files via `@path/to/file.md`, the runtime agent sometimes **skips reading them** and improvises an answer instead. This document describes the problem, decomposes it into three distinct failure modes, and presents eleven solution patterns with the scenarios they fit and good/bad examples for each.

---

## 1. Problem statement

### 1.1 What progressive disclosure promises

Claude Code skills use a three-tier progressive-disclosure model:

1. **Tier 1 (always loaded)** — YAML frontmatter `name` + `description` of every installed skill (~100 tokens each).
2. **Tier 2 (loaded on trigger)** — full `SKILL.md` body when the model decides the skill applies.
3. **Tier 3 (loaded on demand)** — bundled files like `references/foo.md`, `examples/bar.md`, `scripts/baz.py`. The model **chooses** to read these.

The promise of tier 3: keep `SKILL.md` lean, push examples and edge cases into satellite files, save context budget.

### 1.2 What goes wrong

The third tier is opt-in. There is **no enforcement mechanism**. The model can ignore an `@reference` and produce output anyway. When it does, the output is often plausibly-shaped but factually wrong — wrong format, wrong scenario classification, wrong edge-case handling.

The skip is not the model "trying to save tokens." It is a downstream effect of how next-token prediction interacts with prompt structure. By the time the model reaches the `@reference`, it may already have an answer in mind that the reference would only contradict — and contradicting yourself feels worse than skipping a footnote.

### 1.3 Why it is dangerous

Reference skips are **silent failures**:

- The model produces output that looks reasonable.
- It does not announce "I skipped the reference."
- The error surfaces only when downstream tooling rejects it, or when a human notices the format is wrong, or — worst — when the wrong output is committed and deployed.

This is fundamentally different from a tool error or a refusal: those are visible. Skip failures masquerade as success.

---

## 2. Root cause: three distinct failure modes

The naive framing — "the model is being lazy" — is not actionable. Decompose into three failure modes that often co-occur but require different fixes:

### Mode A — Naked hop

The `@reference` appears without contextual scaffolding that motivates the jump. Surrounding prose does not establish *why* reading the file is necessary. The reference reads as a footnote, not an instruction.

> _Symptom: reference appears at end of paragraph in soft prose ("for details, see..."). Model treats it as optional and proceeds._

### Mode B — Pre-satisfaction

By the time the model encounters the `@reference`, it has already sampled a plausible-looking continuation. The reference would force it to revise, but the existing draft satisfies the local objective. Skipping feels cheaper than re-deriving.

> _Symptom: even with strong "you must read X" framing, the model skips. The reference appeared too late in the flow._

### Mode C — Optional framing

The linguistic register of the reference makes it sound dismissable. Words like *see*, *refer*, *for details*, *FYI*, *if interested* signal "footnote" to the model the same way they would to a human reader.

> _Symptom: reference is positioned correctly and appears early enough, but the wording does not convey "this is required."_

### Why decomposition matters

The three modes have **non-interchangeable fixes**:

| Mode | What's broken | What fixes it |
|------|---------------|---------------|
| A | Surrounding context doesn't justify the jump | Inline anchor + causal phrasing + numbered step |
| B | Model already committed before reading | Move reference earlier; sub-agent isolation; output schema requiring reference content |
| C | Linguistic register reads as skippable | Imperative phrasing ("STOP — read X") |

A skill that suffers from Mode B will not be saved by stronger Mode-C imperatives. Get the diagnosis right before applying the fix.

---

## 3. Solution patterns

Eleven patterns, organized by **mechanism of action** rather than alphabetically. Each entry: what it does, which failure mode it targets, scenario fit, anti-fit, and good/bad examples.

### Pattern 1 — Imperative + STOP framing

**Mechanism:** Replace soft "see also" language with imperative "STOP — read this before continuing."

**Targets:** Mode C (optional framing).

**Use when:** The reference is positioned reasonably and is genuinely required — you just need the linguistic register to match.

**Don't use alone when:** The model has already had room to commit (Mode B) — louder phrasing won't undo a plan it has already drafted.

#### ❌ Bad

```markdown
After analyzing the conflicts, generate a unified diff for the user.
For details on edge cases, see @examples/overlap.md.
```

The reference reads as a footnote.

#### ✅ Good

```markdown
After analyzing the conflicts, generate a unified diff for the user.

> ⚠️ STOP — before producing any diff, you MUST read @examples/overlap.md.
> Do not improvise the format. The example contains the only correct
> structure; deviating will fail downstream validation.
```

The stake is named, the action is imperative, the consequence of skipping is explicit.

---

### Pattern 2 — Numbered step for the read

**Mechanism:** Promote "read the reference" from a parenthetical into its own numbered step in the workflow.

**Targets:** Mode A (naked hop).

**Use when:** Multi-step workflow where one step requires external knowledge before it can proceed.

**Don't use when:** Single-step task; or the reference is so short (<10 lines) that inlining it is cheaper than ceremonying around it.

#### ❌ Bad

```markdown
### Step 3: Resolve overlap

When two PRs touch the same file, fetch each version, diff them,
and let the user pick. (Reference: @examples/overlap.md)
```

The reference is annotation, not action.

#### ✅ Good

```markdown
### Step 3a: Read @examples/overlap.md in full

### Step 3b: Identify which scenario in the example matches the
current overlap (multi-PR same-line, multi-PR different-line, etc.)

### Step 3c: Apply the matched scenario's resolution pattern.
```

Reading the file is now a checkable step. Skipping it is structurally visible.

---

### Pattern 3 — Inline anchor + reference for depth

**Mechanism:** Embed a one-line skeleton of the pattern inline; put the full worked example with reasoning in the reference. The anchor primes attention; the reference adds depth.

**Targets:** Mode A primarily; partially Mode B (the anchor seeds the right token distribution before the model can drift).

**Use when:** Most references — this is the workhorse pattern. Default to this shape unless you have a specific reason for another.

**Don't use when:** The step is so high-risk that even the anchor is insufficient and the full example must stay inline (use Pattern 7 instead).

#### ❌ Bad — pure reference, no anchor

```markdown
### Step 3: Multi-PR overlap resolution

For how to handle overlap, see @examples/overlap-resolution.md.
```

If the model skips, it has nothing to fall back on.

#### ❌ Bad — full inline (defeats the goal of progressive disclosure)

```markdown
### Step 3: Multi-PR overlap resolution

When two or more PRs touch the same file, you must fetch each
version using `gh pr view <PR>:<file>`, then construct a unified
diff with the LOCAL version on top, each PR version below...
[80 more lines of example]
```

Works behaviorally, but bloats `SKILL.md` past its useful length.

#### ✅ Good — anchor + reference

```markdown
### Step 3: Multi-PR overlap resolution

> **Pattern (1-line):** Overlap file → fetch ALL PR versions →
> present LOCAL vs each PR diffs → user picks ONE.
> Full worked example with <thinking> trace: @examples/overlap.md

3a. Identify all PRs that touch this file...
```

Even if the model skips the reference, the anchor steers it toward the correct shape. The reference catches the long tail of edge cases.

---

### Pattern 4 — Front-load references

**Mechanism:** Move critical `@reference` reads to the top of `SKILL.md`, before any executable step. Read the file before the model has a chance to draft a plan.

**Targets:** Mode B (pre-satisfaction).

**Use when:** The reference describes a workflow-level invariant — naming conventions, format rules, classification taxonomy — that applies throughout the workflow, not just at one step.

**Don't use when:** The reference is highly localized to one specific step; front-loading it dilutes attention by the time the relevant step is reached.

#### ❌ Bad — referenced too late

```markdown
### Step 1: Parse input
### Step 2: Determine PRs
### Step 3: Fetch versions
### Step 4: Build diff
   Format follows the rules in @rules/diff-format.md.
### Step 5: Present to user
```

By Step 4, the model has already absorbed the surrounding context and may sketch a diff before reading the rules.

#### ✅ Good — front-loaded

```markdown
## Required context (read before proceeding)

@rules/diff-format.md — diff structure used throughout this skill

---

### Step 1: Parse input
### Step 2: Determine PRs
...
```

The format rules are absorbed before any drafting can occur.

---

### Pattern 5 — Forced manifest read

**Mechanism:** First step of the skill is "read these files in order" with explicit confirmation. The skip becomes a gate, not a mid-flow decision.

**Targets:** Mode A + Mode B simultaneously (the read is the first action, not a side-quest).

**Use when:** Multiple references are all required and you can't trust selective reading.

**Don't use when:** Most users won't need most of the references; or the manifest itself becomes a token-budget burden.

#### ❌ Bad — references scattered

```markdown
### Step 1: ... (uses @rules/A.md)
### Step 2: ... (uses @rules/B.md)
### Step 3: ... (uses @rules/C.md)
```

Three independent skip opportunities.

#### ✅ Good — single manifest gate

```markdown
## Step 0: Required context

Before doing anything else, read these files top to bottom:

1. @rules/diff-format.md
2. @examples/overlap-cases.md
3. @rules/csproj-conventions.md

State "context loaded" when complete. Do not proceed otherwise.
```

One gate, one decision point, low surface for skipping.

---

### Pattern 6 — Output schema requiring reference content

**Mechanism:** Design the output format so that a correct answer is **impossible** without reading the reference. Force the model to emit values that exist only in the referenced file.

**Targets:** Mode B (pre-satisfaction). Even if the model has a draft answer, the schema forces a re-derivation.

**Use when:** The reference contains discrete enumerable categories, scenario names, or a closed taxonomy you can require in the output.

**Don't use when:** The reference is continuous prose with no nameable discrete elements; output format is constrained externally and you can't add fields.

#### ❌ Bad — schema indifferent to reference

```markdown
Output a JSON object with:
- `summary`: brief description
- `recommendation`: what to do
```

Model can produce these from anywhere.

#### ✅ Good — schema requires reference content

```markdown
Output a JSON object with:
- `applied_scenario`: one of [
    "multi_pr_same_line",
    "multi_pr_different_line",
    "version_conflict",
    "namespace_collision"
  ] — defined in @examples/overlap.md
- `decision_trace`: which paragraph in @examples/overlap.md
  the resolution was based on
- `recommendation`: ...
```

Scenario names are not in `SKILL.md`. To produce them, the model must read the reference. A grep-able audit follows: if `applied_scenario` is invented or unrecognized, the skip is detectable.

---

### Pattern 7 — Risk-tiered inlining

**Mechanism:** Refuse to extract examples for the highest-risk steps. Keep them inline, even at token cost. Extract only for low-risk paths.

**Targets:** All three modes — by removing the jump entirely.

**Use when:** A specific step has been observed to fail repeatedly when extracted; or the consequence of failure is severe (wrong code committed, production config corrupted, PR merged incorrectly).

**Don't use when:** Used wholesale — inlining everything defeats progressive disclosure and hits attention-decay problems past 500-line `SKILL.md`.

#### ❌ Bad — extracting everything for "cleanness"

```markdown
### Step 3: Overlap resolution → @examples/overlap.md
### Step 4: csproj merge       → @examples/csproj.md
### Step 5: Branch sync        → @examples/branch.md
```

Three high-risk steps, three skip opportunities.

#### ✅ Good — risk-tiered

```markdown
### Step 3: Overlap resolution

[80 lines of inline example with <thinking> trace — too risky to extract]

### Step 4: csproj merge

[80 lines of inline example — same reasoning]

### Step 5: Branch sync (low-risk happy path)

> **Pattern:** fetch → rebase → push. See @examples/branch.md for the
> rare conflict case.
```

The high-risk steps pay the inline tax. The low-risk one uses anchor + reference.

---

### Pattern 8 — Deterministic scripts

**Mechanism:** Replace the prompt step with a script invocation. The model calls the script; the script does the work. No prompt path means no improvisation surface.

**Targets:** All three modes — eliminating the prompt eliminates the failure modes that come with it.

**Use when:** The step is well-defined with enumerable inputs and outputs — XML parsing, format validation, marker detection, file diffing, version comparison, regex extraction.

**Don't use when:** The step requires semantic judgment (code intent, user intent, code review); I/O boundary is fuzzy.

#### ❌ Bad — prompt-as-parser

```markdown
### Step 2: Parse the .csproj file

Read the .csproj XML and extract all `<PackageReference>` elements
along with their `Version` attribute. Handle conditional references
(`<PackageReference Condition="...">`) carefully...
```

The model is being asked to do XML parsing in prompt, with all the fragility that implies.

#### ✅ Good — script invocation

```markdown
### Step 2: Parse the .csproj file

Run `scripts/parse_csproj.py <path>`. The script returns JSON with
all PackageReference entries, normalized. Use the JSON directly;
do not re-parse the XML.
```

100% deterministic. No prompt-level improvisation possible.

---

### Pattern 9 — Sub-agent isolation

**Mechanism:** Delegate the high-risk subflow to a sub-agent invoked via the `Task` tool. The sub-agent receives only the relevant skill subset and starts with a clean context.

**Targets:** Mode B (pre-satisfaction) primarily. The sub-agent has no committed plan when it starts. Also Mode A — the sub-agent's prompt is focused, so references are not naked hops away from a long parent flow.

**Use when:** Complex multi-step subflow with high risk and a clean input/output contract. The two or three highest-risk paths in a workflow.

**Don't use when:** Step is trivially short (sub-agent overhead exceeds benefit); I/O contract is unclear (sub-agent doesn't know what to return).

#### ❌ Bad — high-risk step inline in long parent flow

```markdown
### Step 7: Resolve overlap

[80 lines of instruction competing with the surrounding 400-line
SKILL.md for the model's attention; references appear deep into
a long execution chain where attention has decayed]
```

#### ✅ Good — sub-agent boundary

```markdown
### Step 7: Resolve overlap

Delegate to the `overlap-resolver` sub-agent via Task tool.

Input: { files: [...], prs: [...], local_branch: "..." }
Expect: { resolution: "...", chosen_version: "...", trace: "..." }

Validate the returned `chosen_version` exists in one of the input PRs.
```

The sub-agent's prompt lives in a separate file. Inside that prompt, references are read against a clean context with no competing concerns.

---

### Pattern 10 — Self-check / validation loop

**Mechanism:** Append an explicit checklist at the end of high-risk steps. Force the model to answer "did I read X? does my output have Y?" before proceeding.

**Targets:** Catch-net for all three modes. Not a primary defense — the model can also lie to itself on the checklist — but a meaningful fraction of skips are caught.

**Use when:** Stacked with other patterns. As a single defense it is weak; as a layer in defense-in-depth it pays for itself.

**Don't use alone when:** Used as the only mitigation — the model can produce a plausible-looking checklist with all "yes" without having actually done the work.

#### ❌ Bad — no validation

```markdown
### Step 3: Resolve overlap

Identify which PRs touch the file and produce a diff.
```

No reflective gate. Model proceeds whether or not it skipped the reference.

#### ✅ Good — explicit self-check

```markdown
### Step 3: Resolve overlap

[step body]

### Self-check before proceeding to Step 4:

- [ ] Did you read @examples/overlap.md? (If not, STOP and read now.)
- [ ] Does your diff include both LOCAL and each PR's version?
- [ ] Did you ask the user to pick exactly ONE version?
- [ ] Did you record the chosen version in the migration marker?

If any answer is "no", re-read the reference and retry this step.
```

Catches some skips. Stack with Pattern 3 or 9 for stronger guarantees.

---

### Pattern 11 — Hooks (Claude Code-specific)

**Mechanism:** Use Claude Code's hook system to mechanically enforce conditions before skill execution — e.g., verify required files have been read, verify required tools have been called.

**Targets:** All three modes — this is the only pattern that provides a **mechanical guarantee** rather than a behavioral suggestion.

**Use when:** Truly critical paths where no improvisation is acceptable. The cost of a skip is high enough to justify the maintenance burden of a hook.

**Don't use when:** The reference is nice-to-have rather than must-have; the hook itself becomes more burden than the occasional skip; the hook would block legitimate flexibility.

**Note:** Hook capabilities depend on your Claude Code version and project configuration. Verify what's available in your environment before designing around them.

---

## 4. Decision matrix

| Scenario | Primary | Stack with |
|----------|---------|------------|
| Step is scriptable (parsing, validation, format check) | **Pattern 8** | — |
| High-risk step with clean I/O contract | **Pattern 9** | Pattern 6 (output schema) |
| High-risk step with fuzzy I/O | **Pattern 7** (inline) | Pattern 5 (manifest) + 6 (schema) |
| Mid-risk multi-step, model drift suspected | **Pattern 3** + **Pattern 2** | Pattern 10 (self-check) |
| Multiple references all required | **Pattern 5** (manifest) | Pattern 4 (front-load) |
| Reference contains discrete enumerable categories | **Pattern 6** (output schema) | Pattern 3 (anchor) |
| Reference is a workflow-level invariant | **Pattern 4** (front-load) | Pattern 1 (imperative) |
| Reference framing is just too soft | **Pattern 1** (imperative) | — |
| Critical path, no improvisation acceptable | **Pattern 11** (hook) | Pattern 8 + 9 |

---

## 5. Meta-principles for choosing

### 5.1 Eliminate before mitigating

If the step can be scripted (Pattern 8) or hooked (Pattern 11), do that first. Do not stack mitigations on a prompt path that doesn't need to exist as prompt. Eliminating the improvisation surface is structurally stronger than fighting it with phrasing.

### 5.2 Diagnose mode before applying fix

The three failure modes are not interchangeable. Stronger imperative phrasing (Pattern 1) does nothing for pre-satisfaction (Mode B). Front-loading the reference (Pattern 4) does nothing for optional framing (Mode C). Identify which mode is biting in your specific case before reaching for a pattern.

The diagnostic question to ask:

- _Did the model produce something that looks correct but uses the wrong format?_ → Likely Mode C (it knew where to look, but didn't feel obligated). Try Pattern 1.
- _Did the model produce something internally consistent but not aligned with the reference's content?_ → Likely Mode B (it had its own answer first). Try Pattern 4 / 9 / 6.
- _Did the model produce something disconnected from the reference's domain entirely?_ → Likely Mode A (the jump never registered). Try Pattern 2 / 3 / 5.

### 5.3 Defense in depth for high-risk paths

For genuinely critical steps, stacking 2–3 patterns is appropriate, not over-engineering. Sub-agent (9) + inline anchor (3) + output schema (6) covering the same step is reasonable when the step is worth protecting. No single pattern covers all three failure modes.

### 5.4 The goal is behavioral stability, not minimum line count

A 450-line `SKILL.md` that drops format-correctness by 14 points is a regression no matter how clean it looks. Refactoring is not free; structural changes that move content into references must be paid for with patterns that compensate for the lost inline scaffolding. If the patterns don't fully compensate, the content shouldn't have moved.

### 5.5 Measure when you can

Reference-skip behavior cannot be predicted reliably from reading the prompt. The only honest test is running the workflow N times and observing whether the reference was actually read (visible in the tool-use trace) and whether the output was correct. Build a simple smoke-test pass through the affected workflow before declaring a refactor successful, even without a full eval harness.

---

## 6. Anti-patterns to avoid

A short list of things that consistently make the skip problem worse:

- **Apologetic framing.** _"You may want to look at @ref"_ — sounds like advice, not instruction.
- **Truncated reference paths in long lists.** When a step lists six `@references` in passing, the model treats them as a bibliography, not a reading list.
- **References to non-existent files** that were renamed or moved. The model fails silently and improvises. Validate references in CI.
- **Stacking five patterns on a low-risk step** because patterns are "good." Patterns have cost (line count, attention dilution, maintenance). Apply them where they earn their keep.
- **Treating the SKILL.md as the only place patterns matter.** If the calling command duplicates skill logic, patterns applied to the skill don't help when the command's prompt drifts. Collapse duplication first.

---

## 7. Summary

The reference-skip problem is **silent improvisation under progressive disclosure**. It has three distinct failure modes — naked hop, pre-satisfaction, optional framing — that require non-interchangeable fixes. Eleven patterns cover the space, organized from cheapest mitigation (imperative phrasing) to strongest guarantee (hooks and scripts). Choose by diagnosis, eliminate before mitigating, stack on high-risk paths, and measure outcomes when refactoring.

The deepest principle: **progressive disclosure is not a uniform tax**. It is a per-step decision that trades token cost against improvisation risk. Any single skill should have steps that are inline, steps that are referenced with anchors, steps that are scripts, and steps that are sub-agents — chosen per step based on risk and I/O shape, not chosen as a project-wide policy.
