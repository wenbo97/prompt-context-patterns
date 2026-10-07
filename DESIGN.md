# Pattern Reference Design

## Purpose

A bilingual engineering reference for finding a method, understanding its use case and checking its evidence. The homepage is editorial; the browser is a read-only product surface; pattern pages prioritize focused reading.

## Visual direction

Use a simple white engineering handbook. Avoid oversized headings, repeated card borders and abstract Chinese labels. Chinese titles show their English originals; immutable source versions and categories are actionable links. The signature is a visible before/after comparison spine: the same task, a weak instruction, the improved instruction and the observable difference.

## Canonical tokens

Runtime ownership: shared SCSS tokens in assets/main.scss. This document mirrors accepted values; components consume the shared tokens.

| Role | Value |
| --- | --- |
| Canvas | #FFFFFF |
| Surface | #FFFFFF |
| Text | #0F172A |
| Secondary text | #475569 |
| Link and focus | #1D4ED8 |
| Border | #CBD5E1 |
| Bad example marker | #B91C1C |
| Good example marker | #15803D |

Body: Inter, Noto Sans SC, system-ui, sans-serif. Code: JetBrains Mono, ui-monospace, monospace. Body size 16px, line height 1.8. A light theme only. Code and bilingual long text wrap without hiding content.

Cloudflare production sets `external_fonts: false` in its deployment override. The shared layout omits Google Fonts requests and the same SCSS font stacks use fonts installed on the device, falling back to system-ui and ui-monospace. This deployment variant reduces external dependencies for mainland and overseas readers; it does not change colors, type sizes, layout or interaction ownership.

The shared pattern, historical-article and prose reading owners use overflow-wrap: anywhere so unbroken technical identifiers and reference paths remain visible inside the column. Ordinary words keep their natural wrapping; this rule does not clip or hide overflow.

## Layout and states

Desktop: a 1180px site shell; detail pages use a centered 780px reading column without a sidebar. Search results use compact single-column rows. Source-repository filters use a native disclosure; categories and source status stay visible. Pattern paragraphs cap at approximately 78 characters; comparison examples can use the full main column. Historical posts use the same centered reading measure. The complete index keeps explicit ID/title/category/status column widths to avoid vertical Chinese wrapping. Below 768px use one column and natural document scrolling. Mobile bad/good examples stack in that order.

Card titles use the link color and an underline so their action remains visible. Shared grid cards extend the detail hit area across the card while preserving the category link. On the current topic page, the matching category is a neutral, non-interactive tag above that hit area; mixed lists retain category links.

Bad and good examples remain Markdown code blocks with red and green left borders respectively, plus explicit headings. Authors mark blocks with `{: .example--bad}` or `{: .example--good}` after the closing fence. These attributes work with both plain and highlighted code and do not depend on the block immediately following a heading. Shared SCSS owns both semantic colors; code text and syntax highlighting retain their existing colors.

Pattern numbers communicate stable identity, not rank or evidence strength. Provenance badges use words and borders rather than color alone. Loading, empty, no-results and error states reserve space and provide a useful next action. Visible focus, WCAG 2.2 AA contrast, 200% zoom and reduced-motion support are required.

Detail pages have a non-sticky on-page navigation after the summary, linking to the seven existing sections. It stays inside the reading column, wraps naturally, uses shared link/focus colors, and remains usable without JavaScript.

Native anchors share a continuous inline-block baseline with a 100% maximum width and top alignment. Shared brand/button/index primitives retain their existing flex/block variants. Wrapped label gaps belong to the link box; surrounding prose keeps its own reading flow.

The homepage teaching comparison uses the same explicit bad/good roles and shared red/green tokens on its prefix labels and left markers. The use-case row stays neutral; all three rows align.

The bilingual homepage uses two explicit headline lines naming the reference and its instructional content. Both desktop hero columns align at the top; below 768px they stack naturally. Chinese copy identifies the content directly rather than translating an imperative slogan. Homepage titles and descriptions follow the visible copy.
