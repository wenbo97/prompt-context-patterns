# Topic card link regression — 2026-10-05

The user reported that the highlighted P6/P25 cards on `/topics/prompt-zh/` did not open. Browser inspection reproduced a narrower symptom: Chinese title anchors navigated correctly, while English labels and blank card space did nothing. The prior reading revision also styled linked titles as plain black text without an underline, obscuring the action.

The shared card now extends its native title anchor over the card via a scoped CSS hit area. Category anchors remain independent above that area. Card titles again use the canonical blue link color and underline. No JavaScript click handler or nested anchor is introduced.

Verification:

- New topic-card Playwright test failed before the fix on English-name navigation (URL remained the topic page).
- `npx playwright test --grep 'topic card|reading surfaces|search, facets'`: 6 passed after the fix. Exercises P6/P25 title, English label, blank area, keyboard, category navigation, mobile/no-JavaScript clicks, search/Back and Axe/reflow at 375/768/1280px. Topic page added to the existing accessibility matrix.
- Pixel-click probe confirmed all three targets navigate for both reported cards; desktop screenshot inspected at `.tools/screens/topic-links-1280.png`.
- `bundle exec jekyll build`: succeeded.
- `npm run check:links`: 876 pages / 18,265 links, zero errors.
- Premium strict audit: zero findings; see `topic-card-static.json`.
- `git diff --check`: clean.

Verification uses the locally served site in Playwright Chromium, not the user's browser profile/extensions. Local delivery only; no push or deployment. Earlier full content verification remains documented in `reading-ux.md`.
