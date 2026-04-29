# Advanced Input/Output, Domain & Communication Patterns

Deep patterns for data transformation, domain knowledge encoding, visualization, interactive reasoning, style transformation, and audience adaptation — extending the foundational I/O patterns (14-17) and knowledge patterns (23-26) with production-grade architectures discovered across 500+ plugins.

**Source research:** Extracted from analysis of 500+ production AI agent plugins across DevOps, security, migration, and incident response domains.

---

## Pattern 81: Natural Language to Relational Schema Decomposition

**Prevalence:** <1% of plugins
**Related patterns:** [Domain Knowledge Embedding](#pattern-24), [Phased Execution](#pattern-2)

**What it is:** A mandatory intermediate reasoning step that forces the model to decompose an arbitrary natural language subject into a formal relational structure before any code generation. The five-step procedure (identify entities, classify, define relationships, determine generation order, bound complexity) acts as a structured reasoning scaffold.

### Positive Example

```markdown
Decompose ${input:subject} into a normalized relational model.
This is a mandatory first step before any code generation.

1. Identify Entities: List all distinct real-world objects or concepts
2. Classify Each Entity:
   - Lookup/Dimension tables: Relatively static reference data
   - Fact/Transaction tables: Event-driven records that reference lookups
3. Define Relationships: For every pair of related entities, specify:
   - Relationship type: one-to-one, one-to-many, or many-to-many
   - The foreign key column and which table it references
4. Determine Generation Order: Build a dependency graph so parent/lookup
   tables are generated before child/fact tables
5. Aim for 3-7 tables depending on domain complexity.

| Subject | Entities (Tables) | Key Relationships |
| Hospital patient records | Patients, Doctors, Departments, Visits, Diagnoses | Visits->Patients (FK) |
| E-commerce sales | Customers, Products, Categories, Orders, OrderItems | Orders->Customers (FK) |
```

**Why this works:** Unlike Pattern 24 (embedding static schema), this teaches the model *how to derive* a schema from an unstructured concept. The entity classification (Lookup vs Fact) gives the model a taxonomy. The dependency graph ensures correct generation order. The 3-7 table bound prevents both under-decomposition and over-engineering.

### Negative Example

```markdown
Generate a database schema for ${input:subject}.
Create all necessary tables with appropriate columns and relationships.
Make sure to include primary keys and foreign keys.
```

**Why this fails:** No decomposition procedure means the model invents tables ad hoc, often creating too many (15+ tables for a simple domain) or too few (a single flat table). Without entity classification (Lookup vs Fact) there is no generation order, so child tables may reference parents that do not exist yet. The lack of a complexity bound gives no signal to stop adding tables.

---

## Pattern 82: Chart Decision Tree with Anti-Pattern Guards

**Prevalence:** <1% of plugins
**Related patterns:** [Tool Routing Tables](#pattern-21), [Negative Constraints](#pattern-6)

**What it is:** A multi-branch decision tree that maps *data shapes* to *visualization types* with quantitative selection criteria (cardinality guards) and inline anti-pattern prevention.

### Positive Example

```markdown
Category comparison → bar or horizontal_bar (Plotly)
Value over time → time_series (Plotly)
Distribution → histogram or box_plot (Plotly)
Part-to-whole (2-7 categories) → pie (Plotly)
Distribution across groups (20+ points/group) → violin (Plotly)
Change decomposition (3-20 factors) → waterfall (Plotly)

## Two-Variable Routing
Two numeric columns?
  +-- Meaningful third numeric (size)? 5-100 entities? → bubble_scatter
  +-- Population shape/density? Row count >500? → density_2d
  +-- Individual points with selection? → scatter_brush (D3)
  +-- Grouped by category?
        +-- >20 pts/group? → violin
        +-- <20 pts/group? → box_plot

## Anti-Patterns — Avoid:
1. Pie chart with more than 7 slices — becomes unreadable
2. 3D charts — distort perception of values
3. Dual y-axes — confuse readers about axis mapping
4. Truncated y-axis on bar charts — exaggerates differences
5. Too many series on one line chart — >7 lines become spaghetti
6. Rainbow color palettes — lack perceptual ordering, fail for colorblind
```

**Why this works:** Three layers: flat lookup for simple cases, multi-branch decision trees for ambiguous cases, and anti-patterns that short-circuit bad decisions. Cardinality guards (pie: 2-7 categories, violin: 20+ points/group) prevent selecting charts that render poorly.

### Negative Example

```markdown
Choose the best chart type for the data.
Options: bar, line, pie, scatter, histogram, box plot, violin, waterfall.
Pick whichever seems most appropriate for the user's data.
```

**Why this fails:** No selection criteria means the model defaults to bar or line charts regardless of data shape. Without cardinality guards, it will happily produce a pie chart with 50 slices or a violin plot with 3 data points. The missing anti-pattern list means nothing prevents dual y-axes or 3D charts.

---

## Pattern 83: Audience-Purpose-Driven Content Calibration

**Prevalence:** ~1% of plugins
**Related patterns:** [Workflow Mode Branching](#pattern-3), [Structured Output Templates](#pattern-14)

**What it is:** Establishing the audience and purpose as first-class inputs that gate all downstream decisions about output format, detail level, and presentation style.

### Positive Example

```markdown
### Step 1: Understand the Report

Ask about context before selecting charts:
- Audience — who reads this? (technical team, management, external stakeholders)
- Purpose — what kind? (investigation, monitoring, comparison, status update)
- Key questions — what should the reader learn?

These answers drive chart selection and level of detail:
- Audit trail needs → chart_table_query (shows visualization + raw query results)
- Summary KPI metrics → kpi_query (headline numbers with source query)
- Investigation findings → narrative (multi-paragraph explanatory text)
```

**Why this works:** The audience/purpose frame propagates through every downstream decision. Audit-trail audiences get raw data alongside visualizations; executives get headline numbers; investigators get narrative explanations. This is tone/audience adaptation applied to data visualization, not just prose.

### Negative Example

```markdown
### Step 1: Create the Report

Generate a report with appropriate charts and tables.
Include relevant KPIs and findings.
Use a professional tone suitable for business stakeholders.
```

**Why this fails:** Hardcoding "business stakeholders" collapses all audience distinctions into one. An audit team needs raw query results alongside every chart; an executive needs a single KPI headline. Without asking about purpose (investigation vs monitoring vs status update), the model produces a generic dashboard that serves no audience well.

---

## Pattern 84: Socratic Investigation Loop with Active Research

**Prevalence:** <1% of plugins
**Related patterns:** [Interactive Flow Control](#pattern-7), [Evidence Chain](#pattern-26)

**What it is:** The model alternates between *active tool-based research* (reading code, grepping patterns) and *Socratic questioning*, using its research findings to formulate increasingly precise questions. It deliberately withholds solutions to help the user discover insights.

### Positive Example

```markdown
This is NOT classic rubber duck debugging where you sit silently.
You are a full research partner who:
- Actively investigates the codebase using tools (Grep, Read, Task agents)
- Asks informed questions based on what you discover
- Guides them to insights through interactive exploration

### Investigation Loop
1. Research Before Asking
   - Evaluate relevance: which leads are "hot trail" vs "cold trail"?
   - Follow hot trail (1-3 most relevant sources)
   - Acknowledge cold leads: "I also see X, Y, Z — should I explore those?"
2. Brief Analysis (1-3 sentences)
3. Ask a Thoughtful Question (2-4 specific options based on research)
4. Process the Answer

Session guard: After 8-10 questions without converging, check in:
"We've explored quite a bit — should we keep digging or move forward?"
```

**Why this works:** The hot/cold trail triage prevents exhaustive research before asking a single question, maintaining conversational momentum. The model withholds solutions deliberately — guided discovery produces deeper understanding than answer delivery. The convergence guard prevents infinite exploration.

### Negative Example

```markdown
Help the user debug their issue using the Socratic method.
Ask clarifying questions to understand the problem.
Guide them toward the solution without giving the answer directly.
Use available tools to read code when needed.
```

**Why this fails:** No investigation loop structure means the model either asks shallow questions without reading code first, or reads the entire codebase before asking anything. Without hot/cold trail triage, every lead gets equal attention. The missing convergence guard (8-10 question check-in) lets the session spiral into endless questioning with no resolution.

---

## Pattern 85: Knowledge Base Index with Intent-to-Source Routing

**Prevalence:** ~2% of plugins
**Related patterns:** [Reference File Injection](#pattern-23), [Intent Classification](#pattern-20)

**What it is:** A two-tier retrieval system: a lightweight index file read on every invocation (small token cost), followed by selective deep reads of only matching knowledge base files. Per-source disambiguation tables handle overlapping domains.

### Positive Example

```markdown
1. Read <knowledge base>/INDEX.md — lightweight index with keywords & descriptions
2. Match user's question against index entries' keywords/descriptions
3. Only then read matching knowledge base file(s) in full
4. If no match: fall back to Grep across all .md files

INDEX.md structure:
| File | Data Source | Keywords | Description |
| get-active-action-items.md | GetActiveActionItems() | SFI, action items, person | Individual SFI queries |
| s360-active-action-items.md | ComplianceDashboard ActiveActionItems | SFI, action items, overdue | Aggregate SFI tracking |

Per-source disambiguation (inside each KB file):
| Need | Use |
| Individual action items for a person | GetActiveActionItems() (this) |
| Aggregated counts by KPI/wave | SFIFactTable or ComplianceDashboardSFISnapshot |
| Org-leader-level rollups | ActiveActionItems (turbologsna) |
```

**Why this works:** Two-tier retrieval minimizes token cost — read the index always, read full files selectively. Per-source disambiguation handles the hardest case: multiple sources with overlapping keywords but different appropriate use cases.

### Negative Example

```markdown
Read all knowledge base files at the start of every conversation.
Match the user's question against the full content of each file.
If multiple files match, combine their guidance into a single answer.
```

**Why this fails:** Reading all KB files on every invocation wastes tokens on irrelevant content. Without an index layer, matching against full file content is slow and imprecise. Combining guidance from overlapping sources without a disambiguation table produces contradictory advice when two sources cover the same keyword for different use cases.

---

## Pattern 86: Heuristic Scoring with Signal Detection

**Prevalence:** <1% of plugins
**Related patterns:** [Scoring Rubrics](#pattern-27)

**What it is:** Scoring rubrics where each score level specifies *machine-detectable signals* — word counts, regex patterns, structural markers — rather than subjective descriptors.

### Positive Example

```markdown
### Problem Statement (1-5)
| Score | Heuristic Signals |
| 1 | No section matching "problem", "background", "overview", "context" |
| 2 | Section found but <30 words, no user focus |
| 3 | Has user focus (mentions user/customer/developer) OR >80 words |
| 4 | Has specific numbers OR research evidence, AND user focus |
| 5 | Has research evidence AND >=2 specific numbers AND user focus |

Research evidence patterns: "interviewed N", "surveyed N", "research shows",
"based on data/research/feedback", "support ticket", "NPS score"

Scoring philosophy:
- AI-generated boilerplate caps at 2-3; real substance required for 4-5
- Near-perfect (48-55) requires: user research, competitive analysis, metrics with baselines
```

**Why this works:** Testable conditions (word counts, pattern matches, AND/OR logic) replace subjective labels. The "AI boilerplate caps at 2-3" rule explicitly constrains scoring of generic content.

### Negative Example

```markdown
### Problem Statement (1-5)
| Score | Description |
| 1 | Poor — missing or very weak problem statement |
| 2 | Below average — problem statement lacks depth |
| 3 | Adequate — reasonable problem statement |
| 4 | Good — strong problem statement with clear user focus |
| 5 | Excellent — comprehensive, evidence-backed problem statement |
```

**Why this fails:** Every descriptor is subjective — "lacks depth", "reasonable", and "strong" have no measurable definition. The model cannot distinguish a score-3 from a score-4 without concrete signals like word counts or evidence patterns. AI-generated boilerplate reads as "reasonable" and scores 3, when it should cap at 2.

---

## Pattern 87: Eager Incremental Materialization

**Prevalence:** <1% of plugins
**Related patterns:** [Interactive Flow Control](#pattern-7), [Confirmation Gates](#pattern-8)

**What it is:** Instructing the model to create artifacts *during* the conversation (not after), using tool calls as a real-time feedback channel to the user.

### Positive Example

```markdown
EAGER TOOL INVOCATION (CRITICAL)
Do NOT wait until the end to create plan items. Instead:
1. Create plan shell IMMEDIATELY when user provides product name
2. Create epics AS THEY EMERGE during discussion
3. Add features AS THEY'RE DEFINED

Why: Each tool call triggers a real-time WIP spinner in the plan tray,
giving immediate visual feedback that the plan is taking shape.

You CAN and SHOULD create items while still asking clarifying questions.
```

**Why this works:** Inverts the default "gather all info, then act" behavior. Tool calls become a communication channel — the user sees their words immediately producing artifacts. Permission to "create items while asking questions" overrides the model's tendency to wait for complete information.

### Negative Example

```markdown
Gather all requirements from the user first.
Once you have a complete picture, create the plan with all epics and features.
Make sure everything is finalized before making any tool calls.
```

**Why this fails:** The "gather everything first" instruction reinforces the model's default behavior of deferring all action until the conversation ends. The user sees no visible progress during a long requirements discussion, loses engagement, and has no opportunity to course-correct based on partially materialized artifacts.

---

## Pattern 88: Data Shape to Query Pattern Detection

**Prevalence:** <1% of plugins
**Related patterns:** [Intent Classification](#pattern-20), [Domain Knowledge Embedding](#pattern-24)

**What it is:** Inferring visualization intent from data artifacts — examining DataFrame column names AND original query text to detect patterns that map to specific chart types with confidence scores.

### Positive Example

```markdown
When source_type is "kusto", run pattern detection:

| Pattern Signal | Chart Type | Confidence |
| AD_score/AD_flag columns | time_series with anomaly highlights | high |
| Percentile columns (p50, p95, p99) | time_series with threshold highlights | high |
| render areachart in query | area or stacked_area | 0.9 (ADX hint) |
| Grouped continuous data (>50 rows) | violin (requires 20+ pts/group) | medium |
| Mixed pos/neg deltas (3-20 rows) | waterfall | medium |
| Source/target columns (<50 rows) | mermaid diagram | low |

Present ALL matches with confidence. Auto-populate from highest match.
User confirms, overrides, or rejects before proceeding.
```

**Why this works:** Dual-signal approach (column names + query text) provides higher accuracy than either alone. Confidence scores allow ranked suggestions rather than a single guess. This classifies intent from *data structure*, not from user text.

### Negative Example

```markdown
Analyze the data and choose the best chart type.
Consider the number of rows and columns to determine
whether a bar chart, line chart, or scatter plot is appropriate.
```

**Why this fails:** Ignoring column names and query text discards the strongest signals for chart selection. "Number of rows and columns" is too coarse — a 100-row, 3-column dataset could be a time series, a category comparison, or a distribution depending on what the columns represent. Without confidence scores, the model commits to one chart type instead of presenting ranked alternatives for user confirmation.

---

## Pattern 89: Writability Rules and Linguistic Substitution Tables

**Prevalence:** <1% of plugins
**Related patterns:** [Negative Constraints](#pattern-6), [Self-Critique](#pattern-28)

**What it is:** A complete style transformation engine: substitution tables (jargon→simple), detection heuristics (passive voice "by zombies" test), quantitative targets (15-20 word sentence average, 80% active verbs), and a self-verification checklist.

### Positive Example

```markdown
### Passive voice detection
Can you add "by zombies" after the verb and it still makes sense? → passive

### Jargon substitution (26 entries)
| Instead of | Use |
| commence | start, begin |
| comply with | keep to, follow |
| ensure | make sure |
| utilise | use |

### Nominalisation detection
Words ending in -tion, -sion, -ment, -ence, -ance with a simpler verb inside:
| Avoid | Use |
| We made an arrangement | We arranged |
| We reached an agreement | We agreed |

### Quality targets
- Average sentence length: 15-20 words
- Active verbs: ≥80%
- Zero remaining jargon with simpler alternatives
```

**Why this works:** Substitution tables give the model an exhaustive lookup. Detection heuristics ("by zombies" test, suffix patterns) teach HOW to detect problems. Quantitative targets make compliance measurable. Reusable as a post-processor by other skills.

### Negative Example

```markdown
Write in plain English. Avoid jargon and complex language.
Use short sentences and active voice where possible.
Keep the tone professional but accessible.
```

**Why this fails:** "Avoid jargon" without a substitution table means the model must decide what counts as jargon on every word — it will miss "utilise" and "commence" while flagging technical terms that have no simpler alternative. "Short sentences" and "active voice where possible" are unquantified, so there is no way to verify compliance. The model has no detection method for passive voice or nominalisations.

---

## Pattern 90: Cross-Platform Surface Compatibility Matrix

**Prevalence:** <1% of plugins
**Related patterns:** [Cross-Platform Handling](#pattern-17), [Error Handling](#pattern-15)

**What it is:** A compatibility degradation matrix mapping source/target platform pairs to specific feature losses and automated resolution paths, combined with bounded retry semantics.

### Positive Example

```markdown
| Source Surface | Target Surface | Issues | Resolution |
| Teams (v1.5+) | Outlook (v1.4) | Table, Carousel unsupported | transform_card with downgrade to 1.4 |
| Generic (v1.6) | Windows (v1.3) | Action.Execute, Table | transform_card with downgrade to 1.3 |

Bounded retry:
- Max 2 retry cycles for fix-and-revalidate loops
- MCP server unreachable → do NOT attempt to hand-write card JSON
- Tool-call budget: max 3 primary calls per user request
```

**Why this works:** Platform pairs have specific resolution commands — no guessing. The "do not hand-write JSON" rule prevents a common failure mode where models bypass tooling. Bounded retries prevent infinite fix-validate loops.

### Negative Example

```markdown
Ensure the card is compatible with the target platform.
If validation fails, fix the card and try again.
If the MCP server is unavailable, generate the card JSON directly.
```

**Why this fails:** "Ensure compatibility" without a platform-pair matrix forces the model to guess which features degrade on which surfaces. Unbounded "fix and try again" creates infinite retry loops when the same validation error recurs. Allowing hand-written JSON when the server is down bypasses schema validation entirely, producing malformed cards that fail silently on the target surface.

---

## Pattern 91: Hub-Spoke Domain Router with Overlap Resolution

**Prevalence:** ~1% of plugins
**Related patterns:** [Intent Classification](#pattern-20), [Skill Composition](#pattern-19)

**What it is:** A multi-level specificity cascade for disambiguating between specialized plugins with overlapping keyword spaces. Context-dependent routing rules where the same keyword routes differently based on co-occurring terms.

### Positive Example

```markdown
## Overlap Resolution (specificity-first)

1. Specific product area named (ProductA, ProductB, ProductC) → domain plugin
2. "Flight" + "ProductC bug" → productc-investigation (has flight classification rules)
   "Flight" standalone → flight-investigation
3. General Excel telemetry → kql-reference
4. Bug ID mentioned → classify by tag/title pattern:
   - BugTracker/Triage → fetch-bug
   - ProductC → productc-investigation
   - Unknown → ask user
5. "Pipeline" → "CI/CD health" vs "ADF query" → ask if unclear
6. Still ambiguous → present top 2-3 candidates and ask user to pick

If target plugin not installed:
"The {domain} capability requires {plugin-name}.
Install with: /plugin install {plugin-name}@marketplace"
```

**Why this works:** Six-level specificity cascade provides deterministic disambiguation. Context-dependent rules (rule 2: "flight" means different things based on co-occurring "ProductC bug") handle real ambiguity. Graceful degradation turns routing failures into actionable install guidance.

### Negative Example

```markdown
Route the user's request to the most relevant plugin.
If the request mentions a product name, use that product's plugin.
If unclear, ask the user which plugin they want.
```

**Why this fails:** No specificity cascade means overlapping keywords (e.g., "flight" appears in both Shield and flight-investigation contexts) are resolved by whichever plugin the model thinks of first. Jumping straight to "ask the user" for any ambiguity puts the disambiguation burden on users who may not know which plugins exist. Missing install guidance means uninstalled plugins silently fail instead of producing an actionable next step.
