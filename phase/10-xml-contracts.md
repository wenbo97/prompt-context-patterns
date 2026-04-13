# Chapter 10: Same Prompt, Different Shape Every Time

## Problem

We had 14 skills in the migration pipeline. Each skill's output was consumed by the next skill or by an agent. But the output **shape** kept changing:

```
Run 1: {"status": "pass", "error_count": 0}
Run 2: {"result": "success", "errors": []}
Run 3: Status: PASS\nErrors: none
```

Same skill, same input, three different outputs. The downstream agent tries to parse `result.status` and gets `undefined` because this time the field is called `result`.

## Thinking

The skill prompt said:

```markdown
Return the build result including status and any errors found.
```

This is the prompt equivalent of a function with no type signature. The AI returns "the build result" in whatever format feels natural at that moment. JSON keys, field names, even the choice between JSON and plain text — all undefined.

We needed **contracts**: a formal definition of what goes in and what comes out, that the AI actually respects.

After testing different approaches:
- Markdown tables describing the format → AI follows ~70% of the time
- JSON schema in a code block → AI follows ~80% of the time
- **XML tags** defining input/output → AI follows ~95% of the time

## Solution

Wrapped every skill and agent with XML-structured contracts:

```xml
<skill name="run-build">
  
  <input>
    - project_path: string — absolute path to .csproj
    - build_mode: "full" | "quick" — type of build to run
  </input>
  
  <output>
    - status: "PASS" | "FAIL" | "ERROR"
    - error_count: integer
    - errors: array of {code: string, message: string, file: string}
    - duration_seconds: integer
  </output>
  
  <constraints>
    1. Return EXACTLY the fields listed in <output>. No extra fields.
    2. Status must be one of the three enum values. Not "success", not "passed".
    3. If build cannot run, status is "ERROR", not "FAIL".
  </constraints>
  
  <steps>
    1. Execute build command for the given project_path
    2. Parse build output for error lines
    3. Classify each error by code
    4. Assemble output per the schema above
  </steps>

</skill>
```

**Why XML works better than markdown or JSON schema**:

XML tags activate a different mode in the language model. When the model sees `<output>`, it treats the content as a **formal specification** rather than a suggestion. It's the difference between:
- "Please return status and errors" → the model interprets freely
- `<output>status: "PASS"|"FAIL"|"ERROR"</output>` → the model follows the spec

We also added `<context><references>` blocks to agents, telling them **when** to read each rule file:

```xml
<context>
  <references>
    - BEFORE starting: Read rules/error-categories.md
    - WHEN encountering NU1701: Read rules/nu1701-handling.md
    - BEFORE escalating to Tier 3: Read rules/tier-escalation.md
  </references>
</context>
```

Without this, agents loaded all rules upfront and sometimes applied Phase 1 rules during Phase 2.

## Testing Prompt Changes

The final piece: **prompt regression tests**. We built a test suite where each skill has scenario-based tests:

```yaml
# Test: upgrade-packages skill
tests:
  - name: "Mixed upgrade and skip"
    input:
      csproj: fixtures/mixed-packages.csproj
      packages_csv: fixtures/packages.csv
    assert:
      - type: contains
        value: "VersionOverride=\"4.0.0\""
      - type: not-contains
        value: "VersionOverride=\"1.0.0\""  # this package should be skipped
        
  - name: "No-op for netstandard-only project"
    input:
      csproj: fixtures/netstandard-only.csproj
    assert:
      - type: equals
        value: "NO_CHANGES_NEEDED"
```

Now a prompt change can be tested in seconds instead of running a 30-minute migration.

**The rules**:
1. XML `<input>` and `<output>` tags produce dramatically more consistent results than prose instructions.
2. Tell agents WHEN to read each rule file, not just that the files exist.
3. Prompt changes need regression tests. Without them, every edit is a gamble.
