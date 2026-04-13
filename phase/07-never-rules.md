# Chapter 7: NEVER Rules — Learning from Production Failures

## Problem

Three different failure patterns kept recurring despite our prompt improvements:

**Failure A**: Build log analysis missed obvious errors
```
[Build Agent] Parsing build output with findstr...
[Build Agent] No errors found! ✓
[Reality] There were 3 errors. findstr's regex silently failed on the pattern.
```

**Failure B**: A 2-minute dependency analysis took 20+ minutes
```
[Migrator] Analyzing dependencies for ProjectA...
[Migrator] Let me run a quick build to check if Dependency X is needed...
[Migrator] Now let me try building without Dependency Y...
[Migrator] What about Dependency Z...
           ↑ 6 "exploratory builds" during what should be a file-reading phase
```

**Failure C**: Build cache corruption
```
[Build Agent] Running quickbuild... (partial incremental build)
[Build Agent] Error found. Fixing...
[Build Agent] Running quickbuild again...
[Build Agent] Different error?! The cache is stale from the first quickbuild.
```

## Thinking

These aren't bugs in the traditional sense. The AI's actions are individually reasonable:
- `findstr` is a legitimate Windows tool for searching text
- Running a build to check a dependency is a valid analysis technique
- Running quickbuild twice to verify a fix makes sense

The problem is **context-specific constraints** that the AI doesn't know about:
- `findstr` has quirky Windows regex behavior that silently drops matches
- The dependency analysis phase should be read-only — builds belong to a later phase
- `quickbuild` modifies cache state, so a second run sees stale data

## Solution

We formalized these as **NEVER rules** — the highest-attention prompt element:

```markdown
## NEVER Rules

NEVER use `findstr` for parsing build logs.
→ Reason: Windows regex silently drops matches on certain patterns.
→ Use: Read the log file directly and search with string matching.

NEVER run build commands during the dependency analysis phase.
→ Reason: This phase is read-only. Builds belong to the Build phase.
→ What to do instead: Analyze .csproj XML and project references only.

NEVER run `quickbuild` more than once per session.
→ Reason: First run modifies build cache. Subsequent runs see stale state.
→ What to do instead: Use full `build` for verification after fixes.
```

Why "NEVER" specifically?

We tested different phrasings:
- "Avoid using findstr" → AI used it 40% of the time
- "Prefer not to use findstr" → AI used it 60% of the time
- "Do not use findstr" → AI used it 15% of the time
- "**NEVER** use findstr" → AI used it <5% of the time

**The rule**: Extract NEVER rules from observed production failures, not from theoretical concerns. Each NEVER rule should include the **reason** (so the AI understands the constraint) and the **alternative** (so it knows what to do instead).
