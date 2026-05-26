# Patternfoo — Pattern A/B Eval TUI

**Date:** 2026-05-26
**Status:** Approved (brainstorming → design phase complete)
**Successor to:** `eval/decision-tree-ab/` (legacy, retained read-only)

---

## 1. Goal

Replace the ad-hoc `eval/decision-tree-ab/` shell scripts with a reusable A/B testing tool for prompt-engineering patterns in this catalog. Built on **promptfoo** (matrix runner + `llm-rubric` grading + web report) with a thin **Ink** TUI for pattern selection and configuration.

- Show all 155 catalog patterns; only Top 10 are runnable in MVP (others tagged `[TODO]`)
- Pattern authoring = drop a directory under `patterns/`, no code change
- Provider is configurable: defaults to `anthropic:messages:claude-opus-4-7` against a local endpoint (mirrors `blog-cc-dev.cmd`), but any promptfoo-native provider ID works

---

## 2. Directory Layout

```
eval/patternfoo/
├── README.md
├── package.json                        # ink, ink-select-input, promptfoo (peer)
├── src/
│   ├── cli.tsx                         # Ink entry
│   ├── screens/
│   │   ├── PatternList.tsx             # (a) pick patterns
│   │   ├── Config.tsx                  # (b) provider / model / N / apiBaseUrl
│   │   └── RunAndSummary.tsx           # (c)+(e) live progress, then summary
│   ├── catalog.ts                      # 155 pattern meta (id, name, status)
│   └── configGen.ts                    # emit promptfooconfig.yaml
├── patterns/
│   ├── 006-negative-constraints/
│   ├── 008-decision-tree/              # migrated from decision-tree-ab
│   ├── 017-schema-lock/
│   ├── 100-progressive-disclosure/
│   ├── 103-reconnaissance/
│   ├── 145-iron-law/
│   ├── 146-rationalization-table/
│   ├── 148-anti-performative/
│   ├── 151-hard-gate/
│   └── 152-dot-graph/
└── results/                            # gitignored, promptfoo outputs
```

Each `patterns/NNN-slug/` directory:

- `meta.yaml` — `id`, `name`, `category`, `hypothesis`, `status: ready|todo`
- `prompt-a.md` — baseline (no pattern)
- `prompt-b.md` — same task, with the pattern applied
- `scenarios.yaml` — promptfoo `tests:` block (input matrix)
- `rubric.md` — `llm-rubric` grading criteria

Adding a new pattern = add a directory. The TUI auto-discovers via `fs.readdirSync('patterns')`.

---

## 3. Top 10 Patterns (MVP)

| # | Pattern | Category |
|---|---------|----------|
| 8 | Decision Tree vs Prose | structural-scaffolding |
| 6 | Negative Constraints / Prohibited Actions | execution-control |
| 17 | Schema Lock (JSON output contract) | input-output-contracts |
| 100 | Progressive Disclosure (3-level loading) | open-source-skills |
| 103 | Reconnaissance-Then-Action | open-source-skills |
| 145 | Iron-Law Inviolable Rule Framing | execution-control |
| 146 | Rationalization-Prevention Table | quality-and-feedback |
| 148 | Anti-Performative-Agreement Vocabulary Ban | execution-control |
| 151 | HARD-GATE Block Tag | structural-scaffolding |
| 152 | DOT-Graph Decision Flow | structural-scaffolding |

Covers: structure / constraint / contract / discipline / anti-rationalization / loading — five axes, each with a clear "what success looks like" suited to `llm-rubric`.

All other 145 patterns appear in the list as `[TODO]` and are not selectable to run.

---

## 4. TUI Flow (Ink, 3 screens)

```
[Screen 1: PatternList]              [Screen 2: Config]
> 008 Decision Tree vs Prose         Provider:    anthropic:messages:claude-opus-4-7
  006 Negative Constraints           apiBaseUrl:  http://localhost:4141   (blank = official)
  145 Iron-Law Rule Framing          apiKey:      ******
  ...                                Judge model: anthropic:messages:claude-haiku-4-5
  031 Phase Gates           [TODO]   Runs N:      10
                                     [enter] run
[Screen 3: RunAndSummary]
[145 iron-law]   ████░░░░  6/20   $0.02
[151 hard-gate]  ██░░░░░░  2/20   $0.01
                  ─── (when done) ───
145 Iron-Law:  B passes 18/20, A passes  4/20 ✓
151 HARD-GATE: B passes 19/20, A passes  7/20 ✓
Full report: [y] open promptfoo view  [n] exit
```

