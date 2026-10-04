# Legacy pattern and blog audit

Audit date: 2026-10-03. This report covers the existing corpus; new methods from the ten repositories are recorded separately by the source harvesters.

The machine-readable decisions are in [legacy-review.json](legacy-review.json). All 206 numeric identities and K1–K6 have exactly one disposition. The numeric catalog retains **122 active methods**, consolidates **75 aliases**, and removes **9 entries**. Every active numeric method has independently authored English and Chinese descriptions, scenarios, mechanisms, matched bad/good teaching prompts, observable expectations and boundaries. K1–K4 remain four distinct new candidates; K6 is an alias of the observable-goals candidate and K5 consolidates into #25.

## Coverage and grading

- Parsed all 155 numeric write-ups and six K sections outside fenced code. The original section text and locations are preserved in [legacy-prepared.json](legacy-prepared.json); the 51 later entries were reviewed from their actual metadata/problem summaries, not treated as if full bodies already existed.
- Reviewed all six technique guides, two standards pages and four historical articles, with their bilingual companions. Eight navigation/index/readme pages are included in the 32 page-level remediation decisions in the JSON.
- Active numeric scores are conservative **8/10** editorial assessments of the revised content: scenario 2, mechanism 2, contrast 2, observable 1, boundaries 1. The concrete task, mechanism and comparison are complete; the short expectation and boundary text provide useful but limited checks. These scores do **not** claim the teaching prompts were experimentally run.
- **69 active numeric entries** have pinned observed mechanism exemplars; **53** retain `source-unconfirmed` because this audit did not establish a matching pinned exemplar. Lack of trace was assessed independently from usefulness. All retained examples are labelled `teaching-construction` and `editorial-review-only`.
- All earliest-origin statuses remain `unknown`. An occurrence in a public skill is evidence of that implementation, not evidence its author invented the method first.

Validation passed for 206 numeric IDs, six K records, every retained bilingual field, active-only related IDs, merge destinations, score gates, and 94 source records covering 69 distinct line ranges. See [legacy-validation.json](legacy-validation.json). Source commits match the actual local repository HEADs, paths exist, and cited ranges fit their frozen files. No external skill script was executed.

## Removed entries

| ID | Legacy claim | Why it is removed |
|---|---|---|
| 44 | Severity promotion/demotion by area | Capping accessibility or rollout issues by topic can hide serious failures. No validated calibration supports the fixed caps. Use evidence-backed local severity criteria instead. |
| 49 | Blast radius and impact formulas | Arbitrary weights combine different units and imply numeric precision the source does not establish. |
| 55 | Skip triage based on model identity | A model name alone does not identify input, policy, revision or evaluation freshness; unchanged model identity can still need a new assessment. |
| 66 | Never reveal any skill/configuration | Blanket secrecy for public skill files conflicts with transparent inspection. Protect actual secrets and private instructions through the applicable boundary. |
| 97 | Refuse all delivery beyond the owner's own accounts | The universal refusal despite owner consent is an unsupported policy claim, not a portable engineering mechanism. Use the actual data-handling matrix and authorization. |
| 125 | Five-minute cache / 300-second dead zone | A community-extracted prompt contains cache assumptions, but this does not establish a portable timing rule for every runtime. Bounded polling survives in #76/#77. |
| 142 | Delete-then-create immutable memory is atomic | Deletion followed by creation is not atomic; interruption can lose the old and new data. The dream metaphor does not fix this. |
| 187 | Inline author justification suppresses a finding | A comment is an unverified claim, not an automatic waiver. Evidence-based adjudication remains in #47. |
| 189 | Pretrained leading word necessarily sharpens behavior | A mnemonic can aid terminology, but the claimed token-level efficacy has no measured support and the usable vocabulary mechanism belongs in #194. |

Removal withdraws the article content and current-index entry; the identity must remain a compatibility tombstone and must not be reused for a different method.

## Substantive repairs

The revised examples correct several operational mistakes rather than merely changing wording:

- #127 stages and commits **sequentially**; independent status/diff/log reads may be parallel. The old example raced `git add` with `git commit`.
- #59 preserves both committed history and dirty/untracked files; a rescue tag alone does not save local edits.
- #123 keeps granted authorization valid within its actual scope instead of inventing per-turn reapproval. #8/#151 ask only at an actual declared boundary.
- #10/#134 distinguish prompt labels from runtime enforcement; removing an editor tool does not remove shell or network write capability.
- #68 minimizes data before context ingestion and no longer claims pseudonymization eliminates every identity risk.
- #76 removes the universal assertion that one server's 403 cancels unrelated calls.
- #100/#128 replace fresh-attention-window, unlimited-resource and unlimited-memory promises with host-dependent loading and verified durable state.
- #116 preserves calculations for editable artifacts without declaring all immutable snapshots invalid.
- #135/#141 use documented host capabilities, not assumed universal fork/cache behavior or invented convenience APIs.
- #160 permits focused independent checks when evidence is stale, incomplete or leaves a concrete doubt; it is not a universal ban on reviewer tests.
- #178 uses input fingerprints rather than modification times alone; #183 uses context-specific encoders rather than treating HTML escaping as universally safe.
- #153/#155 present source integrity and lifecycle schemas as illustrative contracts, not verified accepted fields in every marketplace.

