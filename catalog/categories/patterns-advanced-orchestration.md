# Advanced Agent Orchestration Patterns

Deep patterns for multi-agent coordination, routing, consensus, and delegation — extending the foundational orchestration patterns (18-22) with production-grade architectures discovered across 560+ plugins.

**Source research:** agent-orchestrator, multiagent-planning, review-swarm, consensus-code-review, review-verdict, zen-agents, dev-team, triage-team, delegate-agency, mtp-e2e-orchestrator, model-router, component-router, synthetics-agents

---

## Pattern 31: Adversarial Persona Framing

**Prevalence:** ~3% of orchestration plugins
**Related patterns:** [Persona/Role Assignment](#pattern-5), [Multi-Agent Orchestration](#pattern-18), [Self-Critique](#pattern-28)

**What it is:** Assigning agents explicitly adversarial mindsets with attack/defense stances, rather than neutral analysis roles. The agent is told to assume problems exist and to actively try to break things.

**When to use:**
- Code review where finding real bugs matters more than politeness
- Security analysis where a penetration tester mindset improves coverage
- Design review where challenging assumptions prevents groupthink
- Any multi-agent setup that benefits from intellectual tension

### Positive Example

```markdown
You are the **attacker** in an adversarial panel.
BREAK things. Find flaws, edge cases, and failure modes.
Assume there's at least one issue - find it.
```

```markdown
**The Breaker** (Correctness):
Think like a chaos monkey. Your sole focus is finding ways this code
**produces wrong results, crashes, or behaves unexpectedly**.
Your mindset:
- "What if I send garbage?"
- "What if I click rapidly?"
- "What if the network dies mid-call?"

**The Exploiter** (Security):
Think like a penetration tester. Your sole focus is finding ways this code
can be **exploited, abused, or leak sensitive data**.
```

**Why this works:** Concrete attack questions ("What if I send garbage?") are more actionable than "look for bugs." The chaos-monkey/pentester metaphors encode proven methodologies. Assigning adversarial intent overcomes the model's default tendency toward agreement and validation.

### Negative Example

```markdown
Review the code carefully and look for any issues. Be thorough.
```

**Why this fails:** No adversarial framing means the model defaults to confirmatory analysis. "Be thorough" doesn't specify an attack strategy.

---

## Pattern 32: Hub-and-Spoke SDLC State Machine

**Prevalence:** ~1% of plugins (but highly impactful)
**Related patterns:** [Phased Execution](#pattern-2), [Multi-Agent Orchestration](#pattern-18)

**What it is:** A central orchestrator agent that owns a state machine representing the software development lifecycle. Specialist agents are stateless workers that complete one state transition and return control to the hub via a structured Completion Report.

**When to use:**
- End-to-end development workflows spanning requirements → design → review → deploy
- When multiple specialist agents must work in sequence with handoff context
- When the orchestrator needs to track overall progress across many steps

### Positive Example

```markdown
## SDLC State Machine

INTENT_RECEIVED → PRD_CREATED → DESIGN_CREATED → DESIGN_REVIEWED_R1 →
DESIGN_R1_ADDRESSED → DESIGN_REVIEWED_R2 → IMPLEMENTATION_PLANNED →
IMPLEMENTED → PEER_REVIEWED → PR_COMMENTS_ADDRESSED → MERGED → DEPLOYED

## Completion Report (required from every specialist agent)

| Field | Value |
| **Agent** | peer-reviewer |
| **State Completed** | PEER_REVIEWED |
| **Artifacts** | {PR ID, review comments posted} |
| **Summary** | Reviewed PR #NNN, posted M comments |
| **Findings** | Blocker: N, High: N, Medium: N, Low: N |
```

**Why this works:** The state machine gives the orchestrator deterministic knowledge of "where we are." Completion Reports are structured — the orchestrator reads them to decide the next transition without parsing free-text. Every agent returns the same schema, making handoffs uniform.

### Negative Example

```markdown
## Workflow
1. First, create a PRD
2. Then design the system
3. Get it reviewed
4. Implement it
5. Create a PR

Each agent should report back what they did when finished.
```

**Why this fails:** No explicit state names means the orchestrator cannot track transitions deterministically. "Report back what they did" is free-text — the orchestrator must parse natural language instead of reading structured fields. There is no schema for handoff artifacts, so each agent invents its own format.

---

## Pattern 33: M x N Cross-Model Consensus Grid

**Prevalence:** ~1% of plugins
**Related patterns:** [Deduplication/Consensus](#pattern-22), [Scoring Rubrics](#pattern-27)

**What it is:** For each review dimension (M lenses), launch N different AI models in parallel. Then consolidate per-lens (N→1), then meta-consolidate across lenses (M→1). Creates a 3-tier pipeline that uses cross-model diversity to catch hallucinations and increase confidence.

**When to use:**
- High-stakes code review where single-model hallucination risk is unacceptable
- When different models have different strengths (security vs performance vs style)
- When organizational policy requires multi-model validation

### Positive Example

```markdown
Step 3: Launch M x N sub-agents (all parallel)
Step 3b: Per-lens consolidation (N→1 per lens, all parallel)
  - Validate each finding against actual code (catch hallucinations)
  - Note which models flagged each finding
  - Single-model-only findings = low confidence
Step 3c: Meta-consolidation (M→1 final)
  - De-duplicate across lenses
  - Cross-reference against existing PR threads
  - Suppress findings matching Closed/Fixed/WontFix threads
```

```markdown
### Consensus Scoring

| Agreement | Action |
|-----------|--------|
| 3/3 models | `[high]` confidence — almost certainly real |
| 2/3 models | Accept — verify specifics, `[medium]`+ confidence |
| 1/3 models | Adversarially challenge — keep only if it survives scrutiny |
```

**Why this works:** Cross-model diversity catches model-specific hallucinations. The 3/3 → 2/3 → 1/3 scoring table is deterministic. Per-lens consolidators validate against actual code before passing to meta-consolidation.

### Negative Example

```markdown
Run the review with multiple models and combine the results.
If models disagree, use your best judgment to pick the right answer.
```

**Why this fails:** "Combine the results" has no consolidation structure — no per-lens grouping, no hallucination validation against actual code. "Use your best judgment" replaces a deterministic scoring table with subjective reasoning, defeating the purpose of multi-model consensus.

---

## Pattern 34: Dual-Model Adversarial Planning

**Prevalence:** <1% of plugins
**Related patterns:** [Self-Critique](#pattern-28), [Confirmation Gates](#pattern-8)

**What it is:** Two AI models independently create plans for the same task, self-harden their plans, then cross-review each other's plans. A human picks the winner, and improvements from the losing plan are merged in.

**When to use:**
- High-stakes architectural decisions where a single perspective is insufficient
- When you want to reduce bias from a single model's training distribution
- When the cost of a wrong plan exceeds the cost of running two parallel sessions

### Positive Example

```markdown
Phase 5: Independent plans created by two agents (in separate sessions)
Phase 6: Each agent hardens their own plan (self-review)
Phase 7: Cross-review and gap analysis performed
Phase 8: Base plan selected by user
Phase 9: Final plan created with merged improvements from both
```

Cross-session blocking enforced via shared config file:
```json
{
  "planAPhase": 4,
  "planBPhase": 3,
  "planASelectedIdea": null,
  "planBSelectedIdea": null,
  "alignedIdea": null
}
```

**Why this works:** Independence prevents confirmation bias — each model works without seeing the other's approach. Cross-review creates adversarial tension. Human selection preserves agency. The config file provides cross-session coordination without coupling.

### Negative Example

```markdown
Have two agents collaborate on a plan together. They should
discuss ideas back and forth until they converge on the best approach.
```

**Why this fails:** Collaboration allows the first agent's framing to anchor the second, destroying independence. Convergence through discussion produces groupthink — the exact bias that dual-model adversarial planning is designed to eliminate. There is no human selection point, so neither agent's weaknesses get checked.

---

## Pattern 35: Cost-Optimized Model Routing

**Prevalence:** <1% of plugins
**Related patterns:** [Intent Classification](#pattern-20), [Tool Routing Tables](#pattern-21)

**What it is:** Decomposing tasks into subtasks, classifying each on multiple dimensions, and routing to the cheapest model that meets quality requirements. Includes cost reporting with savings comparison.

**When to use:**
- When running many sub-agents and cost matters
- When tasks have varying complexity (some need Opus, others just Haiku)
- When you want to demonstrate cost savings vs naive "use the best model for everything"

### Positive Example

```markdown
## Classification Dimensions (per subtask)
- Reasoning depth (shallow/moderate/deep)
- Output criticality (low/medium/high)
- Precision required (approximate/exact)
- Context load (light/moderate/heavy)
- Novelty (pattern/novel)
- Estimated tokens
- Domain

## Routing Priorities
Priority 1 — Output criticality: high → Force premium model
Priority 2 — Reasoning depth: deep → Force sonnet or opus
Priority 5 — Novelty: pattern → Prefer cheaper model

## Cost Report
| Model | Subtasks | Cost |
| haiku-4.5 | 2 | $0.03 |
| sonnet-4.5 | 1 | $0.25 |
| TOTAL | 3 | $0.28 |
Baseline (all Sonnet): $0.75 | Savings: 63%
```

### Negative Example

```markdown
Use the most capable model for all subtasks to ensure quality.
We can optimize costs later if needed.
```

**Why this fails:** Routing every subtask to the premium model wastes budget on shallow tasks (pattern matching, formatting) that cheaper models handle equally well. "Optimize later" never happens — there is no classification framework to identify which tasks could be downgraded, so the cost baseline becomes the permanent cost.

---

## Pattern 36: Handoff Context Protocol

**Prevalence:** ~2% of orchestration plugins
**Related patterns:** [Phased Execution](#pattern-2), [Reference File Injection](#pattern-23)

**What it is:** A standardized context block that the orchestrator prepares before every agent handoff, ensuring the receiving agent has all necessary context without reading unnecessary data.

### Positive Example

```markdown
**Handoff Context Summary**
**Task:** {specific task the user requested}
**Target Agent:** {which agent will handle this}
**SDLC State:** {current state in the SDLC chain}
**Inputs:** [requirements doc path, work item ID, PR ID]
**Constraints & Decisions:** [list of prior decisions that constrain this agent]
**Expected Output:** [what the orchestrator needs back]
```

**Why this works:** The receiving agent gets exactly what it needs — task, state, inputs, constraints, and expected output — in a uniform format. No guessing about context. The orchestrator synthesizes context rather than forwarding raw conversation history.

### Negative Example

```markdown
Pass the full conversation history to the next agent so it has
all the context it needs to continue the work.
```

**Why this fails:** Raw conversation history contains irrelevant turns, dead ends, and retracted ideas that pollute the receiving agent's context window. The agent must parse unstructured dialogue to extract its actual task, constraints, and inputs — wasting tokens and risking misinterpretation of abandoned ideas as active requirements.

---

## Pattern 37: Context Efficiency Rule (Orchestrator Reads Nothing)

**Prevalence:** ~1% of plugins
**Related patterns:** [Multi-Agent Orchestration](#pattern-18), [Handoff Context Protocol](#pattern-36)

**What it is:** The orchestrator passes file paths to sub-agents and consolidators but never reads file contents itself. Only reads the final consolidated report. This preserves the orchestrator's context window for coordination logic.

### Positive Example

```markdown
The orchestrator must NOT read changed file contents, full diffs, or
sub-agent output into its own context. Pass **paths** to sub-agents
and consolidators. Only read the final meta-consolidator report.
```

**Why this works:** The orchestrator's context window stays clean for coordination decisions. Sub-agents do the heavy lifting of reading and analyzing code. The orchestrator only needs to read the final summary to present to the user.

### Negative Example

```markdown
The orchestrator reads each changed file, analyzes it, then
delegates specific findings to sub-agents for deeper investigation.
```

**Why this fails:** The orchestrator reads all file contents into its own context, consuming the window with code details instead of coordination logic. By the time it delegates to sub-agents, it has less capacity for tracking state, managing handoffs, and synthesizing the final report.

---

## Pattern 38: Complexity-Tiered Dispatch

**Prevalence:** ~2% of orchestration plugins
**Related patterns:** [Intent Classification](#pattern-20), [Workflow Mode Branching](#pattern-3)

**What it is:** Classifying incoming tasks by complexity tier, then adjusting the model selection, planning phases, and agent pipeline based on the tier.

### Positive Example

```markdown
| Tier | Signals | Model | Planning Phase |
| Simple | Single file, clear fix | haiku | None — route directly |
| Standard | Feature, 2-3 files | Default | Optional |
| Complex | Architecture, 4+ files, security | sonnet+ | Recommended |
```

Complex tasks trigger sequential phases: researcher → architect → coder.
Simple tasks route directly to coder.

### Negative Example

```markdown
Analyze the task complexity and choose an appropriate approach.
For harder tasks, think more carefully before coding.
```

**Why this fails:** No concrete tier definitions means the model must invent its own complexity classification each time, producing inconsistent routing. "Think more carefully" is not actionable — it does not specify additional phases (researcher, architect) or model upgrades. Without signal-to-tier mappings, a 4-file architecture change might get the same treatment as a typo fix.

---

## Pattern 39: Persistent Team with Message Board

**Prevalence:** ~1% of plugins
**Related patterns:** [Multi-Agent Orchestration](#pattern-18)

**What it is:** Agents created as a persistent team that communicate via a shared message board and individual state files. The orchestrator facilitates cross-agent discussion rather than commanding agents.

### Positive Example

```markdown
## Communication Protocol
- After forming or updating your perspective, write your FULL current
  position to your state file
- Your state file is the source of truth - keep it current

## State Files
{tmp}/brainstorm-${SESSION_ID}-advocate-state.md
{tmp}/brainstorm-${SESSION_ID}-skeptic-state.md
{tmp}/brainstorm-${SESSION_ID}-architect-state.md
```

**Why this works:** State files are the single source of truth — agents don't need to parse conversation history. The orchestrator reads state files to synthesize perspectives. Each agent manages its own state independently.

### Negative Example

```markdown
The agents should communicate by sending messages to each other
through the orchestrator, which relays them back and forth.
```

**Why this fails:** Relay-based communication means each agent's state is scattered across conversation turns, not stored persistently. If the orchestrator's context compacts or an agent session restarts, prior positions are lost. There is no single file an agent can read to recover its full current position.

---

## Pattern 40: Delegation to Cloud Agent via Work Item

**Prevalence:** <1% of plugins
**Related patterns:** [Skill Composition](#pattern-19)

**What it is:** Delegating tasks to a cloud-hosted coding agent by creating a work item (e.g., ADO) assigned to the agent, tagged with the target repository.

### Positive Example

```markdown
System.Tags: copilot:repo=<orgName>/<projectName>/<repoName>@<branchName>
System.AssignedTo: GitHub Copilot
```

Uses a try-REST-API-then-fallback-to-work-item strategy.

**Why this works:** The agent is discovered and assigned like any other team member. The tag provides repository context. The work item becomes the audit trail.

### Negative Example

```markdown
Call the cloud agent's API directly with the code changes
and wait for it to return the result.
```

**Why this fails:** Direct API calls create tight coupling — the caller blocks waiting for a response, there is no audit trail of what was requested, and if the call fails there is no fallback. Work-item-based delegation is asynchronous, auditable, and uses the same assignment mechanism as human developers.

---

## Pattern 41: Loop Prevention with Max Iterations

**Prevalence:** ~3% of plugins
**Related patterns:** [Error Handling](#pattern-15), [Confirmation Gates](#pattern-8)

**What it is:** Hard limits on retry/feedback loops to prevent infinite cycling between agents. Different thresholds for different loop types, with structured reporting when limits are hit.

### Positive Example

```markdown
Loop max 3 iterations. If tests still fail after 3 rounds:
- Report structured failure with remaining issues
- Ask whether to proceed with known failures or stop
```

```markdown
12 round warning, 20 round hard stop
```

**Why this works:** Hard stops prevent infinite loops that consume time and tokens. The structured failure report preserves partial progress. Asking the user to decide (proceed vs stop) keeps a human in the loop.

### Negative Example

```markdown
Keep retrying until the tests pass. If they don't pass,
try a different approach and retry again.
```

**Why this fails:** No iteration cap means the loop can run indefinitely, burning tokens on the same failing test. "Try a different approach" without structure leads to random exploration. When the loop eventually times out externally, there is no structured report of what was attempted or what partial progress was made.

---

## Pattern 42: Agent Memory Isolation

**Prevalence:** ~1% of plugins
**Related patterns:** [Prompt Injection Defense](#pattern-10), [Read-Only Boundary](#pattern-12)

**What it is:** Each agent in a team has isolated memory/state directories. Cross-agent communication happens only through designated artifact directories, never by reading another agent's internal state.

### Positive Example

```markdown
MEMORY_ROOT/memory/{role}/     — per-agent memory files
MEMORY_ROOT/decisions/{role}/  — per-agent decisions
MEMORY_ROOT/artifacts/         — inter-agent work products (shared)
MEMORY_ROOT/messages/          — team message board (shared)

Rules:
- Agents may only read their own memory + their own decisions files
- Agents may NOT read other agents' memory, charters, or history
- The coordinator does NOT inject one agent's output into another's memory
- Inter-agent handoffs use artifacts in MEMORY_ROOT/artifacts/
```

**Why this works:** Isolation prevents one agent from being influenced by another's internal reasoning. Shared artifacts are the controlled interface. The coordinator mediates all cross-agent communication, maintaining oversight.

### Negative Example

```markdown
Agents can read each other's memory files to understand what
other team members are thinking and coordinate accordingly.
```

**Why this fails:** Cross-reading memory allows one agent's reasoning errors or biases to propagate to others. An agent that reads the reviewer's draft critique before finishing its own analysis will anchor on those findings instead of discovering issues independently. The lack of a controlled interface makes it impossible to audit what influenced each agent's conclusions.

---

## Pattern 43: Sparse Git Worktree for Isolated Review

**Prevalence:** ~2% of review-related plugins
**Related patterns:** [Read-Only Boundary](#pattern-12)

**What it is:** Creating a sparse git worktree containing only PR-changed files for review, avoiding materializing the full repository in large monorepos.

### Positive Example

```markdown
git worktree add --no-checkout --detach $worktreePath {commit}
git -C $worktreePath sparse-checkout set $changedFiles
```

**Why this works:** In monorepos with 40k+ files, materializing everything wastes time and disk. Sparse checkout means the agent only sees relevant files. The worktree is isolated — no risk of modifying the main working tree.

### Negative Example

```markdown
Clone the repository and check out the PR branch to review
the changed files.
```

**Why this fails:** A full clone of a 40k+ file monorepo wastes minutes and gigabytes when the PR only touches 5 files. Checking out the PR branch in the main working tree risks polluting uncommitted changes. There is no isolation between the review workspace and the developer's active work.

---

## Pattern 44: Severity Promotion/Demotion by Area

**Prevalence:** ~2% of review plugins
**Related patterns:** [Scoring Rubrics](#pattern-27), [Deduplication/Consensus](#pattern-22)

**What it is:** Automatically adjusting finding severity based on the review area, encoding organizational risk appetite directly into the prompt.

### Positive Example

```markdown
Security and Correctness findings: promoted +1 severity level
Performance and Architecture findings: capped at HIGH
A11y and Rollout findings: capped at MEDIUM

Verdict rules:
- Approve: 0 CRITICAL, 0 HIGH
- Approve with suggestions: 0 CRITICAL in Security/Correctness
- Request changes: 1+ CRITICAL or 1+ HIGH in Security/Correctness or 3+ HIGH elsewhere
```

**Why this works:** Security bugs are inherently more dangerous than style issues — the promotion encodes this. Caps prevent low-risk areas from blocking merges. Verdict rules are deterministic, not subjective.

### Negative Example

```markdown
Flag all issues found during review. The reviewer should use
their judgment to decide which ones are important enough to block the PR.
```

**Why this fails:** Without severity adjustment by area, a style nit in CSS and a SQL injection in authentication both start at the same level. "Use their judgment" produces inconsistent verdicts across reviews — one reviewer blocks on performance warnings while another approves with the same findings. There are no deterministic verdict rules, so the approve/reject decision is unpredictable.
