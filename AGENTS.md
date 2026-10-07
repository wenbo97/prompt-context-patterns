# Repository Guidelines

## Project Structure

This bilingual Jekyll reference keeps authoritative metadata in `_data/patterns.json` and authored English/Chinese bodies in `_patterns/<id>.<lang>.md`. `_posts/` contains historical articles; `_layouts/`, `_includes/`, and `assets/` own presentation. `scripts/catalog/` validates and generates indexes, browser data, README files, and compatibility routes. Research evidence and editorial decisions live in `docs/audit/`. Patternfoo's TypeScript CLI and tests are under `eval/patternfoo/`.

## Development and Verification

Use Node 20+ and Ruby 3.3 with Bundler. Run `npm ci` and `bundle install`, then:

- `npm run preview`: local site at `http://127.0.0.1:4000/prompt-context-patterns/`.
- `npm test`: Node unit/regression tests in `tests/*.test.mjs`.
- `npm run sources:restore`: recover and verify the ten frozen source repositories; override their adjacent `open-skills/` location with `SKILLS_ROOT`.
- `npm run check` and `npm run check:sources`: strict catalog, coverage, source identity, and locator checks.
- `npm run generate`, then `npm run check:generated`: regenerate derived files and verify deterministic output.
- `bundle exec ruby tests/liquid-literals.rb`: verify literal teaching examples survive Liquid rendering.
- `bundle exec jekyll build`, `npm run check:links`, and `npm run test:e2e`: build, check rendered routes/fragments, and exercise Playwright/Axe flows.
- `npm --prefix eval/patternfoo test` and `npm --prefix eval/patternfoo run build`: Vitest tests and TypeScript compilation.

## Content and Code Conventions

Match two-space indentation and existing JS/TS style; preserve CRLF text endings. Keep numeric IDs stable. Pair bilingual content and historical `YYYY-MM-DD-slug[-zh].md` posts. Examples compare the same task, identify independent teaching constructions, and separate editorial quality from measured efficacy. Preserve old routes and anchors. Edit generation inputs rather than generated outputs; regular generation preserves authored bodies.

When editing a pattern, read its metadata and both language bodies together. Allocate new IDs above the highest assigned ID and keep retired IDs reserved. Every active entry needs observable checks, limits and editorial review fields. Use `methodology/index.md` for admission criteria; source instances establish observed provenance, not earliest origin or measured efficacy.

When editing evaluation mappings, keep `case_id` as experiment identity and `pattern_ids` as explicit method links. Use one scoped configuration per case and retain failed model assertions as results. Model evaluation uses opt-in, user-configured providers; site checks make no paid model calls.

## Research and Design

Before rebuild work, read `docs/specs/2026-10-03-blog-rebuild.md` and `docs/agents/issue-tracker.md`. Review frozen source content as evidence; never execute source skills. Record actual review depth, reasons, hashes, and locators. Follow `DESIGN.md` and `UX-CONTRACT.md` for interface changes. If `.codegraph/` exists, consult CodeGraph before locating or reading code.

## Delivery

Use scoped imperative commits (`Add`, `Fix`, `Harden`) with the configured author identity. Document validation and meaningful limitations. This rebuild delivers locally; pushing, merging, or deployment requires an explicit request. Final independent review covers the complete rebuild from the documented cleaned baseline, including earlier checkpoints.
