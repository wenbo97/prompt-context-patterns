# Prompt, Context & Agent Orchestration Patterns

Practical patterns for writing stable AI prompts, engineering context, and orchestrating agents — backed by reproducible A/B tests.

**Blog:** [https://wenbo97.github.io/prompt-context-patterns/](https://wenbo97.github.io/prompt-context-patterns/)

## What's Here

```
_posts/          Blog articles (EN + ZH)
eval/            A/B test scripts and results
  decision-tree-ab/
    prompt-prose*.md     Prose-style prompts (control group)
    prompt-tree*.md      Decision-tree prompts (test group)
    run.sh               Test runner
    results/             Raw outputs from each run
```

## Patterns

| Pattern | Post (EN) | Post (ZH) | A/B Test |
|---------|-----------|-----------|----------|
| Decision Tree | [Read](https://wenbo97.github.io/prompt-context-patterns/2026/04/19/decision-tree-pattern/) | [阅读](https://wenbo97.github.io/prompt-context-patterns/2026/04/19/decision-tree-pattern-zh/) | `eval/decision-tree-ab/` |
| Prompt Engineering (overview) | [Read](https://wenbo97.github.io/prompt-context-patterns/2026/04/19/prompt-engineering-patterns/) | — | — |

## Run the A/B Tests Yourself

Requires [Claude Code CLI](https://claude.ai/code).

```bash
# Default: 5 runs per scenario, current model
bash eval/decision-tree-ab/run.sh

# Custom: 10 runs with haiku
bash eval/decision-tree-ab/run.sh 10 haiku
```

Three scenarios are tested:
- **Simple** — clear input, exact rule match
- **Ambiguous** — input doesn't match any rule exactly
- **Complex** — 10 overlapping rules with mixed signals

## License

MIT
