# Chapter 8: Six Bugs That Were Actually Prompt Bugs

## Problem

After stabilizing the architecture, we did a systematic review of remaining failures. Six P0 issues looked like code bugs but were actually **prompt design flaws**.

## The Six Bugs

### Bug 1: The Temporal Paradox

```yaml
Agent Step 1.5: Read build_attempts from session state
Agent Step 3:   Set build_attempts = count(builds)
```

Step 1.5 reads a value that Step 3 creates. Sometimes it finds a leftover value from a previous run. Sometimes it finds null. The agent behaves differently each time.

**Fix**: Document the data flow. Every step declares what it reads and writes. Cross-check when inserting new steps between existing ones.

### Bug 2: String + String ≠ Number + Number

```
build_attempts = "1"    // string from JSON parse
build_attempts += "1"   // string concatenation
build_attempts += "1"   // now it's "111", not 3
```

In prompt-driven systems, data types aren't enforced. The AI passes values between steps as whatever the runtime decides.

**Fix**: Explicit type conversion at every boundary: `build_attempts = parseInt(build_attempts) + 1`

### Bug 3: null Means Infinity

```javascript
max_turns = config.max_turns;  // undefined — config didn't set it
while (current_turn < max_turns) {  // undefined comparison → always false? always true?
    // depends on the runtime. some treat it as "no limit"
}
```

**Fix**: `max_turns = config.max_turns ?? 50` — always provide a safe default. "Not set" should never mean "infinite."

### Bug 4: Uncounted Recovery Builds

The agent tracked build attempts to know when to give up. But "infrastructure error" builds (network timeout, disk full) weren't counted. After 3 infra errors and 2 real builds, the agent thought it had 2 attempts when it actually had 5.

**Fix**: Count all builds, regardless of why they failed. The context window doesn't care about the reason.

### Bug 5: "Mostly Worked" Is Not a Status

```
Status: completed_with_errors
Definition: "if there are some issues but the migration mostly worked"
```

Two reviewers disagreed on whether a project with 1 warning was "completed" or "completed_with_errors." If humans disagree, the AI will be random.

**Fix**: Deterministic criteria:
```
completed         = local build PASS + CI build PASS
completed_w_errors = local build PASS + CI build WARNINGS (not errors)
failed            = everything else
```

### Bug 6: Tool Name Too Long

```
Tool name: "persistent-build-environment-manager_initialize_environment"
Some AI clients: truncated to "persistent-build-enviro..." → tool not found
```

**Fix**: Rename to short names. `ssg_init_env` works everywhere.

## The Pattern

All six bugs share a trait: **they worked in testing but failed at scale**. A temporal paradox only triggers when there's leftover state. String concatenation only matters when the count exceeds 9. Null-as-infinity only matters when the config file is incomplete.

**The rule**: In prompt-driven systems, every implicit assumption is a future bug. Make types explicit, defaults explicit, status criteria explicit, and tool names short.
