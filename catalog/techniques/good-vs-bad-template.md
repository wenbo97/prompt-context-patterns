# Prompt Writing Comparison: Good vs Bad

> Same task: Verify whether a .csproj has completed .NET multi-target framework migration
> For use in Claude Code SKILL.md

---

# ❌ BAD Example

```markdown
# Verify Migration

Check if a csproj file has been properly migrated to support multiple target frameworks.

You need to look at the csproj file and make sure it has the right target frameworks.
Check that it has both the old framework and the new one. Also check that the packages
are correct and there aren't any issues. If there are problems, report them. If everything
is fine, say it's good.

Make sure to check:
- The target framework is correct
- Packages are properly conditioned
- No duplicate references
- Build should work
- The file isn't broken

Output the results in a structured way. Include the status and any issues found.
If there are warnings, include those too. Make it clear and easy to understand.

Don't modify any files. This is a read-only check. Be thorough but don't
take too long. If you're not sure about something, flag it as a warning
rather than an error.

Example: if you check a project and it has net472 and net8.0, that's good.
If it only has net472, that's bad because the migration hasn't happened.
```

---

## BAD Example: Line-by-Line Analysis

```
"Check if a csproj file has been properly migrated"
  → "properly" is a subjective word — the model doesn't know what YOUR standard of "properly" is
  → Each execution the model will define "properly" on its own, leading to inconsistent behavior

"make sure it has the right target frameworks"
  → What is "right"? net8.0? net9.0? net10.0? Not specified
  → The model will guess, or guess differently each time

"Also check that the packages are correct and there aren't any issues"
  → "correct" is undefined
  → "issues" is undefined
  → The information content of this sentence is effectively zero

"Output the results in a structured way"
  → "structured way" could be JSON, YAML, Markdown table, plain text list...
  → Ten executions might produce five different formats

"Be thorough but don't take too long"
  → Self-contradictory instructions — the model cannot optimize for two conflicting objectives
  → Each time it will randomly strike a different balance between "thorough" and "quick"

"Example: if you check a project and it has net472 and net8.0, that's good"
  → The example only gives a conclusion ("that's good"), not an output format
  → The model knows what is correct, but doesn't know how to report it

Overall problems:
  → No input/output contract — the caller has no idea what it will receive
  → No enumerated values — "status" could be "good"/"bad"/"ok"/"pass"/"fail"/any word
  → Instructions and constraints are mixed together — the model's attention is diluted evenly across paragraphs
  → No concrete check items — "packages are correct" is not an executable check
  → Example is too vague — it does not show the expected output token sequence
```

---
---

# ✅ GOOD Example

````markdown

# Verify Migration

<!-- version: 1.4.0 -->
<!-- depends_on: upgrade-package-ref@1.x -->
<!-- last_tested: 2026-03-25 -->

## Purpose
Verify whether a single .csproj file has completed multi-target framework migration. Read-only check — does not modify any files.

<input_contract>
- `projectPath`: string — absolute or relative path to the .csproj file
- `netCoreTargets`: string — expected new TFM(s) (e.g., "net8.0" or "net8.0;net10.0")
- `previousTFM`: string — original TFM before migration (e.g., "net472" or "netstandard2.0")
</input_contract>

<output_contract>
| Field        | Type   | Values                                        |
|--------------|--------|-----------------------------------------------|
| `status`     | string | `"PASS"`, `"FAIL"`, `"WARN"`                  |
| `checks`     | array  | Result of each check (see check schema below) |
| `summary`    | string | One-sentence conclusion                       |

Check schema:
| Field      | Type   | Values                                         |
|------------|--------|------------------------------------------------|
| `check`    | string | Check item name (see the check list in Step 2) |
| `result`   | string | `"PASS"`, `"FAIL"`, `"WARN"`, `"SKIP"`         |
| `expected` | string | Expected value                                 |
| `found`    | string | Actual value                                   |
| `detail`   | string | Empty string for PASS; explanation for FAIL/WARN/SKIP |
</output_contract>

