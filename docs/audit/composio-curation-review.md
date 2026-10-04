# Composio Candidate Curation Cross-Check

This is a mechanism-level recommendation pass over the 41 bilingual candidates in `harvest-composio.json` against the active legacy catalog and current `core`, `ecc`, and `gstack` reports. It does not change candidate statuses, the global decision map, or target articles. Recommendations below describe where an eventual consolidation should land and which teaching contrast must survive.

## Existing Merges: Preserve and Resolve Redirects

The 19 existing merges remain valid. Where a suggested legacy ID has since been merged, use its current active destination:

| Candidate | Current target | Mechanism and teaching detail to retain |
|---|---|---|
| `composio-discover-connect-execute` | Legacy **#109** | Discover the live action schema, verify the intended connection, then execute; keep the contrast with guessed endpoint names. |
| `composio-runtime-trace-first` | Legacy **#26** | Trace current runtime evidence before claiming a cause; retain missing coverage as an explicit result. |
| `composio-progressive-disclosure` | Legacy **#100** | Keep the entrypoint small and load branch material only when its trigger applies. |
| `composio-intent-reference-routing` | Legacy **#100** (its suggested **#85** now redirects here) | Bind the selected reference to the task/audience, then load it on that branch; this is a pointer condition within progressive disclosure. |
| `composio-helper-blackbox` | Legacy **#104** | Use the documented helper interface for deterministic work; preserve the bad/good contrast between contract use and reimplementing guessed internals. |
| `composio-rendered-reconnaissance` | Legacy **#103** | Inspect rendered/current state before acting; the result of observation selects the next action. |
| `composio-creative-philosophy` | Legacy **#101** | Translate a design concept into concrete constraints before producing the artifact; do not imply measured quality improvement. |
| `composio-refinement-pass` | Legacy **#28** (its suggested **#102** now redirects here) | Apply a named failure-mode review to a draft; keep the check concrete and avoid universal emotional-effect claims. |
| `composio-collaborative-section-drafting` | Legacy **#106** | Complete and review one coherent section before expanding the draft. |
| `composio-audience-purpose-calibration` | Legacy **#83** | Choose detail and presentation from the audience’s decision need, not from a generic verbosity rule. |
| `composio-validate-before-package` | Legacy **#51** | Run a real artifact checker before packaging; keep the observed pass/fail result separate from prose assurance. |
| `composio-unavailable-capability` | Legacy **#173** | Report the missing capability and use only a documented alternative; unrelated-provider search results are not evidence of support. |
| `composio-catalog-with-generated-fallback` | Legacy **#143** | Select a matching catalog item first; use a constrained fallback only when none fits. |
| `composio-workflow-tool-design` | Legacy **#144** | Shape tools around bounded intents, useful evidence, and actionable errors; protocol hints alone do not enforce trust. |
| `composio-baseline-preserving-edit-oracle` | Legacy **#176** | Compare changed and unchanged behavior against the same baseline inputs, including failures. |
| `composio-capability-branch-routing` | Legacy **#20** (its suggested **#113** now redirects here) | Route from an observed input property; keep the property and selected branch visible. |
| `composio-visible-action-confirmation` | Legacy **#8** | Show the concrete external effect at the authorization boundary; retain the constraint that confirmation depends on task scope. |
| `composio-secret-bearing-composite` | Legacy **#11** | Inspect nested/composite values for secrets before exposing output; do not infer safety from the outer field name. |
| `composio-eval-feedback-improvement` | Legacy **#119** | Preserve tasks, baseline, and observable assertions while iterating; source examples are not efficacy measurements. |

## Rejected Candidate: Retain the Rejection

| Candidate | Evidence issue | Recommendation |
|---|---|---|
| `composio-verified-randomness-claim` | The source promises secure, unbiased, seeded/verifiable, manipulation-proof selection but provides no implementation or audit protocol. | Keep rejected; no active-catalog merge can turn the unsupported guarantees into evidence. |

## Active Candidates: Consolidation Recommendations

These are recommendations only; the 21 candidates remain active in the harvest pending a separate decision-map review.

