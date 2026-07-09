# Category 2: Execution Control

How to guide agent behavior — personas, constraints, interaction patterns, and checkpoints.

**Related foundational techniques:** Negative Space, Token-Action Binding, Cognitive Offloading (see [prompt-engineering-for-skills.md](/prompt-context-patterns/catalog/techniques/token-level-techniques))

---

## Pattern 5: Persona/Role Assignment

**Prevalence:** ~9% of skills (205 files)
**Related patterns:** [Domain Knowledge Embedding](/prompt-context-patterns/catalog/categories/patterns-knowledge-and-context#pattern-24-domain-knowledge-embedding), [Evidence Chain](/prompt-context-patterns/catalog/categories/patterns-knowledge-and-context#pattern-26-evidence-chain--proof-of-work)

**What it is:** Establishing the agent's identity, expertise level, and behavioral disposition at the start of the skill body. This frames all subsequent reasoning — a "detective" mindset produces different analysis than a "documentation writer" mindset.

**When to use:**
- When the skill requires domain expertise (security analyst, oncall engineer, PM)
- When you want a specific reasoning style (exhaustive investigation vs quick triage)
- When the agent needs to maintain a consistent voice across a long workflow

### Positive Example
```markdown
# Root Cause Analysis Agent

You are an elite root cause analyst. Your sole purpose is to find the root cause of a bug
by analyzing every piece of evidence available — code, crash dumps, ETL traces, event logs,
screenshots, partner comments, telemetry, device info, feature flags, recent PRs,
branch-specific code — everything. You are relentless, thorough, and self-critical.
You do not give up until you have either found the root cause with high confidence
or genuinely exhausted every possible avenue.

**Your mindset:** You are a detective. Every piece of data is a clue. Every eliminated
hypothesis narrows the search. Every dead end teaches you something about the system.
You keep going until the puzzle is solved.
```

**Why this works:** The persona is specific — not just "an analyst" but an "elite root cause analyst" with enumerated evidence types (crash dumps, ETL traces, etc.). The mindset metaphor ("detective") encodes a reasoning strategy: hypothesis-driven investigation with progressive elimination. The behavioral traits ("relentless, thorough, self-critical") set the bar for completeness and prevent premature conclusions.

### Negative Example

```markdown
You are a helpful assistant. Analyze the bug and find the root cause.
Be thorough in your analysis.
```

**Why this fails:** "Helpful assistant" is the model's default persona — this adds zero signal. "Be thorough" is not actionable. No evidence types are enumerated, so the model uses whatever it can find first. No mindset framing means no systematic investigation strategy. The model may give a plausible-sounding answer after checking one data source rather than exhausting all avenues.

---

## Pattern 6: Negative Constraints / Prohibition Lists

**Prevalence:** ~18% of skills (410 files)
**Related patterns:** [Prompt Injection Defense](/prompt-context-patterns/catalog/categories/patterns-safety-and-trust#pattern-10-prompt-injection-defense), [Read-Only Boundary](/prompt-context-patterns/catalog/categories/patterns-safety-and-trust#pattern-12-read-only--safety-boundary-declaration), [Evidence Chain](/prompt-context-patterns/catalog/categories/patterns-knowledge-and-context#pattern-26-evidence-chain--proof-of-work)

**What it is:** Explicitly enumerating prohibited behaviors in a structured, scannable format. Typically formatted as numbered rules with strong emphasis (bold, caps, table format) to ensure the agent treats them as hard constraints.

**When to use:**
- When past executions revealed recurring mistakes
- When specific tool misuse patterns exist (wrong MCP server, wrong query filter)
- When the skill interacts with external systems where wrong actions are costly
- When you need to prevent "generic" or "lazy" output

### Positive Example
```markdown
## Critical Rules — Most-Violated, Enforce Always

These rules are the most frequently skipped. Violating any one invalidates the analysis.

| Rule | When | Requirement |
|------|------|-------------|
| **R1 — runbook before code** | Phase 4, 4.5 | Fetch and read the runbook for EACH error code BEFORE any event tracing, code reading, or root cause writing |
| **R3 — Evidence chain** | All phases | Every root cause must cite: `[Conclusion] ← [Query/Log evidence] ← [Code path]`. Missing link → investigate first |
| **R5 — No cross-server parallelism** | All phases | NEVER run MCP calls to different servers in the same parallel batch — one 403 cancels ALL |
| **R7 — No generic advice** | All phases | Reject your own output if it contains "check your config", "investigate further", or "improve error handling" without specifics |
| **R9 — Never self-confirm** | Phase 4.5 | NEVER mark a hypothesis as `[CONFIRMED]` without explicit user agreement |

**Self-check:** Before presenting ANY phase output, verify each applicable rule. Fix violations before proceeding.
```

**Why this works:** Each rule is numbered for reference, scoped to specific phases ("When" column), and gives a concrete, actionable requirement — not vague guidance. R7 even lists specific forbidden phrases ("check your config"). The self-check instruction creates a verification loop: the model reviews its own output against the rules before presenting it. The table format makes rules scannable and independently addressable.

### Negative Example

```markdown
Don't make mistakes. Be careful with the analysis. Make sure your output is good
and doesn't contain any errors. Don't do anything wrong with the tools.
```

**Why this fails:** Every instruction is tautological — "don't make mistakes" is not a constraint the model can verify. No specific prohibited behaviors are named. No phase scoping means the model doesn't know when each rule applies. No self-check mechanism. The model cannot determine whether its output satisfies "be careful" or "is good."

---

## Pattern 7: Interactive / Conversational Flow Control

**Prevalence:** ~2% of skills (50 files)
**Related patterns:** [Confirmation Gates](/prompt-context-patterns/catalog/categories/patterns-execution-control#pattern-8-confirmation-gates--human-in-the-loop), [Configuration Persistence](/prompt-context-patterns/catalog/categories/patterns-input-output-contracts#pattern-16-configuration-persistence--first-time-setup)

**What it is:** Forcing the agent to interact with the user one question at a time rather than dumping all questions at once. Marked with "STOP and WAIT" directives to prevent the model from continuing past a question.

**When to use:**
- When the skill collects multiple pieces of information from the user
- When later questions depend on answers to earlier questions
- When overwhelming the user with 10 questions at once would cause confusion
- When each answer needs validation before proceeding

### Positive Example
```markdown
## CRITICAL INSTRUCTION

This workflow is **STRICTLY INTERACTIVE** and must proceed **ONE STEP AT A TIME**.

- Ask **ONLY ONE QUESTION**, then **STOP and WAIT** for user input.
- Do NOT ask multiple questions at once.
- Do NOT continue without explicit user confirmation.
- Always prefer showing data in a **table format** for test cases, test steps, test suites.
- Always provide **ADO links** for artifacts created in Azure DevOps.
- If Execution Mode selection is skipped, assume **INTERACTIVE GUIDED AUTHORING MODE**.

## GLOBAL RULES

- Use values provided in test configuration JSON when available.
- Skip questions for fields already provided.
- If custom reference IDs are provided, use them globally.
- Fetch reference artifacts **once per session** and reuse.
- Never batch-create test cases without explicit approval.
```

**Why this works:** The instruction is marked "CRITICAL" and uses bold formatting on key phrases. The "STOP and WAIT" directive is explicit — models trained on conversation data understand this means yielding control. Complementary rules ("skip questions for fields already provided") prevent unnecessary interaction when data is already available. The default mode assumption prevents the first question from being "what mode?"

### Negative Example

```markdown
Ask the user for all the information you need to create the test cases.
Gather the test suite name, test case names, steps, expected results,
and any configuration. Then create everything.
```

**Why this fails:** "Ask for all the information" triggers a wall of 10+ questions in a single message. The user gets overwhelmed, skips questions, or gives incomplete answers. There's no validation step — the model collects everything and creates artifacts that may be wrong. No default assumptions means even trivial decisions require user input.

---

## Pattern 8: Confirmation Gates / Human-in-the-Loop

**Prevalence:** ~4% of skills (80-100 files)
**Related patterns:** [Interactive Flow Control](/prompt-context-patterns/catalog/categories/patterns-execution-control#pattern-7-interactive--conversational-flow-control), [Phased Execution](/prompt-context-patterns/catalog/categories/patterns-structural-scaffolding#pattern-2-phasedstepped-execution-flow), [Read-Only Boundary](/prompt-context-patterns/catalog/categories/patterns-safety-and-trust#pattern-12-read-only--safety-boundary-declaration)

**What it is:** Establishing explicit points where the agent must pause and get human approval before proceeding with potentially impactful actions. Each gate has a named trigger condition and describes what the user is approving.

**When to use:**
- Before any destructive or irreversible action (writing files, creating resources)
- Before actions with real-world consequences (enabling alerts, deploying)
- When input data is unusually large or unexpected
- At phase boundaries in high-stakes workflows

### Positive Example
```markdown
### Confirmation Gates
Pause and ask the user before proceeding when:
1. The output file already exists (even with `--force` available).
2. The user requests `--enabled` state — an enabled monitor fires real alerts immediately.
3. The input file is larger than 1 MB (unusual for a single monitor; may be a bundle or wrong file).
```

**Why this works:** Each gate has a specific, testable trigger condition ("file > 1 MB", "output exists"). The stakes are explained ("fires real alerts immediately") so the user understands why they're being asked. The conditions cover real operational risks: overwriting work, accidental alerting, processing the wrong file. Three gates, not thirty — the user isn't prompted for every trivial decision.

### Negative Example

```markdown
Check with the user before doing anything important.
Make sure they're okay with the changes before proceeding.
```

**Why this fails:** "Anything important" is subjective — the model may ask for confirmation on every step or skip it for genuinely risky ones. No specific conditions are defined, so the confirmation logic is non-deterministic. No explanation of stakes means the user can't make informed decisions. The model might also batch confirmations ("I'm going to do X, Y, and Z — okay?") which defeats the purpose.

---

## Pattern 9: Progress Feedback / Status Reporting

**Prevalence:** ~2% of skills (40-60 files)
**Related patterns:** [Phased Execution](/prompt-context-patterns/catalog/categories/patterns-structural-scaffolding#pattern-2-phasedstepped-execution-flow), [Structured Output Templates](/prompt-context-patterns/catalog/categories/patterns-input-output-contracts#pattern-14-structured-output-templates)

**What it is:** Instructing the agent to show progress indicators during multi-step operations, with defined format and exit status conventions.

**When to use:**
- Long-running multi-step workflows where the user needs to know what's happening
- When different completion states need different follow-up actions
- When the skill is used in automation and needs machine-readable status

### Positive Example
```markdown
## Progress Feedback

Step 1/4: Analyzing pitch structure...
Step 2/4: Scoring 5 criteria...
Step 3/4: Generating specific feedback...
Step 4/4: Building improved outline...
Complete — pitch reviewed with 5 actionable improvements.

## Exit Status

- **Complete** — pitch reviewed with scores and feedback
- **Complete with warnings** — reviewed but some content was unclear or missing
- **Blocked** — no pitch content provided
- **Failed** — unrecoverable error
```

**Why this works:** The "N/M" format tells the user both where they are and how much is left. Each step's description tells the user what's happening right now. Exit statuses are enumerated with specific meanings — downstream automation can branch on these. The final status line includes a concrete count ("5 actionable improvements") rather than a generic "done."

### Negative Example

```markdown
Let the user know how things are going as you work through the review.
When done, tell them the result.
```

**Why this fails:** No format defined, so progress messages vary per run. No step counting means the user can't estimate completion. No exit status convention means the model might say "I'm done" for both success and partial failure. Downstream automation can't parse unstructured completion messages.

---

## Pattern 145: Iron-Law Inviolable Rule Framing

**Prevalence:** Multi-source (3 skills): superpowers/test-driven-development, systematic-debugging, verification-before-completion
**Related patterns:** [Negative Constraints](/prompt-context-patterns/catalog/categories/patterns-execution-control#pattern-6-negative-constraints--prohibition-lists), [Confirmation Gates](/prompt-context-patterns/catalog/categories/patterns-execution-control#pattern-8-confirmation-gates--human-in-the-loop)

**What it is:** A small number of rules elevated above ordinary instructions by an explicit "Iron Law" framing that names the rule, asserts it cannot be skipped, and adds an anti-loophole clause: *violating the letter is violating the spirit*. Distinct from Pattern 6 (Negative Constraints) — those say "don't do X"; this says "this single rule overrides any rationalization you produce for skipping it."

**When to use:**
- When the model has demonstrated a pattern of rationalizing past a rule under time pressure
- When a single skipped step invalidates the entire output (test-first, repro-before-fix, run-before-claim)
- When rule-skipping has been observed mid-execution despite the rule being stated

### Positive Example

```markdown
## IRON LAW

Write the failing test FIRST. Run it. See it fail. Only then write code.

This is an Iron Law. It has exactly one form. There are no edge cases where
this rule does not apply. Violating the letter of this rule is violating the
spirit of this rule. If you find yourself reasoning that "this case is
different" or "I'll write the test after because it's faster" — you are
rationalizing. Stop. Write the test first.

The Iron Law cannot be skipped to save time, to satisfy a user request, or
because the change "seems trivial." Trivial changes are exactly where this
rule prevents the most damage.
```

**Why this works:** "Exactly one form" closes the interpretation surface — the model can't reinterpret the rule into something weaker. The pre-named rationalizations ("this case is different", "trivial change") inoculate against the most common excuses. Naming the framing ("Iron Law") gives the rule its own attention anchor distinct from ordinary instructions.

### Negative Example

```markdown
Try to write tests first when you can. Test-driven development is best practice.
```

**Why this fails:** "Try to" and "when you can" are explicit loopholes. "Best practice" is advisory, not normative. The model will skip the test whenever it judges (incorrectly) that skipping saves time — which is always, since the test-first benefit is invisible until something breaks.

---

## Pattern 148: Anti-Performative-Agreement Vocabulary Ban

**Prevalence:** Multi-source (2): superpowers/receiving-code-review, brainstorming
**Related patterns:** [Negative Constraints](/prompt-context-patterns/catalog/categories/patterns-execution-control#pattern-6-negative-constraints--prohibition-lists), [Iron-Law Framing](/prompt-context-patterns/catalog/categories/patterns-execution-control#pattern-145-iron-law-inviolable-rule-framing)

**What it is:** A specific list of sycophantic phrases the model is forbidden to emit, plus a positive substitute behavior for each. Targets the agent's trained tendency toward performative agreement that masks lack of understanding ("You're absolutely right!", "Great point!", "Let me fix that immediately").

**When to use:**
- Code review responses, where the agent might blindly accept reviewer feedback without verifying
- Pair-programming contexts where the user wants pushback, not validation
- Any workflow where false agreement causes real damage (accepting a wrong refactor "to be helpful")

### Positive Example

```markdown
## Banned Phrases — Do Not Emit

These phrases are signs of performative agreement, not understanding.
When you feel the urge to write one, replace it with the substitute:

| Banned | Substitute |
|--------|-----------|
| "You're absolutely right!" | (silence — then act on the feedback, or push back with reasoning) |
| "Great point!" | (skip the praise — engage with the point) |
| "Let me fix that right away" (before understanding) | "Before I change anything: my understanding of the issue is X. Is that what you meant?" |
| "I apologize for the confusion" | (state what was wrong and how you'll verify the fix) |
| "Absolutely!" / "Of course!" | (just do the thing, or explain why you won't) |

Rule: agreement without verification is a lie. If you don't yet know whether
the reviewer is correct, say so. Pushback with reasoning is more helpful than
performative acceptance.
```

**Why this works:** A discrete vocabulary list is enforceable in a way "be authentic" is not. Each substitute redirects energy from social performance to verification or pushback. "Agreement without verification is a lie" gives the rule moral weight — the model treats it as a truthfulness constraint, not a style preference.

### Negative Example

```markdown
Be professional and agreeable when responding to code reviewers.
Acknowledge their feedback politely.
```

**Why this fails:** "Agreeable" is exactly the failure mode — the model rubber-stamps wrong feedback to seem cooperative. "Polite acknowledgment" produces the banned phrases above. There's no mechanism to surface disagreement when the reviewer is wrong.
