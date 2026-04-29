# Advanced Workflow, Execution Control & Autonomy Patterns

Deep patterns for workflow orchestration, state machines, incident response, deployment pipelines, monitoring, planning, and autonomous agent behavior — extending the foundational execution patterns (5-9) with production-grade architectures discovered across 500+ plugins.

**Source research:** Extracted from analysis of 500+ production AI agent plugins across DevOps, security, migration, and incident response domains.

---

## Pattern 70: State File as Sole Continuity Mechanism

**Prevalence:** ~2% of plugins
**Related patterns:** [Configuration Persistence](#pattern-16), [Persistent Team with Message Board](#pattern-39)

**What it is:** Each phase of a multi-agent pipeline reads and writes a shared markdown/JSON state file, since agents run in isolated context windows with no shared memory. The state file is the ONLY way information flows between phases.

### Positive Example

```markdown
Every phase reads the state file at start and writes updated state at end.
The state file is the SOLE continuity mechanism between phases.

State file structure:
- Phase status (pending/in-progress/completed/failed)
- Phase artifacts (file paths, PR URLs, work item IDs)
- Accumulated decisions and context
- Error state for recovery

Recovery: If a phase fails, the next invocation reads the state file
and resumes from the last completed phase, not from the beginning.
```

**Why this works:** Agents have no shared memory — the state file bridges context windows. Structured phase status enables resume-from-failure without re-running completed phases. Accumulated decisions prevent context loss.

### Negative Example

```markdown
Each phase passes its results to the next phase via the return value.
If a phase fails, restart the entire pipeline from the beginning.
```

**Why this fails:** Return values exist only within a single context window — when the next agent starts in a new session, those values are gone. Restarting from the beginning wastes all work from completed phases and creates an infinite retry loop if the failing phase is non-deterministic.

---

## Pattern 71: Zero-Questions Triage (Maximum Autonomy)

**Prevalence:** <1% of plugins
**Related patterns:** [Interactive Flow Control](#pattern-7), [Confirmation Gates](#pattern-8)

**What it is:** A fixed protocol with zero user interaction, hard time budgets, and staggered burst queries respecting external rate limits. The agent must complete its entire analysis autonomously within strict time constraints.

### Positive Example

```markdown
Total time budget: 95 seconds
- Phase 1 (Data Gathering): 30s — staggered burst queries (max 3 concurrent)
- Phase 2 (Correlation): 25s — cross-reference all signals
- Phase 3 (Impact Assessment): 20s — quantified customer impact
- Phase 4 (Triage Decision): 20s — severity, routing, immediate actions

Zero user interaction during execution.
Respect external rate limits: stagger MCP calls, max 3 concurrent.
If a data source times out, proceed with available data — note gap.
```

**Why this works:** Time budgets prevent unbounded analysis. Zero interaction means the agent can be triggered automatically (e.g., by an incident alert). Rate limit respect prevents cascading failures in the tools the agent depends on.

### Negative Example

```markdown
Gather all available data before making any triage decision.
Ask the oncall engineer for clarification if any signal is ambiguous.
Query all data sources in parallel for maximum speed.
```

**Why this fails:** "All available data" has no time bound — the agent can spend minutes chasing marginal signals while the incident worsens. Requiring human clarification blocks autonomous execution. Unbounded parallel queries will hit rate limits and cause cascading failures across the MCP tools.

---

## Pattern 72: Pull-Based Kanban Orchestration

**Prevalence:** <1% of plugins
**Related patterns:** [Multi-Agent Orchestration](#pattern-18), [Complexity-Tiered Dispatch](#pattern-38)

**What it is:** A Kanban-style work system where agents pull tasks based on affinity (matching their specialization) rather than being pushed tasks by an orchestrator. Includes a two-tier Ready Gate, fork protocol for dynamic scaling, and scope escalation rules.

### Positive Example

```markdown
Two-Tier Ready Gate:
- Tier 1: Task has clear acceptance criteria AND no blockers
- Tier 2: Task is scoped to ≤ 2 hours of work for one agent

Pull Assignment by Affinity:
- Each agent has skill tags (frontend, backend, infra, test)
- Agents pull tasks matching their affinity from the Ready queue
- If no affinity match, any available agent can pull

Fork Protocol:
- If task exceeds 4 hours estimate, fork into sub-tasks
- Sub-tasks inherit parent's priority but get independent Ready Gate checks
- Original task moves to "Waiting for subtasks" column

Scope Escalation:
- If agent discovers task is larger than estimated, escalate to coordinator
- Coordinator decides: re-scope, fork, or reassign

8 Prompt-Enforced Invariants with Detection/Recovery:
1. No task may bypass Ready Gate
2. No agent may hold > 2 tasks simultaneously
3. Every task must have an owner before leaving Ready
...
```

**Why this works:** Pull-based assignment matches tasks to the best-suited agent naturally. The two-tier Ready Gate prevents poorly-defined tasks from consuming agent time. Fork protocol handles scope creep dynamically. Invariants with detection/recovery prevent system state corruption.

### Negative Example

```markdown
The orchestrator assigns tasks to agents round-robin.
If a task is too large, the agent should try its best to complete it.
Agents can pick up as many tasks as needed to stay busy.
```

**Why this fails:** Round-robin ignores agent specialization, so a frontend task may land on an infra agent. Without a fork protocol, oversized tasks block an agent indefinitely. No limit on concurrent tasks means one agent can hoard work while others idle, and quality degrades when an agent juggles too many contexts.

---

## Pattern 73: Deployment State Machine (Stateless/Re-entrant/Idempotent)

**Prevalence:** ~1% of plugins
**Related patterns:** [Hub-and-Spoke State Machine](#pattern-32), [Error Handling](#pattern-15)

**What it is:** A detailed state machine for deployment workflows where handlers run concurrently and the system is designed to be stateless, re-entrant, and idempotent — any handler can crash and restart without corrupting state.

### Positive Example

```markdown
States: QUEUED → VALIDATING → BUILDING → TESTING → STAGING → CANARY → PRODUCTION → COMPLETED
         ↘ FAILED (from any state)
         ↘ ROLLING_BACK (from CANARY or PRODUCTION)

Design principles:
- Stateless: Handler reads current state from external store, processes, writes new state
- Re-entrant: If handler crashes mid-execution, restart reads same state and re-processes
- Idempotent: Running the same handler twice on the same state produces the same result

Concurrent handlers:
- Multiple handlers can process independent deployment units simultaneously
- Handlers claim work via optimistic locking (read version, write new version)
- Version conflict → re-read state and retry
```

**Why this works:** Stateless + re-entrant + idempotent means crashes are recoverable without human intervention. Optimistic locking enables concurrency without distributed locks. The state machine makes every transition explicit and auditable.

### Negative Example

```markdown
Each handler keeps deployment progress in local variables.
Handlers coordinate via shared in-memory state.
If a handler fails, an operator manually restarts the deployment.
```

**Why this fails:** Local variables are lost on crash, making the deployment unrecoverable without human intervention. Shared in-memory state corrupts when concurrent handlers read-modify-write without locking. Requiring manual restart defeats the purpose of an automated deployment pipeline.

---

## Pattern 74: Autonomous PR Feedback Resolution

**Prevalence:** <1% of plugins
**Related patterns:** [Self-Critique](#pattern-28), [Confirmation Gates](#pattern-8)

**What it is:** The agent autonomously reads PR review comments and decides whether to implement the feedback or push back with a reasoned response — without human intervention for each comment.

### Positive Example

```markdown
For each PR review comment:
1. Classify: bug-fix, style-nit, architecture-concern, question, praise
2. Decide:
   - bug-fix → implement immediately
   - style-nit → implement if < 5 minutes
   - architecture-concern → push back with reasoning if disagree, implement if agree
   - question → respond with explanation
   - praise → acknowledge
3. After all comments resolved: re-request review

Decision log: Record every decision (implement/pushback) with reasoning
for audit trail.
```

**Why this works:** Classification prevents treating all comments equally. The "push back with reasoning" option means the agent doesn't blindly implement every suggestion. The decision log provides accountability.

### Negative Example

```markdown
For each PR review comment:
1. Implement the requested change
2. Mark the comment as resolved
3. After all comments addressed, re-request review
```

**Why this fails:** Blindly implementing every comment means the agent will apply contradictory suggestions, style-nit bikeshedding, and incorrect feedback equally. Without classification, a trivial formatting request consumes the same effort as a critical bug fix. No decision log means reviewers cannot understand why changes were made.

---

## Pattern 75: 11-Phase Autonomous Development Flow

**Prevalence:** <1% of plugins
**Related patterns:** [Phased Execution](#pattern-2), [Skill Composition](#pattern-19)

**What it is:** A complete autonomous development workflow chaining 11 phases from task understanding through deployment, including adversarial code review and CI monitoring.

### Positive Example

```markdown
Phase 1: Task Understanding (read work item, clarify requirements)
Phase 2: Codebase Analysis (repo structure, conventions, dependencies)
Phase 3: Design (architecture, data model, API design)
Phase 4: Implementation (write code following discovered conventions)
Phase 5: Self-Review (adversarial review of own code)
Phase 6: Testing (write and run tests, fix failures)
Phase 7: CI Integration (push, monitor CI, fix build breaks)
Phase 8: Code Review (read reviewer comments, implement/pushback)
Phase 9: Merge (after approval, merge and monitor)
Phase 10: Deployment Monitoring (watch for regression signals)
Phase 11: Work Item Update (close task, write completion notes)

Guardrails:
- Hard stop after 3 consecutive build failures
- Escalate to human after 2 review cycles without approval
- Never force-push, never merge without CI green
```

### Negative Example

```markdown
Phases:
1. Read the task
2. Write the code
3. Push to main
4. Fix any issues that come up in production
```

**Why this fails:** Skipping design, self-review, and testing phases means bugs are discovered in production instead of during development. Pushing directly to main without CI or code review bypasses all quality gates. "Fix issues in production" treats production as the test environment.

---

## Pattern 76: Staggered Burst Query with Rate Limit Respect

**Prevalence:** ~2% of plugins
**Related patterns:** [Tool Routing Tables](#pattern-21), [Error Handling](#pattern-15)

**What it is:** When making multiple MCP/API calls, stagger them with controlled concurrency and explicit rate limit awareness rather than firing all in parallel.

### Positive Example

```markdown
Staggered burst queries:
- Max 3 concurrent MCP calls
- Group queries by target service (all Kusto together, all ADO together)
- Wait for each group to complete before starting the next
- If any call returns 429 (rate limited): back off 2s, retry once, then skip

Cross-server parallelism rule:
NEVER run MCP calls to different servers in the same parallel batch —
one 403 cancels ALL parallel calls in the batch.
```

**Why this works:** The cross-server anti-parallelism rule prevents a single auth failure from canceling unrelated queries. Grouping by service maximizes throughput within rate limits. The skip-after-retry policy prevents infinite retry loops.

### Negative Example

```markdown
Fire all MCP queries in parallel for maximum speed.
If a query fails, retry it immediately up to 10 times.
Mix Kusto, ADO, and Graph queries in the same parallel batch.
```

**Why this fails:** Mixing MCP servers in one parallel batch means a single 403 from one server cancels all in-flight queries to other servers. Unlimited parallel queries will exceed rate limits and trigger 429s across the board. Retrying 10 times without backoff amplifies the rate limit problem and can block the agent for minutes.

---

## Pattern 77: Time-Boxed Investigation with Partial Results

**Prevalence:** ~2% of incident-response plugins
**Related patterns:** [Error Handling](#pattern-15), [Progress Feedback](#pattern-9)

**What it is:** Hard time budgets per investigation phase, with mandatory partial-result reporting when time expires rather than continuing indefinitely.

### Positive Example

```markdown
Investigation time budget: 5 minutes per hypothesis
- If hypothesis not confirmed in 5 minutes, mark as INCONCLUSIVE
- Move to next hypothesis
- Report all investigated hypotheses (confirmed, refuted, inconclusive)
- Never spend > 15 minutes total on initial investigation

Partial result format:
| Hypothesis | Status | Evidence | Time Spent |
| DB connection pool exhaustion | CONFIRMED | Connection count = MAX | 2m 30s |
| Memory leak in service X | REFUTED | Memory stable over 24h | 3m 15s |
| Network partition | INCONCLUSIVE | Insufficient data | 5m 00s (timeout) |
```

**Why this works:** Time budgets prevent the agent from going down rabbit holes during incidents when speed matters. The hypothesis table shows everything investigated, including dead ends — critical for handoffs.

### Negative Example

```markdown
Investigate the root cause thoroughly before reporting any findings.
Do not move to the next hypothesis until the current one is fully resolved.
Only report confirmed findings — do not include inconclusive results.
```

**Why this fails:** "Thoroughly" has no time bound, so the agent may spend 30 minutes on one hypothesis while the incident escalates. Requiring full resolution before moving on means a dead-end hypothesis blocks all progress. Hiding inconclusive results loses investigation context that the next responder needs for handoff.

---

## Pattern 78: Deployment Override Knowledge Encoding

**Prevalence:** ~1% of plugins
**Related patterns:** [Domain Knowledge Embedding](#pattern-24)

**What it is:** Encoding the complete taxonomy of deployment override types, their effects, and common KQL filter patterns directly in the prompt to enable precise deployment status queries.

### Positive Example

```markdown
Blocking Override Types (checked by deployment gate system DeploymentBlockRule):
| Type | Effect |
| BlockAll | Blocks all deployment to matching machines |
| Halt | Halts deployment of specific version range |
| HaltAndStop | Halts and stops any in-progress deployment |
| Purge | Rolls back to previous version |

Common KQL Filters:
| Filter | KQL |
| Active only | where IsDeleted == false |
| Blocking types only | where DeploymentConfigurationItemType in ("BlockAll",...) |
| By ring | where TargetFilterExpression has "global" |
```

### Negative Example

```markdown
Query the deployment override API for current status.
Filter out any overrides that seem irrelevant.
Summarize the results for the user.
```

**Why this fails:** Without encoding the override taxonomy, the agent cannot distinguish blocking overrides (Halt) from informational ones. "Seem irrelevant" is subjective — the agent lacks the domain knowledge to filter correctly. No KQL patterns means the agent must guess query syntax for each request, producing inconsistent and often incorrect results.

---

## Pattern 79: Incident Escalation Decision Matrix

**Prevalence:** ~2% of incident-response plugins
**Related patterns:** [Confirmation Gates](#pattern-8), [Blast Radius Formula](#pattern-49)

**What it is:** A decision matrix that determines escalation path based on quantified impact dimensions, with explicit thresholds for when to page, bridge, or escalate to management.

### Positive Example

```markdown
| Customer Impact | Duration | Escalation |
| < 100 users | < 30 min | Sev 3 — assign to oncall |
| 100-10K users | < 1 hour | Sev 2 — page secondary oncall |
| 10K+ users | Any | Sev 1 — bridge call, page management |
| Data loss | Any | Sev 0 — all-hands, exec notification |

Auto-escalation triggers:
- Sev 2 unacknowledged for 15 minutes → escalate to Sev 1
- Any severity with "security breach" signal → Sev 0 immediately
```

### Negative Example

```markdown
Assess the severity of the incident based on your best judgment.
Escalate if the situation seems serious.
Page the oncall team if needed.
```

**Why this fails:** "Best judgment" and "seems serious" are subjective — different agent runs will produce inconsistent severity assignments for identical incidents. Without quantified thresholds (user count, duration), there is no reproducible boundary between Sev 2 and Sev 1. Missing auto-escalation rules mean an unacknowledged Sev 2 can sit for hours without promotion.

---

## Pattern 80: Scope Estimation and Re-estimation Checkpoints

**Prevalence:** ~2% of planning plugins
**Related patterns:** [Complexity-Tiered Dispatch](#pattern-38), [Phased Execution](#pattern-2)

**What it is:** Requiring the agent to estimate task scope before starting, then re-estimate at defined checkpoints during execution. Significant scope increases trigger escalation.

### Positive Example

```markdown
Before starting:
- Estimate: hours of work, number of files, risk level
- If estimate > 8 hours: recommend decomposition

Checkpoint re-estimation (at 25%, 50%, 75%):
- Compare actual progress to estimate
- If actual/estimate > 1.5x: flag scope creep
- If actual/estimate > 2x: stop and escalate to user
```

**Why this works:** Early estimation catches unreasonable tasks before investment. Re-estimation checkpoints catch scope creep in progress. The 1.5x/2x thresholds are concrete, not subjective.

### Negative Example

```markdown
Start working on the task immediately.
If it takes longer than expected, let the user know when you're done.
```

**Why this fails:** Without upfront estimation, the agent commits to tasks that may take days — wasting tokens and time before anyone realizes the scope is wrong. No checkpoints means scope creep is invisible until completion (or failure). Notifying "when done" provides no early warning signal for intervention.
