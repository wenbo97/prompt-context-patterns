# Prompt and Context Engineering Reference

Reusable methods extracted from real agent skills. Every active pattern has a concise description, concrete use case, same-task bad/good examples, observable expectations, limits and provenance.

Current directory: **306** active methods, **272** with located source instances, **34** labelled Source unconfirmed. Merged and withdrawn identities remain reachable and are not counted as active.

[中文](README-zh.md)

## Local preview

Requires Node20+, Ruby3.3 and Bundler.

```bash
npm ci
bundle install
npm run generate
bundle exec jekyll serve --host 127.0.0.1 --port 4000
```

The isolated Windows copy can use `scripts/preview.ps1` with its local Ruby installation. Preview: http://127.0.0.1:4000/prompt-context-patterns/ .

## Content and evidence

- [_data/patterns.json](_data/patterns.json): authoritative metadata and editorial dispositions.
- [_patterns/](_patterns/): independent bilingual bodies.
- [Editorial criteria](methodology/index.md): usefulness and provenance are separate.
- [Legacy audit](docs/audit/legacy-review.md): retention, merge and withdrawal reasons.
- [Source research](docs/research/open-source-skills-top10.md): repositories and frozen revisions.

Pinned commit links establish observed instances, not earliest invention. Teaching examples are independently constructed, not measured model outputs. Historical articles retain dates and fixtures; unsupported numbers without raw outputs are corrected.

## Verification and maintenance

Sources default to the adjacent `open-skills/<owner>/<repo>` directory; override with `SKILLS_ROOT`. Restoration fetches only frozen commits. Existing directories must pass verification and are never reset.

```bash
npm run sources:restore
npm test
npm run check
npm run check:sources
npm run check:generated
bundle exec ruby tests/liquid-literals.rb
bundle exec jekyll build
npm run check:links
npm run check:site
npm run check:dates
npm run test:e2e
npm --prefix eval/patternfoo ci --legacy-peer-deps --omit=peer
npm --prefix eval/patternfoo test
npm --prefix eval/patternfoo run build
```

Build checks do not call models. Real A/B evaluations run explicitly through [Patternfoo](eval/patternfoo/README.md). Legacy runners retain historical fixtures; missing raw outputs are not represented as revalidated results. Text files use CRLF.

Authored last_modified_at records the actual content update date (Asia/Shanghai, YYYY-MM-DD). Update it with relevant title, summary or body changes; generation and builds never refresh it automatically. Ordinary descriptions belong to authored front matter or generator inputs.

## License

This project uses MIT. Referenced files retain their own licensing scope; citations do not assign one license to an entire source corpus.
