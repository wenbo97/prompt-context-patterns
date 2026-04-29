# Category 7: Quality and Feedback

How to ensure output quality — scoring rubrics, self-critique, feedback loops, and version management.

**Related foundational techniques:** Schema Priming, Negative Space, Cognitive Offloading (see [prompt-engineering-for-skills.md](/prompt-context-patterns/catalog/techniques/token-level-techniques))

---

## Pattern 27: Scoring Rubrics / Quantitative Assessment

**Prevalence:** ~4% of skills (80-100 files)
**Related patterns:** [Structured Output Templates](#pattern-14), [Few-Shot Examples](#pattern-25), [Self-Critique](#pattern-28)

**What it is:** Providing numerical scoring frameworks with defined criteria, score ranges, descriptors per score level, and threshold mappings that translate totals into categories.

**When to use:**
- When subjective assessments need to be comparable across runs
- When the output needs quantitative grades (pitch reviews, code quality, readiness audits)
- When multiple dimensions need independent scoring
- When thresholds trigger different follow-up actions

### Positive Example
```markdown
## Scoring Criteria

| # | Criterion | Description | Score Range |
|---|-----------|-------------|-------------|
| 1 | **Hook** | Does the opening grab attention in the first 15 seconds? | 1–5 |
| 2 | **Problem / Solution** | Is the problem clear and the solution compelling? | 1–5 |
| 3 | **Demo Flow** | Is the demo logical, smooth, and shows the product working? | 1–5 |
| 4 | **Technical Clarity** | Are technical choices explained clearly for the audience? | 1–5 |
| 5 | **Call to Action** | Does the pitch end with a clear ask or next step? | 1–5 |

**Total:** 25 points. Scores map to: 20–25 Strong, 13–19 Adequate, <=12 Needs Work.
```
```markdown
**Scoring rubric for Instruction Clarity:**
- **5/5**: All checks pass. Clear phases, strong directives, output format specified.
- **4/5**: Frontmatter complete, workflow exists, minor language weakness.
- **3/5**: Basic structure exists but missing output format or has weak language.
- **2/5**: Missing frontmatter fields or no clear workflow.
- **1/5**: No frontmatter or unstructured prose.
```

**Why this works:** Each criterion has a name, description, and score range — the model knows exactly what to evaluate and how to rate it. The total-to-category mapping (20-25 Strong, 13-19 Adequate, <=12 Needs Work) makes the final verdict deterministic. The skillqa rubric provides per-score-level descriptors, so the model can distinguish a 3 from a 4 with specific criteria. The five criteria cover distinct dimensions — no overlap between "Hook" and "Call to Action."

### Negative Example

```markdown
Rate the pitch on a scale of 1-10. Consider things like how engaging it is,
whether the demo works, and if the technical approach makes sense.
Give an overall assessment.
```

**Why this fails:** A single 1-10 scale with no rubric means each run calibrates differently. "Consider things like" is a suggestion, not a required set of dimensions. No threshold mapping means "7/10" could be "good" on one run and "needs improvement" on another. No per-level descriptors means the model can't distinguish adjacent scores. Multiple runs on the same input will produce different scores.

---

## Pattern 28: Self-Critique / Quality Self-Check

**Prevalence:** ~2% of skills (30-50 files)
**Related patterns:** [Evidence Chain](#pattern-26), [Negative Constraints](#pattern-6), [Scoring Rubrics](#pattern-27)

**What it is:** Requiring the agent to critique its own output before delivering it — identifying weaknesses, flagging low-confidence areas, and verifying compliance with the skill's rules.

**When to use:**
- Specification/document generation where hidden assumptions are dangerous
- Root cause analysis where premature conclusions waste investigation time
- Any skill where the model's confidence varies and the user needs to know
- Skills that produce actionable recommendations (wrong recommendations are costly)

### Positive Example
```markdown
### Adversarial Self-Critique

The spec author's honest assessment of where this spec is weakest. Not generic failure
modes — specific weaknesses in THIS spec.

**Rules:**
- Minimum 3 weaknesses per spec.
- Each weakness must be specific to THIS spec — "specs can be misinterpreted" is not valid.
- Watch indicators must be observable during execution, not after.

### Weakness 1: [Title]
- **Assumption being made:** [the specific assumption]
- **What happens if wrong:** [what the executor would build incorrectly]
- **Watch indicator:** [observable signal during execution]

### Weakness 2: [Title]
...
```

**Why this works:** "Minimum 3 weaknesses" prevents perfunctory self-review. The explicit rejection of generic weaknesses ("specs can be misinterpreted") forces the model to find real issues specific to this output. The three-field structure (assumption, consequence, watch indicator) makes each weakness actionable — the user knows what to monitor during execution. "Adversarial" framing encourages the model to look for problems rather than defend its work.

### Negative Example

```markdown
Review your output and make sure it's good. Fix any issues you find.
```

**Why this fails:** "Make sure it's good" is the same instruction the model followed while generating the output — self-review with the same criteria produces the same result. No minimum weakness count means the model finds zero weaknesses (everything looks good to the author). No structure for weaknesses means they're generic platitudes. "Fix any issues" means the user never sees the weaknesses — the model silently "fixes" them, which may mean sweeping them under the rug.

---

## Pattern 29: Feedback Solicitation

**Prevalence:** <1% of skills (10-20 files)
**Related patterns:** [Progress Feedback](#pattern-9), [Configuration Persistence](#pattern-16)

**What it is:** Instructing the agent to surface a feedback survey or request at a natural stopping point, with priority tiers and session-level deduplication.

**When to use:**
- Skills being actively iterated on that need user feedback
- Skills with multiple potential failure modes that benefit from bug reports
- When you want to capture feature requests at the moment users encounter gaps
- Production skills that need satisfaction metrics

### Positive Example
```markdown
## Feedback

Surface the feedback survey **at most once per session** at a natural stopping point.

**Link:** [Excel AI Tools Pulse](https://aka.ms/ExcelAIToolsPulse) (anonymous, 2 min)

**When to surface** (pick the first that matches, then stop for the session):

1. **Bug** — something went wrong → offer to draft a brief bug report
2. **Feature gap** — user wants something this skill can't do → offer to draft feature request
3. **Satisfaction** — task completed smoothly → one-line mention
4. **First completion** — skill finished successfully, no other trigger → link in closing output

Never interrupt the active task. Never mention the survey again if declined or ignored.
```

**Why this works:** "At most once per session" prevents feedback fatigue. Priority tiers ensure bugs are surfaced before generic satisfaction questions. "Pick the first that matches, then stop" is a deterministic rule. The "never interrupt the active task" constraint ensures feedback doesn't derail work. Different feedback types get different responses (bug → offer to draft report, satisfaction → one-line mention).

### Negative Example

```markdown
Ask the user for feedback when you're done. Include a link to our survey.
```

**Why this fails:** No session-level dedup means the model asks for feedback after every interaction. No priority tiers means bugs get the same treatment as generic satisfaction. "When you're done" is ambiguous in a multi-step workflow — after every step? Only at the end? No constraint against interrupting active work means the model might ask for feedback mid-analysis.

---

## Pattern 30: Version Check / Update Notification

**Prevalence:** <1% of skills (10-20 files)
**Related patterns:** [Configuration Persistence](#pattern-16), [Error Handling](#pattern-15)

**What it is:** Checking whether the installed plugin version matches the latest available version and notifying the user of updates, with graceful fallback when the check fails.

**When to use:**
- Skills that are actively developed and frequently updated
- Skills where version mismatches cause subtle behavior differences
- Skills distributed through a plugin marketplace
- When users need to stay current for security or compatibility reasons

### Positive Example
```markdown
### Check for Updates

**Run this section on every invocation**, before any other workflow section. It is designed
to be non-blocking — if any step fails (network error, file not found, parse error),
log a brief warning and continue silently.

**Read installed version**

    $installedPluginJson = "$env:USERPROFILE\.copilot\installed-plugins\
      marketplace\my-plugin\.claude-plugin\plugin.json"
    $installedVersion = (Get-Content $installedPluginJson -Raw | ConvertFrom-Json).version

**Fetch latest version from GitHub**

Uses `gh api` (GitHub CLI) for authenticated access, with `Invoke-RestMethod` as fallback:

    # Primary: GitHub CLI
    $base64 = gh api repos/org/plugins/contents/plugins/
      my-plugin/.claude-plugin/plugin.json --jq '.content'
    $latestVersion = ([System.Text.Encoding]::UTF8.GetString(
      [Convert]::FromBase64String($base64.Trim())) | ConvertFrom-Json).version

    # Fallback: direct HTTP (works for public repos)
    $latestUrl = "https://raw.githubusercontent.com/org/plugins/
      main/plugins/my-plugin/.claude-plugin/plugin.json"
    $latestVersion = (Invoke-RestMethod -Uri $latestUrl -TimeoutSec 5).version

**Compare versions** using `[version]` type for numeric comparison.

**Report result:**
- If latest > installed: "Update available: v{installed} → v{latest}" + offer update command
- If versions match: "v{installed} (latest)" + continue
- If check fails: "Could not check for updates. Continuing with installed version."
```

**Why this works:** The check is designed to be non-blocking — network failures don't prevent the skill from running. Two fetch methods (gh api + direct HTTP) provide redundancy. Version comparison uses proper numeric parsing (`[version]` type), not string comparison. The three outcomes (update available, up to date, check failed) are each defined with specific user-facing messages. The update path pauses and asks before updating, not auto-updating.

### Negative Example

```markdown
Check if there's a newer version available. If so, tell the user to update.
```

**Why this fails:** No paths specified for installed or remote version. No fallback for network failures means the skill might crash before doing any real work. No version comparison method — string comparison of "1.9.0" vs "1.10.0" gives wrong results. No handling of the "check failed" case. No user confirmation before updating. "Tell the user to update" doesn't give the actual command.
