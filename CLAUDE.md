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

## Pattern Browser & Data Pipeline (catalog/browse)

The interactive browser (`catalog/browse.md` + `assets/catalog.js` + vendored `assets/fuse.min.js`) reads `assets/patterns.json` — the committed, pre-built data for all 206 patterns. GitHub Pages runs no Node build, so the JSON **must be committed**.

Regenerate the data with the Node 18+ tools in `eval/tools/` (no deps):

```bash
node eval/tools/build-patterns.mjs   # parses catalog-index (1–155) + merges harvest (156–206)
                                     #   -> _data/patterns.json + assets/patterns.json
```

**Rebuild ordering matters** — the 156–206 detail links point at real kramdown anchors on the static list pages, so if harvest names change, run the full pass:

```bash
bundle exec jekyll build                  # 1. render static pages so <h2 id> anchors exist
node eval/tools/wire-harvest-detail.mjs   # 2. extract real anchors -> patterns-harvest.json
node eval/tools/build-patterns.mjs        # 3. rebuild patterns.json WITH detail links
bundle exec jekyll build                  # 4. ship updated JSON
node eval/tools/to-crlf.mjs               # 5. normalize generated files to CRLF before commit
```

Sources of truth: `eval/tools/patterns-harvest.json` (156–206 metadata) + `eval/tools/names-zh.json` (Chinese names for 1–155). Link-integrity helpers: `scan-lang-links.mjs` (must report 0), `fix-related-links.mjs`, `fix-lang-links.mjs`.

## Conventions

- All text files use CRLF line endings (enforced via `.gitattributes`)
- Blog content: simple vocabulary in both EN and ZH, concise, scannable
- Pattern posts should include reproducible data (A/B test results, not just theory)
- `eval/decision-tree-ab/results/` is gitignored — test outputs stay local
- `_config.yml` excludes `eval/`, `media/` from the Jekyll build
