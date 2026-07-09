# Catalog Browser + Blog Info Refresh — Design (2026-07-08)

> Status: **DRAFT for review.** Produced by concluding a `/grilling` session on recommended defaults (Push-Right: one decision-ready brief instead of a 10-question walk). Every "Decision" below is a *recommendation* — reversible on the user's say-so. Open decisions that genuinely need the user are collected in §9.

## 0. Scope (settled)

- **This round = an interactive catalog browser**: full-text search + filter by category / source / confidence + category navigation, with **solid EN↔ZH mapping**. *(User picked (a) in grilling Q1.)*
- Visual theme + home page = **light-touch** only, in service of surfacing the browser. No full redesign.
- Blog **info update** rides along: reflect the new pattern count + 4th source (mattpocock) + a harvest announcement.

## 1. Data model — `_data/patterns.yml` as single source of truth  *(grilling Q2 → A)*

One record per pattern, both languages in one record (this is what makes EN↔ZH structural instead of two hand-synced files):

```yaml
- id: 156
  slug: no-pre-judging-reviewer-dispatch
  name_en: "No-Pre-Judging Reviewer Dispatch"
  name_zh: "不预判的评审派发"
  category: advanced-quality        # controlled vocab, see §1.1
  source: superpowers               # 500plus | superpowers | claude-plugins-official | mattpocock | claude-code
  confidence: high                  # high | medium | low  (only for 156+ harvest; 1–155 omit)
  problem_en: "One-line problem it solves."
  problem_zh: "一句话问题。"
  tags: [review, anti-gaming, orchestration]
  detail_en: /catalog/categories/patterns-advanced-quality#pattern-156
  detail_zh: /catalog/categories/patterns-advanced-quality-zh#pattern-156
```

- **Metadata only.** Long-form write-ups (GOOD/BAD, snippets) stay in the existing category `.md` files; each record links to its detail anchor. No mass prose migration.
- `patterns.yml` feeds **both**: (a) the browser (rendered to JSON, see §2) and (b) a Liquid-generated index table — so table and browser can never drift.

### 1.1 Controlled category vocabulary
Reuse the 16 existing catalog categories as the canonical `category` enum (structural-scaffolding, input-output-contracts, execution-control, knowledge-and-context, agent-orchestration, safety-and-trust, quality-and-feedback, advanced-io-domain, advanced-orchestration, advanced-quality, advanced-safety, advanced-workflow, gap-fills, open-source-skills, karpathy-behavioral, claude-code-platform). The harvest adds enough authoring-theory patterns (mattpocock) that a **new category `skill-authoring`** is likely warranted — flagged in §9.

## 2. Tech — pure-Jekyll + vanilla JS, no build step  *(GitHub Pages constraint)*

GitHub Pages runs only whitelisted Jekyll plugins and **cannot run an npm build**. So:

- A Jekyll page `catalog/patterns.json` (Liquid loop over `site.data.patterns`) emits the whole dataset as JSON at build time.
- `assets/catalog.js` (plain ES, no framework) fetches that JSON and does client-side search + filter. ~200 records is trivially fast in-browser; no server, no index pre-build.
- **Fuzzy search:** Fuse.js via CDN `<script>` (no build, ~6 KB gz) — recommended over exact substring so "reviewr"/"dispatch review" still hit. *(Alt: hand-rolled substring match, zero deps — §9.)*
- Graceful degradation: the Liquid-generated static table (§1) remains as the `<noscript>` / no-JS fallback and for SEO.

## 3. Browser UI (`/catalog/browse`)

```
┌─────────────────────────────────────────────┐
│  [ 🔍 search…            ]   EN | 中文  ⇄     │
│  Category ▾  Source ▾  Confidence ▾   (chips) │
├─────────────────────────────────────────────┤
│  #156  No-Pre-Judging Reviewer Dispatch      │
│        advanced-quality · superpowers · high │
│        One-line problem…            [详情 →] │
│  #157  …                                     │
└─────────────────────────────────────────────┘
   205 patterns · 47 shown
```

