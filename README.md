# Prompt, Context & Agent Orchestration Patterns

Practical patterns for writing stable AI prompts, engineering context, and orchestrating agents — backed by reproducible A/B tests.

**Blog:** [https://wenbo97.github.io/prompt-context-patterns/](https://wenbo97.github.io/prompt-context-patterns/)

All content is bilingual (English + 中文).

## What's Here

```
_posts/                Blog articles (each post has a -zh sibling)
_layouts/              Custom Jekyll layouts (default, home, post)
assets/main.scss       Warm-gray theme (Source Serif 4 + Noto Serif SC)
_includes/header.html  Site nav

catalog/               155 prompt patterns for AI agent development
  categories/          Patterns grouped by function
  techniques/          Deep-dive technique guides
  standards/           Review frameworks
  catalog-index.md     EN index · catalog-index-zh.md  ZH index

eval/                  A/B test scripts and results
  decision-tree-ab/
    prompt-prose*.md   Prose-style prompts (control)
    prompt-tree*.md    Decision-tree prompts (test)
    run.sh             Test runner
    analyze.py         Result parser
    results/           Raw outputs (gitignored)
```

## Articles

| Topic | English | 中文 | A/B Test |
|-------|---------|------|----------|
| Decision Tree pattern | [Read](https://wenbo97.github.io/prompt-context-patterns/2026/04/19/decision-tree-pattern/) | [阅读](https://wenbo97.github.io/prompt-context-patterns/2026/04/19/decision-tree-pattern-zh/) | `eval/decision-tree-ab/` |
| Prompt engineering patterns | [Read](https://wenbo97.github.io/prompt-context-patterns/2026/04/19/prompt-engineering-patterns/) | [阅读](https://wenbo97.github.io/prompt-context-patterns/2026/04/19/prompt-engineering-patterns-zh/) | — |
| **155-pattern catalog** | [Read](https://wenbo97.github.io/prompt-context-patterns/2026/05/26/prompt-pattern-catalog/) | [阅读](https://wenbo97.github.io/prompt-context-patterns/2026/05/26/prompt-pattern-catalog-zh/) | — |

## Local Preview

Requires Ruby 3.x + Bundler (Windows: `winget install RubyInstallerTeam.RubyWithDevKit.3.3`).

```bash
bundle install                              # first time only
bundle exec jekyll serve --livereload       # http://127.0.0.1:4000/prompt-context-patterns/
```

GitHub Pages rebuilds automatically on push to `master`.

## Run the A/B Tests Yourself

Requires [Claude Code CLI](https://claude.ai/code).

```bash
bash eval/decision-tree-ab/run.sh           # 5 runs per scenario, default model
bash eval/decision-tree-ab/run.sh 10 haiku  # 10 runs with haiku
python3 eval/decision-tree-ab/analyze.py    # parse results
```

Three scenarios are tested:
- **Simple** — clear input, exact rule match
- **Ambiguous** — input doesn't match any rule exactly
- **Complex** — 10 overlapping rules with mixed signals

## Conventions

- All text files use CRLF line endings (enforced via `.gitattributes`)
- Chinese posts use `-zh` filename suffix and add `lang: zh` to front matter
- The `home` layout auto-pairs EN/ZH posts by slug — no manual index editing needed
- `eval/decision-tree-ab/results/` is gitignored — test outputs stay local

## License

MIT