| Candidate | Mechanism comparison and contrast | Recommendation |
|---|---|---|
| `composio-error-directed-recovery` | Distinguishes auth/permission and invalid-input failures from throttling and valid empty results. “Retry the same 403” is the bad case; matching the repair or bounded backoff to the recorded error is the good case. It also matches `ecc-transient-retry` and the already-merged `core-anthro-error-directed`. | Merge into legacy **#15 Error Handling / Degradation**; preserve the 403-stop vs bounded-429 contrast and the empty-result boundary. |
| `composio-pagination-completion` | Completeness is proven by the endpoint’s terminal cursor, with page/record counts and failure/cap disclosure; it is relative to filters and permission. | Merge into legacy **#193 Two-Axis Completion Criterion** for proving dataset traversal completion. Keep the broader continuation-state contract below as the distinct rule for partial work across API and generated output. |
| `composio-truncation-with-continuation` | A bounded API result needs an opaque service-issued cursor and truthful returned/known-total counts. Generated output needs an authored pointer to the next complete unit plus truthful completed/known-total counts. Both expose partial progress and resume boundaries, but the pointer types are not interchangeable. | Keep the Composio candidate as the identity and merge **`core-leon-continuation-cursor` into it**. Teach API-record continuation and generated-unit continuation as separate examples; never synthesize an API token or present `section seven` as one. Report unknown totals as unknown and partial counts as partial. |
| `composio-checkpoint-bulk-progress` | Persist acknowledged item IDs and continuation state after bounded batches, then resume unresolved work. Its own boundary says a checkpoint is not exactly-once delivery. | Merge into legacy **#73 Resumable Idempotent Actions** as a batch-progress example, retaining the separate idempotency-key/lookup requirement. |
| `composio-stable-external-key-upsert` | Composio’s external ID names a destination entity across sync runs; #73’s `r42` names one intended write action across retries. They have different lifetimes and cannot substitute for one another. | Merge into legacy **#73 Resumable Idempotent Actions** as a natural-entity-key lookup/upsert example. Enrich the example with the distinction: look up/create or use destination-enforced native upsert by entity key; for timeout retries use a separate receiver-enforced operation key and reconcile unknown effects. `core-addy-intent-stable-key` and `core-addy-unknown-effect` are related source mechanisms that also consolidate to #73. |
| `composio-fresh-version-update` | A fresh read supplies a version precondition, and a conflict requires intent-preserving reconciliation. This strengthens `core-matt-stateful-write-reread`, whose own boundary says rereading is not an atomic lock. | Merge into **`core-matt-stateful-write-reread`**; preserve the version-token and conflict path as the teaching contrast. Do not claim the prompt alone supplies concurrency control. |
| `composio-tool-metadata-is-not-authorization` | Read-only/safety annotations are descriptive input; actual operation effects and the caller’s authority must be enforced. This is adjacent to legacy **#134 Tool-Constraint Boundaries** and `ecc-reputation-not-action-authority`. | Merge into legacy **#123 Scoped Authorization and Action Risk**, with #134 as a related pattern; preserve “hint is not enforcement.” |
| `composio-stable-readonly-evaluation` | The Composio method contributes fixed-period archived data, independent non-destructive tasks, and a verified exact-format answer. `core-independent-mutation-sensitive-oracle` contributes an independently derived literal oracle and checks that plausible defects change the result. | Merge into **`core-independent-mutation-sensitive-oracle`**, enriching it with a stable read-only task fixture. Keep separate from legacy **#119**, the broader eval-driven improvement loop, and `ecc-paired-baseline-evaluation`, which compares revisions on the same trial panel. |
| `composio-bounded-artifact-validation` | Measure actual bytes/dimensions against a stated limit, correct the parameter tied to the failed constraint, and remeasure. This is a concrete measurement example of validation, not a new general gate. | Merge into legacy **#51 Schema Validation Gate**; retain numeric evidence and the boundary that current platform limits need fresh verification. |
| `composio-reversible-file-operation-ledger` | Record origin→destination and a recovery/checksum trail while preserving originals; this makes an otherwise destructive move inspectable and reversible. | Merge into legacy **#59 Rescue-Tag-Before-Destructive-Operation** as a file-operation example. |