Canonical display names were adjusted where necessary: #43 is Isolated Review Checkout, #52 Rubric-Based Model Evaluation, #67 Whole-Payload Skill Review, #73 Resumable Idempotent Actions, #116 Preserve Computation in Editable Artifacts, #123 Scoped Authorization and Action Risk, #145 Evidence-Bound Verification Rule, #151 Explicit Preconditions with Gate Markers, and #155 Capability Retirement with Migration Paths. Numeric IDs and original names remain available to migration tooling.

Every numeric merger has a specific English/Chinese rationale in the JSON and [legacy-merge-rationale.tsv](legacy-merge-rationale.tsv). Mergers consolidate the underlying method rather than treating source popularity as quality. Domain-only variants such as chart selection and incident escalation retain their old identity as aliases; their example thresholds are not promoted to universal rules.

## Karpathy provenance and distinctness

The pinned `skills/karpathy-guidelines/SKILL.md` has four principles: consequential assumptions, minimum necessary code, request-traceable surgical edits, and observable goals. It explicitly describes them as derived observations. Its MIT declaration is in the skill frontmatter; there is no standalone root license for indiscriminate reuse of every repository file. Teaching examples here are independently authored.

K1 does not collapse to an interaction loop: its distinguishing mechanism is exposing consequential interpretations. K2 does not collapse to a prohibition list: it limits implementation to requested behavior. K3 permits bounded authorized edits and therefore is not the same as #12's no-write review. K4 reformulates success into observable behavior, rather than merely ordering stages. These four are the candidates `core-karpathy-assumption-disclosure`, `core-karpathy-minimum-necessary-code`, `core-karpathy-surgical-edit` and `core-karpathy-observable-goals` in [harvest-core.json](harvest-core.json); the root integration allocates their numeric identities.

K5 and K6 were local teaching extensions. K5's useful part is explaining the visible mistake, consequence and correction in a matched example; it merges into #25 without requesting hidden internal deliberation. K6 is the sharper goal-to-test formulation inside the observable-goals method and shares K4's canonical candidate. Neither is labelled an additional Karpathy original.

## Unsupported statistics and causal claims

The revised canonical text excludes old prevalence claims such as 2,290 files, approximately 100%, 54%, 40%, 35%, 832 occurrences, and at-least-three independent plugins when no frozen per-file counting procedure substantiates them. Historical repository counts can be discussed as dated release claims, while current counts must come from the new inventory.

The token guide and its copied article give 35/30/25/10 and 92/5/3 probability distributions without a measured run. The standards/checklist convert these into approximately 30% versus 5% deviation. These numbers and the claims that trees, XML, emotional phrases or proximity make outputs deterministic are removed. Attention and entropy stories are not substitute measurements. Fixed 47-token averages and 200/260/300-line universal quality limits are also unsupported as project-wide requirements.

The decision-tree article's **20-run** results—15 versus one primary-action phrasing, 20 versus two secondary variants, and 0/20 versus 20/20 literal action matches—cannot be recomputed from this checkout. `eval/decision-tree-ab/README.md` says result outputs are gitignored, and the `results/` directory is absent. The prompts also differ in literal action enums and output constraints, so even preserved outputs would not isolate tree layout as the cause. Keep the historical date, prompts and runner; remove the figures or explicitly label them previously reported observations with unavailable raw outputs. The branching guide's 5/5 report has the same missing-output limitation.

The old guides' 0%/12% reference skip rates, 92%/78% format-correct rates and 14-point regression example are teaching numbers, not project benchmark results. Domain examples containing traffic, cost, ranking weights, or availability must likewise be marked illustrative or supported by a real source.

Some vendor-scoped advice has a real primary source. Anthropic's [prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) reports up to 30% improvement for queries at the end of complex long multidocument inputs. This is a vendor-reported scoped observation, not a universal guarantee for this catalog. Its [context engineering article](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) supports curated context, selective retrieval and durable notes; it does not validate the invented probability tables in the legacy blog.

The original community system-prompt pointer was also checked at [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts). It is a community extraction of versioned product strings, not official proof of a universal runtime guarantee or the earliest origin of the catalog's names. No excerpts from that repository were copied into the teaching examples.

## Blog remediation and overlap

The anti-laziness page and eleven-pattern reference-skip playbook substantially overlap #23 (explicit reference pointers), #100 (conditional loading), #104 (trusted helper interfaces), #42 (isolated context), #51 (real validation), #119 (evaluation) and #132 (hooks). Keep one guide and route its variants to those canonical entries. Proposed model motivations are hypotheses to test through actual read traces; scripts and hooks have observable interfaces but do not automatically guarantee semantic correctness.

The good/bad guide should become the editorial writing template used by the catalog. The architecture guide should use frozen repository counts, scope-specific licenses and current host mechanics. The standards and review pages should describe this project's actual content contracts; remove orphan references to another migration plugin's commands, rules and private project names. Markdown headers and XML are legitimate structural choices, not competing universal quality requirements.

Historical posts retain their dates and fixed experiment fixtures but gain a revision note and current links. The May article labels an attempt-capped repair loop #23 although #23 is Reference File Injection; its #45 pre-write example is also not the catalog's Directive Review identity. Link the actual current methods and avoid reassigning these numbers. The July article's 155-to-206 change is historical; it must not become the current active total. Its cross-service credential wording should describe suspicious flow and actual authorization, not claim cross-service use is the only possible malicious behavior.

All hrefs, bilingual pairs, count badges, searches and theme indexes should be regenerated from the root's canonical records. Compatibility aliases and removed tombstones are excluded from active search and current totals. This report does not push or publish the site and does not claim the new examples have passed model experiments.
