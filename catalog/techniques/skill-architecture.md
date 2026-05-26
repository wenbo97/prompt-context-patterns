# Skill Architecture Patterns — Lessons from Open-Source Repos

Structural patterns for how skills are **organized, packaged, and composed** — extracted from Anthropic's official `skills` repo and ComposioHQ's `awesome-claude-skills`.

**Data sources:**
- Anthropic official skills: 17 official skills, `marketplace.json`, `template/SKILL.md`
- Community curated skills: 32 unique + 832 Composio skills, `CONTRIBUTING.md`
- **Extraction date:** 2026-04-15

---

## 1. The Canonical Skill Structure

Both repos converge on this minimal structure:

```
skill-name/
├── SKILL.md          # REQUIRED: YAML frontmatter + instructions
├── LICENSE.txt        # OPTIONAL: per-skill license
├── scripts/           # OPTIONAL: helper scripts (Python, Bash, JS)
├── reference/         # OPTIONAL: domain knowledge files
├── templates/         # OPTIONAL: output templates
├── examples/          # OPTIONAL: example inputs/outputs
├── agents/            # OPTIONAL: sub-agent definitions
├── assets/            # OPTIONAL: fonts, images, schemas
└── themes/            # OPTIONAL: pre-built configurations
```

### SKILL.md Anatomy

```yaml
---
name: lowercase-hyphenated-name
description: One line explaining WHEN to activate and WHAT it does
license: "Complete terms in LICENSE.txt" | "Proprietary" | omitted
---

# Skill Title (optional — some skills skip this)

[Body: instructions, workflows, constraints, examples]
```

### Key Design Decisions

| Decision | Anthropic Official | Community |
|----------|-------------------|-----------|
| `name` format | `lowercase-hyphenated` | `lowercase-hyphenated` (enforced by CONTRIBUTING.md) |
| `description` purpose | Trigger condition for Claude | Trigger condition (same intent) |
| `license` field | 15/17 skills include it | ~10% include it |
| Body size | 30-590 lines | 30-500 lines |
| Sections | Varies by complexity | 5-section template recommended |

---

## 2. Description Writing — The Trigger Mechanism

The `description` field is the **most important line** in any skill. It determines when Claude activates the skill. Analysis of 50+ descriptions reveals distinct patterns:

### Pattern A: Action + Domain + Trigger Keywords

```yaml
description: >-
  Guide for creating high-quality MCP servers that enable LLMs to
  interact with external services. Use when building MCP servers to
  integrate external APIs.
```

Structure: `{what it does}. {when to use it}.`

### Pattern B: Capability List

```yaml
description: >-
  Toolkit for interacting with and testing local web applications
  using Playwright. Supports verifying frontend functionality,
  debugging UI behavior, capturing browser screenshots, and viewing
  browser logs.
```

Structure: `{primary capability}. Supports {capability}, {capability}, {capability}.`

### Pattern C: Negative Boundary

```yaml
description: >-
  Suite of tools for creating elaborate HTML artifacts using React,
  Tailwind CSS, shadcn/ui. Use for complex artifacts requiring state
  management — not for simple single-file HTML artifacts.
```

Structure: `{what it does}. Use for {scope} — not for {anti-scope}.`

### Pattern D: Emotional Hook (Community)

```yaml
description: >-
  Automatically creates user-facing changelogs from git commits.
  Turns hours of manual changelog writing into minutes of automated
  generation.
```

Structure: `{what it does}. {value proposition — time saved}.`

### Best Practice

Combine A + C: State the action, the domain, the trigger condition, AND the negative boundary.

```yaml
description: >-
  Migrate .NET Framework projects to .NET Core multi-targeting.
  Use when the user says "start migration" or provides a .csproj path.
  NOT for greenfield .NET projects or projects already on .NET Core.
```

---

## 3. The Five-Section Community Template

From `awesome-claude-skills/CONTRIBUTING.md` — the recommended sections for any skill:

