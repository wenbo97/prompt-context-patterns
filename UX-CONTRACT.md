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

The browser maintains loading, ready and error states independently of language. Switching language or restoring browser history updates the current loading/error message, retry action and static fallback together. Retrying enters loading in the current language; a successful response retains the committed query, facets and limit.

## Detail and migration

Detail pages expose the use case before examples, identify teaching constructions and link pinned evidence. The version hash links to the source file at the recorded immutable commit and line range. Category labels in mixed lists, details and the complete index link to their localized topic pages; current-topic card labels are inert tags. Shared grid cards expand the native title link across the English name, summary and blank space; category links stay independent above that hit area. Keyboard and no-JavaScript navigation use the same native anchor. Chinese titles include their English originals. Chinese explanations use concrete actions; executable names and source metadata remain literal. Repository filters may collapse in a native details element; category and provenance filters remain visible. English/Chinese pages represent the same method and retain the pattern identity. Retired entry points resolve to the active merge target or a short withdrawal explanation. Compatibility pages keep anchors and usable links without JavaScript and are excluded from current discovery and sitemap.

## Reference navigation and examples

Category labels on the current topic's cards are non-interactive tags. They do not enter the tab order or activate the card's detail link. Homepage and search cards, detail headings and the complete index retain localized category links. All other card hit areas preserve native detail navigation.

Index titles and source-repository titles have continuous link boxes across wrapped lines. Guide reference links use inline blocks that include line gaps without making their enclosing paragraph clickable. Pointer activation, keyboard Enter and no-JavaScript navigation use the same native href.

Cross-origin HTTP/HTTPS reference anchors open with `target="_blank"` and `rel="noopener noreferrer"`, including sources, pinned versions, the footer and authored reference links. Internal routes stay in the reading tab. Authored Markdown links use `{:target="_blank" rel="noopener noreferrer"}`; templates output the attributes directly. This behavior does not depend on JavaScript. Source label formatting is presentation only: raw metadata, pinned revisions, paths and line locators are preserved.

Pattern examples use explicit bad/good Markdown block attributes and red/green border tokens, while their textual headings communicate the meaning without color. Pattern and historical heading anchors remain stable.

## Verification

Exercise clear, facet combinations, language switch, load-more, Back, empty results, data error/retry, no JavaScript, keyboard and Chinese composition at 375, 768 and 1280px. Verify source labels, href destinations, long examples, focus, 200% zoom and reduced motion.

## On-page reading navigation

The shared pattern layout owns a localized native nav after the summary. Its seven links reuse the existing section anchors in authored order. It stays in normal document flow, wraps at narrow widths, and works with pointer, keyboard and no JavaScript. No additional sidebar or scroll-state script is required.

Wrapped native links use the global anchor box baseline so pointer activation includes line gaps. Existing brand, button and index owners keep their maintained display variants. Validate a wrapped blog title, category label, migration label and article locale link by center-point activation, plus full-site geometry and native-link traversal.
