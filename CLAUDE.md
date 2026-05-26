# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Jekyll blog published to GitHub Pages at `https://wenbo97.github.io/prompt-context-patterns/`. Content covers prompt engineering patterns, context engineering, and agent orchestration — all bilingual (EN + ZH).

## Build & Preview

```bash
bundle install              # first time only
bundle exec jekyll serve    # local preview at http://localhost:4000/prompt-context-patterns/
```

GitHub Pages builds automatically on push to `master`.

## Blog Posts

- All posts go in `_posts/` with format `YYYY-MM-DD-slug.md`
- Chinese versions use `-zh` suffix: `YYYY-MM-DD-slug-zh.md`
- Front matter must include `layout: post`, `title`, `date`, `categories`
- Chinese posts add `lang: zh`

## A/B Testing (eval/)

Tests compare prose-style vs decision-tree prompts using `claude -p`:

```bash
bash eval/decision-tree-ab/run.sh 20           # 20 runs, default model
bash eval/decision-tree-ab/run.sh 10 haiku      # 10 runs, haiku
python3 eval/decision-tree-ab/analyze.py        # parse results
```

Prompt files follow naming: `prompt-{prose|tree}[-variant].md`. Results are saved to `eval/decision-tree-ab/results/` (gitignored — local only).

## Conventions

- All text files use CRLF line endings (enforced via `.gitattributes`)
- Blog content: simple vocabulary in both EN and ZH, concise, scannable
- Pattern posts should include reproducible data (A/B test results, not just theory)
- `eval/decision-tree-ab/results/` is gitignored — test outputs stay local
- `_config.yml` excludes `eval/`, `media/` from the Jekyll build