```markdown
# {Skill Name}

## When to Use
- [Trigger conditions — bullet list]
- Keywords: [comma-separated trigger words]

## What This Skill Does
- [Capabilities — bullet list]
- [Limitations — explicit boundaries]

## How to Use
### Basic Usage
[Simplest invocation]

### Advanced Usage
[With options/flags]

## Example
[Complete, realistic input → output]

## Tips
- [Power user advice]
- [Common pitfalls]
- [Related workflows]
```

### Analysis: Which Sections Matter Most?

| Section | Impact on Quality | Prevalence |
|---------|------------------|------------|
| **How to Use** (steps) | Critical — provides the execution path | ~90% of skills |
| **Example** (populated) | High — grounds the output format | ~65% of skills |
| **When to Use** (scope) | Medium — prevents mis-activation | ~40% of skills |
| **Tips** (pitfalls) | Medium — prevents common errors | ~50% of skills |
| **What This Skill Does** | Low — redundant with description | ~30% of skills |

---

## 4. Marketplace Packaging

Anthropic's `marketplace.json` groups 17 skills into 3 installable packages:

```json
{
  "plugins": [
    {
      "name": "document-skills",
      "skills": ["xlsx", "docx", "pptx", "pdf"]
    },
    {
      "name": "example-skills",
      "skills": ["algorithmic-art", "brand-guidelines", "canvas-design", ...]
    },
    {
      "name": "claude-api",
      "skills": ["claude-api"]
    }
  ]
}
```

### Grouping Strategy

| Strategy | When to Use | Example |
|----------|-------------|---------|
| **By domain** | Skills share resources (schemas, helpers) | document-skills: xlsx + docx + pptx + pdf |
| **By audience** | Skills target same user type | example-skills: creative + testing + building |
| **Standalone** | Skill is self-contained and specialized | claude-api |

### Resource Sharing Within Packages

The document-skills package shares:
- 39 XSD schemas (OOXML validation)
- Python helper scripts (file manipulation)
- Office helpers (style management, XML editing)

This reduces total package size vs. 4 independent skills.

---

## 5. Script Integration Patterns

### Pattern A: Self-Documenting Script (--help)

```markdown
Always run `python scripts/with_server.py --help` before first use.
Use the script as a black box — do not modify it.
```

Used by: webapp-testing, skill-creator

### Pattern B: Init + Build Pipeline

```markdown
1. Run `bash scripts/init-artifact.sh` (creates project structure)
2. [User develops in the created structure]
3. Run `bash scripts/bundle-artifact.sh` (produces single output file)
```

Used by: web-artifacts-builder, artifacts-builder

### Pattern C: Validation Script

```markdown
Before packaging, run validation:
`python scripts/package_skill.py --validate`
Checks: frontmatter present, description non-empty, no broken references
```

Used by: skill-creator

### Pattern D: Data Processing Script

```markdown
Use bundled scripts for file processing:
- `scripts/read_pdf.py` — extract text from PDF
- `scripts/create_pdf.py` — generate PDF with reportlab
- `scripts/merge_pdfs.py` — combine multiple PDFs
```

Used by: pdf, docx, pptx, xlsx

---

## 6. Reference File Organization

### Flat References (simple skills)

```
mcp-builder/
├── SKILL.md
└── reference/
    ├── mcp_best_practices.md
    ├── node_mcp_server.md
    ├── python_mcp_server.md
    └── evaluation.md
```

### Hierarchical References (complex skills)

```
claude-api/
├── SKILL.md
├── shared/           # Cross-language
│   ├── models.md
│   ├── prompt-caching.md
│   └── tool-use-concepts.md
├── python/
│   └── claude-api/
│       ├── README.md
│       ├── streaming.md
│       └── tool-use.md
├── typescript/
│   └── claude-api/
│       ├── README.md
│       └── ...
└── [5 more languages]
```

### Theme/Variant References

```
theme-factory/
├── SKILL.md
└── themes/
    ├── arctic-frost.md
    ├── ocean-depths.md
    ├── sunset-boulevard.md
    └── [7 more themes]
```

### Key Insight: Reference Files as Progressive Disclosure Tier 3

All reference files follow the Progressive Disclosure pattern (Pattern 100):
- SKILL.md tells the model WHICH file to read
- The model reads the file only when entering the relevant phase/workflow
- If the workflow doesn't require that file, it's never loaded

