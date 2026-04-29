# Claude Code Platform Patterns

Patterns extracted from the **Claude Code system prompt** (Anthropic's official CLI agent). These cover platform-level concerns: how the harness manages memory, permissions, scheduling, tool routing, agent dispatch, and context survival. Extends the catalog with patterns 121-132.

**Source research:** `C:\src\claude-code-system-prompts\claude-code-system-prompt.md` — the full system prompt powering Claude Code CLI.

**Extraction date:** 2026-04-24

---

## Pattern 121: Typed Memory Taxonomy

**Prevalence:** Unique to Claude Code platform (not observed in plugin skills)
**Related patterns:** [Configuration Persistence (16)](#pattern-16), [State File Continuity (70)](#pattern-70), [Reference File Injection (23)](#pattern-23)

**What it is:** A file-based persistent memory system with four discrete memory types — `user`, `feedback`, `project`, `reference` — each with distinct write triggers, usage rules, and staleness profiles. An always-loaded index file (MEMORY.md) points to individual memory files with frontmatter metadata.

**When to use:**
- Multi-session agent systems where conversation state must survive restarts
- When different kinds of remembered information have different lifetimes and verification rules
- When you need to distinguish "who the user is" from "what they told me to do differently" from "what's happening in the project"

### Positive Example

```markdown
## Memory Types

| Type | When to Save | How to Use |
|------|-------------|------------|
| `user` | Learn details about user's role, preferences, knowledge | Tailor behavior to user's perspective |
| `feedback` | User corrects approach OR confirms non-obvious approach | Guide behavior so user doesn't repeat guidance |
| `project` | Learn who is doing what, why, or by when | Understand broader context behind requests |
| `reference` | Learn about resources in external systems | Remember where to look for information |

## What NOT to Save
- Code patterns, architecture, file paths — derive from current state
- Git history — `git log` / `git blame` are authoritative
- Debugging solutions — the fix is in the code
- Anything in CLAUDE.md files

## Staleness Rule
Before acting on a memory: verify it is still correct by reading current
state. If memory conflicts with what you observe now — trust what you see,
update or remove the stale memory.
```

**Why this works:** The four types create a **decision filter** at write time — the agent doesn't dump everything into one log. The "what NOT to save" list is equally important: it prevents the memory from becoming a stale cache of derivable information. The staleness rule ("verify before acting") prevents the most dangerous failure mode of persistent memory — acting on outdated facts.

### Negative Example

```markdown
## Memory
Save important things the user tells you to a memory file.
Read the memory file at the start of each conversation.
```

**Why this fails:** No type taxonomy means everything goes into one file. No staleness rule means the agent trusts 3-week-old memories about file paths that have since been renamed. No "what NOT to save" list means the memory fills with derivable facts (file structure, git history) that rot faster than they're updated.

---

## Pattern 122: Bidirectional Feedback Capture

**Prevalence:** Unique to Claude Code platform
**Related patterns:** [Feedback Solicitation (29)](#pattern-29), [Mandatory Self-Learning After Failure (95)](#pattern-95)

**What it is:** Recording both corrections ("don't do X") AND confirmations ("yes, exactly like that") as feedback memories. Corrections are easy to notice; confirmations are quieter — the system explicitly watches for them.

**When to use:**
- Long-running agent-user relationships where behavioral drift is a risk
- When you want the agent to maintain validated approaches, not just avoid past mistakes
- When the user's silence or acceptance is itself a signal

### Positive Example

```markdown
Record from failure AND success: if you only save corrections, you will
avoid past mistakes but drift away from approaches the user has already
validated, and may grow overly cautious.

## Body Structure for Feedback Memories
Lead with the rule itself, then:
- **Why:** the reason the user gave (a past incident, a strong preference)
- **How to apply:** when/where this guidance kicks in

Knowing *why* lets you judge edge cases instead of blindly following the rule.

## Examples

user: don't mock the database — we got burned last quarter
assistant: [saves: integration tests must hit real DB. Why: mock/prod
           divergence masked a broken migration]

user: yeah the single bundled PR was the right call here
assistant: [saves: for refactors in this area, user prefers one bundled PR.
           Confirmed after I chose this approach — a validated judgment call]
```

**Why this works:** The "Why + How to apply" structure turns a raw instruction into a **transferable principle** — the agent can apply the rule to novel edge cases, not just the exact scenario where it was learned. Capturing confirmations prevents the agent from becoming overly cautious (only remembering what NOT to do).

### Negative Example

```markdown
When the user corrects you, save what they said to avoid repeating the mistake.
```

**Why this fails:** Only captures corrections. After 50 sessions of saving only "don't do X," the agent has a long list of prohibitions but no memory of what worked. It becomes hesitant and second-guesses approaches that were previously validated.

---

## Pattern 123: Reversibility × Blast-Radius Permission Model

**Prevalence:** Core to Claude Code; echoed in ~4% of plugins via [Confirmation Gates (8)](#pattern-8)
**Related patterns:** [Confirmation Gates (8)](#pattern-8), [Read-Only Boundary (12)](#pattern-12), [Tiered Permissions (60)](#pattern-60)

**What it is:** A two-dimensional permission assessment: how reversible is the action, and how far does its effect reach? Local + reversible = proceed freely. Remote + irreversible = always confirm. Critically, **approval is non-sticky** — approving a push once does NOT authorize all future pushes.

**When to use:**
- Autonomous agents that mix safe exploration with risky mutations
- Any system where the agent can affect shared state (git repos, APIs, messaging)
- When you need a mental model for which actions need human approval

### Positive Example

```markdown
## Action Risk Assessment

                    Local              Shared/Remote
                    ┌──────────────────┬──────────────────┐
   Reversible       │ Proceed freely   │ Confirm first    │
                    │ (edit file,      │ (comment on PR,  │
                    │  run tests)      │  create branch)  │
                    ├──────────────────┼──────────────────┤
   Hard to reverse  │ Confirm first    │ ALWAYS confirm   │
                    │ (delete file,    │ (force push,     │
                    │  reset --hard)   │  close PR,       │
                    │                  │  send message)   │
                    └──────────────────┴──────────────────┘

CRITICAL: Approval is NON-STICKY.
A user approving `git push` once does NOT mean they approve it in all contexts.
Authorization stands for the scope specified, not beyond.
```

**Why this works:** The 2×2 matrix gives the agent a **decision framework** rather than a list of specific commands. Non-sticky approval prevents the agent from escalating its own permissions over time through precedent accumulation.

### Negative Example

```markdown
Always ask before running dangerous commands like `rm -rf` or `git push --force`.
```

**Why this fails:** Enumerated dangerous commands will always miss new cases. No framework for evaluating novel actions. No concept of scope — once the user says "yes push," the agent might push everywhere.

---

## Pattern 124: Tool Preference Hierarchy with Hard Routing

**Prevalence:** Core to Claude Code; similar concept in [Tool Routing Tables (21)](#pattern-21) but this adds a **ban layer**
**Related patterns:** [Tool Routing Tables (21)](#pattern-21), [Intent Classification (20)](#pattern-20)

**What it is:** Mapping categories of operations to preferred tools, then BANNING the generic alternative (shell commands) when a dedicated tool exists. This is stronger than "prefer X over Y" — it's "NEVER use Y for this task."

**When to use:**
- Agent harnesses with overlapping tool capabilities (shell can do anything, but dedicated tools are better)
- When the generic tool has worse UX, performance, or auditability
- When you need deterministic tool selection, not probabilistic preference

### Positive Example

```markdown
IMPORTANT: Avoid using Bash to run `find`, `grep`, `cat`, `head`, `tail`,
`sed`, `awk`, or `echo` commands. Instead use the appropriate dedicated tool:

 - File search: Use Glob (NOT find or ls)
 - Content search: Use Grep (NOT grep or rg)
 - Read files: Use Read (NOT cat/head/tail)
 - Edit files: Use Edit (NOT sed/awk)
 - Write files: Use Write (NOT echo >/cat <<EOF)

While the Bash tool can do similar things, the built-in tools provide a
better user experience and make it easier to review tool calls.
```

**Why this works:** The parenthetical "NOT X" after each mapping eliminates ambiguity. The agent can't rationalize "well, grep via bash is faster" — the ban is explicit. The UX justification ("easier to review") gives the agent a reason to internalize the rule rather than treat it as arbitrary.

### Negative Example

```markdown
Use the right tool for the job. Prefer built-in tools when available.
```

**Why this fails:** "Prefer" is not "never." The agent will rationalize using bash for grep when it feels convenient. No explicit mapping means the agent must figure out which tool fits each operation.

---

## Pattern 125: Cache-Aware Scheduling

**Prevalence:** Unique to Claude Code platform (scheduling infrastructure)
**Related patterns:** [State File Continuity (70)](#pattern-70), [Time-Boxed Investigation (77)](#pattern-77)

**What it is:** Selecting delay intervals for recurring/polling tasks based on the LLM prompt cache TTL. The cache has a 5-minute window — sleeping past it means the next wake-up reads the full context uncached (slower, more expensive). The system explicitly identifies a "dead zone" (exactly 300s) that should never be chosen.

**When to use:**
- Any autonomous agent loop with polling/sleep intervals
- Cost-optimization for long-running agent sessions
- Scheduled tasks in LLM-powered systems with caching layers

### Positive Example

```markdown
## Picking delaySeconds

The prompt cache has a 5-minute TTL.

| Range | Cache | When to use |
|-------|-------|-------------|
| 60-270s | Warm (cache hit) | Active work: checking builds, polling state |
| 300s | DEAD ZONE | Worst-of-both: pays cache miss, doesn't amortize |
| 300-3600s | Cold (cache miss) | Genuinely idle: nothing to check for minutes |

**Don't pick 300s.** If you're tempted to "wait 5 minutes," either drop to
270s (stay in cache) or commit to 1200s+ (one miss buys a much longer wait).

Default idle: 1200-1800s (20-30 min). Don't burn cache 12x/hour for nothing.

Think about what you're WAITING FOR, not "how long should I sleep."
If you kicked off an 8-minute build, sleeping 60s burns the cache 8 times
before it finishes — sleep ~270s twice instead.
```

**Why this works:** The "dead zone" concept is memorable and prevents the most wasteful choice. The "think about what you're waiting for" reframe shifts from arbitrary intervals to goal-oriented scheduling. The 8-minute build example makes the cost of wrong intervals concrete.

### Negative Example

```markdown
Wait an appropriate amount of time between checks. Don't check too frequently.
```

**Why this fails:** No framework for "appropriate." No awareness of cache boundaries. The agent will pick round numbers (60s, 300s, 600s) that either waste cache or waste money.

---

## Pattern 126: Agent Briefing Protocol

**Prevalence:** Core to Claude Code's Agent tool; echoed in [Handoff Context Protocol (36)](#pattern-36)
**Related patterns:** [Handoff Context Protocol (36)](#pattern-36), [Hub-and-Spoke (32)](#pattern-32), [Multi-Agent Orchestration (18)](#pattern-18)

**What it is:** A set of rules for how an orchestrator writes prompts to sub-agents. The core principle: "brief the agent like a smart colleague who just walked into the room." Sub-agents have zero context from the parent conversation. The critical anti-pattern: "Never delegate understanding" — never write "based on your findings, fix the bug."

**When to use:**
- Any system that dispatches work to sub-agents
- When the orchestrator must formulate prompts for specialist agents
- When agent results need to be synthesized by the orchestrator, not the agent

### Positive Example

```markdown
## Writing Agent Prompts

Brief the agent like a smart colleague who just walked into the room.
- Explain what you're trying to accomplish and WHY
- Describe what you've already learned or ruled out
- Give enough context that the agent can make judgment calls

**Never delegate understanding.** Don't write:
  "based on your findings, fix the bug"
  "based on the research, implement it"
Those phrases push synthesis onto the agent instead of doing it yourself.

Write prompts that prove you understood: include file paths, line numbers,
what specifically to change.

## Good prompt:
"Review migration 0042_user_schema.sql for safety. Context: we're adding a
NOT NULL column to a 50M-row table. I've checked locking behavior but want
independent verification. Report: is this safe, and if not, what breaks?"

## Bad prompt:
"Look at the migration and tell me if it's safe."
```

**Why this works:** "Smart colleague who just walked in" is an instantly graspable mental model. The "never delegate understanding" rule prevents the laziest failure mode of orchestrators — treating sub-agents as oracle boxes rather than specialist workers. The good/bad contrast makes the difference visceral.

### Negative Example

```markdown
Send clear instructions to the agent. Include relevant context.
```

**Why this fails:** "Clear" and "relevant" are judgment calls with no anchor. The orchestrator will write "investigate the issue and fix it" and believe it's clear.

---

## Pattern 127: Parallel-Safe Step Identification

**Prevalence:** Core to Claude Code's git/PR protocols; similar to [Phased Execution (2)](#pattern-2) but adds parallelism annotations
**Related patterns:** [Phased Execution (2)](#pattern-2), [Multi-Agent Orchestration (18)](#pattern-18)

**What it is:** Annotating multi-step workflows with explicit parallelism markers — which steps can run simultaneously and which must wait for predecessors. Used in Claude Code's git commit protocol, PR creation protocol, and general tool calling guidance.

**When to use:**
- Multi-step workflows where some steps are independent
- When the agent must decide between sequential and parallel execution
- When wrong ordering causes data races or stale reads

### Positive Example

```markdown
## Git Commit Protocol

1. Run these in parallel (all independent):
   - `git status` to see untracked files
   - `git diff` to see staged/unstaged changes
   - `git log` to see recent commit style

2. Analyze all changes and draft commit message (depends on step 1)

3. Run these in parallel:
   - `git add` relevant files
   - Create commit with HEREDOC message
   - Run `git status` after commit (depends on commit completing —
     run sequentially after commit, but parallel with add)

4. If pre-commit hook fails: fix and create NEW commit (never amend)
```

**Why this works:** Numbered steps with explicit "run these in parallel" headers remove ambiguity. The parenthetical dependency notes ("depends on step 1") explain WHY certain steps can't be parallelized. Step 4's "NEW commit (never amend)" prevents the most dangerous error in this flow.

### Negative Example

```markdown
Run git status, git diff, and git log. Then analyze changes and commit.
```

**Why this fails:** No parallelism annotation. The agent runs all three sequentially (3x slower). No dependency reasoning means a future editor might reorder steps incorrectly.

---

## Pattern 128: Context Compaction Survival Protocol

**Prevalence:** Unique to Claude Code platform; extends [State File Continuity (70)](#pattern-70)
**Related patterns:** [State File Continuity (70)](#pattern-70), [Phase Data Contract (SSG P14)](#pattern-14)

**What it is:** Explicit instructions for what state must survive when the system automatically compresses prior messages as the conversation approaches context limits. The agent is told which fields to preserve (by name) and that the conversation is NOT limited by the context window — messages are compressed, not lost.

**When to use:**
- Long-running agent sessions that exceed context window limits
- Multi-phase workflows where early decisions affect late phases
- Any system with automatic context compression/summarization

### Positive Example

```markdown
## Context Compaction

The system will automatically compress prior messages as it approaches
context limits. This means your conversation is not limited by the
context window.

When compaction occurs, preserve ALL fields from the Phase Data Contract:
- projectPath, netCoreTargets, assemblyName, branchName
- LocalBuildStatus, LocalBuildAttempts, LocalBuildErrors
- Current phase number (0, 1, 1.5, 2, 3, or 4)

During Phase 3, ALSO preserve build-repair loop state:
- quickbuildUsed (boolean)
- previousRootCauses (array)
- Current attempt counter N
```

**Why this works:** Named fields are unambiguous — the agent knows exactly what to keep. Phase-specific additions (Phase 3 loop state) prevent the "preserve everything" anti-pattern. The reassurance that "conversation is not limited" prevents the agent from panicking about context loss.

### Negative Example

```markdown
Try to remember important information from earlier in the conversation.
```

**Why this fails:** "Important" is undefined. The agent will either remember too much (wasting compressed context on derivable facts) or too little (losing critical state like the current attempt counter).

---

## Pattern 129: Non-Sticky Authorization Scope

**Prevalence:** Unique to Claude Code; extends [Confirmation Gates (8)](#pattern-8) with a temporal dimension
**Related patterns:** [Confirmation Gates (8)](#pattern-8), [Tiered Permissions (60)](#pattern-60)

**What it is:** The explicit rule that user approval of an action in one context does NOT create a standing authorization. Each approval is scoped to the specific request, not the action category. This prevents "permission creep" where an agent accumulates implicit approvals over a long session.

**When to use:**
- Long-running agent sessions where the same action type recurs in different contexts
- When the risk profile of an action changes with context (pushing to feature branch vs main)
- Safety-critical systems where permission scope must be explicit

### Positive Example

```markdown
A user approving an action (like a git push) once does NOT mean that they
approve it in all contexts. Unless actions are authorized in advance in
durable instructions like CLAUDE.md files, always confirm first.

Authorization stands for the scope specified, not beyond.
Match the scope of your actions to what was actually requested.
```

**Why this works:** Two sentences, crystal clear. "Scope specified, not beyond" is a memorable principle. The exception (CLAUDE.md durable instructions) prevents the rule from being annoying for explicitly pre-authorized actions.

---

## Pattern 130: Investigate Before Destroying

**Prevalence:** Unique to Claude Code; extends [Read-Only Boundary (12)](#pattern-12) with an investigation mandate
**Related patterns:** [Read-Only Boundary (12)](#pattern-12), [Confirmation Gates (8)](#pattern-8)

**What it is:** When encountering unexpected state (unfamiliar files, branches, configurations, lock files), the agent must investigate the root cause before taking destructive action. This prevents the agent from using destruction as a shortcut to remove obstacles.

**When to use:**
- Autonomous agents operating in shared development environments
- When the workspace may contain other people's in-progress work
- Any agent that has access to destructive operations (delete, reset, clean)

### Positive Example

```markdown
When you encounter an obstacle, do not use destructive actions as a shortcut.

- Try to identify root causes and fix underlying issues rather than
  bypassing safety checks (e.g. --no-verify)
- If you discover unexpected state like unfamiliar files, branches, or
  configuration, investigate before deleting or overwriting — it may
  represent the user's in-progress work
- Resolve merge conflicts rather than discarding changes
- If a lock file exists, investigate what process holds it rather than
  deleting it

In short: measure twice, cut once.
```

**Why this works:** Concrete examples (lock files, unfamiliar branches, merge conflicts) anchor the abstract principle. "May represent the user's in-progress work" gives a WHY that makes the rule feel protective rather than bureaucratic. "Measure twice, cut once" is a memorable anchor.

### Negative Example

```markdown
Be careful with destructive operations. Ask before deleting things.
```

**Why this fails:** "Be careful" is not actionable. No investigation mandate. The agent might ask "can I delete this lock file?" without investigating what holds it — the question itself is premature.

---

## Pattern 131: Output Visibility Awareness

**Prevalence:** Unique to Claude Code platform
**Related patterns:** [Progress Feedback (9)](#pattern-9), [Structured Output Templates (14)](#pattern-14)

**What it is:** The agent is explicitly told that users can't see most tool calls or internal thinking — only text output is visible. This creates a communication obligation: state what you're about to do before the first tool call, give updates at key moments, and summarize at end of turn.

**When to use:**
- Any agent where tool execution is hidden from the user
- When the user experiences the agent as a text stream, not a tool-call log
- When silence during long operations would confuse the user

### Positive Example

```markdown
Assume users can't see most tool calls or thinking — only your text output.

Before your first tool call: state in one sentence what you're about to do.
While working: give short updates at key moments — when you find something,
change direction, or hit a blocker.
End-of-turn summary: one or two sentences. What changed and what's next.

Brief is good — silent is not. One sentence per update is almost always enough.

Don't narrate your internal deliberation. State results and decisions directly.
Write so the reader can pick up cold: complete sentences, no unexplained jargon.
```

**Why this works:** "Brief is good — silent is not" captures the tension perfectly. The three-point structure (before/during/after) covers the full turn lifecycle. "Pick up cold" prevents context-dependent shorthand that confuses users who scrolled away.

### Negative Example

```markdown
Keep the user informed about what you're doing.
```

**Why this fails:** No structure for when to communicate. The agent either narrates every tool call (noisy) or says nothing until the end (confusing).

---

## Pattern 132: Hook-Driven Automation Awareness

**Prevalence:** Unique to Claude Code platform
**Related patterns:** [Confirmation Gates (8)](#pattern-8), [Configuration Persistence (16)](#pattern-16)

**What it is:** The system declares that users can configure shell commands ("hooks") that execute automatically in response to tool calls or events. The agent must treat hook feedback as coming from the user, and if blocked by a hook, adapt rather than retry.

**When to use:**
- Agent platforms with extensible event systems
- When external processes can intercept and modify agent behavior
- When the agent needs to distinguish between user-initiated and system-initiated feedback

### Positive Example

```markdown
Users may configure 'hooks' — shell commands that execute in response to
events like tool calls, in settings.

Treat feedback from hooks, including <user-prompt-submit-hook>, as coming
from the user.

If you get blocked by a hook:
1. Determine if you can adjust your actions in response to the blocked message
2. If not, ask the user to check their hooks configuration
3. Do NOT re-attempt the exact same action that was blocked
```

**Why this works:** "Treat as coming from the user" is a simple attribution rule. The three-step response (adapt → escalate → don't retry) prevents infinite loops. The explicit "do NOT re-attempt" prevents the most common failure mode.

### Negative Example

```markdown
The system may run additional checks on your tool calls. Handle any errors that occur.
```

**Why this fails:** No attribution model. "Handle errors" could mean retry, which is exactly wrong when a hook intentionally blocked the action.