- Search matches `name`+`problem`+`tags` in the **active language**.
- Filters are multi-select chips; counts update live.
- **EN/中文 toggle** flips every card's language via the record's `_en`/`_zh` fields and rewrites detail links to the matching-language anchor — one control, whole page. Persisted in `localStorage`.
- Card → detail link jumps to the anchored write-up in the correct-language category page.

## 4. EN↔ZH mapping (the user's explicit priority)

- Structural: one record, two language fields → no parallel-file drift for **metadata**.
- Detail pages stay bilingual as today (`-zh` siblings), but each record stores **both** `detail_en` and `detail_zh`, so the toggle always resolves the right side.
- Migration fills ZH metadata for 1–155 from the existing `catalog-index-zh.md`; the ~50 new harvest patterns need ZH names/problems written (small, one-time).

## 5. Migration (the body of work)

1. **Script** `eval/tools/build-patterns-yml.mjs` (Node, local-only, gitignored): parse `catalog/catalog-index.md` + `catalog-index-zh.md` table rows → emit `_data/patterns.yml` for ids 1–155 (name_en/zh, category, detail links). Semi-automatic; hand-fix stragglers.
2. Append the admitted harvest patterns (156+) from `candidates.md` + `candidates-mattpocock.md` with their source/confidence/problem — the candidate files already carry EN name+problem+source; ZH gets written here.
3. Regenerate the index tables from `patterns.yml` (Liquid) so old tables match the new source of truth.

## 6. Blog info update (goal 2)

- **Count bump** everywhere the total appears — but only **after** §9 decides how many candidates are admitted (final count = 155 + admitted). Touch: `index.md` home, `catalog/index.md`, `catalog/catalog-index(.md/-zh)` intro, `README.md`, and a note in the catalog post.
- **New source** everywhere sources are listed: add `mattpocock/skills` (and it being the 4th source) to the intro paragraphs.
- **New announcement post** `_posts/2026-07-08-harvest-2026-07-*.md` (EN+ZH): "N new patterns from superpowers, claude-plugins-official, mattpocock/skills" — mirrors the 2026-05 harvest post style, links to the browser.

## 7. Home / visual (light touch)

- Home hero gains a prominent **"Browse N patterns →"** button pointing at `/catalog/browse` (currently home only lists 3 posts + a one-line catalog link).
- Keep the warm-gray serif theme. Add only the CSS needed for the browser controls/cards, matching existing tokens (`$brand-color`, `$surface-color`, etc.).

## 8. Phasing (suggested execution order, once approved)

1. Migration script → `_data/patterns.yml` for 1–155 (verify count = 155).
2. Decide admitted harvest set (§9) → append 156+.
3. `patterns.json` emitter + `catalog.js` + browser page + CSS.
4. Regenerate index tables from data; wire home button + nav.
5. Info bumps + announcement post.
6. Author full write-ups for admitted new patterns into category md files *(could be deferred — §9)*.

## 9. Open decisions that genuinely need the user

1. **How many candidates to admit?** ~50 harvested (33 in `candidates.md` + 17 strong in `candidates-mattpocock.md`). Options: (a) admit all high-confidence only (~30), (b) admit high+medium (~50), (c) I pre-curate a recommended set and you approve. → *Recommend (c).* This sets the final count for §6.
2. **New category `skill-authoring`?** The mattpocock haul (Leading Word, No-Op Test, Invocation Economics, Sequence Cut…) is a coherent new cluster. → *Recommend yes.*
3. **Author full write-ups this round, or defer?** Browser + metadata can ship with detail links pointing at a stub; full GOOD/BAD write-ups for 50 patterns is a large bilingual writing job. → *Recommend defer write-ups to a follow-up round; ship the browser + metadata + announcement now.*
4. **Fuzzy search lib?** Fuse.js CDN (recommended) vs zero-dep substring.
5. **Browser URL:** `/catalog/browse` (recommended) vs making it the catalog landing `/catalog/` with the tables moving to `/catalog/index`.
```
