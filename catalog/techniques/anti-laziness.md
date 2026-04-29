# Preventing Agent Laziness in Skill References

**Topic:** When refactoring a Claude Code skill to use progressive disclosure (extracting examples into reference files), how do you keep the runtime agent from skipping the reference reads and improvising?

**Audience:** Skill / plugin authors who already understand Claude Code's `SKILL.md` model and are facing a real refactor (e.g. command + skill files growing past comfortable size).

---

## 1. Background: how Claude Code skills work

Skills use a **three-tier progressive disclosure** model. Understanding all three tiers is the prerequisite for reasoning about laziness.

### Tier 1 — Metadata pre-load (~100 tokens per skill)

At session startup, Claude Code scans every skill directory and injects only the YAML frontmatter (`name` + `description`) of each `SKILL.md` into the system prompt. This is what powers skill discovery: the model sees a list like

```
<available_skills>
  <skill>
    <name>sync-prerequisite-prs</name>
    <description>Use when the user wants to sync...</description>
  </skill>
  ...
</available_skills>
```

and uses the descriptions to decide whether a skill applies. You can install dozens of skills with no meaningful context cost.

### Tier 2 — `SKILL.md` full body (loaded on trigger)

When the model decides a skill applies, it issues a `view`/`bash` call to read the full `SKILL.md` into context. Anthropic recommends keeping this body **under ~500 lines / ~1,500–2,000 words** for reliable instruction-following.

### Tier 3 — Bundled files (loaded on demand by the model)

Anything else in the skill directory — `references/`, `examples/`, `scripts/`, `assets/` — is **not** auto-loaded. The model has to explicitly choose to read it. The official phrasing is _"Claude **chooses to** read forms.md when filling out a form"_ — `chooses to` is the operative phrase. **There is no enforcement.**

This third tier is where the laziness problem lives.

---

## 2. Why agents skip reference reads (root cause analysis)

Skipping is rarely the model "trying to save tokens." It's a downstream effect of how next-token prediction interacts with prompt framing.

| Cause | Mechanism |
|---|---|
| **Pattern completion bias** | After reading the parent `SKILL.md`, the model has already sampled a plausible-looking plan for the next step. The reference becomes a "lookup if uncertain" — and the model isn't uncertain. |
| **Optional framing** | Phrases like _"For details, see @overlap.md"_ are semantically optional. The model treats them as it would a footnote in prose. |
| **No contradiction signal** | Without an inline example, the model's internal distribution looks "good enough" to itself. There's no inline anchor saying _"the obvious answer is wrong"_. |
| **Long-chain attention decay** | Deep into a multi-step workflow, attention to early instructions ("you must read references") fades. |
| **Context-pressure heuristic** | Under context pressure or near token limits, the model is more likely to skip "extra" reads. |

The implication: **prose alone cannot reliably defeat skipping**. The framing of the reference, its position in the workflow, and the structural redundancy around it all matter more than how strongly you tell the model to read it.

---

## 3. Strategies — with good and bad examples

Strategies are listed roughly by **strength of guarantee**, weakest-but-cheapest first.

### Strategy 1 — Imperative framing, not "see also"

Don't write a reference reference like a footnote. Write it like a load-bearing instruction.

#### ❌ Bad
```markdown
### Step 3: Resolve overlap

Identify which PRs touch the file and produce a unified diff for the user.
For more details on edge cases, see @overlap.md.
```

#### ✅ Good
```markdown
### Step 3: Resolve overlap

> ⚠️ STOP — before producing any output for this step, you MUST read
> @examples/overlap.md. Do not improvise. The example contains the only
> correct format for the diff.

Identify which PRs touch the file...
```

**Strength:** Low. The model can still skip imperative phrasing. But it raises skip cost cheaply.

---

### Strategy 2 — Make the read itself a numbered step

Skipping a numbered step feels different to the model than skipping a "see also."

#### ❌ Bad
```markdown
### Step 3: Resolve overlap
After analyzing the conflicts, generate the diff.
(Reference: @examples/overlap.md)
```

#### ✅ Good
```markdown
### Step 3a: Read @examples/overlap.md in full
### Step 3b: Identify which scenario in the example matches the current case
### Step 3c: Apply the pattern from that scenario to produce the diff
```

