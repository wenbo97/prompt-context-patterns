# Prompt Pattern Catalog — Index

A catalog of **142 prompt engineering patterns** extracted from 500+ production AI agent plugins (2,293 SKILL.md files) across community plugin repositories, 2 open-source skill repositories, and the Claude Code system prompt architecture. The original 30 patterns (1-30) include positive/negative examples. The advanced 61 patterns (31-91) were discovered through deep research across the full plugin collection. The 8 gap-fill patterns (92-99) were found in a targeted sweep for under-explored categories. The final 21 patterns (100-120) were extracted from Anthropic's official skills repo and ComposioHQ's awesome-claude-skills repo. Patterns 121-142 cover platform-level concerns from Claude Code's composable system prompt.

**Data sources:**
Extracted from analysis of 500+ production AI agent plugins across DevOps, security, migration, and incident response domains.

**Extraction dates:** 2026-04-13 (original 30), 2026-04-14 (advanced 31-91), 2026-04-15 (open-source 100-120)

---

## How to Use This Catalog

1. **Building a new skill?** Scan the quick-reference table below to find patterns relevant to your use case.
2. **Reviewing an existing skill?** Check which patterns it uses and which it's missing.
3. **Learning prompt engineering?** Read the category files in order — they build from structure to orchestration to quality.

### Companion Files

| File | What it covers |
|------|---------------|
| [prompt-engineering-for-skills.md](techniques/token-level-techniques) | **Theory** — 9 foundational techniques grounded in conditional entropy / attention distribution |
| [template.md](techniques/good-vs-bad-template) | **Deep dive** — One BAD vs GOOD comparison with line-by-line analysis |
| **This catalog (patterns 1-30)** | **Foundational Patterns** — 30 patterns with positive/negative examples |
| [patterns-advanced-orchestration.md](categories/patterns-advanced-orchestration) | **Advanced** — 14 agent orchestration & multi-agent patterns (31-44) |
| [patterns-advanced-quality.md](categories/patterns-advanced-quality) | **Advanced** — 11 quality, review & evaluation patterns (45-55) |
| [patterns-advanced-safety.md](categories/patterns-advanced-safety) | **Advanced** — 14 safety, trust & compliance patterns (56-69) |
| [patterns-advanced-workflow.md](categories/patterns-advanced-workflow) | **Advanced** — 11 workflow, execution & autonomy patterns (70-80) |
| [patterns-advanced-io-domain.md](categories/patterns-advanced-io-domain) | **Advanced** — 11 I/O, domain & communication patterns (81-91) |
| [patterns-gap-fills.md](categories/patterns-gap-fills) | **Gap fills** — 8 onboarding, productivity, migration & creative patterns (92-99) |
| [patterns-open-source-skills.md](categories/patterns-open-source-skills) | **Open-Source** — 21 patterns from Anthropic official + community skill repos (100-120) |
| [patterns-karpathy-behavioral.md](categories/patterns-karpathy-behavioral) | **Behavioral** — 5 Karpathy-derived patterns: surface assumptions, minimum viable code, surgical changes, verify-per-step, narrate mistake path |
| [patterns-claude-code-platform.md](categories/patterns-claude-code-platform) | **Platform** — 12 Claude Code platform patterns: memory, permissions, scheduling, tool routing, agent dispatch (121-132) |
| [patterns-claude-code-platform-extended.md](categories/patterns-claude-code-platform-extended) | **Platform Extended** — 10 patterns: compositional assembly, tool constraints, security monitor, team coordination, dream memory (133-142) |
| [skill-architecture-patterns.md](techniques/skill-architecture) | **Architecture** — Skill packaging, composition, sub-agents, marketplace, reference org |
| [skill-reference-laziness-analysis.md](techniques/anti-laziness) | **Deep Dive** — 8 strategies to prevent agent laziness in Tier 3 reference reads, with risk-tiered decision framework |
| [reference-skip-playbook.md](techniques/reference-skip-playbook) | **Deep Dive** — 11 solution patterns for the reference-skip problem: 3 failure modes (naked hop, pre-satisfaction, optional framing), decision matrix, anti-patterns |

---

## Quick-Reference Table

