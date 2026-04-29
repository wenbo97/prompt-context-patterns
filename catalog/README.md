# Prompt Engineering Examples & Pattern Catalog

A reference library for writing stable, predictable prompts for Claude Code skills and plugins. Contains **120 prompt engineering patterns** extracted from 500+ production AI agent plugins (community plugin marketplace), Anthropic's official skills repo, and community open-source skills.

## Contents

### Theory & Deep Dives

| File | Description |
|------|-------------|
| [prompt-engineering-for-skills.md](/prompt-context-patterns/catalog/techniques/token-level-techniques) | 9 foundational techniques grounded in conditional entropy and attention distribution |
| [template.md](/prompt-context-patterns/catalog/techniques/good-vs-bad-template) | Side-by-side BAD vs GOOD prompt comparison with line-by-line analysis |
| [skill-reference-laziness-analysis.md](/prompt-context-patterns/catalog/techniques/anti-laziness) | 8 strategies to prevent agents from skipping Tier 3 reference file reads, with decision framework |
| [reference-skip-playbook.md](/prompt-context-patterns/catalog/techniques/reference-skip-playbook) | 11 solution patterns for the reference-skip problem, organized by 3 failure modes (naked hop, pre-satisfaction, optional framing) with decision matrix |

### Pattern Catalog (120 Patterns)

Start with the [pattern-catalog-index.md](/prompt-context-patterns/catalog/catalog-index) for a quick-reference table of all patterns.

#### Foundational Patterns (1-30)

| File | Category | Patterns |
|------|----------|----------|
| [patterns-structural-scaffolding.md](/prompt-context-patterns/catalog/categories/patterns-structural-scaffolding) | Structural Scaffolding | YAML frontmatter, phased execution, mode branching, `$ARGUMENTS` |
| [patterns-execution-control.md](/prompt-context-patterns/catalog/categories/patterns-execution-control) | Execution Control | Persona/role, negative constraints, interactive flow, confirmation gates, progress feedback |
| [patterns-safety-and-trust.md](/prompt-context-patterns/catalog/categories/patterns-safety-and-trust) | Safety & Trust | Injection defense, data redaction, read-only boundaries, activation scope |
| [patterns-input-output-contracts.md](/prompt-context-patterns/catalog/categories/patterns-input-output-contracts) | I/O Contracts | Structured output templates, error handling, config persistence, cross-platform |
| [patterns-agent-orchestration.md](/prompt-context-patterns/catalog/categories/patterns-agent-orchestration) | Agent Orchestration | Multi-agent topologies, skill composition, intent routing, tool mapping, consensus |
| [patterns-knowledge-and-context.md](/prompt-context-patterns/catalog/categories/patterns-knowledge-and-context) | Knowledge & Context | Reference files, domain knowledge, examples, evidence requirements |
| [patterns-quality-and-feedback.md](/prompt-context-patterns/catalog/categories/patterns-quality-and-feedback) | Quality & Feedback | Scoring rubrics, self-critique, feedback loops, version management |

#### Advanced Patterns (31-99)

| File | Patterns | Focus |
|------|----------|-------|
| [patterns-advanced-orchestration.md](/prompt-context-patterns/catalog/categories/patterns-advanced-orchestration) | 31-44 | Agent orchestration & multi-agent coordination |
| [patterns-advanced-quality.md](/prompt-context-patterns/catalog/categories/patterns-advanced-quality) | 45-55 | Quality, review & evaluation |
| [patterns-advanced-safety.md](/prompt-context-patterns/catalog/categories/patterns-advanced-safety) | 56-69 | Safety, trust & compliance |
| [patterns-advanced-workflow.md](/prompt-context-patterns/catalog/categories/patterns-advanced-workflow) | 70-80 | Workflow, execution & autonomy |
| [patterns-advanced-io-domain.md](/prompt-context-patterns/catalog/categories/patterns-advanced-io-domain) | 81-91 | I/O, domain & communication |
| [patterns-gap-fills.md](/prompt-context-patterns/catalog/categories/patterns-gap-fills) | 92-99 | Onboarding, productivity, migration & creative |

#### Open-Source Patterns (100-120)

| File | Patterns | Source |
|------|----------|--------|
| [patterns-open-source-skills.md](/prompt-context-patterns/catalog/categories/patterns-open-source-skills) | 100-120 | Anthropic official skills repo + ComposioHQ community skills |

### Architecture

| File | Description |
|------|-------------|
| [skill-architecture-patterns.md](/prompt-context-patterns/catalog/techniques/skill-architecture) | Skill packaging, composition, sub-agents, marketplace patterns, and reference organization |

## How to Use

1. **Building a new skill?** Scan the [quick-reference table](/prompt-context-patterns/catalog/catalog-index#quick-reference-table) to find patterns relevant to your use case.
2. **Reviewing an existing skill?** Check which patterns it uses and which it's missing.
3. **Learning prompt engineering?** Start with the [theory](/prompt-context-patterns/catalog/techniques/token-level-techniques), then read the foundational category files in order.

## Data Sources

| Source | Size | Extraction Date |
|--------|------|-----------------|
| Community plugin marketplace | 500+ plugins, 2,293 SKILL.md files | 2026-04-13/14 |
| `skills` (Anthropic official) | 17 skills + 35 reference files | 2026-04-15 |
| `awesome-claude-skills` (Community) | 32 unique + 832 Composio skills | 2026-04-15 |
