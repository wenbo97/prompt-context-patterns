# Category 4: Input/Output Contracts

How data flows in and out — output templates, error handling, configuration, and platform adaptation.

**Related foundational techniques:** Schema Priming, Grounding/Anchoring, Cognitive Offloading (see [prompt-engineering-for-skills.md](../techniques/token-level-techniques))

---

## Pattern 14: Structured Output Templates

**Prevalence:** ~26% of skills (590 files)
**Related patterns:** [Few-Shot Examples](#pattern-25), [Scoring Rubrics](#pattern-27), [Progress Feedback](#pattern-9)

**What it is:** Prescribing the exact format, structure, or template that the agent's output must follow — from table schemas and report sections to complete markdown documents with placeholder variables.

**When to use:**
- When downstream consumers (humans or automation) need to parse the output
- When consistency across runs matters (comparing reports over time)
- When the output is complex enough that format drift would reduce usefulness
- When the skill's value is in the structure, not just the content

### Positive Example
```markdown
### Output
# Pitch Review — CodePilot

**Format:** 5 slides, ~3 minutes | **Overall:** 16/25 (Adequate)

## Scorecard

| Criterion | Score | Feedback |
|-----------|-------|----------|
| Hook | 2/5 | Title slide alone is not a hook. Start with a pain point: "Your PR has been waiting 3 days. Sound familiar?" |
| Problem / Solution | 4/5 | Problem is clear and quantified. Solution is specific. Add one metric: "reduces review time by 60%." |
| Demo Flow | 4/5 | Live demo in VS Code is strong. Add a before/after comparison to make impact visible. |
| Technical Clarity | 4/5 | Architecture diagram is clear. Mention latency and cost briefly for judge credibility. |
| Call to Action | 2/5 | "Thank you" is not a CTA. End with: "Try it today — install from VS Code marketplace." |

## Suggested Improved Outline

| Slide | Content | Time |
|-------|---------|------|
| 1 | **Hook:** "Your PR has been waiting 3 days." + problem stat | 0:00–0:30 |
| 2 | **Solution:** CodePilot overview + key metric (60% faster reviews) | 0:30–1:00 |
| 3 | **Demo:** Live VS Code refactor suggestion → PR comment | 1:00–2:00 |
| 4 | **How It Works:** Architecture + cost/latency | 2:00–2:30 |
| 5 | **CTA:** "Install now" or "Join our beta" + team slide | 2:30–3:00 |

Complete — pitch scored 16/25, 5 actionable improvements provided.
```

**Why this works:** The template shows the exact structure a completed output should have — header format, scorecard table columns, improved outline table columns, and closing status line. The model can't invent a different structure because the shape is fully specified. The example includes populated content, not just column headers, so the model sees what a real entry looks like (e.g., feedback is a specific suggestion, not a grade).

### Negative Example

```markdown
Output the results in a structured way. Include the scores and feedback.
Make it clear and easy to understand. Use a table if appropriate.
```

**Why this fails:** "Structured way" could be JSON, YAML, markdown table, bullet list, or plain prose — the model picks a different one each time. "If appropriate" makes table usage optional. No column definitions means the model might create a 3-column table on one run and a 7-column table on the next. No example content means the model might put grades in the feedback column instead of specific suggestions.

---

## Pattern 15: Error Handling / Graceful Degradation

**Prevalence:** ~10% of skills (222 files)
**Related patterns:** [Phased Execution](#pattern-2), [Tool Routing Tables](#pattern-21), [Configuration Persistence](#pattern-16)

**What it is:** Prescribing what the agent should do when things go wrong — tool failures, missing data, timeouts, malformed inputs — with phase-specific degradation strategies.

**When to use:**
- Multi-phase workflows where partial results are still valuable
- Skills that depend on external tools/APIs that can fail
- Skills with multiple data sources where some may be unavailable
- Long-running workflows where a single failure shouldn't waste all prior work

### Positive Example
```markdown
### Timeout & Error Handling
Every Bash command specifies a timeout. On timeout:
1. Retry ONCE with the same timeout
2. If retry fails, apply graceful degradation:
   - **Phase 1 (metadata) timeout/failure:** STOP — no manifest, cannot proceed
   - **Phase 2 (collect) timeout/failure:** Check if manifest was partially written.
     If `changed_files` present → re-run Phase 3 with `--api-only`. If missing → STOP
   - **Phase 3 (finalize) timeout/failure:** Check if partial diffs exist.
     If some → proceed with available diffs. If none → STOP
   - **Agent timeout/failure:** Log "Agent {name} did not complete" and continue with
     remaining agents' results. If ALL 5 agents fail → STOP
   - **Posting (Step 8.1) timeout:** Report partial results and offer retry

Common error patterns:
- `az CLI not found` → tell user to run `az login`
- HTTP 401/403 (ADO) → token expired, re-run `az login`
- HTTP 404 → PR not found, verify URL
- `No manifest found` → Phase 1 did not complete, re-run from Phase 1

### Partial Result Handling
- Missing diff for a file → skip that file, note in output
- Missing local context → proceed without (review still works, just shallower)
- Agent returns no findings → treat as "no issues found" (not an error)
- Agent returns malformed output → attempt salvage (infer severity from keywords)
```

**Why this works:** Each failure mode has a specific response — not a generic "handle errors gracefully." The degradation is phase-specific: Phase 1 failure is fatal (no data), but Phase 3 failure allows partial results. The retry policy is explicit (once, same timeout). Common error patterns are mapped to specific user-facing messages with actionable fixes. Partial result handling defines what "skip" means for each data type.

### Negative Example

```markdown
If something goes wrong, try to recover gracefully. Report any errors to the user.
If a tool fails, try an alternative approach.
```

**Why this fails:** "Try to recover gracefully" gives no recovery strategy. "Try an alternative approach" doesn't specify what the alternatives are for each tool. Each run will handle failures differently — sometimes retrying, sometimes skipping, sometimes stopping. No distinction between fatal failures (Phase 1 — can't proceed) and non-fatal ones (one agent — can proceed with others).

---

## Pattern 16: Configuration Persistence / First-Time Setup

**Prevalence:** ~4% of skills (80-100 files)
**Related patterns:** [Interactive Flow Control](#pattern-7), [Cross-Platform Handling](#pattern-17), [$ARGUMENTS Pattern](#pattern-4)

**What it is:** A "check for config, create if missing" pattern for skills that need user-specific settings across sessions. The config is saved to a well-known path and loaded on subsequent invocations.

**When to use:**
- Skills that need organization/project/team context that doesn't change between runs
- Skills that depend on external tool authentication (az login, gh auth)
- Skills that need user preferences that should persist
- Multi-command plugins where all commands share the same config

### Positive Example
```markdown
## First-Time Setup

On every invocation, check whether saved configuration exists before doing anything else.

### Step 1: Load Saved Configuration

Check for the config file. Use `$HOME` which works across all platforms:

    cat "$HOME/.config/ado-flow/config.json" 2>/dev/null

If the file exists and contains valid JSON with all required fields (`organization`,
`work_item_project`, `pr_project`), skip ahead to the relevant task workflow.

If the file does not exist or is missing fields, proceed with setup steps below.

### Step 2: Check Prerequisites

Verify Azure CLI and the DevOps extension are installed:

    az version 2>/dev/null && az extension show --name azure-devops 2>/dev/null

If Azure CLI is missing, display install instructions per platform.

### Step 3: Collect Configuration

Ask the user for these details one at a time:

1. **Organization name** - "What is your Azure DevOps organization name?"
2. **Project for work items** - "What project should I create work items in?"
3. **Project for pull requests** - "What project are your repositories in?"

### Step 4: Save Configuration

    mkdir -p "$HOME/.config/ado-flow"
    cat > "$HOME/.config/ado-flow/config.json" <<EOF
    {
      "organization": "{ORG}",
      "work_item_project": "{WORK_ITEM_PROJECT}",
      "pr_project": "{PR_PROJECT}"
    }
    EOF

Confirm: "All set! Your configuration has been saved."
```

**Why this works:** The check-load-setup-save flow is explicit and deterministic. Required fields are named (`organization`, `work_item_project`, `pr_project`) — the model knows exactly what constitutes "valid" config. Prerequisite checking happens before data collection (don't collect org name if az CLI isn't installed). The config path uses `$HOME` for cross-platform compatibility. Questions are collected "one at a time" (Pattern 7 composition).

### Negative Example

```markdown
If this is the user's first time, ask them for their Azure DevOps settings.
Save the settings somewhere for next time.
```

**Why this fails:** "Ask for settings" doesn't enumerate which settings. "Save somewhere" doesn't specify a path — each run might save to a different location. No prerequisite check means the skill might collect config and then fail because az CLI isn't installed. No validation step means malformed config gets saved and breaks future runs.

---

## Pattern 17: Cross-Platform Handling

**Prevalence:** ~3% of skills (60-80 files)
**Related patterns:** [Configuration Persistence](#pattern-16), [Error Handling](#pattern-15)

**What it is:** Providing different instructions for Windows, macOS, and Linux environments — different commands, paths, tools, and fallback chains.

**When to use:**
- Skills that use system-specific tools (TTS engines, file managers, notification systems)
- Skills that reference file paths (temp dirs, config dirs)
- Skills that invoke CLI tools with platform-specific availability
- Any skill used across development environments

### Positive Example
```markdown
## Platform Support

| Platform | TTS Engine | Focus Detection |
|----------|-----------|-----------------|
| Windows | OneCore (Mark) with SAPI fallback | Windows Terminal tab inspection (UI Automation) |
| macOS | `say` command (system voices) | `osascript` frontmost app + window title |
| Linux | espeak-ng / spd-say / festival / notify-send | `xdotool` (X11), Wayland stub |

## Cache Location

- **Windows:** `$env:TEMP\claude_voice\{session-id}.txt`
- **macOS/Linux:** `${TMPDIR:-/tmp}/claude_voice/{session-id}.txt`
```

**Why this works:** A table maps each platform to its primary tool and fallback. The fallback chain is explicit (Linux: espeak-ng → spd-say → festival → notify-send). Cache paths use the correct platform-specific environment variables. The Wayland "stub" acknowledgment means the model knows Wayland support is limited rather than attempting X11 commands that will fail silently.

### Negative Example

```markdown
Play a notification sound when done. Use whatever audio tool is available on the system.
```

**Why this fails:** "Whatever is available" requires the model to probe for installed tools at runtime — different tools on different systems. No fallback chain means the model might try `say` on Linux and fail silently. No platform-specific paths means temp files go to `/tmp` on Windows (which maps to `C:\tmp\`, a directory that doesn't exist). Each run on the same platform might use a different tool.
