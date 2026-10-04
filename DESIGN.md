# Pattern Reference Design

## Purpose

A bilingual engineering reference for finding a method, understanding its use case and checking its evidence. The homepage is editorial; the browser is a read-only product surface; pattern pages prioritize focused reading.

## Visual direction

Use a cold-white engineering handbook, not the previous warm serif theme. The signature is a visible before/after comparison spine: the same task, a weak instruction, the improved instruction and the observable difference.

## Canonical tokens

Runtime ownership: shared SCSS tokens in assets/main.scss. This document mirrors accepted values; components consume the shared tokens.

| Role | Value |
| --- | --- |
| Canvas | #F8FAFC |
| Surface | #FFFFFF |
| Text | #0F172A |
| Secondary text | #475569 |
| Link and focus | #1D4ED8 |
| Border | #CBD5E1 |

Body: Inter, Noto Sans SC, system-ui, sans-serif. Code: JetBrains Mono, ui-monospace, monospace. Body size 17px, line height 1.7. A light theme only. Code and bilingual long text wrap without hiding content.

## Layout and states

Desktop: a 1180px reading shell with theme navigation and the main reading column. Pattern paragraphs cap at approximately 78 characters; comparison examples can use the full main column. Below 768px use one column and natural document scrolling. Mobile bad/good examples stack in that order.

Pattern numbers communicate stable identity, not rank or evidence strength. Provenance badges use words and borders rather than color alone. Loading, empty, no-results and error states reserve space and provide a useful next action. Visible focus, WCAG 2.2 AA contrast, 200% zoom and reduced-motion support are required.