**Strength:** Moderate. The numbered structure makes the read part of the workflow's spine. Still defeatable, but harder.

---

### Strategy 3 — Inline anchor + reference for depth

The single most useful technique: keep a **one-line skeleton** of the pattern inline, and put the worked example with full reasoning in the reference. The anchor primes attention; the reference adds depth.

#### ❌ Bad — pure reference, no anchor
```markdown
### Step 3: Multi-PR overlap resolution

For how to handle overlap, see @examples/overlap-resolution.md.
```

If the model skips, it has nothing.

#### ❌ Bad — full inline (defeats the refactor)
```markdown
### Step 3: Multi-PR overlap resolution

When two or more PRs touch the same file, you must:
1. Fetch the version from each PR using `gh pr view`...
[80 more lines of example with thinking trace]
```

This works but bloats context.

#### ✅ Good — anchor + reference
```markdown
### Step 3: Multi-PR overlap resolution

> **Pattern anchor (1-line):** Overlap file → fetch ALL PR versions →
> present LOCAL vs each PR diffs → user picks ONE.
> Full worked example with <thinking> trace: @examples/overlap.md

3a. Identify all PRs that touch this file...
```

**Strength:** Good. Even if the model skips the reference, the anchor steers it toward the right token distribution. The reference is for the long tail of edge cases.

---

### Strategy 4 — Tier inline-vs-reference by risk (the most important principle)

Progressive disclosure is **not a uniform tax**. It should only be applied where the cost of "skip then improvise" is acceptable.

**Decision matrix:**

| Content type | Where it lives | Why |
|---|---|---|
| High-risk step examples (overlap resolution, diff mechanism, csproj resolution) | **Inline in `SKILL.md`** | The model WILL improvise wrong without these. Cost of inline >> cost of failure. |
| Happy-path examples (single-PR merge, trivial flows) | Extract to `@examples/...md` with 1-line anchor | Low risk. Model can infer correct behavior from step instructions alone. |
| Duplicated logic between command + skill (PR status gate, marker detection, progress format) | Keep in skill SSOT, remove from command | Duplication causes drift; pick one home. |
| Deterministic operations (XML parsing, format validation, marker detection) | **Bundled scripts**, not prompt | 100% deterministic, zero improvisation surface. |

The goal of refactoring is not "minimum lines." It is **minimum lines _consistent with stable behavior on the high-risk paths_**.

---

### Strategy 5 — Replace prompt with deterministic code

Anthropic's official guidance: _"Prefer scripts for deterministic operations: write `validate_form.py` rather than asking Claude to generate validation code."_

Any step that can be a script should be a script. Scripts cannot improvise.

#### ❌ Bad
```markdown
### Step 2: Parse the .csproj file

Read the .csproj XML and extract all `<PackageReference>` elements
along with their `Version` attribute. Handle conditional references
(`<PackageReference Condition="...">`) carefully...
```

#### ✅ Good
```markdown
### Step 2: Parse the .csproj file

Run `scripts/parse_csproj.py <path>`. The script returns JSON with all
`PackageReference` entries normalized. Use the JSON directly; do not
re-parse XML in prompt.
```

**Strength:** Very high (perfect on the deterministic part). Use wherever the operation is well-defined.

---

### Strategy 6 — Validation loop / self-check

Add an explicit checklist at the end of high-risk steps. Not bulletproof, but a catch-net.

#### ✅ Good
```markdown
### Self-check before proceeding:
- [ ] Did you read @examples/overlap.md? (If no, STOP and read now.)
- [ ] Does the diff include both LOCAL and each PR's version?
- [ ] Did you ask the user to pick ONE version?

If any answer is "no", re-read the reference and retry this step.
```

**Strength:** Moderate. Catches a fraction of skips. Cheap to add.

---

### Strategy 7 — Sub-agent isolation (strongest)

For genuinely high-risk paths, spawn a sub-agent (via `Task` tool) with an isolated, focused context. The sub-agent gets only the relevant skill subset and has nothing else to do — no shortcuts to take.

