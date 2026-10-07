# Reading experience revision — 2026-10-05

## Request and result

Address the reported oversized search cards, unclear detail hierarchy, missing version/category links and literal Chinese wording. Search uses compact single-column rows, a nonwrapping clear action and an optional repository-filter disclosure. Details and historical posts share a centered 780px reading measure. The complete index has explicit column widths that keep category and source status readable on mobile.

Version links open the source file at the stored immutable commit and line range. Categories link to their localized topic pages from the complete index, search rows, shared cards and detail headings. The source overview links its version hash to the frozen repository tree.

All 306 active Chinese titles and summaries were rewritten against their English meaning. Their English originals are visible in Chinese discovery and detail views. All 306 Chinese bodies received clearer section labels and common terminology cleanup. Key explanatory sections of P1, P2, P8, P23, P27, P100 and P240 were rewritten individually. This is not a claim that every body paragraph or historical article received a full literary rewrite. Executable ASCII identifiers, English content, IDs, provenance and editorial scores were preserved. Archived harvest decisions remain historical evidence; current catalog metadata and authored bodies are the editing sources. Regular generation preserves those bodies; the one-time rebuild integrator is not a content-editing command.

## Verification

- `npm test`: 19 passed.
- `bundle exec ruby tests/liquid-literals.rb`: 5 literal-render roundtrips passed.
- `bundle exec jekyll build`: succeeded.
- `npm run check:generated`: zero differences.
- `node scripts/catalog/check.mjs --sources`: 390 identities, 306 active, 334 evidence files; zero errors.
- `npm run check:links`: 876 pages, 18,265 local links/fragments; zero errors.
- `npm run test:e2e`: 10 passed, including category/version targets, repository disclosure, search/Back, error/retry, IME, no-JavaScript fallback, keyboard and Axe checks at 375/768/1280px.
- Rendered contract inspection: 1,106 immutable file-version links and 612 detail category links matched metadata; all metadata outside the two Chinese copy fields was unchanged. See `reading-ux-contracts.json`.
- Premium strict project audit: zero findings. See `reading-ux-static.json`.
- Desktop/mobile search, detail and complete-index screenshots inspected at 1280/375px; no horizontal overflow. Screenshots are local under `.tools/screens/reading-*.png`.
- `git diff --check`: clean.

The 200% check emulates a 640 CSS-pixel viewport; it does not exercise browser chrome zoom. Source targets were verified against stored metadata and frozen local Git blobs, without claiming live GitHub availability or device testing. No push or deployment. Original checkout retains master `eed1503a8081030077a7d1224d0e24a50681ff6d` and its pre-existing untracked `.tools/` and `AGENTS.md`.
