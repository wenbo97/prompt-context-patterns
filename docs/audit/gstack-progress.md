# Gstack source review closure

Controlling scope: `docs/specs/2026-10-03-blog-rebuild.md`. Frozen source: `garrytan/gstack` at `f30b7b788a210d217ea3125bf3001b29cbc2a463`.

The source harvest is closed with **0 pending rows**: 2,656 files total, 512 analyzed, 2,137 scoped exclusions and 7 exact duplicates. Review kinds are 385 full-semantic, 127 difference-review, 2,137 scoped-relevance and 7 verified-equivalence. `docs/audit/harvest-gstack.json` records the dispositions and evidence. The former 808 pending rows are all accounted for; support roles were read in bounded batches before closure.

The source-role review covered test, browse, migration, Supabase, browser-skill, documentation-asset and root-support batches. Complete text was read for the nine Supabase files and the three Hacker News browser-skill files; both contribution-chart images were rendered and viewed. Large release/backlog archives were classified through bounded structural and representative-content samples, not full semantic reviews. Runtime, migrations, network checks, tests, builds and evals were not run. No upstream correctness, security or performance audit is claimed. `docs/audit/gstack-embedded-method-review.json` records support-content review boundaries and candidate curation.

The four essential prompt/calibration fixtures and `test/redact-semantic-pass.eval.ts` received full direct reads. The paid eval was not executed. Existing 17 authored candidates were preserved. Two bilingual eight-field candidates are now in the harvest, for 19 total:

- `gstack-persona-grounded-peer-benchmarking` compares persona-specific journeys between products, including equal start/result boundaries, evidence types and unknown durations.
- `gstack-capability-tiered-instruction-digest` preserves a versioned rules-only baseline for hosts that cannot run the full suite, while explicitly withholding unavailable workflows and leaving AGENTS.md copying to the user.

Curation: keep persona-based peer benchmarking distinct from `gstack-comparable-coverage-trends` (longitudinal checks), ECC's paired trial-panel evaluation, fixed-context scoring and the shared-host UI comparison. Keep the instruction-only digest distinct from legacy #100's on-demand loading and #173's unavailable-capability report: it distributes a limited but useful behavioral tier. Treat the generated `gstack/llms.txt` as another example of #100, not a separate candidate.

The local scope finalizer needed a disposition guard because the historical role ledger includes already-closed paths absent from the pending-only shape cache. The guard preserves existing exclusions and duplicates; pending rows still require matching hash evidence. No source files were changed and no commit was made.
