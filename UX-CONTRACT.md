# Pattern Reference Interaction Contract

## Canonical owners

The shared header owns navigation and locale links. The catalog browser owns search, filters, load-more and browser-history state. Shared card and provenance markup own labels across the homepage, themes and search results. Global SCSS owns focus and scrollbars. Use semantic links, buttons, search input and checkbox-like toggle buttons; no authored select, modal, toast or CRUD flow is needed.

| Capability | Canonical owner | Source of truth | Allowed variants | Verification |
| --- | --- | --- | --- | --- |
| Scrollbar | assets/main.scss global document baseline | DESIGN.md | forced colors use system colors | tests/e2e/site.spec.mjs computed styles and reflow |

Business scope: [approved rebuild specification](docs/specs/2026-10-03-blog-rebuild.md). This reference has no account, billing, mutation, permission or deletion flow. Pattern withdrawal is an editorial build-time operation.

## Catalog state

URL parameters: q, category (repeated), repo (repeated), trace (repeated), lang (en or zh), limit (multiples of 30). OR within a facet, AND across facets. Default ordering is numeric ID; non-empty search uses relevance with ID as tie-breaker. Search examines both languages. Changing query/filters resets limit to 30. Load more raises it by 30. Back restores query, facets, language and loaded count. Language changes preserve the other state. Local storage remembers language only and is optional.

Search waits for compositionend when using an IME. Clear is immediate. Failed data load has a retry button and a static-index link. Empty catalog and no matches have different localized messages. Counts use a polite status region. Keyboard focus remains on the action used; loading more does not reset focus or jump the page.

## Detail and migration

Detail pages expose the use case before examples, identify teaching constructions and link pinned evidence. English/Chinese pages represent the same method and retain the pattern identity. Retired entry points resolve to the active merge target or a short withdrawal explanation. Compatibility pages keep anchors and usable links without JavaScript and are excluded from current discovery and sitemap.

## Verification

Exercise clear, facet combinations, language switch, load-more, Back, empty results, data error/retry, no JavaScript, keyboard and Chinese composition at 375, 768 and 1280px. Verify source labels, href destinations, long examples, focus, 200% zoom and reduced motion.