| # | Pattern | Category | Prevalence | Key Benefit |
|---|---------|----------|-----------|-------------|
| 1 | [YAML Frontmatter Metadata](categories/patterns-structural-scaffolding#pattern-1-yaml-frontmatter-metadata-block) | Structural | ~100% | Platform-level identity and tool permissions |
| 2 | [Phased/Stepped Execution](categories/patterns-structural-scaffolding#pattern-2-phasedstepped-execution-flow) | Structural | ~54% | Deterministic ordering with per-phase goals |
| 3 | [Workflow Mode Branching](categories/patterns-structural-scaffolding#pattern-3-workflow-mode-branching) | Structural | ~5% | Same skill serves different audiences |
| 4 | [$ARGUMENTS Variable](categories/patterns-structural-scaffolding#pattern-4-arguments-variable-pattern) | Structural | ~7% | Parse user input with flags and options |
| 5 | [Persona/Role Assignment](categories/patterns-execution-control#pattern-5-personarole-assignment) | Execution | ~9% | Sets expertise level and reasoning style |
| 6 | [Negative Constraints](categories/patterns-execution-control#pattern-6-negative-constraints--prohibition-lists) | Execution | ~18% | Prevents specific known mistakes |
| 7 | [Interactive Flow Control](categories/patterns-execution-control#pattern-7-interactive--conversational-flow-control) | Execution | ~2% | One question at a time, STOP and WAIT |
| 8 | [Confirmation Gates](categories/patterns-execution-control#pattern-8-confirmation-gates--human-in-the-loop) | Execution | ~4% | Human approval before risky actions |
| 9 | [Progress Feedback](categories/patterns-execution-control#pattern-9-progress-feedback--status-reporting) | Execution | ~2% | Step N/M status with exit codes |
| 10 | [Prompt Injection Defense](categories/patterns-safety-and-trust#pattern-10-prompt-injection-defense) | Safety | <1% | Treat external content as untrusted data |
| 11 | [Sensitive Data Redaction](categories/patterns-safety-and-trust#pattern-11-sensitive-data-redaction) | Safety | ~2% | Named data types with replacement patterns |
| 12 | [Read-Only Boundary](categories/patterns-safety-and-trust#pattern-12-read-only--safety-boundary-declaration) | Safety | ~4% | Declare operational scope limits |
| 13 | [Activation Scope](categories/patterns-safety-and-trust#pattern-13-activation-scope-when-to-use--when-not-to-use) | Safety | ~7% | When to Use / When NOT to Use with redirects |
| 14 | [Structured Output Templates](categories/patterns-input-output-contracts#pattern-14-structured-output-templates) | I/O Contracts | ~26% | Exact output format with populated example |
| 15 | [Error Handling / Degradation](categories/patterns-input-output-contracts#pattern-15-error-handling--graceful-degradation) | I/O Contracts | ~10% | Phase-specific failure responses |
| 16 | [Configuration Persistence](categories/patterns-input-output-contracts#pattern-16-configuration-persistence--first-time-setup) | I/O Contracts | ~4% | Check-load-setup-save for user settings |
| 17 | [Cross-Platform Handling](categories/patterns-input-output-contracts#pattern-17-cross-platform-handling) | I/O Contracts | ~3% | Platform-specific tools and paths |
| 18 | [Multi-Agent Orchestration](categories/patterns-agent-orchestration#pattern-18-multi-agent-orchestration--agent-topologies) | Orchestration | ~2% | Agent topology with consensus scoring |
| 19 | [Skill Composition](categories/patterns-agent-orchestration#pattern-19-skill-composition--cross-skill-invocation) | Orchestration | ~4% | Delegate to existing skills (DRY) |
| 20 | [Intent Classification](categories/patterns-agent-orchestration#pattern-20-intent-classification--smart-routing) | Orchestration | ~6% | Route input to correct sub-workflow |
| 21 | [Tool Routing Tables](categories/patterns-agent-orchestration#pattern-21-tool-routing-tables) | Orchestration | ~16% | Task-to-tool mapping with "NOT these" |
| 22 | [Deduplication / Consensus](categories/patterns-agent-orchestration#pattern-22-deduplication--consensus-algorithms) | Orchestration | ~1% | Weighted similarity with defined thresholds |
| 23 | [Reference File Injection](categories/patterns-knowledge-and-context#pattern-23-reference-file--knowledge-base-injection) | Knowledge | ~17% | Pointers to external knowledge files |
| 24 | [Domain Knowledge Embedding](categories/patterns-knowledge-and-context#pattern-24-domain-knowledge-embedding) | Knowledge | ~22% | Inline schemas, field tables, query templates |
| 25 | [Few-Shot Examples](categories/patterns-knowledge-and-context#pattern-25-few-shot-examples) | Knowledge | ~21% | Complete input/output pairs |
| 26 | [Evidence Chain / Proof-of-Work](categories/patterns-knowledge-and-context#pattern-26-evidence-chain--proof-of-work) | Knowledge | ~5% | Traceable conclusions with mandatory manifest |
| 27 | [Scoring Rubrics](categories/patterns-quality-and-feedback#pattern-27-scoring-rubrics--quantitative-assessment) | Quality | ~4% | Criteria, score ranges, category thresholds |
| 28 | [Self-Critique](categories/patterns-quality-and-feedback#pattern-28-self-critique--quality-self-check) | Quality | ~2% | Adversarial weakness identification |
| 29 | [Feedback Solicitation](categories/patterns-quality-and-feedback#pattern-29-feedback-solicitation) | Quality | <1% | Priority-tiered survey with session dedup |
| 30 | [Version Check](categories/patterns-quality-and-feedback#pattern-30-version-check--update-notification) | Quality | <1% | Non-blocking update notification |

---

## Advanced Patterns Quick-Reference Table (31-80)

Discovered through deep research across 500+ plugins. Grouped by category.

### Category 8: Advanced Agent Orchestration (categories/patterns-advanced-orchestration)

| # | Pattern | Key Benefit |
|---|---------|-------------|
| 31 | [Adversarial Persona Framing](categories/patterns-advanced-orchestration#pattern-31-adversarial-persona-framing) | Attack mindset finds real bugs, not surface issues |
| 32 | [Hub-and-Spoke SDLC State Machine](categories/patterns-advanced-orchestration#pattern-32-hub-and-spoke-sdlc-state-machine) | Deterministic progress through development lifecycle |
| 33 | [M x N Cross-Model Consensus Grid](categories/patterns-advanced-orchestration#pattern-33-m-x-n-cross-model-consensus-grid) | Cross-model diversity catches hallucinations |
| 34 | [Dual-Model Adversarial Planning](categories/patterns-advanced-orchestration#pattern-34-dual-model-adversarial-planning) | Independent plans reduce single-model bias |
| 35 | [Cost-Optimized Model Routing](categories/patterns-advanced-orchestration#pattern-35-cost-optimized-model-routing) | 60%+ cost savings via task-appropriate model selection |
| 36 | [Handoff Context Protocol](categories/patterns-advanced-orchestration#pattern-36-handoff-context-protocol) | Uniform context transfer between agents |
| 37 | [Context Efficiency Rule](categories/patterns-advanced-orchestration#pattern-37-context-efficiency-rule-orchestrator-reads-nothing) | Orchestrator context stays clean for coordination |
| 38 | [Complexity-Tiered Dispatch](categories/patterns-advanced-orchestration#pattern-38-complexity-tiered-dispatch) | Right-size agent pipeline to task complexity |
| 39 | [Persistent Team with Message Board](categories/patterns-advanced-orchestration#pattern-39-persistent-team-with-message-board) | State files enable cross-agent discussion |
| 40 | [Delegation to Cloud Agent](categories/patterns-advanced-orchestration#pattern-40-delegation-to-cloud-agent-via-work-item) | Work items as agent assignment mechanism |
| 41 | [Loop Prevention with Max Iterations](categories/patterns-advanced-orchestration#pattern-41-loop-prevention-with-max-iterations) | Hard stops prevent infinite agent cycles |
| 42 | [Agent Memory Isolation](categories/patterns-advanced-orchestration#pattern-42-agent-memory-isolation) | Prevents cross-agent influence and injection |
| 43 | [Sparse Git Worktree for Review](categories/patterns-advanced-orchestration#pattern-43-sparse-git-worktree-for-isolated-review) | Monorepo-safe isolated file access |
| 44 | [Severity Promotion/Demotion by Area](categories/patterns-advanced-orchestration#pattern-44-severity-promotiondemotion-by-area) | Organizational risk appetite in the prompt |

### Category 9: Advanced Quality & Evaluation (categories/patterns-advanced-quality)

| # | Pattern | Key Benefit |
|---|---------|-------------|
| 45 | [Directive-Based Review with on_fail](categories/patterns-advanced-quality#pattern-45-directive-based-review-with-on_fail-classification) | Three-way Pass/Review/Fail per criterion |
| 46 | [Multi-Stage Repo Discovery Before Review](categories/patterns-advanced-quality#pattern-46-multi-stage-repo-discovery-before-review) | Reviews calibrated to repo conventions |
| 47 | [Evidence-First Review](categories/patterns-advanced-quality#pattern-47-evidence-first-review-demonstrate-dont-cite-rules) | "Demonstrate, don't cite rules" — actionable bugs |
| 48 | [Rule-Catalog Review (YAML)](categories/patterns-advanced-quality#pattern-48-rule-catalog-review-hierarchical-yaml) | Versioned, auditable, independently updatable rules |
| 49 | [Blast Radius & Impact Formulas](categories/patterns-advanced-quality#pattern-49-blast-radius--on-call-impact-formulas) | Quantified operational impact scoring |
| 50 | [Adversarial Triad + Counterarguments](categories/patterns-advanced-quality#pattern-50-adversarial-triad-with-counterargument-phase) | Two-round review eliminates groupthink |
| 51 | [Schema Validation Gate](categories/patterns-advanced-quality#pattern-51-schema-validation-gate) | Machine-enforced output format compliance |
| 52 | [LLM-as-Judge (8 Scenarios)](categories/patterns-advanced-quality#pattern-52-llm-as-judge-evaluation-scenarios-8-types) | Full evaluation toolkit including meta-judging |
| 53 | [Retrospective Quality Rubric](categories/patterns-advanced-quality#pattern-53-retrospective-quality-rubric-incident-postmortem) | Anti-pattern/pattern pairs for postmortems |
| 54 | [Test Scaffolding + Convention Enforcement](categories/patterns-advanced-quality#pattern-54-test-scaffolding-with-convention-enforcement) | Complete test generation with anti-pattern tables |
| 55 | [Smart Triage-Skip with Model Tracking](categories/patterns-advanced-quality#pattern-55-smart-triage-skip-with-model-tracking) | Prevents duplicate triage, enables model upgrades |

### Category 10: Advanced Safety & Compliance (categories/patterns-advanced-safety)

| # | Pattern | Key Benefit |
|---|---------|-------------|
| 56 | [MCP-Response-as-Data Guardrail](categories/patterns-advanced-safety#pattern-56-mcp-response-as-data-guardrail) | Prevents infrastructure detail leakage |
| 57 | [Prompt-Injection-as-Security-Finding](categories/patterns-advanced-safety#pattern-57-prompt-injection-as-security-finding) | Turns attacks into actionable review findings |
| 58 | [Prosecutor-Defender-Judge Architecture](categories/patterns-advanced-safety#pattern-58-prosecutor-defender-judge-architecture) | Adversarial audit with accuracy metrics |
| 59 | [Rescue-Tag-Before-Destructive-Operation](categories/patterns-advanced-safety#pattern-59-rescue-tag-before-destructive-operation) | Automatic undo points for all destructive ops |
| 60 | [Tiered Permission Model (RED/DEFER/GREEN)](categories/patterns-advanced-safety#pattern-60-tiered-permission-model-red--defer--green) | Three-tier risk classification with preflight analysis |
| 61 | [Data Classification Matrix (4-Level)](categories/patterns-advanced-safety#pattern-61-data-classification-matrix-4-level) | Unambiguous sensitivity taxonomy with tool-specific rules |
| 62 | [XPIA Defense Model](categories/patterns-advanced-safety#pattern-62-xpia-defense-model-cross-plugin-injection-attack) | Four-layer defense for cross-plugin injection attacks |
| 63 | [Severity Rubric with Litmus Tests](categories/patterns-advanced-safety#pattern-63-severity-rubric-with-litmus-tests) | "Would you wake someone at 3 AM?" — calibration anchors |
| 64 | [Security Posture Delta Analysis](categories/patterns-advanced-safety#pattern-64-security-posture-delta-analysis) | Code + infrastructure correlation for real risk |
| 65 | [Confidence-Gated Reporting](categories/patterns-advanced-safety#pattern-65-confidence-gated-reporting) | Asymmetric thresholds: lower for security findings |
| 66 | [System-Prompt Non-Disclosure](categories/patterns-advanced-safety#pattern-66-system-prompt-non-disclosure) | Prohibits revealing agent configuration |
| 67 | [40-Point Skill Security Checklist](categories/patterns-advanced-safety#pattern-67-40-point-security-skill-review-checklist) | Supply-chain defense for plugin marketplace |
| 68 | [Orchestrator-Only (No Direct Data)](categories/patterns-advanced-safety#pattern-68-orchestrator-only-pattern-no-direct-data-processing) | LLM never sees raw PII; tools handle data |
| 69 | [Policy-as-Data (Declarative YAML)](categories/patterns-advanced-safety#pattern-69-policy-as-data-declarative-yaml-configs) | Compliance rules decoupled from agent code |

### Category 11: Advanced Workflow & Autonomy (categories/patterns-advanced-workflow)

| # | Pattern | Key Benefit |
|---|---------|-------------|
| 70 | [State File as Sole Continuity](categories/patterns-advanced-workflow#pattern-70-state-file-as-sole-continuity-mechanism) | Bridges isolated agent context windows |
| 71 | [Zero-Questions Triage](categories/patterns-advanced-workflow#pattern-71-zero-questions-triage-maximum-autonomy) | Full autonomous analysis in 95 seconds |
| 72 | [Pull-Based Kanban Orchestration](categories/patterns-advanced-workflow#pattern-72-pull-based-kanban-orchestration) | Agents pull tasks by affinity, fork on scope creep |
| 73 | [Deployment State Machine (Idempotent)](categories/patterns-advanced-workflow#pattern-73-deployment-state-machine-statelessre-entrantidempotent) | Crash-recoverable stateless deployment handlers |
| 74 | [Autonomous PR Feedback Resolution](categories/patterns-advanced-workflow#pattern-74-autonomous-pr-feedback-resolution) | Agent implements or pushes back on review comments |
| 75 | [11-Phase Autonomous Dev Flow](categories/patterns-advanced-workflow#pattern-75-11-phase-autonomous-development-flow) | End-to-end from task to deployment, with guardrails |
| 76 | [Staggered Burst Query + Rate Limits](categories/patterns-advanced-workflow#pattern-76-staggered-burst-query-with-rate-limit-respect) | Cross-server anti-parallelism prevents cascade failures |
| 77 | [Time-Boxed Investigation](categories/patterns-advanced-workflow#pattern-77-time-boxed-investigation-with-partial-results) | Hard budgets with partial result reporting |
| 78 | [Deployment Override Knowledge Encoding](categories/patterns-advanced-workflow#pattern-78-deployment-override-knowledge-encoding) | Complete override taxonomy for precise queries |
| 79 | [Incident Escalation Decision Matrix](categories/patterns-advanced-workflow#pattern-79-incident-escalation-decision-matrix) | Quantified thresholds for severity and escalation |
| 80 | [Scope Estimation Checkpoints](categories/patterns-advanced-workflow#pattern-80-scope-estimation-and-re-estimation-checkpoints) | Re-estimation at 25/50/75% catches scope creep |

### Category 12: Advanced I/O & Domain Specialization (categories/patterns-advanced-io-domain)

| # | Pattern | Key Benefit |
|---|---------|-------------|
| 81 | [NL to Relational Schema Decomposition](categories/patterns-advanced-io-domain#pattern-81-natural-language-to-relational-schema-decomposition) | Teaches model to derive schemas, not just embed them |
| 82 | [Chart Decision Tree + Anti-Pattern Guards](categories/patterns-advanced-io-domain#pattern-82-chart-decision-tree-with-anti-pattern-guards) | Data-shape to visualization with cardinality guards |
| 83 | [Audience-Purpose Content Calibration](categories/patterns-advanced-io-domain#pattern-83-audience-purpose-driven-content-calibration) | Output format/detail driven by who reads it and why |
| 84 | [Socratic Investigation Loop](categories/patterns-advanced-io-domain#pattern-84-socratic-investigation-loop-with-active-research) | Active research + Socratic questioning for guided discovery |
| 85 | [Knowledge Base Index + Intent Routing](categories/patterns-advanced-io-domain#pattern-85-knowledge-base-index-with-intent-to-source-routing) | Two-tier retrieval: lightweight index then selective deep read |
| 86 | [Heuristic Scoring with Signal Detection](categories/patterns-advanced-io-domain#pattern-86-heuristic-scoring-with-signal-detection) | Machine-detectable signals replace subjective rubric labels |
| 87 | [Eager Incremental Materialization](categories/patterns-advanced-io-domain#pattern-87-eager-incremental-materialization) | Create artifacts during conversation, not after |
| 88 | [Data Shape to Query Pattern Detection](categories/patterns-advanced-io-domain#pattern-88-data-shape-to-query-pattern-detection) | Infer visualization from data columns + query text |
| 89 | [Writability Rules + Substitution Tables](categories/patterns-advanced-io-domain#pattern-89-writability-rules-and-linguistic-substitution-tables) | Complete style transformation with detection heuristics |
| 90 | [Cross-Platform Compatibility Matrix](categories/patterns-advanced-io-domain#pattern-90-cross-platform-surface-compatibility-matrix) | Source/target degradation paths with bounded retry |
| 91 | [Hub-Spoke Router with Overlap Resolution](categories/patterns-advanced-io-domain#pattern-91-hub-spoke-domain-router-with-overlap-resolution) | Multi-level specificity cascade for disambiguation |

### Category 13: Gap Fills — Onboarding, Productivity, Migration & Creative (categories/patterns-gap-fills)

| # | Pattern | Key Benefit |
|---|---------|-------------|
| 92 | [DAG Journey with Typed Gates](categories/patterns-gap-fills#pattern-92-dag-journey-with-typed-gates) | Non-linear onboarding with manual gates and backfill |
| 93 | [Multi-Source Evidence Harvest + Goal Synthesis](categories/patterns-gap-fills#pattern-93-multi-source-evidence-harvest-with-goal-aligned-synthesis) | 6+ source parallel harvest with audience-stratified output |
| 94 | [Promise Detection and KB Sync](categories/patterns-gap-fills#pattern-94-promise-detection-and-knowledge-base-sync) | Extracts implicit commitments from conversations |
| 95 | [Mandatory Self-Learning After Failure](categories/patterns-gap-fills#pattern-95-mandatory-self-learning-after-failure-resolution) | Knowledge base grows with every error resolution |
| 96 | [Risk-Ordered Batch Migration + Build-Verify](categories/patterns-gap-fills#pattern-96-risk-ordered-batch-migration-with-build-verify-loops) | Batched migration with same-error-signature revert |
| 97 | [PII-Motivated Delivery Restriction](categories/patterns-gap-fills#pattern-97-pii-motivated-delivery-restriction) | Absolute delivery channel restriction, no override |
| 98 | [Audience-Register Translation Review](categories/patterns-gap-fills#pattern-98-audience-register-translation-review-with-matched-frameworks) | Engineer-to-executive review with matched frameworks |
| 99 | [Automated Accessibility Post-Processing](categories/patterns-gap-fills#pattern-99-automated-accessibility-post-processing-pipeline) | A11y pipeline with 25 assertion eval |

### Category 14: Open-Source Skill Patterns (categories/patterns-open-source-skills)

| # | Pattern | Key Benefit |
|---|---------|-------------|
| 100 | [Progressive Disclosure Architecture](categories/patterns-open-source-skills#pattern-100-progressive-disclosure-architecture) | 3-tier context loading minimizes token waste |
| 101 | [Creative Philosophy Scaffolding](categories/patterns-open-source-skills#pattern-101-creative-philosophy-scaffolding) | Forces conceptual depth before visual execution |
| 102 | [Mandatory Refinement Pass](categories/patterns-open-source-skills#pattern-102-mandatory-refinement-pass) | Self-imposed quality gate with emotional anchoring |
| 103 | [Reconnaissance-Then-Action](categories/patterns-open-source-skills#pattern-103-reconnaissance-then-action) | Observe state before acting, prevents blind interaction |
| 104 | [Helper Script as Black Box](categories/patterns-open-source-skills#pattern-104-helper-script-as-black-box) | Scripts encapsulate complexity; model uses --help first |
| 105 | [Anti-Slop Design Guidelines](categories/patterns-open-source-skills#pattern-105-anti-slop-design-guidelines) | Named AI anti-patterns with specific alternatives |
| 106 | [Section-by-Section Collaborative Drafting](categories/patterns-open-source-skills#pattern-106-section-by-section-collaborative-drafting) | Iterative per-section build with user approval |
| 107 | [Reader Testing with Sub-Agent](categories/patterns-open-source-skills#pattern-107-reader-testing-with-sub-agent) | Fresh-eyes review by spawning a naive reader |
| 108 | [Blind A/B Comparison](categories/patterns-open-source-skills#pattern-108-blind-ab-comparison) | Double-blind skill evaluation eliminates bias |
| 109 | [Composio 3-Step SaaS Integration](categories/patterns-open-source-skills#pattern-109-composio-3-step-saas-integration) | Universal Search-Connect-Execute for any SaaS API |
| 110 | [Algorithm-as-Domain Knowledge](categories/patterns-open-source-skills#pattern-110-algorithm-as-domain-knowledge) | Embed actual system internals as prompt knowledge |
| 111 | [Clarifying Questions Before Action](categories/patterns-open-source-skills#pattern-111-clarifying-questions-before-action) | Targeted parameter-gathering questions before work |
| 112 | [Output Format with Populated Example](categories/patterns-open-source-skills#pattern-112-output-format-with-populated-example) | Complete realistic output, not abstract schema |
| 113 | [Multi-Workflow Routing by Input Type](categories/patterns-open-source-skills#pattern-113-multi-workflow-routing-by-input-type) | Same skill routes create/read/edit by input |
| 114 | [Font/Asset Bundling with Directory Reference](categories/patterns-open-source-skills#pattern-114-fontasset-bundling-with-directory-reference) | Bundled assets by relative path, no downloads |
| 115 | [QA Sub-Agent with Visual Verification](categories/patterns-open-source-skills#pattern-115-qa-sub-agent-with-visual-verification) | Spawn sub-agent to screenshot and inspect output |
| 116 | [Never-Hardcode Financial Rules](categories/patterns-open-source-skills#pattern-116-never-hardcode-financial-rules) | All calculated values must use formulas |
| 117 | [Multi-Language SDK Routing](categories/patterns-open-source-skills#pattern-117-multi-language-sdk-routing) | Detect language, load language-specific docs only |
| 118 | [Surface Selection by Architecture](categories/patterns-open-source-skills#pattern-118-surface-selection-by-architecture) | Route to single-call / workflow / agent by need |
| 119 | [Eval-Driven Skill Improvement Loop](categories/patterns-open-source-skills#pattern-119-eval-driven-skill-improvement-loop) | TDD for prompts: write tests → grade → improve |
| 120 | [Non-Anthropic Provider Guard](categories/patterns-open-source-skills#pattern-120-non-anthropic-provider-guard) | Early exit when imports indicate wrong ecosystem |

### Category 15-16: Claude Code Platform Patterns (patterns-claude-code-platform*.md)

| # | Pattern | Key Benefit |
|---|---------|-------------|
| 121 | [Typed Memory Taxonomy](categories/patterns-claude-code-platform#pattern-121-typed-memory-taxonomy) | Four memory types with distinct write triggers and staleness rules |
| 122 | [Bidirectional Feedback Capture](categories/patterns-claude-code-platform#pattern-122-bidirectional-feedback-capture) | Record corrections AND confirmations to prevent behavioral drift |
| 123 | [Reversibility × Blast-Radius](categories/patterns-claude-code-platform#pattern-123-reversibility--blast-radius-permission-model) | 2×2 permission matrix with non-sticky approval |
| 124 | [Tool Preference with Hard Routing](categories/patterns-claude-code-platform#pattern-124-tool-preference-hierarchy-with-hard-routing) | Ban shell equivalents when dedicated tools exist |
| 125 | [Cache-Aware Scheduling](categories/patterns-claude-code-platform#pattern-125-cache-aware-scheduling) | Schedule delays around prompt cache TTL dead zones |
| 126 | [Agent Briefing Protocol](categories/patterns-claude-code-platform#pattern-126-agent-briefing-protocol) | "Brief like a colleague" + never delegate understanding |
| 127 | [Parallel-Safe Step Identification](categories/patterns-claude-code-platform#pattern-127-parallel-safe-step-identification) | Annotate multi-step workflows with parallelism markers |
| 128 | [Context Compaction Survival](categories/patterns-claude-code-platform#pattern-128-context-compaction-survival-protocol) | Named fields to preserve across context compression |
| 129 | [Non-Sticky Authorization](categories/patterns-claude-code-platform#pattern-129-non-sticky-authorization-scope) | Approval scoped to specific request, not action category |
| 130 | [Investigate Before Destroying](categories/patterns-claude-code-platform#pattern-130-investigate-before-destroying) | Investigate root cause before destructive shortcuts |
| 131 | [Output Visibility Awareness](categories/patterns-claude-code-platform#pattern-131-output-visibility-awareness) | Communicate in text since tool calls are hidden from user |
| 132 | [Hook-Driven Automation](categories/patterns-claude-code-platform#pattern-132-hook-driven-automation-awareness) | Treat hook feedback as user input; adapt, don't retry |
| 133 | [Compositional Prompt Assembly](categories/patterns-claude-code-platform-extended#pattern-133-compositional-prompt-assembly) | Small versioned fragments assembled conditionally |
| 134 | [Tool-Constraint Boundaries](categories/patterns-claude-code-platform-extended#pattern-134-tool-constraint-agent-boundaries) | Remove tools from agents, don't just instruct against use |
| 135 | [Fork vs Fresh Spawning](categories/patterns-claude-code-platform-extended#pattern-135-fork-vs-fresh-spawning-strategy) | Cache-sharing fork vs independent fresh agent |
| 136 | [Security Monitor Agent](categories/patterns-claude-code-platform-extended#pattern-136-security-monitor-agent-dedicated-threat-classifier) | Separate agent evaluating every action against threat model |
| 137 | [Analysis-First Compaction](categories/patterns-claude-code-platform-extended#pattern-137-analysis-first-compaction) | Think in analysis tags before producing summaries |
| 138 | [Team Task Board](categories/patterns-claude-code-platform-extended#pattern-138-team-task-board-coordination) | Shared task list with async messaging between agents |
| 139 | [Background Job Narration](categories/patterns-claude-code-platform-extended#pattern-139-background-job-narration-protocol) | Machine-parseable completion signals for classifier |
| 140 | [Autonomous Trust Calibration](categories/patterns-claude-code-platform-extended#pattern-140-autonomous-trust-calibration) | "Steward, not initiator" — scale trust by blast radius |
| 141 | [REPL as Tool Composition](categories/patterns-claude-code-platform-extended#pattern-141-repl-as-tool-composition-layer) | JavaScript layer for loops/branches over tool calls |
| 142 | [Immutable Memory + Dream](categories/patterns-claude-code-platform-extended#pattern-142-immutable-memory-with-dream-consolidation) | Never-edit memory files with periodic consolidation agent |

---

## Category Files

<a id="cat-1"></a>
### [Category 1: Structural Scaffolding](categories/patterns-structural-scaffolding)
How a skill prompt is organized — the skeleton that holds everything together.

**Patterns:** YAML Frontmatter (1), Phased Execution (2), Workflow Mode Branching (3), $ARGUMENTS Variable (4)

<a id="cat-2"></a>
### [Category 2: Execution Control](categories/patterns-execution-control)
How to guide agent behavior — personas, constraints, interaction patterns, and checkpoints.

**Patterns:** Persona/Role Assignment (5), Negative Constraints (6), Interactive Flow Control (7), Confirmation Gates (8), Progress Feedback (9)

<a id="cat-3"></a>
### [Category 3: Safety and Trust](categories/patterns-safety-and-trust)
Guardrails that prevent the agent from causing harm — injection defense, data redaction, boundaries, and scope.

**Patterns:** Prompt Injection Defense (10), Sensitive Data Redaction (11), Read-Only Boundary (12), Activation Scope (13)

<a id="cat-4"></a>
### [Category 4: Input/Output Contracts](categories/patterns-input-output-contracts)
How data flows in and out — output templates, error handling, configuration, and platform adaptation.

**Patterns:** Structured Output Templates (14), Error Handling (15), Configuration Persistence (16), Cross-Platform (17)

<a id="cat-5"></a>
### [Category 5: Agent Orchestration](categories/patterns-agent-orchestration)
How multiple agents coordinate — topologies, skill composition, routing, tool mapping, and consensus.

**Patterns:** Multi-Agent Orchestration (18), Skill Composition (19), Intent Classification (20), Tool Routing Tables (21), Dedup/Consensus (22)

<a id="cat-6"></a>
### [Category 6: Knowledge and Context](categories/patterns-knowledge-and-context)
How information is managed — reference files, domain knowledge, examples, and evidence requirements.

**Patterns:** Reference File Injection (23), Domain Knowledge Embedding (24), Few-Shot Examples (25), Evidence Chain (26)

<a id="cat-7"></a>
### [Category 7: Quality and Feedback](categories/patterns-quality-and-feedback)
How to ensure output quality — scoring rubrics, self-critique, feedback loops, and version management.

**Patterns:** Scoring Rubrics (27), Self-Critique (28), Feedback Solicitation (29), Version Check (30)

<a id="cat-8"></a>
### [Category 8: Advanced Agent Orchestration](categories/patterns-advanced-orchestration)
Production-grade multi-agent architectures — state machines, consensus grids, adversarial planning, cost-optimized routing, memory isolation.

**Patterns:** Adversarial Persona (31), Hub-and-Spoke State Machine (32), Cross-Model Consensus (33), Adversarial Planning (34), Model Routing (35), Handoff Context (36), Context Efficiency (37), Complexity Tiers (38), Message Board (39), Cloud Delegation (40), Loop Prevention (41), Memory Isolation (42), Sparse Worktree (43), Severity Promotion (44)

<a id="cat-9"></a>
### [Category 9: Advanced Quality & Evaluation](categories/patterns-advanced-quality)
Deep review architectures — directive-based review, evidence-first analysis, adversarial triads, LLM-as-judge, test scaffolding.

**Patterns:** Directive Review (45), Repo Discovery (46), Evidence-First (47), Rule Catalog (48), Impact Formulas (49), Adversarial Triad (50), Schema Gate (51), LLM-as-Judge (52), Retro Rubric (53), Test Scaffolding (54), Triage Skip (55)

<a id="cat-10"></a>
### [Category 10: Advanced Safety & Compliance](categories/patterns-advanced-safety)
Production security — MCP data guardrails, XPIA defense, prosecutor-defender-judge, data classification, policy-as-data.

**Patterns:** MCP-Data Guardrail (56), Injection-as-Finding (57), Prosecutor-Defender-Judge (58), Rescue Tags (59), Tiered Permissions (60), Data Classification (61), XPIA Defense (62), Litmus Tests (63), Posture Delta (64), Confidence Gates (65), Non-Disclosure (66), Skill Security Checklist (67), Orchestrator-Only (68), Policy-as-Data (69)

<a id="cat-11"></a>
### [Category 11: Advanced Workflow & Autonomy](categories/patterns-advanced-workflow)
Execution control at scale — state files, zero-questions triage, Kanban orchestration, autonomous development, incident response.

**Patterns:** State File Continuity (70), Zero-Questions (71), Kanban Pull (72), Deployment State Machine (73), PR Feedback Resolution (74), Autonomous Dev Flow (75), Burst Query (76), Time-Boxed Investigation (77), Override Knowledge (78), Escalation Matrix (79), Scope Checkpoints (80)

<a id="cat-12"></a>
### [Category 12: Advanced I/O & Domain Specialization](categories/patterns-advanced-io-domain)
Input/output transformation, domain reasoning scaffolds, visualization instruction, interactive reasoning, style transformation, and audience adaptation.

**Patterns:** Schema Decomposition (81), Chart Decision Tree (82), Audience Calibration (83), Socratic Loop (84), KB Index Routing (85), Heuristic Scoring (86), Eager Materialization (87), Data Shape Detection (88), Writability Rules (89), Compatibility Matrix (90), Overlap Resolution Router (91)

<a id="cat-13"></a>
### [Category 13: Gap Fills — Onboarding, Productivity, Migration & Creative](categories/patterns-gap-fills)
Patterns from under-explored areas: DAG-based onboarding journeys, personal productivity, self-learning migration, and creative output accessibility.

**Patterns:** DAG Journey (92), Evidence Harvest (93), Promise Detection (94), Self-Learning (95), Batch Migration (96), Delivery Restriction (97), Register Translation Review (98), A11y Post-Processing (99)

<a id="cat-14"></a>
### [Category 14: Open-Source Skill Patterns](categories/patterns-open-source-skills)
Patterns extracted from Anthropic's official Agent Skills repo (17 skills) and ComposioHQ's community-curated awesome-claude-skills repo (32 unique + 832 Composio template skills). Covers progressive disclosure, creative scaffolding, visual QA, eval-driven improvement, SaaS integration templates, and multi-language SDK routing.

**Patterns:** Progressive Disclosure (100), Creative Philosophy (101), Refinement Pass (102), Reconnaissance-Then-Action (103), Helper Script Black Box (104), Anti-Slop (105), Collaborative Drafting (106), Reader Testing (107), Blind A/B (108), SaaS Integration (109), Algorithm-as-Knowledge (110), Clarifying Questions (111), Populated Examples (112), Input-Type Routing (113), Asset Bundling (114), Visual QA (115), Never-Hardcode (116), Language Routing (117), Architecture Selection (118), Eval-Driven Loop (119), Provider Guard (120)

**Architecture companion:** [skill-architecture-patterns.md](techniques/skill-architecture) — Skill packaging, marketplace grouping, reference file organization, sub-agent design, script integration, and cross-repo comparison.

<a id="cat-15"></a>
### [Category 15: Claude Code Platform Patterns](categories/patterns-claude-code-platform)
Patterns extracted from the Claude Code system prompt — platform-level concerns: memory taxonomy, permission models, scheduling, tool routing, agent dispatch, and context survival.

**Patterns:** Typed Memory Taxonomy (121), Bidirectional Feedback Capture (122), Reversibility × Blast-Radius (123), Tool Preference with Hard Routing (124), Cache-Aware Scheduling (125), Agent Briefing Protocol (126), Parallel-Safe Step Identification (127), Context Compaction Survival (128), Non-Sticky Authorization (129), Investigate Before Destroying (130), Output Visibility Awareness (131), Hook-Driven Automation (132)

<a id="cat-16"></a>
### [Category 16: Claude Code Platform Patterns — Extended](categories/patterns-claude-code-platform-extended)
Deeper architectural patterns from Claude Code's composable prompt system, agent spawning, security classification, team coordination, and memory consolidation.

**Patterns:** Compositional Prompt Assembly (133), Tool-Constraint Agent Boundaries (134), Fork vs Fresh Spawning (135), Security Monitor Agent (136), Analysis-First Compaction (137), Team Task Board Coordination (138), Background Job Narration (139), Autonomous Trust Calibration (140), REPL as Tool Composition Layer (141), Immutable Memory with Dream Consolidation (142)

---

## Mapping to Foundational Techniques

How the 30 patterns relate to the 9 foundational techniques in [prompt-engineering-for-skills.md](techniques/token-level-techniques):

| Foundational Technique | Patterns That Apply It |
|----------------------|----------------------|
| **Decision Trees** | Workflow Mode Branching (3), Intent Classification (20), Error Handling (15), Input-Type Routing (113), Language Routing (117), Architecture Selection (118) |
| **Grounding / Anchoring** | Domain Knowledge Embedding (24), Few-Shot Examples (25), Structured Output Templates (14), Populated Examples (112), Algorithm-as-Knowledge (110), Reconnaissance-Then-Action (103) |
| **Cognitive Offloading** | Phased Execution (2), Evidence Chain (26), Scoring Rubrics (27), Helper Script Black Box (104), Collaborative Drafting (106), Eval-Driven Loop (119) |
| **Attention Locality** | Negative Constraints (6), Reference File Injection (23), Tool Routing Tables (21), Progressive Disclosure (100) |
| **Token-Action Binding** | Confirmation Gates (8), Interactive Flow Control (7), Progress Feedback (9), Clarifying Questions (111) |
| **Schema Priming** | YAML Frontmatter (1), Structured Output Templates (14), Scoring Rubrics (27), Populated Examples (112) |
| **Negative Space** | Negative Constraints (6), Activation Scope (13), Read-Only Boundary (12), Anti-Slop (105), Provider Guard (120), Never-Hardcode (116) |
| **XML Semantic Boundaries** | Structured Output Templates (14), Few-Shot Examples (25), Domain Knowledge (24), Creative Philosophy (101) |
| **Few-Shot with Reasoning** | Few-Shot Examples (25), Evidence Chain (26), Self-Critique (28), Blind A/B (108), Refinement Pass (102) |

---

## Source Data

Extracted from analysis of 500+ production AI agent plugins across DevOps, security, migration, and incident response domains, plus Anthropic's official Agent Skills repo (17 skills) and ComposioHQ's community-curated awesome-claude-skills repo (32 unique + 832 Composio template skills).