#### ❌ Bad
```markdown
### Step 3: Resolve overlap

[80 lines of inline instruction competing with everything else
in the 500-line SKILL.md for the model's attention]
```

#### ✅ Good
```markdown
### Step 3: Resolve overlap

Delegate to the `overlap-resolver` sub-agent.
Pass: { files: [...], prs: [...] }
Expect: { resolution: "...", chosen_version: "..." }
```

The sub-agent's prompt lives in a separate file, loaded only inside the sub-agent's clean context.

**Strength:** Highest. Eliminates attention dilution. Failure is contained. Easy to retry.

**Cost:** Architectural complexity. Worth it for the 2–3 highest-risk paths in a workflow, not for everything.

---

### Strategy 8 — Empirically test, don't reason about it

You cannot guess the skip rate. Use a harness like **promptfoo** to run the workflow N times and measure:

- Did the model issue a `view`/`bash` call on the reference file? (Inspect tool-use trace.)
- Did the output match the expected format?
- Does the skip rate change when you reword the framing?

Iterate empirically. The Anthropic `skill-creator` skill ships with an eval framework specifically for this.

#### ❌ Bad
> "I think this framing should work, let's ship it."

#### ✅ Good
> "Baseline (916-line version): 0% skip rate, 92% format-correct. New version (450 lines): 12% skip rate, 78% format-correct. → Reject this refactor; isolate which extraction caused the regression."

**Strength:** This is what tells you the other strategies actually worked.

---

## 4. Decision framework

When deciding whether to extract a piece of inline content into a reference:

```
For each chunk of inline content:

  1. Is the step deterministic?
     YES → Replace with a script. Remove from prompt entirely.
     NO  → continue.

  2. If the model improvised this step, would the result be
     (a) wrong-and-the-user-would-not-notice, or
     (b) catastrophically wrong / hard to roll back?
     (a) → safe to extract to @reference. Use Strategy 3 (anchor + reference).
     (b) → keep inline. The token cost is paying for behavioral stability.

  3. Is this content duplicated between command and skill?
     YES → Pick the SSOT (usually the skill), delete from the other.

  4. Could this be a sub-agent boundary?
     YES → Strategy 7. Especially if the step is complex AND
           high-risk AND has a clear input/output contract.
```

---

## 5. Conclusions

1. **Reference reads are not enforced.** Anything in `references/` is opt-in. Treat every `@reference` as something the model _might_ skip.

2. **Prose alone cannot reliably defeat skipping.** Imperative phrasing helps a little; structural changes (numbered steps, anchors, sub-agents, scripts) help much more.

3. **Don't extract uniformly.** Tier by risk. High-risk few-shot examples (where improvisation is dangerous) **stay inline**, even at token cost. Low-risk examples extract cleanly.

4. **Anchor + reference beats pure reference.** A one-line skeleton of the pattern, inline, primes the model's attention even if the full reference is skipped. This is the workhorse pattern.

5. **Determinism > prompt.** Anything that can be a script should be a script. Zero improvisation surface.

6. **Sub-agents are underused.** For high-risk multi-step paths with a clean input/output contract, sub-agent isolation is dramatically more reliable than inlining or referencing.

7. **The goal is not "minimum lines."** The goal is **minimum lines consistent with stable behavior on the high-risk paths**. A 450-line refactor that drops format-correctness by 14 points is a failed refactor regardless of how clean it looks.

8. **Measure, don't guess.** Build a baseline with the existing version, run a fixed eval set on every refactor variant, and only accept changes that hold or improve the metric. promptfoo + skill-creator's eval harness are designed for exactly this.

---

## Appendix: quick-reference checklist for each refactor PR

Before merging a skill refactor that extracts content into references:

- [ ] Every extracted reference has a 1-line inline anchor
- [ ] High-risk steps (where improvisation = wrong output) still have inline examples
- [ ] Numbered-step framing for "read @reference" (not "see also")
- [ ] Deterministic operations are scripts, not prompts
- [ ] Duplicated logic between command and skill is collapsed to one SSOT
- [ ] Eval suite run on baseline AND new version; skip rate + format-correct rate compared
- [ ] No metric regression > 2–3% on any high-risk path
