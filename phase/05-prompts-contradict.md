# Chapter 5: When Prompts Contradict Each Other

## Problem

After 300+ migrations, we noticed bizarre inconsistencies. The AI would produce perfectly formatted output for one project, then completely different formatting for the next. Same skill, same version, different results.

```json
// Project A output (correct):
{"status": "completed", "errors": 0, "pr_url": "..."}

// Project B output (also from the AI, same skill):
## Migration Result
- Status: Done ✓  
- Errors: none
- PR: [link](...)
```

How is the same prompt producing JSON one time and Markdown the next?

## Thinking

We had three files that could be loaded into the AI's context:
- `agent-prompt.md`: "Output results as JSON"
- `migration-guide.md`: "Summarize results in a readable format"  
- `system-config.md`: "Return structured data"

All three were correct individually. But "JSON", "readable format", and "structured data" are three different instructions. The AI follows whichever is **closest to its current position in the context window** — which depends on conversation length, which varies per project.

We also found a subtler version of the same bug: the TFM (target framework) value was written in 12 different skill files. After a few edits, 9 said `net8.0`, 2 said `net8.0;net10.0`, and 1 still said `net6.0`.

## Solution

**One rule, one file.** No exceptions.

We established the **SSOT (Single Source of Truth) pattern**:

```
BEFORE: 
  agent-prompt.md     → "output as JSON"
  migration-guide.md  → "readable format"
  system-config.md    → "structured data"

AFTER:
  rules/output-format.md        → defines the exact JSON schema
  agent-prompt.md               → "See rules/output-format.md"
  migration-guide.md            → "See rules/output-format.md"
  system-config.md              → "See rules/output-format.md"
```

Same for configuration values:

```
BEFORE:
  skill-01.md through skill-12.md → each contains "net8.0" hardcoded

AFTER:
  migration-config.json → {"targetFrameworks": "net8.0;net10.0"}
  skill-01.md through skill-12.md → "read target from migration-config.json"
```

**The rule**: If any value or instruction appears in more than one prompt file, it **will** drift. Extract to a single file. Reference everywhere. This applies to output formats, config values, error handling rules, execution sequences — everything.

**Bonus insight**: When you reduce conflicting instructions from ~240 lines to ~20 lines in a focused single file, the AI follows them more reliably. Shorter, concentrated rules get more model attention than long, diluted ones.
