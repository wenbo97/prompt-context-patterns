# Stable Branching in Skills: Suggestions

**Core principle:** if a branch can be decided by code, don't hand it to the LLM. The more a branch depends on a natural-language condition, the higher the drift probability.

Ordered from most to least stable — these techniques compose.

## 1. Push the decision into a hook or bash preprocessing (most stable)

If both "problem XX" and "whitelist hit" are programmatically detectable, resolve the branch *before* the skill even runs:

- A `UserPromptSubmit` hook detects problem XX → checks the whitelist → injects the result into context (e.g. `<branch>condition_1</branch>`). The skill body then only executes; it does not decide.
- Or preprocess at the top of `SKILL.md` with bash:

  ```bash
  if grep -qF "$TARGET" "${CLAUDE_PLUGIN_ROOT}/whitelist.txt"; then
    export BRANCH=1
  else
    export BRANCH=2
  fi
  ```

  The prompt then dispatches on `$BRANCH` with no ambiguity.

Whatever this layer can resolve should not be left to the prompt layer.

## 2. Force "decide first, then act" via externalized CoT

If the LLM really must judge, don't let it reason and act in the same breath. Require it to **materialize the judgment as structured output first**, then execute:

```xml
<assessment>
  <problem_detected>yes|no</problem_detected>
  <whitelist_hit>yes|no|n/a</whitelist_hit>
  <chosen_branch>1|2|none</chosen_branch>
  <rationale>one-line justification</rationale>
</assessment>
```

The subsequent action becomes "execute the conclusion of `assessment`" rather than "think and act simultaneously." This lifts branch stability more than few-shot alone — measurable in a quick eval.

## 3. Use a decision table instead of natural-language if-else

Avoid prose like "if…, otherwise…". Write explicit XML branches whose preconditions are boolean expressions, not sentences:

```xml
<branch when="problem_xx AND whitelist_hit">…</branch>
<branch when="problem_xx AND NOT whitelist_hit">…</branch>
<branch when="NOT problem_xx">no-op, exit</branch>
```

## 4. Few-shot must cover all branches plus negative examples

At minimum three: whitelist hit, whitelist miss, and **a negative example that does not trigger problem XX at all**. The negative is the easiest one to forget and the most important for preventing over-triggering. Add one or two edge cases on top (empty whitelist, ambiguous problem signal).

## 5. Split into separate skills when branch actions diverge significantly

If `condition_1` and `condition_2` differ substantially in tool-call surface or output format, keeping them in one skill means their few-shot examples fight each other for signal. Route at a higher level — via a command or hook — and let each skill serve a single branch. Overall stability is usually better.

## Recommended rollout order

1. Resolve what you can with a hook (#1).
2. For the rest, combine externalized CoT (#2) with a decision table (#3) as the backbone.
3. Cover the edges with few-shot (#4).
4. Only split skills (#5) if the first four still can't hold the branch stable.

**Quantitative validation:** run the eval harness from `skill-creator` with 5–10 cases per branch and read the hit rate. More reliable than intuition.

---

## Appendix: Decision Tree A/B Test Example

### The scenario

A deployment assistant must decide what to do given a server config and deployment request. The logic has 5 branches.

### Prose version (unstable)

```
Rules:
- If the server is in maintenance mode and the deployment is not marked as urgent, skip.
- If the server is in maintenance mode but the deployment is urgent, proceed with warning.
- If the server is healthy and the target matches, deploy normally.
- If the server is healthy but the target doesn't match, reject.
- If the server status is unknown, check health first.
```

### Decision tree version (stable)

```
## Server status?
├─ "maintenance"
│   └─ Deployment urgent?
│       ├─ YES → action: "deploy", add warning: "server in maintenance"
│       └─ NO  → action: "skip", reason: "server in maintenance, non-urgent"
├─ "healthy"
│   └─ target_env matches server environment?
│       ├─ YES → action: "deploy", reason: "normal deployment"
│       └─ NO  → action: "reject", reason: "environment mismatch"
└─ other/unknown
    └─ action: "check_health", reason: "server status unknown"
```

### Results (5 runs each, ambiguous input: status="degraded")

- **Prose:** correct decision 5/5, but action name, reason text, and warnings array vary across runs. One run added extra commentary outside the JSON.
- **Tree:** correct decision 5/5, identical output all 5 runs. Action and reason match the tree leaf exactly.

Full test: [prompt-context-patterns/eval/decision-tree-ab](https://github.com/wenbo97/prompt-context-patterns/tree/master/eval/decision-tree-ab)
