# Advanced Quality, Review & Evaluation Patterns

Deep patterns for code review, bug analysis, test generation, and LLM-as-judge evaluation — extending the foundational quality patterns (27-30) with production-grade architectures discovered across 560+ plugins.

**Source research:** code-review, code-reviewer, peer-reviewer, deep-review, pr-review-critic, aspen-pr-review, review-swarm, review-verdict, consensus-code-review, bug-assessor, bug-hunter, test-sentinel, llm-as-judge-eval, plugin-eval, hackathon-evaluator, retro-bar-raiser

---

## Pattern 45: Directive-Based Review with on_fail Classification

**Prevalence:** ~2% of review plugins
**Related patterns:** [Scoring Rubrics](#pattern-27), [Negative Constraints](#pattern-6)

**What it is:** Parameterizing reviews via YAML "directives" where each criterion carries an `on_fail` field (`fail` or `review`) that determines whether a "Not Met" verdict is blocking or advisory.

### Positive Example

```yaml
criteria:
  - text: All codeflows from the PR-linked issues are fixed
    on_fail: review
  - text: At least one codeflow shows progress (non-zero fix count)
    on_fail: fail
  - text: No high-severity risks introduced
    on_fail: fail
```

Decision rules (three-way):
- **Fail** if: any `on_fail: fail` criterion is `Not Met`, `build_error_likelihood` is `High`, `runtime_error_likelihood` is `High`
- **Pass** only if: every criterion is `Met`, both likelihoods `Low`, no uncertainty priority <= 2, no Medium+ risk
- **Review** otherwise (preference for Review over Pass when evidence is incomplete)

**Why this works:** The `on_fail` field makes blocking vs advisory explicit per criterion. The three-way decision (Pass/Review/Fail) avoids the binary trap where everything is either "approved" or "rejected." Preference for Review over Pass prevents false confidence.

### Negative Example

```yaml
criteria:
  - text: All codeflows from the PR-linked issues are fixed
  - text: At least one codeflow shows progress (non-zero fix count)
  - text: No high-severity risks introduced

Decision: If any criterion is Not Met → Fail. Otherwise → Pass.
```

**Why this fails:** Without `on_fail` classification, every unmet criterion is equally blocking. A minor incomplete codeflow fix produces the same verdict as a high-severity risk introduction. The binary Pass/Fail decision forces reviewers to either rubber-stamp incomplete work or block PRs over advisory concerns.

---

## Pattern 46: Multi-Stage Repo Discovery Before Review

**Prevalence:** ~2% of review plugins
**Related patterns:** [Reference File Injection](#pattern-23), [Domain Knowledge Embedding](#pattern-24)

**What it is:** Before reviewing any code, the agent performs multiple discovery stages to learn the repo's conventions, architecture, and patterns — then applies review criteria calibrated to what it learned.

### Positive Example

```markdown
## Discovery (before any review)
- Stage 0: Tech stack detection (Backend/Frontend/Library/Infra/Full-stack)
- Stage 1a: Architecture & wiring
- Stage 1b: Conventions & patterns
- Stage 1c: Functional flows
- Stage 1d: Test patterns
- Stage 1e: Data access patterns
- Stage 1f: Best-practice inventory
- Stage 2: Business context and intent (trace call chains, identify scale/frequency)

## 6-Dimension Review (after discovery)
1. Convention Enforcement
2. Completeness (Round-the-Circle)
3. Security (OWASP-aligned)
4. Performance
5. Data Access
6. Test Coverage
```

Includes a 29-point **Coding Conventions Checklist** (A1-A29) with language-specific examples.

**Why this works:** Discovery prevents the model from applying generic review criteria to a repo with specific conventions. A reviewer who understands the repo's patterns catches meaningful violations, not false positives.

### Negative Example

```markdown
## Review Checklist
1. Check for code style violations
2. Check for security issues
3. Check for performance problems
4. Check for test coverage
5. Verify PR description is complete
```

**Why this fails:** The checklist applies generic criteria without any repo discovery. It will flag style violations that are actually the repo's convention, miss project-specific patterns (e.g., required middleware registration), and produce false positives that erode developer trust in the reviewer.

---

## Pattern 47: Evidence-First Review ("Demonstrate, Don't Cite Rules")

**Prevalence:** ~2% of review plugins
**Related patterns:** [Evidence Chain](#pattern-26), [Adversarial Persona Framing](#pattern-31)

**What it is:** Instead of citing abstract rules ("missing null check"), the reviewer must demonstrate the concrete failure path with specific code references.

### Positive Example

```markdown
**Demonstrate, don't cite rules.** Instead of "missing null check," show:
`getUser()` returns null on cache miss (CacheManager.ts:89), so `user.email`
at line 45 throws TypeError.

Eight attack patterns:
1. null/empty/boundary  2. stale data  3. error paths  4. sequence breaking
5. resource exhaustion  6. concurrency  7. performance  8. security

Trust boundary analysis:
- Entry points (validation appropriate) vs internal code (should trust callers)
- Over-protective checks are a SMELL correlating with real bugs

Call stack analysis:
- Look UP: Who calls this? Could a caller violate assumptions?
- Look DOWN: What do callees assume? Could this code pass invalid state?
```

**Why this works:** Demonstrated bugs with file:line references are immediately actionable. Abstract rule citations ("OWASP A1") require the developer to figure out the actual issue. The eight attack patterns provide systematic coverage.

### Negative Example

```markdown
**Review finding:** Missing null check on user input.
This violates OWASP A1 (Injection) and CWE-476 (NULL Pointer Dereference).
Recommendation: Add input validation per secure coding guidelines.
```

**Why this fails:** The reviewer cites rule IDs but never shows which function, which line, or which input path leads to the failure. The developer must re-discover the actual bug themselves. "Add input validation" is too vague to act on without knowing the specific entry point and data flow.

---

## Pattern 48: Rule-Catalog Review (Hierarchical YAML)

**Prevalence:** ~1% of review plugins
**Related patterns:** [Tool Routing Tables](#pattern-21), [Domain Knowledge Embedding](#pattern-24)

**What it is:** Reviews driven by a hierarchical catalog of YAML rule files, each with evaluation type (regex, metric, semantic) and rule IDs. Includes "trained rules" generated from historical PR comment analysis.

### Positive Example

```markdown
Rule catalogs:
- base-rules-test-quality.yaml (TEST-*)
- base-rules-security.yaml (SEC-*)
- base-rules-code-quality.yaml (CODE-*)
- base-rules-workflow.yaml (WF-*)
- base-rules-pr-metadata.yaml (PR-*)
- trained-rules.yaml (TRAINED-*) — rules from historical PR comment analysis

Evaluation types per rule:
- `regex` — pattern matching against code
- `metric` — computed thresholds (e.g., method length > 50 lines)
- `semantic` — LLM-guided via `hint` field
```

**Why this works:** Rules are versioned, auditable, and independently updatable. Trained rules capture team-specific conventions that generic checklists miss. The three evaluation types match the right technique to each rule's nature.

### Negative Example

```markdown
Review rules (embedded in prompt):
- Methods should not be too long
- Avoid security vulnerabilities
- Tests should cover edge cases
- Code should follow team conventions
- Use meaningful variable names
```

**Why this fails:** Rules are embedded as prose in the prompt, making them unversioned and unauditable. "Too long" and "meaningful" are subjective with no evaluation type specified. There is no way to update a single rule without rewriting the entire prompt, and no mechanism to learn team-specific conventions from historical data.

---

## Pattern 49: Blast Radius & On-Call Impact Formulas

**Prevalence:** <1% of plugins
**Related patterns:** [Scoring Rubrics](#pattern-27)

**What it is:** Quantified formulas for assessing the operational impact of code changes, producing numeric scores that map to risk levels.

### Positive Example

```markdown
## Blast Radius
Blast Radius = (Direct Consumers) + (Transitive Consumers x 0.5) + (Cross-Repo Refs x 2)
Risk: 0-5 Low, 6-15 Medium, 16-50 High, 50+ Critical

## On-Call Impact Score
OIS = (Blast Radius x 0.3) + (User Impact x 0.3) + (Data Risk x 0.2) + (Recovery Difficulty x 0.2)
Risk: 0-25 Low, 26-50 Medium, 51-75 High, 76-100 Critical

## Weighted Merge Readiness Score (0-100)
CI passing (20%) + Regression risks (20%) + Breaking changes (15%) +
Review completeness (15%) + Sanity checks (10%) + Work items (5%) +
PR description (5%) + Threads (5%) + Test coverage (5%)

Verdict: 90-100 Ready, 70-89 Caution, 50-69 Needs work, <50 Do not merge
```

**Why this works:** Numeric formulas produce consistent scores across reviews. The weights encode organizational priorities (CI passing matters more than PR description). Cross-repo references get 2x weight because they affect the most people.

### Negative Example

```markdown
## Risk Assessment
Evaluate the blast radius of this change.
Consider: How many consumers? Is it cross-repo? Could it page on-call?
Rate as: Low / Medium / High / Critical
```

**Why this fails:** Without a formula, "Medium" from one reviewer is "High" from another. There is no way to distinguish a change with 5 direct consumers from one with 50. The subjective rating produces inconsistent scores that cannot be compared across reviews or tracked over time.

---

## Pattern 50: Adversarial Triad with Counterargument Phase

**Prevalence:** ~1% of plugins
**Related patterns:** [Adversarial Persona Framing](#pattern-31), [Multi-Agent Orchestration](#pattern-18)

**What it is:** Three agents with opposing mindsets (Advocate/Skeptic/Architect) run in parallel, then a second round of three counterargument agents challenge each original perspective. Disputed points escalate to peer consultation.

### Positive Example

```markdown
Round 1 (parallel): Advocate, Skeptic, Architect — independent reviews
Round 2 (parallel): 3 counterargument agents read the OTHER two reviews
Round 3: Disputed agents message each other directly (peer consultation)

Conflict resolution:
- If Skeptic shows reproducible path, it's a bug regardless of Advocate's defense
- If Architect says blocking, Architect wins on architectural concerns
- file:line evidence beats "probably"
- Peer consultation resolution = highest confidence
```

**Why this works:** Two rounds prevent groupthink — counterarguments challenge initial positions. Evidence-based conflict resolution is deterministic. Peer consultation resolves disputes the rules can't handle.

### Negative Example

```markdown
Three reviewers analyze the PR independently.
Combine findings into a single list.
If reviewers disagree, include both opinions in the output.
```

**Why this fails:** Independent reviews without a counterargument phase produce a union of opinions, not a resolved verdict. "Include both opinions" defers the conflict to the developer instead of resolving it. Without evidence-based conflict resolution rules, the developer cannot tell which reviewer is correct.

---

## Pattern 51: Schema Validation Gate

**Prevalence:** ~2% of review plugins
**Related patterns:** [Structured Output Templates](#pattern-14), [Error Handling](#pattern-15)

**What it is:** Every agent runs a schema validator on its output JSON. If validation fails, the agent must fix violations and re-run until it passes. The orchestrator checks for validation success before accepting output.

### Positive Example

```markdown
Every agent runs `validate_review.py` on its output JSON.
If validation fails: fix violations and re-run until PASSED.
Orchestrator checks for "Schema validation: PASSED" in agent output.
Agents that skip validation are re-launched.
```

**Why this works:** Schema validation catches malformed output before it propagates. The re-launch mechanism prevents agents from silently producing garbage.

### Negative Example

```markdown
Output your review as JSON with fields: severity, description, file, line.
Make sure the JSON is valid.
```

**Why this fails:** "Make sure the JSON is valid" is an instruction, not a verification mechanism. There is no validator that runs after generation, no re-try loop on failure, and no orchestrator gate. The agent can produce malformed JSON (missing fields, wrong types) and the downstream consumer discovers the error too late to recover.

---

## Pattern 52: LLM-as-Judge Evaluation Scenarios (8 Types)

**Prevalence:** <1% of plugins
**Related patterns:** [Scoring Rubrics](#pattern-27), [Self-Critique](#pattern-28)

**What it is:** A comprehensive toolkit of eight distinct evaluation scenarios for using LLMs to judge AI outputs, each with specific input/output contracts.

### Positive Example

```markdown
1. **Live API Testing**: Call endpoint, judge response (verdict/reasoning/confidence)
2. **Offline Batch**: Evaluate pre-collected pairs against assertions
3. **Meta-Judge (Judge the Judge)**: Validate another LLM's judgment — AGREE/DISAGREE
4. **Pairwise Comparison (A/B)**: Compare two outputs, pick winner with criteria
5. **Multi-Aspect**: Grade 6 dimensions 1-10 (accuracy, helpfulness, safety, tone, relevance, clarity)
6. **Regression Testing**: Compare baseline vs candidate — BETTER/SAME/WORSE with severity
7. **Safety & Compliance**: Screen for PII, harmful content, policy violations, bias
8. **Claim-Based Grounding (Claimbreak)**: Extract factual claims, convert to verifiable
   questions, assess grounding (SUPPORTED/UNSUPPORTED/PARTIAL) with grounding_score
```

**Why this works:** Eight scenarios cover the full evaluation space. Each has a specific contract, not a vague "evaluate quality." Meta-judging enables judging the judge. Claimbreak catches confabulation by verifying individual claims.

### Negative Example

```markdown
Evaluate the AI's response for quality.
Rate on a scale of 1-10.
Provide reasoning for your score.
```

**Why this fails:** A single "quality" dimension collapses accuracy, safety, helpfulness, and tone into one number. There is no scenario distinction — the same prompt is used whether evaluating a chatbot response, a batch of test cases, or a regression between model versions. Without claim-level grounding, a response that is 90% correct but contains one fabricated fact scores high overall.

---

## Pattern 53: Retrospective Quality Rubric (Incident Postmortem)

**Prevalence:** <1% of plugins
**Related patterns:** [Evidence Chain](#pattern-26), [Scoring Rubrics](#pattern-27)

**What it is:** A comprehensive checklist for evaluating incident postmortem quality, with anti-patterns that catch vague or blameful writing.

### Positive Example

```markdown
Customer Impact:
- Anti-pattern: "customers experienced slower performance"
- Pattern: "450K read requests (12% of traffic) received 5xx errors for 117 minutes"

Five Whys: structure, depth, branching, detection/prevention analysis

Repair Items must have:
- Actionable scope
- Verifiable completion criterion
- Individual owner + target date
```

**Why this works:** The anti-pattern/pattern pairs teach the model exactly what "quantitative" means for customer impact. Repair items require individual ownership — "the team will fix it" is rejected.

### Negative Example

```markdown
Review the postmortem for completeness:
- Does it describe what happened?
- Does it identify root cause?
- Does it list action items?
- Is the tone blameless?
```

**Why this fails:** The checklist accepts vague answers as complete. "Customers experienced degraded performance" passes "describe what happened" without quantifying impact. "The team will improve monitoring" passes "list action items" without an owner, date, or verifiable completion criterion. There are no anti-pattern examples to calibrate what "complete" actually means.

---

## Pattern 54: Test Scaffolding with Convention Enforcement

**Prevalence:** ~1% of plugins
**Related patterns:** [Domain Knowledge Embedding](#pattern-24), [Phased Execution](#pattern-2)

**What it is:** Comprehensive test generation with enforced conventions, anti-pattern tables, deterministic test rules, and fleet mode for parallel generation.

### Positive Example

```markdown
Enforced Conventions:
- AAA pattern (Arrange/Act/Assert) in every test
- Naming: {Method}_{Scenario}_{Expected}
- [Description("...")] on every test method
- Folder mirroring (test project mirrors source structure)

Anti-Pattern Table (10 entries):
| Anti-Pattern | Problem | Correct Approach |
| Testing internal state | Brittle to refactoring | Test observable behavior |
| Shared mutable state | Order-dependent tests | Fresh setup per test |

Deterministic Test Rules:
| Non-deterministic Source | Replacement |
| DateTime.Now | Inject IClock |
| Random | Seed-based or inject |
| File I/O | In-memory abstraction |

Edge Case Checklist:
null, empty, single, boundary, duplicate, whitespace, case sensitivity,
concurrent, default/zero, large input

Fleet Mode: Parallel generation with sub-agents, hard stop after 3 consecutive build failures
```

**Why this works:** Convention enforcement prevents "tests that pass but are wrong." The anti-pattern table addresses specific recurring mistakes. Deterministic test rules eliminate flaky tests at generation time. Fleet mode scales to large codebases.

### Negative Example

```markdown
Generate unit tests for the changed files.
Ensure good coverage of edge cases.
Use mocking where appropriate.
Follow the existing test style.
```

**Why this fails:** "Good coverage" and "where appropriate" are subjective — the model decides what counts as an edge case. Without an explicit edge case checklist, null inputs and boundary values are routinely missed. "Follow the existing test style" requires the model to infer conventions that may be inconsistent across the codebase, and there is no anti-pattern table to prevent common mistakes like testing internal state or sharing mutable fixtures.

---

## Pattern 55: Smart Triage-Skip with Model Tracking

**Prevalence:** <1% of plugins
**Related patterns:** [Deduplication/Consensus](#pattern-22), [Configuration Persistence](#pattern-16)

**What it is:** Before triaging a bug, check if it was already triaged by looking for metadata signatures. If triaged by the same model, skip. If by a different model, re-triage (allowing model upgrades to add value).

### Positive Example

```markdown
Check for existing triage:
- If triaged by same model → skip
- If triaged by different model → re-triage
- This prevents duplicate assessments while allowing model upgrades
```

**Why this works:** Prevents wasted computation on already-triaged bugs. The model-tracking enables progressive improvement as better models become available.

### Negative Example

```markdown
Before triaging, check if the bug already has a triage comment.
If it does, skip it.
```

**Why this fails:** Checking for "a triage comment" without tracking which model produced it means a triage from an older, less capable model is treated as final. Model upgrades never get a chance to improve triage quality. The skip is also fragile — any comment (even a human note) could be mistaken for a prior triage, causing bugs to be permanently skipped.
