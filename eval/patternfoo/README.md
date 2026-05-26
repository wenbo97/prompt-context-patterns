# patternfoo

A/B-test prompt patterns from the catalog using promptfoo + an Ink TUI.

## Run

```bash
cd eval/patternfoo
npm install
npm start
```

Configure provider + API endpoint on first run; saved to `~/.patternfoo/config.json`.

## Add a pattern

Create a directory under `patterns/NNN-slug/` with:
- `meta.yaml` (id, name, category, hypothesis, status: ready|todo)
- `prompt-a.md` (baseline) and `prompt-b.md` (with pattern)
- `scenarios.yaml` (promptfoo `tests:` block)
- `rubric.md` (llm-rubric grading)

The TUI auto-discovers it on next launch.

## Reset

If a promptfoo upgrade leaves a SQLite schema mismatch (errors like "no such column" on eval), delete the local promptfoo database:

```bash
rm ~/.promptfoo/promptfoo.db
```

It will be recreated on the next eval run.