<constraints>
1. Do not modify any files — this is a read-only skill
2. Do not run dotnet build — static analysis only
3. If the file at projectPath does not exist, return status: "FAIL" immediately without running any checks
4. Each check is independent — one FAIL does not affect execution of other checks
5. Final status determination rule: any check FAIL → "FAIL"; no FAIL but has WARN → "WARN"; all PASS or SKIP → "PASS"
</constraints>

```

<steps>

## Step 1: Read and Parse .csproj

```bash
cat "$projectPath"
```

If file does not exist → return `{ status: "FAIL", checks: [], summary: "File not found: $projectPath" }`

Extract the following elements from the file content:
- Value of `<TargetFramework>` or `<TargetFrameworks>`
- All `<PackageReference>` elements and their Condition attributes
- All `<ProjectReference>` paths

If any element is missing, handle it according to the specific check's definition (e.g., a missing `<TargetFramework>` is PASS for Check 2, not SKIP).

## Step 2: Execute Check Items

Execute the following checks in order. Each check is independent — one failure does not skip subsequent checks.

### Check 1: TargetFrameworks Contains Both Old and New TFMs

- expected: `<TargetFrameworks>` contains both `{previousTFM}` and every TFM in `{netCoreTargets}`
- PASS: `<TargetFrameworks>net472;net8.0</TargetFrameworks>` when previousTFM=net472, netCoreTargets=net8.0
- FAIL: Still `<TargetFramework>net472</TargetFramework>` (singular form, not migrated)
- FAIL: `<TargetFrameworks>` exists but is missing previousTFM or netCoreTargets

### Check 2: No Singular TargetFramework Exists

- expected: No `<TargetFramework>` tag appears in the file (should have been replaced with plural form)
- PASS: No `<TargetFramework>` tag
- FAIL: `<TargetFramework>` still exists

### Check 3: PackageReference Conditioning

- expected: Platform-specific PackageReferences have Condition attributes
- WARN: Known .NET Framework-only packages (e.g., System.Runtime.Caching) found without Condition
- PASS: All platform-specific packages are conditioned, or no platform-specific packages exist
- Known .NET Framework-only package list: System.Runtime.Caching, System.ServiceModel.*, Microsoft.AspNet.*

### Check 4: No Duplicate PackageReferences

- expected: Same package name does not appear twice (ignoring Condition differences)
- PASS: No duplicates
- WARN: Same package appears under different Conditions (legal but needs manual review)
- FAIL: Same package appears twice under the same Condition

### Check 5: ProjectReference Paths Are Valid

- expected: Every `<ProjectReference Include="...">` path points to an existing file
- PASS: All referenced paths exist
- WARN: A path does not exist (could be a relative path resolution issue)

## Step 3: Assemble Output

Assemble results per the output_contract format. Status determination rule per constraints item 5.

</steps>

<examples>

### Example 1: Normal Pass

<example>

<input>
projectPath: src/Services/Auth/Auth.csproj
netCoreTargets: net8.0
previousTFM: net472
</input>

<expected_output>
{
  "status": "PASS",
  "checks": [
    { "check": "TargetFrameworks contains old+new TFM", "result": "PASS", "expected": "net472;net8.0", "found": "net472;net8.0", "detail": "" },
    { "check": "No singular TargetFramework", "result": "PASS", "expected": "absent", "found": "absent", "detail": "" },
    { "check": "PackageReference conditioned", "result": "PASS", "expected": "all conditioned", "found": "all conditioned", "detail": "" },
    { "check": "No duplicate PackageReference", "result": "PASS", "expected": "no duplicates", "found": "0 duplicates", "detail": "" },
    { "check": "ProjectReference paths valid", "result": "PASS", "expected": "all exist", "found": "3/3 exist", "detail": "" }
  ],
  "summary": "All 5 checks passed. Migration verified."
}
</expected_output>
</example>

### Example 2: Not Migrated + Problematic Packages

<example>
<input>
projectPath: src/Legacy/Reporting.csproj
netCoreTargets: net8.0;net10.0
previousTFM: net472
</input>

<expected_output>
{
  "status": "FAIL",
  "checks": [
    { "check": "TargetFrameworks contains old+new TFM", "result": "FAIL", "expected": "net472;net8.0;net10.0", "found": "net472", "detail": "Still using singular <TargetFramework>. Migration not applied." },
    { "check": "No singular TargetFramework", "result": "FAIL", "expected": "absent", "found": "<TargetFramework>net472</TargetFramework>", "detail": "Singular form still present." },
    { "check": "PackageReference conditioned", "result": "WARN", "expected": "all conditioned", "found": "System.Runtime.Caching unconditioned", "detail": "Known .NET Framework-only package without Condition attribute." },
    { "check": "No duplicate PackageReference", "result": "PASS", "expected": "no duplicates", "found": "0 duplicates", "detail": "" },
    { "check": "ProjectReference paths valid", "result": "PASS", "expected": "all exist", "found": "5/5 exist", "detail": "" }
  ],
  "summary": "2 checks FAILED, 1 WARNING. Migration not complete."
}
</expected_output>
</example>

</examples>
````

---

## Why the GOOD Example Works: Point-by-Point Analysis

```
1. Input Contract is precise down to type and meaning
   BAD:  "look at the csproj file" — which file? How is it passed in?
   GOOD: projectPath: string — absolute or relative path to the .csproj file
   Effect: The model doesn't need to guess the input source — it directly uses $projectPath

