# Working on Pattern Reference

The authoritative directory is `_data/patterns.json`; authored English/Chinese bodies are `_patterns/<id>.<lang>.md`. When changing a pattern, read its metadata and both bodies together. When judging provenance, inspect the pinned source and distinguish an observed instance from earliest origin.

## Content edits

Preserve stable IDs. Allocate new IDs above the highest assigned value and keep retired IDs reserved. Every active entry needs a concrete use case, same-task bad/good teaching constructions, observable expectations, limits and editorial review fields. Read `methodology/index.md` for admission criteria; a source link is not an efficacy experiment.

When changing source analysis or adding methods, read `docs/specs/2026-10-03-blog-rebuild.md` and the relevant `docs/audit/harvest-*.json` record. Keep source repositories read-only. Inventory or family screening alone is not full semantic review.

## Generation and verification

Use root package.json for current commands. Generated browser assets, source/theme counts and compatibility pages come from canonical metadata; do not edit them independently. Regular generation preserves authored bodies. The integration script is an editorial migration tool, not the normal build step.

When changing presentation, read DESIGN.md and UX-CONTRACT.md before shared tokens or navigation. Verify Chinese composition, error/retry, Back, no-JavaScript fallback and narrow layouts in the real browser. When changing routes, run the built-site href and legacy-fragment checker.

When changing evaluation mappings, preserve case_id as experiment identity and pattern_ids as explicit method links. One case gets one scoped config; a failed model assertion remains a result. Model evaluation is opt-in with user-configured providers; site checks do not run paid calls.

## Local conventions

Text files use CRLF. Historical posts retain dates and fixtures; label missing raw outputs instead of inventing current numbers. Preserve real authors and source licenses. New commits omit AI coauthor trailers. Local changes are not automatically pushed or published.
