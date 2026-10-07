# Blog interface repairs and content revision

Approved on 2026-10-05; revised by the user-approved continuation plan on 2026-10-06. Work in the isolated `rebuild/skills-catalog` checkout, starting from `313ac65413ea7cbf4d82a8a583d8eb5c4b235ac7`. Preserve local work and source evidence. No commit, push, merge or deployment is requested.

## Audience and delivery

Readers know basic AI/development concepts and want an actionable method, not just a reference card. Rewrite Chinese naturally and expand English and Chinese to the same instructional depth. Cover site labels, themes, search states, guides, methodology and all 306 active patterns. Historical post prose and experiments remain unchanged; external-link behavior applies to their rendered references too.

Complete the Chrome technical audit, interface improvements and six bilingual pilots before one combined user review. The agent owns technical QA; the user reviews visual quality, Chinese expression and instructional depth. Do not begin the other 300 patterns until the combined checkpoint is accepted. Then proceed in ten batches with progress reports and no approval per batch.

## Phase 1: interface and interaction

- UI-001: use pattern metadata only when the page has a pattern ID. Ordinary titles, descriptions and Open Graph metadata must not inherit P1. Search initial HTML and runtime titles both need validation.
- UI-002: continuous native hit areas for wrapped complete-index titles, source-repository titles and standalone guide/reference links. Keep keyboard and no-JavaScript navigation.
- Category behavior: matching categories on the current topic's cards are inert tags, shielded from stretched detail links. Mixed lists, detail headings and the complete index retain localized topic links.
- External HTTP/HTTPS references open a new tab through native `target="_blank"` and `rel="noopener noreferrer"`. Internal navigation stays in the reading tab. Use rendered template attributes or Markdown link attributes, without relying on JavaScript.
- Examples remain fenced Markdown. Bad borders use `#B91C1C`, good borders use `#15803D`; explicit headings, existing code background and syntax highlighting remain. Block attributes identify the role independently of heading adjacency.
- UI-003: remove Markdown formatting from displayed source section labels, preserve literal names and raw evidence metadata. P14/P25 are active; P112 is already merged into P25 and must retain its bilingual transition route.
- Update shared design and interaction contracts, add genuine browser regression checks, and provide preview routes and responsive screenshots.

## Phase 2: editorial standards and pilots

Rewrite P1, P8, P23, P224, P323 and P387 in both languages. Preserve the existing seven section headings and anchors:

1. Use case: task, prerequisites and the problem.
2. Mechanism: executable steps, inputs, decisions and outputs; a short paragraph is acceptable for a simple method.
3. Bad example: a complete failing instruction for that task, with a concrete defect.
4. Good example: a complete usable alternative for the same task, explaining placeholders.
5. Why the change matters: the causal connection between the change and the defect.
6. Observable expectation: a check, expected outcome and failure conditions.
7. Limits: prerequisites, costs or unsuitable situations; relevant method links where supported.

Prefer concrete Chinese actions and short sentences. Explain necessary terms when introduced; preserve executable names, metadata keys, paths and calls. Update pattern title, summary and scenario metadata when needed. Do not impose a word minimum, pad simple methods or compress complex steps into one sentence.

New examples are independent teaching constructions, not measurements or upstream quotations. Verify the method against already frozen evidence without expanding upstream research. Deliver six bilingual previews, before/after Chinese comparisons and an authoring standard for user acceptance.

## Phase 3: full revision

First unify global Chinese labels, explanations and terminology. Revise the remaining 300 patterns in ten batches of 30, following the existing category order and ascending ID within each category. Each batch includes bilingual bodies and corresponding metadata; review every method for clarity, factual mechanism, same-task contrasts and testable results.

Edit authoritative metadata and authored bodies, and edit generation inputs rather than generated outputs. Regenerate derived indexes/search data after metadata changes. Preserve IDs, URLs, anchors, provenance and CRLF. Record completed IDs, previews, validation and unresolved items per batch. Surface proposed mechanism/provenance/merge changes separately from prose revision.

## Phase 4: final verification

Run catalog/source checks, deterministic generation checks, Liquid literal checks, unit tests, Jekyll build, rendered links/legacy anchors, Playwright/Axe, Patternfoo tests/build and the frontend static audit. Validate 375/768/1280px, keyboard, no JavaScript, language/history/search states and 200% reflow; distinguish emulated reflow from actual browser zoom.

Confirm all bilingual active content is covered. Deliver the coverage ledger, preview routes, actual verification results and remaining limitations. Do not claim all upstream links were visited or that editorial improvements establish measured model efficacy.

## Continuation requirements approved on 2026-10-06

Inventory the actual built site and its rendered elements. Visit every HTML route in real Chrome at 375/768/1280px, retain and review each screenshot, and activate every link instance to verify destination identity, language and fragments. Record runtime search/filter/load-more/history states and honest keyboard/no-JavaScript/IME/200% evidence. Response mocks prove only the behavior under test; external accessibility needs real responses. Keep resumable per-page/element evidence and report restricted or untested items.

Add localized native on-page navigation to the seven stable detail anchors without changing the reading-column visual direction. Supply minimum teaching inputs and illustrative outputs in all six pilots.

Validate sitemap coverage against indexable built routes, canonical URLs, reciprocal hreflang and robots. Check all 57 legacy pages, eight historical post routes and 206 bilingual legacy pattern mappings. Preserve readable migration links and anchors without JavaScript; report client-side redirects honestly. Preserve Google/Bing properties and public verification files; perform redacted credential checks of project configuration, reachable Git history and publication artifacts. Exclude local audit reports from the deployed artifact.

After explicitly authorized release, verify production pages, compatibility entries, robots, sitemap and verification files before checking/updating existing sitemap submissions in Google/Bing. Record submission, crawl and indexing separately. The unchanged domain/baseurl uses path migration, not Change of Address. No automatic schedule or immediate indexing promise.
