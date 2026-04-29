# Prompt Patterns from Open-Source Skill Repositories

**Patterns 100-120** — Extracted from Anthropic's official `skills` repo (17 skills) and ComposioHQ's `awesome-claude-skills` repo (32 unique skills + 832 Composio automation skills).

**Data sources:**
- Anthropic official Agent Skills (17 SKILL.md files + 35 reference files)
- Community curated skills (32 SKILL.md files + 832 Composio skills)
- **Extraction date:** 2026-04-15

**Relationship to existing catalog:** Patterns 1-99 were extracted from 500+ production plugins across DevOps, security, migration, and incident response domains. These 21 patterns (100-120) come from the open-source ecosystem and represent either genuinely new techniques or significant refinements not observed internally.

---

## Quick-Reference Table

| # | Pattern | Category | Source Repo | Key Benefit |
|---|---------|----------|-------------|-------------|
| 100 | [Progressive Disclosure Architecture](#pattern-100-progressive-disclosure-architecture) | Structural | skills (skill-creator) | 3-tier context loading minimizes token waste |
| 101 | [Creative Philosophy Scaffolding](#pattern-101-creative-philosophy-scaffolding) | Creative | skills (canvas-design) | Forces conceptual depth before visual execution |
| 102 | [Mandatory Refinement Pass](#pattern-102-mandatory-refinement-pass) | Quality | skills (canvas-design) | Self-imposed quality gate with specific critique language |
| 103 | [Reconnaissance-Then-Action](#pattern-103-reconnaissance-then-action) | Execution | skills (webapp-testing) | Observe state before acting, prevents blind interaction |
| 104 | [Helper Script as Black Box](#pattern-104-helper-script-as-black-box) | Execution | skills (webapp-testing) | Scripts encapsulate complexity; model uses `--help` first |
| 105 | [Anti-Slop Design Guidelines](#pattern-105-anti-slop-design-guidelines) | Quality | skills (frontend-design) | Explicit list of "AI aesthetic" anti-patterns to avoid |
| 106 | [Section-by-Section Collaborative Drafting](#pattern-106-section-by-section-collaborative-drafting) | Workflow | skills (doc-coauthoring) | Iterative per-section build instead of full-document generation |
| 107 | [Reader Testing with Sub-Agent](#pattern-107-reader-testing-with-sub-agent) | Quality | skills (doc-coauthoring) | Fresh-eyes review by spawning a naive reader agent |
| 108 | [Blind A/B Comparison](#pattern-108-blind-ab-comparison) | Evaluation | skills (skill-creator) | Double-blind skill evaluation eliminates confirmation bias |
| 109 | [Composio 3-Step SaaS Integration](#pattern-109-composio-3-step-saas-integration) | Integration | awesome (Composio) | Search → Connect → Execute pattern for any SaaS API |
| 110 | [Algorithm-as-Domain Knowledge](#pattern-110-algorithm-as-domain-knowledge) | Knowledge | awesome (twitter-optimizer) | Embed actual system internals as prompt knowledge |
| 111 | [Clarifying Questions Before Action](#pattern-111-clarifying-questions-before-action) | Execution | awesome (multiple) | Structured question list before any work begins |
| 112 | [Output Format with Populated Example](#pattern-112-output-format-with-populated-example) | I/O | awesome (multiple) | Show complete realistic output, not abstract schema |
| 113 | [Multi-Workflow Routing by Input Type](#pattern-113-multi-workflow-routing-by-input-type) | Structural | skills (docx, pdf) | Same skill routes to create/read/edit based on input |
| 114 | [Font/Asset Bundling with Directory Reference](#pattern-114-fontasset-bundling-with-directory-reference) | Knowledge | skills (canvas-design) | Reference bundled assets by relative path |
| 115 | [QA Sub-Agent with Visual Verification](#pattern-115-qa-sub-agent-with-visual-verification) | Quality | skills (pptx) | Spawn sub-agent to screenshot and inspect output |
| 116 | [Never-Hardcode Financial Rules](#pattern-116-never-hardcode-financial-rules) | Safety | skills (xlsx) | All calculated values must use formulas, never literals |
| 117 | [Multi-Language SDK Routing](#pattern-117-multi-language-sdk-routing) | Structural | skills (claude-api) | Detect programming language, load language-specific docs |
| 118 | [Surface Selection by Architecture](#pattern-118-surface-selection-by-architecture) | Structural | skills (claude-api) | Route to single-call / workflow / agent pattern by need |
| 119 | [Eval-Driven Skill Improvement Loop](#pattern-119-eval-driven-skill-improvement-loop) | Quality | skills (skill-creator) | Write tests → run → grade → improve → benchmark cycle |
| 120 | [Non-Anthropic Provider Guard](#pattern-120-non-anthropic-provider-guard) | Safety | skills (claude-api) | Early exit when imports indicate wrong ecosystem |

---

<a id="pattern-100-progressive-disclosure-architecture"></a>
## Pattern 100: Progressive Disclosure Architecture

**Category:** Structural Scaffolding  
**Source:** `skills/skill-creator/SKILL.md`  
**Prevalence:** Documented as best practice in Anthropic's official skill writing guide  

### Concept

Load context in three tiers based on need, not all at once. Prevents token bloat.

### The Three Tiers

| Tier | What | When Loaded | Size Target |
|------|------|-------------|-------------|
| **Tier 1: Metadata** | YAML frontmatter (`name`, `description`) | Always in context (system prompt) | ~100 words |
| **Tier 2: SKILL.md body** | Core instructions, workflow, boundaries | When skill is invoked | <5,000 words |
| **Tier 3: Bundled resources** | Reference files, scripts, schemas, examples | On-demand via Read tool | Unlimited |

### Good: Progressive loading

```yaml
---
name: mcp-builder
description: Guide for creating MCP servers...
---

# MCP Server Builder

## Phase 1: Research
Read the framework documentation:
- TypeScript: Read `reference/node_mcp_server.md`
- Python: Read `reference/python_mcp_server.md`
```

The model reads Tier 3 files only when it enters Phase 1. If the user's question is answered by Tier 2 alone, those files are never loaded.

### Bad: Everything inline

```yaml
---
name: mcp-builder
description: Guide for creating MCP servers...
---

# MCP Server Builder

## TypeScript MCP Server Documentation
[... 2000 lines of TypeScript SDK docs ...]

## Python MCP Server Documentation
[... 1500 lines of Python SDK docs ...]
```

Every invocation pays the full token cost even if the user only wants TypeScript.

### Why It Works

Token context is finite. Progressive disclosure concentrates attention on the immediately relevant tier. Tier 3 resources are loaded into a fresh attention window (via Read tool) right when they're needed — maximizing attention locality.

### Application to Our Plugin

Our migration plugin uses this pattern: CLAUDE.md (Tier 2, always loaded) references on-demand files via `@rules/...` (Tier 3, read when entering a phase). The `<always-loaded>` vs `<on-demand>` sections in CLAUDE.md are an explicit progressive disclosure architecture.

---

<a id="pattern-101-creative-philosophy-scaffolding"></a>
## Pattern 101: Creative Philosophy Scaffolding

**Category:** Creative Workflow  
**Source:** `skills/canvas-design/SKILL.md`, `skills/algorithmic-art/SKILL.md`  
**Prevalence:** 2 skills (both Anthropic official)  

### Concept

Before producing creative output, force the model to articulate a **design philosophy** — a named aesthetic movement with principles. This prevents generic output by establishing conceptual constraints.

### Good: Philosophy-first

```markdown
## Step 1: Create Design Philosophy

Create a `.md` file articulating a visual philosophy/aesthetic movement:
- Give the movement a NAME (e.g., "Chromatic Language", "Geometric Silence")
- Articulate through: space, form, color, scale, rhythm, composition
- This is a PHILOSOPHY, not a layout description
- Use craftsmanship language throughout

## Step 2: Deduce the Subtle Reference
Identify the conceptual thread from the original request.
This becomes the "soul" of the piece.

## Step 3: Express Philosophy on Canvas
Apply the philosophy visually. Museum-quality output.
```

### Bad: Direct generation

```markdown
## Step 1: Create the design
Make a beautiful poster based on the user's request.
Use good colors and layout.
```

### Why It Works

The philosophy step forces the model to make deliberate artistic choices BEFORE execution. This creates a strong prior that constrains all subsequent generation — reducing the probability of generic "AI slop" output. The named movement acts as an attention anchor.

### Evidence

Both `canvas-design` and `algorithmic-art` use this pattern. The algorithmic-art version creates an "algorithmic philosophy" manifesto before writing any p5.js code. Output quality is notably higher than direct generation.

---

<a id="pattern-102-mandatory-refinement-pass"></a>
## Pattern 102: Mandatory Refinement Pass

**Category:** Quality  
**Source:** `skills/canvas-design/SKILL.md`  
**Prevalence:** 3 skills  

### Concept

After the initial output, the prompt forces a self-critique and polish step with specific language that raises the quality bar.

### Good: Explicit refinement with emotional anchoring

```markdown
## Final Step: Refinement

Examine your work critically. Use this exact thought:
"It isn't perfect enough. It must be pristine."

Look for:
- Alignment issues (off by even 1 pixel)
- Color harmony (does every color earn its place?)
- Typography kerning and weight
- Negative space balance
- Overall composition from 3 feet away

Make corrections. Do NOT skip this step.
```

### Bad: Optional quality check

```markdown
## Optional: Review your work
If time permits, check for any issues.
```

### Why It Works

The phrase "It isn't perfect enough. It must be pristine." acts as an emotional prompt that shifts the model's generation distribution toward higher-quality tokens. The specific checklist items provide concrete attention targets. Making it mandatory (not optional) prevents the model from skipping it to "save effort."

---

<a id="pattern-103-reconnaissance-then-action"></a>
## Pattern 103: Reconnaissance-Then-Action

**Category:** Execution Control  
**Source:** `skills/webapp-testing/SKILL.md`  
**Prevalence:** 1 skill (but highly applicable pattern)  

### Concept

Before interacting with a dynamic system (browser, API, CLI), first observe its current state. Never act blind.

### Good: Observe first

```markdown
## Reconnaissance-Then-Action Pattern

When testing any webpage:
1. **First:** Take a screenshot to see what the page actually looks like
2. **Second:** Inspect the DOM to identify precise selectors
3. **Third:** Identify the specific elements you need to interact with
4. **Fourth:** Execute your action using the identified selectors

NEVER click, type, or navigate without first observing the current state.
```

### Bad: Act immediately

```markdown
## Testing
1. Click the login button
2. Type the username
3. Submit the form
```

### Why It Works

Dynamic systems have state that the model cannot predict from the prompt alone. The reconnaissance step provides grounding (Technique 2) — concrete observations that anchor subsequent actions. Without it, the model hallucinates element locations and state.

### Broader Application

This pattern applies beyond browser testing:
- **File systems:** `ls` before `mv`
- **Git:** `git status` before `git add`
- **Databases:** `SELECT` before `UPDATE`
- **APIs:** `GET` before `PUT`

Our build-repair-agent uses a variant: always read build output before applying fixes.

---

<a id="pattern-104-helper-script-as-black-box"></a>
## Pattern 104: Helper Script as Black Box

**Category:** Execution Control  
**Source:** `skills/webapp-testing/SKILL.md`, `skills/web-artifacts-builder/SKILL.md`  
**Prevalence:** 5 skills  

### Concept

Bundle complex operations into scripts. The model calls the script with `--help` first, then uses it as a black box. The model never needs to understand the script's internals.

### Good: Script with --help discovery

```markdown
## Helper Scripts

### scripts/with_server.py
Manages server lifecycle for testing. Always run `--help` first:
```bash
python scripts/with_server.py --help
```

Use it as a black box — do not modify the script or duplicate its logic.

### scripts/bundle-artifact.sh
Bundles React app into single HTML. Run directly:
```bash
bash scripts/bundle-artifact.sh
```
```

### Bad: Inline all logic

```markdown
## Starting the server
1. Check if port 3000 is in use
2. If yes, kill the process
3. Run `npm start` in background
4. Wait for server to be ready
5. Check health endpoint
6. If health fails, retry 3 times
...
```

### Why It Works

Scripts provide cognitive offloading (Technique 3) — the model doesn't need to reason about server lifecycle management, it just calls a function. The `--help` discovery pattern means the model adapts to the script's actual interface rather than guessing.

---

<a id="pattern-105-anti-slop-design-guidelines"></a>
## Pattern 105: Anti-Slop Design Guidelines

**Category:** Quality / Negative Space  
**Source:** `skills/frontend-design/SKILL.md`, `skills/web-artifacts-builder/SKILL.md`  
**Prevalence:** 2 skills (Anthropic official)  

### Concept

Explicitly name the generic patterns that AI tends to produce, and prohibit them. This is a specialized application of Negative Constraints (Pattern 6) for creative output.

### Good: Named anti-patterns

```markdown
## Design Guidelines

Avoid these "AI slop" aesthetics:
- Excessive centered layouts (everything stacked vertically)
- Purple/blue gradient backgrounds (the default AI palette)
- Uniform rounded corners on everything
- Inter font everywhere
- Card-based layouts with no visual hierarchy
- Gratuitous animation with no purpose
- Stock photo placeholders

Instead:
- Use asymmetric layouts with intentional tension
- Choose colors that serve the content's mood
- Mix sharp and rounded corners deliberately
- Select typefaces that match the content's personality
```

### Bad: Vague quality instruction

```markdown
## Design
Make it look professional and modern.
```

### Why It Works

"Professional and modern" is the exact distribution that produces AI slop — it's the statistical average of all "nice-looking" websites the model has seen. Naming the specific anti-patterns suppresses those modes, while the alternatives boost distinctive choices. This is Negative Space (Technique 7) with domain-specific precision.

---

<a id="pattern-106-section-by-section-collaborative-drafting"></a>
## Pattern 106: Section-by-Section Collaborative Drafting

**Category:** Workflow  
**Source:** `skills/doc-coauthoring/SKILL.md`  
**Prevalence:** 1 skill  

### Concept

Instead of generating a full document at once, build it section by section with user input at each stage. Each section goes through: clarify → brainstorm → curate → gap-check → draft → refine.

### Good: Iterative per-section build

```markdown
## Stage 2: Section-by-Section Building

For EACH section in the outline:

1. **Clarify:** "What's the main point you want this section to make?"
2. **Brainstorm:** Generate 3-5 possible approaches for this section
3. **Curate:** User picks the approach (or combines)
4. **Gap Check:** "What information am I missing to write this well?"
5. **Draft:** Write the section
6. **Refine:** User provides feedback, iterate until satisfied

Only move to the next section when the current one is approved.
```

### Bad: Full document generation

```markdown
## Writing
Generate the complete document based on the outline.
Present it to the user for review.
```

### Why It Works

Full-document generation dilutes attention across the entire piece. Section-by-section concentrates the model's attention on one coherent unit. User feedback at each stage provides course correction before errors compound. The fixed 6-step micro-workflow provides cognitive offloading for the writing process itself.

---

<a id="pattern-107-reader-testing-with-sub-agent"></a>
## Pattern 107: Reader Testing with Sub-Agent

**Category:** Quality  
**Source:** `skills/doc-coauthoring/SKILL.md`  
**Prevalence:** 1 skill  

### Concept

After writing a document, spawn a separate agent (sub-agent) to read it as a naive reader. The sub-agent has no context about the writing process — it only sees the document. This provides genuine "fresh eyes" review.

### Good: Sub-agent as naive reader

```markdown
## Stage 3: Reader Testing

### With Sub-Agents (preferred)
Spawn a sub-agent with ONLY the document (no outline, no conversation history).
Give it these instructions:
- Read the document as if you've never seen it before
- Predict what each section will say BEFORE reading it (to test if structure is clear)
- Note any confusion, jargon, or missing context
- Rate each section's clarity on 1-5

### Without Sub-Agents (fallback)
Read the document as if for the first time.
For each section heading, predict its content before reading.
Note surprises — any surprise = a clarity issue.
```

### Bad: Self-review without isolation

```markdown
## Review
After writing, re-read the document yourself and check for clarity issues.
```

The author agent already knows the intent behind every sentence. Self-review without memory isolation produces false confidence — the agent fills in gaps from its own context rather than detecting them.

### Why It Works

The main agent has seen the entire writing process — it cannot be a naive reader. A sub-agent with memory isolation (Pattern 42) genuinely doesn't know the backstory. Its confusion is real signal, not simulated.

### Relationship to Existing Patterns

This combines Memory Isolation (Pattern 42) with Self-Critique (Pattern 28), but adds a structural twist: the sub-agent tests predictions against reality, not just "is this good?"

---

<a id="pattern-108-blind-ab-comparison"></a>
## Pattern 108: Blind A/B Comparison

**Category:** Evaluation  
**Source:** `skills/skill-creator/SKILL.md`, `skills/skill-creator/agents/comparator.md`  
**Prevalence:** 1 skill (but deeply developed)  

### Concept

Compare two skill versions by running both on the same inputs, then having a blind comparator agent evaluate the outputs without knowing which version produced which. This eliminates confirmation bias.

### Architecture

```
1. Run Skill Version A on N test cases → collect outputs
2. Run Skill Version B on same N test cases → collect outputs
3. Randomly assign as "Output A" and "Output B" (blind)
4. Comparator agent reads both outputs + rubric
5. Comparator determines winner without knowing version labels
6. Analyzer agent extracts actionable improvements from winner
```

### The Comparator's 7-Step Process

```markdown
1. Read both outputs without seeing skill content
2. Understand what the task asked for
3. Generate evaluation rubric (content + structure dimensions)
4. Evaluate each output against rubric
5. Check assertions (from test cases)
6. Determine winner with scores and reasoning
7. Write results as structured JSON
```

### Bad: Author picks the winner

```markdown
## Comparison
Run both versions, then decide which one you think is better
and explain why.
```

The author of the "improved" version has anchoring bias toward their own changes. Without blinding and a structured rubric, the evaluator reliably picks the version they expect to be better.

### Why It Works — if they know which version is "new" or "improved," they rate it higher. Blinding removes this bias entirely. The 7-step process provides cognitive offloading for the evaluation itself.

---

<a id="pattern-109-composio-3-step-saas-integration"></a>
## Pattern 109: Composio 3-Step SaaS Integration

**Category:** Integration  
**Source:** `awesome-claude-skills/composio-skills/*` (832 skills)  
**Prevalence:** 832 skills use this exact pattern  

### Concept

A universal template for integrating with any SaaS API through three deterministic steps: Search → Connect → Execute.

### The Template

```markdown
## How to use this skill

1. **Search for available tools:**
   Use RUBE_SEARCH_TOOLS with toolkit name "{service}" to discover available actions.

2. **Check and establish connection:**
   Use RUBE_MANAGE_CONNECTIONS to verify or create the API connection.
   If no connection exists, provide the setup URL to the user.

3. **Execute the action:**
   Use RUBE_MULTI_EXECUTE_TOOL to run the discovered action.

## Known Pitfalls
- Always search for tools first — tool names change between versions
- Always verify connection before execution — expired tokens cause silent failures
```

### Bad: Hardcoded API calls

```markdown
## Slack Integration
Call `chat.postMessage` with the channel ID and message text.
Use the bot token from environment variable SLACK_TOKEN.
```

Hardcoded action names break when the API changes. Hardcoded auth skips connection validation, causing silent failures on expired tokens.

### Why It Works — it works for 832+ different SaaS APIs because it abstracts away all service-specific details into the tool discovery step. The model doesn't need to know Slack's API or Jira's API — it discovers available actions at runtime.

### Broader Application

This Search → Connect → Execute pattern applies to any integration where:
- The available actions are dynamic (APIs change)
- Authentication is a separate concern
- The model should discover capabilities rather than having them hardcoded

---

<a id="pattern-110-algorithm-as-domain-knowledge"></a>
## Pattern 110: Algorithm-as-Domain Knowledge

**Category:** Knowledge  
**Source:** `awesome-claude-skills/twitter-algorithm-optimizer/SKILL.md`  
**Prevalence:** 1 skill (but the technique is broadly applicable)  

### Concept

Embed the actual internals of an external system (ranking algorithm, scoring model, recommendation engine) as structured domain knowledge in the prompt. The model then optimizes content against the real algorithm, not a guess.

### Good: Real algorithm internals

```markdown
## Twitter's Core Ranking Models

1. **Real-graph:** Predicts interaction probability between user pairs
2. **SimClusters:** Community detection via user-topic embedding spaces
3. **TwHIN:** Knowledge graph embeddings (user-tweet-author triples)
4. **Tweepcred:** PageRank-style reputation scoring on social graph

## Engagement Signals (Weighted)
- Explicit: likes (1x), replies (3x), retweets (5x), quotes (10x)
- Implicit: profile visits, link clicks, dwell time, bookmarks
- Negative: block (-100x), mute (-50x), "not interested" (-20x)

## Optimization Strategy
For each tweet, map to algorithm components:
1. Will this trigger Real-graph? (personal relevance)
2. Does it fit SimClusters? (community resonance)
3. What signals will it maximize? (engagement weights)
```

### Bad: Generic advice

```markdown
## How to write good tweets
- Be engaging
- Use hashtags
- Post at good times
```

### Why It Works

Domain Knowledge Embedding (Pattern 24) is strengthened enormously when the knowledge is the actual system internals, not a human summary. The model can reason about specific mechanisms (SimClusters, Real-graph) rather than vague concepts ("engagement").

---

<a id="pattern-111-clarifying-questions-before-action"></a>
## Pattern 111: Clarifying Questions Before Action

**Category:** Execution Control  
**Source:** `awesome-claude-skills/file-organizer/SKILL.md`, `content-research-writer/SKILL.md`, `lead-research-assistant/SKILL.md`, `meeting-insights-analyzer/SKILL.md`, `tailored-resume-generator/SKILL.md`, and 5+ others  
**Prevalence:** ~40% of community skills  

### Concept

Before doing any work, ask 3-5 specific clarifying questions. Not open-ended "what do you want?" but targeted questions that gather the parameters needed to proceed.

### Good: Targeted questions

```markdown
## Step 1: Understand the Scope

Before organizing ANY files, ask these questions:
1. Which directory should I focus on? (specific path)
2. What's the main problem? (duplicates / messy naming / wrong locations / all of the above)
3. Are there any files or folders I should NEVER touch?
4. How aggressive should I be? (suggest only / move files / delete duplicates)
```

### Bad: Open-ended or no questions

```markdown
## Step 1: Organize
Look at the user's files and organize them.
```

### Why It Works

Each question constrains a parameter that would otherwise be under-determined. This is a runtime application of Schema Priming (Technique 6) — the questions define the "schema" of the task before execution begins. The numbered list provides Token-Action Binding (Technique 5) — each question maps to one parameter.

### Prevalence Note

This is by far the most common pattern in community skills (~40%). It appears at the start of almost every non-trivial skill, suggesting it's a natural "best practice" that skill authors independently discover.

---

<a id="pattern-112-output-format-with-populated-example"></a>
## Pattern 112: Output Format with Populated Example

**Category:** I/O Contracts  
**Source:** `awesome-claude-skills/domain-name-brainstormer/SKILL.md`, `changelog-generator/SKILL.md`, `developer-growth-analysis/SKILL.md`, and 8+ others  
**Prevalence:** ~35% of community skills  

### Concept

Show a complete, realistic output example with actual data — not an abstract schema with placeholder types. The example IS the schema.

### Good: Populated example

```markdown
## Example Output

### Available (.com)
| Domain | Status | Price |
|--------|--------|-------|
| codeflow.com | Available | ~$12/yr |
| devpulse.com | Available | ~$12/yr |

### Available (Alternative TLDs)
| Domain | Status | Price |
|--------|--------|-------|
| codeflow.dev | Available | ~$14/yr |
| codeflow.io | Available | ~$30/yr |

### Recommendations
**Top Pick:** codeflow.com — short, memorable, .com availability
**Runner-up:** devpulse.dev — modern TLD, developer audience signal
```

### Bad: Abstract schema

```markdown
## Output Format
Return a table with columns: domain, status, price.
Group by availability.
Include recommendations.
```

### Why It Works

The populated example is stronger grounding than an abstract schema because:
1. The model sees exact formatting (table alignment, headers, section structure)
2. The data distribution is demonstrated (price ranges, TLD variety, recommendation style)
3. The tone is established (concise descriptions, comparison language)

This is Grounding (Technique 2) + Schema Priming (Technique 6) combined.

---

<a id="pattern-113-multi-workflow-routing-by-input-type"></a>
## Pattern 113: Multi-Workflow Routing by Input Type

**Category:** Structural  
**Source:** `skills/docx/SKILL.md`, `skills/pdf/SKILL.md`, `skills/pptx/SKILL.md`  
**Prevalence:** 4 document skills  

### Concept

A single skill handles multiple fundamentally different workflows (create, read, edit) by routing based on what the user provides as input.

### Good: Input-type routing

```markdown
## Workflow Selection

What does the user want?
├─ **Read/analyze** an existing document?
│  └─ Use `pandoc` to convert to markdown, then analyze
│
├─ **Create** a new document from scratch?
│  └─ Use docx-js (JavaScript) to build programmatically
│
├─ **Edit** an existing document (preserve formatting)?
│  └─ Unpack OOXML, edit XML directly, repack
│     (This is the only way to preserve styles, track changes, etc.)
```

### Bad: Single workflow

```markdown
## Creating Documents
Here's how to create Word documents...
(User who wants to EDIT is lost)
```

### Why It Works

This is a specialized form of Intent Classification (Pattern 20), but the routing key is the input type (nothing vs. existing file vs. both), not the user's stated intent. The decision tree format provides deterministic routing with no ambiguity.

---

<a id="pattern-114-fontasset-bundling-with-directory-reference"></a>
## Pattern 114: Font/Asset Bundling with Directory Reference

**Category:** Knowledge / Context  
**Source:** `skills/canvas-design/SKILL.md` (54 fonts), `skills/algorithmic-art/SKILL.md` (templates)  
**Prevalence:** 4 skills  

### Concept

Bundle physical assets (fonts, templates, schemas) alongside the skill and reference them by relative path. The model uses the assets directly — no downloading, no external dependencies.

### Good: Bundled assets with path reference

```markdown
## Available Fonts

Use fonts from the `./canvas-fonts` directory. Available families:
- Playfair Display (Regular, Bold, Italic)
- Space Mono (Regular, Bold)
- Crimson Text (Regular, Italic)
- ...

Always use absolute paths resolved from the skill directory.
Do NOT download fonts from the internet.
```

### Bad: Downloading at runtime

```markdown
## Fonts
Download a font from Google Fonts that matches the design.
Use the URL: https://fonts.googleapis.com/css2?family=...
```

Runtime downloads introduce network failures, version drift, and unpredictable availability. The model may also hallucinate font URLs that return 404.

### Why It Works The model doesn't need to check if a font exists or handle download failures. The relative path reference creates a closed system — all resources are known at prompt-writing time.

---

<a id="pattern-115-qa-sub-agent-with-visual-verification"></a>
## Pattern 115: QA Sub-Agent with Visual Verification

**Category:** Quality  
**Source:** `skills/pptx/SKILL.md`  
**Prevalence:** 1 skill  

### Concept

After generating visual output (slides, images, PDFs), spawn a sub-agent to screenshot the result and verify it meets quality standards. The QA agent has visual inspection capabilities.

### Good: Visual QA loop

```markdown
## Quality Assurance

After generating slides:
1. Spawn a sub-agent with screenshot capability
2. Sub-agent opens each slide and takes screenshots
3. Sub-agent checks against these criteria:
   - No text overflow outside slide boundaries
   - No repeated layouts on consecutive slides
   - No accent lines under titles (anti-pattern)
   - Color palette consistency
   - Font size readability
4. Report issues → fix → re-verify
```

### Bad: Text-only review

```markdown
## Quality Check
Review the generated slide XML to verify layout is correct.
Check that no text exceeds the slide boundaries.
```

Slide XML coordinates are opaque numbers (EMU units). No amount of text-based XML inspection can reliably detect visual overflow, misalignment, or color clashes.

### Why It Works (overflow, alignment, color clashes). The sub-agent provides a genuine visual feedback loop. This is a specialized combination of Reader Testing (Pattern 107) and Memory Isolation (Pattern 42).

---

<a id="pattern-116-never-hardcode-financial-rules"></a>
## Pattern 116: Never-Hardcode Financial Rules

**Category:** Safety / Domain  
**Source:** `skills/xlsx/SKILL.md`  
**Prevalence:** 1 skill (but critical for any data skill)  

### Concept

For spreadsheet/financial output, all calculated values MUST use formulas — never hardcoded numbers. This ensures the spreadsheet remains functional when inputs change.

### Good: Formula-first rule

```markdown
## Critical Rule: Formulas, Never Hardcoded Values

NEVER put a calculated number directly in a cell.
ALWAYS use an Excel formula.

✅ Cell C2: =A2*B2 (calculates price × quantity)
❌ Cell C2: 150 (hardcoded result of 10 × 15)

After creating the spreadsheet, MANDATORY: run LibreOffice recalculation
to verify all formulas produce correct results.
```

### Bad: Computed values in cells

```markdown
## Spreadsheet
Fill in the total column with the calculated values.
For row 2, the total is 150. For row 3, the total is 230.
```

Hardcoded results produce a dead spreadsheet. When any input changes, totals silently become stale with no indication of error.

### Why It Works This explicit prohibition with the formula-first alternative redirects that tendency. The mandatory recalculation step provides a verification gate.

### Broader Application

This pattern generalizes to: **never embed computed results when the computation can be preserved**. Applies to:
- SQL views instead of materialized snapshots
- Config templates instead of expanded configs
- Build scripts instead of committed build outputs

---

<a id="pattern-117-multi-language-sdk-routing"></a>
## Pattern 117: Multi-Language SDK Routing

**Category:** Structural  
**Source:** `skills/claude-api/SKILL.md`  
**Prevalence:** 1 skill  

### Concept

Detect the user's programming language from imports/file extensions/explicit statement, then load only the relevant SDK documentation.

### Good: Language detection + selective loading

```markdown
## Language Detection

Determine the user's language:
├─ Python imports (`import anthropic`, `from anthropic`) → Read `python/claude-api/README.md`
├─ TypeScript imports (`import Anthropic`, `from @anthropic-ai/sdk`) → Read `typescript/claude-api/README.md`
├─ Java → Read `java/claude-api.md`
├─ Go → Read `go/claude-api.md`
├─ Ruby → Read `ruby/claude-api.md`
├─ C# → Read `csharp/claude-api.md`
├─ PHP → Read `php/claude-api.md`
├─ cURL / no code → Read `curl/examples.md`
└─ Unknown → Ask user

Always load `shared/models.md` regardless of language.
```

### Bad: Load all language docs

```markdown
## API Documentation
Here is the complete Claude API reference for all languages:
[... Python docs ...] [... TypeScript docs ...] [... Java docs ...]
[... Go docs ...] [... Ruby docs ...]
```

Loading all 7 language SDKs wastes ~1800 lines of context on 6 irrelevant languages. Attention dilution causes the model to mix up language-specific idioms.

### Why It Works The model only loads ~200 lines of language-specific docs instead of ~2000 lines of all-language docs. Token savings directly improve output quality by concentrating attention.

---

<a id="pattern-118-surface-selection-by-architecture"></a>
## Pattern 118: Surface Selection by Architecture

**Category:** Structural  
**Source:** `skills/claude-api/SKILL.md`  
**Prevalence:** 1 skill  

### Concept

After determining the language, determine the architectural pattern the user needs, and load only that pattern's documentation.

### Good: Architecture routing

```markdown
## Surface Selection

What is the user building?
├─ **Single API call** (classification, extraction, Q&A)
│  └─ Load: language-specific basic examples
├─ **Multi-step workflow** (pipelines, chains)
│  └─ Load: tool-use docs + streaming docs
├─ **Autonomous agent** (tool loop, planning)
│  └─ Load: tool-use + agent design docs
├─ **Managed agent** (Anthropic-hosted)
│  └─ Load: managed-agents docs (beta)
```

### Bad: Single pattern for all use cases

```markdown
## Claude API
Use messages.create() to call the Claude API.
Pass your prompt in the messages array.
```

A single-call example leaves users building agents or workflows without guidance on tool use, streaming, or multi-turn patterns. They reinvent these architectures poorly.

### Why It Works means the model loads exactly the right subset of documentation. A Python user building a simple classifier loads ~100 lines. A TypeScript user building an autonomous agent loads ~400 lines. Neither loads the full 2000+ line corpus.

---

<a id="pattern-119-eval-driven-skill-improvement-loop"></a>
## Pattern 119: Eval-Driven Skill Improvement Loop

**Category:** Quality / Evaluation  
**Source:** `skills/skill-creator/SKILL.md`  
**Prevalence:** 1 skill (Anthropic official)  

### Concept

A structured loop for improving skills through automated evaluation: write test cases → run them → grade results → extract improvements → apply → re-benchmark.

### The 5-Step Eval Process

```markdown
## Running Evaluations

1. **Create test cases** (`evals.json`):
   - 5+ prompts covering different scenarios
   - Each with expectations (MUST contain, MUST NOT contain, behavioral checks)

2. **Run tests:** Spawn sub-agent per test case
   - Sub-agent executes the skill with the test prompt
   - Captures full transcript + output

3. **Grade:** Spawn grader sub-agent
   - Reads expectations + transcript
   - Extracts claims, verifies each against evidence
   - PASS/FAIL per expectation with reasoning

4. **Analyze:** Spawn analyzer sub-agent
   - Surfaces per-assertion patterns (which expectations fail most?)
   - Cross-eval patterns (are failures correlated?)
   - Generates improvement suggestions

5. **Improve:** Apply suggestions to SKILL.md
   - Re-run evals to verify improvement
   - Benchmark: compare old vs new versions
```

### Bad: Manual spot-checking

```markdown
## Testing
Try a few prompts and see if the output looks good.
If it does, ship it.
```

Manual spot-checking catches obvious failures but misses edge cases. Without a persistent eval suite, prompt changes silently regress previously-working scenarios.

### Why It Works The eval suite catches regressions that manual testing misses. The multi-agent architecture (executor, grader, analyzer) prevents self-evaluation bias.

---

<a id="pattern-120-non-anthropic-provider-guard"></a>
## Pattern 120: Non-Anthropic Provider Guard

**Category:** Safety / Activation Scope  
**Source:** `skills/claude-api/SKILL.md`  
**Prevalence:** 1 skill  

### Concept

Before executing, check if the user's code uses a different provider (OpenAI, Google, etc.). If so, exit immediately — don't attempt to adapt.

### Good: Provider detection with early exit

```markdown
## Non-Anthropic Detection (BEFORE anything else)

If the code imports or uses any of these, STOP and say
"This skill is for the Anthropic/Claude API. Your code uses {provider}.":

- `import openai` / `from openai`
- `import { OpenAI }` / `@google/generative-ai`
- `langchain` with non-Anthropic models
- Any `OPENAI_API_KEY` references

Do NOT try to adapt the code to work with Claude.
Do NOT suggest replacing the provider.
Just inform and stop.
```

### Bad: No provider check

```markdown
## Getting Started
Help the user write code that calls the Claude API.
```

Without provider detection, the model may attempt to adapt OpenAI code to the Anthropic SDK, producing hybrid code that uses neither API correctly.

### Why It Works, but with automatic detection instead of relying on the user to know when the skill applies. The early exit prevents the model from attempting an ill-suited transformation that would waste tokens and produce incorrect output.

---

## Cross-Cutting Observations

### Pattern Prevalence by Repo

| Pattern Category | Anthropic `skills` | Community `awesome` | Both |
|-----------------|--------------------|--------------------|------|
| Progressive Disclosure | Strong (multiple skills) | Rare | - |
| Clarifying Questions | Moderate | Very strong (~40%) | Yes |
| Populated Examples | Moderate | Very strong (~35%) | Yes |
| Anti-Slop Guidelines | Present | Absent | - |
| Helper Scripts | Present | Absent | - |
| SaaS Integration | Absent | 832 skills | - |
| Algorithm Internals | Absent | Present | - |
| Eval-Driven Improvement | Deep (skill-creator) | Absent | - |

### Quality Gradient

The Anthropic official skills show significantly more sophisticated prompt engineering:
1. **Multi-tier context loading** (Progressive Disclosure)
2. **Sub-agent evaluation architectures** (Blind A/B, Reader Testing)
3. **Anti-pattern naming** (Anti-Slop)
4. **Domain-specific safety rules** (Never-Hardcode Financial)

Community skills favor simpler but widely applicable patterns:
1. **Clarifying Questions** (universal)
2. **Populated Examples** (universal)
3. **Step-by-step Instructions** (7-10 numbered steps)
4. **Use Case Catalogs** (when to use / example workflows)

### Design Philosophy Differences

| Aspect | Anthropic Official | Community |
|--------|-------------------|-----------|
| Invocation | Implicit (description triggers) | Explicit (user must know skill exists) |
| Context management | Progressive disclosure | Everything inline |
| Quality assurance | Sub-agent verification | Self-check or none |
| Error handling | Degradation paths | Rarely mentioned |
| Bundled resources | Scripts, schemas, fonts | Minimal |
| Skill size | 50-600 lines | 30-500 lines |