2. Output Contract locks down field names and enumerated values
   BAD:  "output the results in a structured way"
   GOOD: status can only be "PASS" | "FAIL" | "WARN", each check has a fixed schema
   Effect: Ten executions, ten identical output formats. Downstream agents can reliably parse

3. Constraints are placed before steps (high-attention position)
   BAD:  "Don't modify any files" buried in the middle of a paragraph
   GOOD: constraints item 1, independently numbered, isolated with XML tags
   Effect: The model has already "seen" the constraints before it starts executing steps

4. Each check item defines specific PASS/FAIL/WARN conditions
   BAD:  "make sure the target framework is correct"
   GOOD: "FAIL: Still <TargetFramework>net472</TargetFramework> (singular form, not migrated)"
   Effect: Instead of letting the model judge what is "correct", it provides enumerated determination conditions

5. Examples show the complete output token sequence
   BAD:  "if it has net472 and net8.0, that's good"
   GOOD: Complete JSON output including specific values for every field
   Effect: The model directly imitates this JSON structure rather than inventing its own

6. Examples cover both happy path and failure path
   BAD:  Only one vague positive example
   GOOD: Example 1 all pass, Example 2 has mixed FAIL + WARN
   Effect: The model sees both patterns and knows what the output looks like on failure

7. Wording eliminates ambiguity
   BAD:  "Be thorough but don't take too long" (contradictory)
   GOOD: "Do not run dotnet build — static analysis only" (clear boundary)
   Effect: The model doesn't need to weigh trade-offs between contradictory instructions

8. Error handling is not separated — it's embedded in the corresponding step
   BAD:  No mention of error cases at all
   GOOD: Step 1 begins with the return value when the file doesn't exist
   Effect: When the model reaches that step, the failure handling is within its attention span

9. Status aggregation rule is explicit and deterministic
   BAD:  "If there are problems, report them" (what counts as a problem?)
   GOOD: "Any check FAIL → FAIL; no FAIL but has WARN → WARN; all PASS → PASS"
   Effect: This is a deterministic logic rule — the model follows it with very high probability

10. Version and dependency info (for humans, not for the model)
    BAD:  Cannot trace which version of the prompt is running
    GOOD: version: 1.4.0, depends_on, last_tested
    Effect: When issues arise, you can quickly pinpoint which modification caused them
```

---

## Core Differences Summary

| Dimension | BAD | GOOD |
|-----------|-----|------|
| Output space | Infinite (model free to improvise) | Highly narrowed (enumerated values + schema) |
| Attention utilization | Evenly diluted (plain paragraph text) | Precisely guided (XML partitioning + positional strategy) |
| Training prior utilization | None (generic English description) | Yes (XML tags activate structured mode) |
| Reproducibility | Low (format differs each time) | High (output contract locks it down) |
| Testability | Impossible (no expected output definition) | Possible (examples serve as test cases) |
| Debugging efficiency | Low (can't tell which step went wrong) | High (each check is independent, pinpointable) |