Config persists at `~/.patternfoo/config.json` so the user only re-enters values when changing them.

---

## 5. Provider Configuration

Three fields exposed in Screen 2; serialized to the generated `promptfooconfig.yaml`:

```yaml
providers:
  - id: anthropic:messages:claude-opus-4-7
    config:
      apiBaseUrl: http://localhost:4141    # blank → promptfoo default (api.anthropic.com)
      apiKey: <dummy or real>
```

Any promptfoo-native provider ID is accepted (`openai:...`, `bedrock:...`, `ollama:...`, etc.). The `apiBaseUrl` field accommodates self-hosted endpoints (matches the local LiteLLM-style endpoint at `localhost:4141` used by `blog-cc-dev.cmd`).

**Why not `exec:claude -p`:** The blog A/B runs use `claude -p` to reuse the local endpoint without an API key. But a testing tool must be **independently reproducible** — anyone with a clone + an API key (or their own endpoint) should reproduce the numbers. `claude -p` carries implicit local state. Native promptfoo providers also give cost/token telemetry; `exec:` does not.

The legacy `eval/decision-tree-ab/run.sh` is retained read-only; a README line marks it superseded.

---

## 6. promptfooconfig.yaml (generated)

Per run, written to `results/{timestamp}/promptfooconfig.yaml`:

```yaml
providers:
  - id: anthropic:messages:claude-opus-4-7
    config:
      apiBaseUrl: http://localhost:4141
      apiKey: dummy
prompts:
  - file://patterns/145-iron-law/prompt-a.md   # label: A
  - file://patterns/145-iron-law/prompt-b.md   # label: B
tests: !include patterns/145-iron-law/scenarios.yaml
defaultTest:
  assert:
    - type: llm-rubric
      value: file://patterns/145-iron-law/rubric.md
  options:
    repeat: 10
    provider: anthropic:messages:claude-haiku-4-5    # judge uses a cheaper model
```

Then spawn:

```
promptfoo eval -c <generated.yaml> -o results/{ts}/output.json
promptfoo view --port 15500          # only when user presses y
```

---

## 7. YAGNI / Out of Scope (MVP)

**Do:**
- 3 screens, linear flow, no back navigation
- Pattern discovery by `readdirSync`
- Single provider string ID with optional baseUrl override

**Do not:**
- TUI-embedded result browser (use `promptfoo view`)
- Pattern editor in TUI
- Concurrency control (promptfoo's `-j` is enough)
- Historical comparison / trend charts (promptfoo built-in)
- Cost budget limits
- Custom provider abstractions

---

## 8. Risks & Mitigation

| Risk | Mitigation |
|---|---|
| `llm-rubric` cost if judge = main provider | Default judge to a cheaper model (haiku) — exposed in TUI config |
| Some Top 10 patterns hard to design discriminating scenarios for | Implement in listed order; downgrade unwriteable ones to `[needs-rubric]` and surface in TUI |
| Ink on Windows + Git Bash rendering quirks | Smoke-test `hello-world` in `cmd.exe` before building screens |
| User's local endpoint missing `anthropic:messages` route | README documents minimum endpoint surface; fall back to `anthropic:claude-` if needed |

---

## 9. Success Criteria

1. `cd eval/patternfoo && npm install && npm start` launches the TUI
2. All 155 patterns visible in the list; Top 10 selectable, others `[TODO]`
3. Selecting `145 + 151`, N=10, hitting enter → promptfoo runs, TUI shows B-vs-A pass rates
4. Pressing `y` opens promptfoo's web report with per-test pass/fail + raw outputs
5. The migrated `008-decision-tree/` produces results consistent with (or improved over) the legacy `eval/decision-tree-ab/prose-complex` run
6. Adding an 11th pattern requires only creating a directory under `patterns/` — no code change

---

## 10. Next Step

Invoke `writing-plans` skill to break this into a sequenced implementation plan.