## Active Candidates: Keep Distinct

| Candidate | Contrast with active catalog or other report | Recommendation |
|---|---|---|
| `composio-schema-reference-expansion` | Resolves a runtime `schemaRef` before constructing arguments; legacy **#23** loads a named prompt/reference asset and does not supply a live tool contract. | Keep active; link to #23 only as adjacent reference-loading guidance. |
| `composio-resolve-scoped-identities` | Looks up a child entity inside its selected parent and passes both returned IDs. `gstack-canonicalize-before-authorization` canonicalizes aliases before a security decision; it does not teach parent-scoped service foreign-key lookup. | Keep active; retain the disambiguation and no cross-workspace ID reuse boundary. |
| `composio-tenant-bound-routing` | Chooses the intended connected organization and includes its tenant ID. Legacy **#123** concerns authorization/effect scope; selecting the correct tenant is not proof that a write is authorized. | Keep active and cross-link to #123. |
| `composio-replace-versus-patch` | Branches on endpoint semantics: append/patch when possible, otherwise read, merge, and send a complete replacement. `core-matt-stateful-write-reread` protects intervening edits but does not decide whether the endpoint replaces or patches. | Keep active as a distinct interface-contract method. |
| `composio-per-item-batch-status` | Reconciles nested item success/failure/missing states against requested IDs even when the outer response succeeds. `ecc-typed-tool-recovery` defines an envelope-level failure/recovery contract. | Keep active; the item-level accounting is materially different. |
| `composio-async-terminal-state` | Saves a remote job ID and polls until its output is complete or remains pending. `ecc-semantic-completion-handshake` checks a local process exit plus completion record; `ecc-drain-before-observer-stop` keeps an observer alive for a producer. | Keep active; preserve the remote-job identity, bounded polling, and pending state. |
| `composio-pilot-fixed-extraction-contract` | Freezes field/null/error rules, validates representative pages, then scales. Legacy **#14** specifies output shape and **#51** validates an artifact; neither requires a representative pilot before broad extraction. | Keep active as a distinct pre-scale gate. |
| `composio-managed-helper-lifecycle` | Tracks helper processes, bounds readiness waits, returns the test result, and cleans up owned processes. `gstack-owned-terminal-cleanup` uses an atomic ownership token for a lock; the source helper does not prove process-tree cleanup. | Keep active; do not merge process cleanup with lock ownership or observer draining. |
| `composio-persist-expiring-output` | Turns temporary access into a verified durable destination under the task’s retention authority. `ecc-exact-artifact-promotion` preserves the identity of a tested artifact through promotion; it does not solve temporary URL expiry or persistence. | Keep active; retain byte/path verification and retention limits. |
| `composio-delta-token-sync` | Applies server-issued additions/updates/deletions before advancing a change token; an expired token requires a fresh snapshot. No reviewed legacy/core/ECC/gstack candidate expresses this incremental API contract. | Keep active. |
| `composio-metadata-capability-selection` | Chooses a currently accessible model/voice by declared capability. `core-anthro-intent-catalog` recommends a current learning resource by user intent; it does not select a runtime capability-compatible identifier. | Keep active; keep discovery metadata tied to the selected identifier. |

## Methods Deliberately Not Split into More Candidates

The additional full-content reviews of Capsule CRM, Docker Hub, Google Admin/Maps/Search Console, LaunchDarkly, Lemon Squeezy, Microsoft Clarity, Mistral AI, New Relic, SharePoint, SurveyMonkey, Wave Accounting, and Zoho Books/Desk reinforce the active identity-scope, pagination, recovery, schema, async, and unavailable-capability methods above. Their remaining sequences (for example geocode→route, create channel→attach policy, or create survey→fetch collectors) depend on provider-specific endpoint contracts and remain observed examples rather than separate general patterns. The three unavailable-toolkit files support **#173** without inventing tool behavior. No candidate is added or removed; the harvest remains **19 merged, 21 active, 1 rejected (41 total)**.