---

## 7. Sub-Agent Architecture

Only 2 of 49 non-Composio skills use sub-agents, both from Anthropic:

### skill-creator: 3 Sub-Agents

| Agent | Role | When Spawned | Memory |
|-------|------|-------------|--------|
| `grader` | Evaluate test results | After each eval run | Isolated (no skill context) |
| `comparator` | Blind A/B comparison | After two versions run | Isolated (doesn't know version labels) |
| `analyzer` | Extract improvements | After comparison | Has both transcripts + results |

### doc-coauthoring: 1 Sub-Agent

| Agent | Role | When Spawned | Memory |
|-------|------|-------------|--------|
| naive-reader | Fresh-eyes review | After document draft | Isolated (only has the document) |

### Key Architectural Rule

**Sub-agents get LESS context, not MORE.** Their value comes from what they DON'T know:
- Grader doesn't know the skill's intent → judges output purely
- Comparator doesn't know version labels → eliminates bias
- Naive-reader doesn't know the writing process → finds genuine confusion

---

## 8. Composio's Universal Template

832 skills use a near-identical template with only 3 variables:

| Variable | Example Values |
|----------|---------------|
| `{service_name}` | "slackbot", "atlassian", "googledrive" |
| `{toolkit_name}` | "SLACKBOT", "ATLASSIAN", "GOOGLEDRIVE" |
| `{specific_tools}` | Varies — some skills list tools, most don't |

### Template Quality Tiers

| Tier | Count | Characteristic |
|------|-------|---------------|
| **Generic** | ~780 | 3-step (Search → Connect → Execute), no specific tools listed |
| **Enriched** | ~50 | Lists specific tool names, parameter tables, common patterns |
| **Custom** | ~2 | Fully custom content beyond the template |

### Lesson: Templates Enable Scale, Not Quality

Composio achieved 832 skills by templating. But the generic skills are low-quality — they provide no domain-specific guidance. The enriched variants (like `googledocs-automation`) that list specific tools and pitfalls are significantly more useful.

**For our plugin:** Templates are useful for generating boilerplate (PR descriptions, branch names) but the high-value content (error handling rules, fix strategies) must be hand-crafted per domain.

---

## 9. Cross-Repo Comparison Summary

| Dimension | Anthropic Official | Community | Our Plugin (migration plugin) |
|-----------|-------------------|-----------|-----------------------------------|
| **Skills count** | 17 | 32 unique + 832 template | 21 skills + 3 agents + 4 commands |
| **Avg SKILL.md size** | ~200 lines | ~120 lines | ~150 lines |
| **Progressive Disclosure** | Explicit 3-tier | Rare | Explicit (`<always-loaded>` / `<on-demand>`) |
| **Sub-agents** | 2 skills use them | 0 skills | 3 agents (build-repair, ado, dependency) |
| **Script bundling** | 5 skills (Python, Bash) | 0 skills | 2 skills (Python) |
| **Eval framework** | Built-in (skill-creator) | None | dev-prompt-review (custom) |
| **Safety boundaries** | Provider guards, anti-slop | Minimal | Extensive (7 guardrails, 4 tiers, 99 patterns) |
| **Domain knowledge** | SDK docs, font catalogs | Algorithm internals, SaaS APIs | Error handling rules, package maps, project maps |
| **Output verification** | Visual QA sub-agent | None | Build loop (7 attempts) |

### What We Can Learn From Each

**From Anthropic Official:**
- Progressive Disclosure is worth formalizing (we already do this)
- Anti-Slop naming is powerful for creative/generative output
- Blind A/B comparison for skill quality evaluation
- Visual QA for generated artifacts

**From Community:**
- Clarifying Questions are universally adopted — we should ensure Phase 0 does this
- Populated Examples are more effective than abstract schemas
- The 5-section template is a good minimum bar for any new skill
- Emotional hooks in descriptions increase human engagement

**From Composio:**
- Universal templates enable scale but not quality
- The Search → Connect → Execute pattern is a powerful abstraction for any dynamic API
- Known Pitfalls sections prevent repeated failures across users
