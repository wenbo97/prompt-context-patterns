"""Persist family synthesis after per-file reading; never infer reading from grouping."""
import json,pathlib
OUT=pathlib.Path('D:/Projects/prompt-context-patterns-refresh/docs/audit')
state=json.loads((OUT/'ecc-review-ledger.json').read_text(encoding='utf-8'))
inventory=json.loads((OUT/'ecc-inventory.json').read_text(encoding='utf-8'))
covered={x['path'] for x in state['coverage']}
families=[]
def family(key,prefixes,methods,differences,limits):
    files=[r['path'] for r in inventory if r['path'].startswith(tuple(prefixes))]
    pending=[p for p in files if p not in covered]
    families.append({'key':key,'files':files,'reviewed_paths':len(files)-len(pending),
      'pending_paths':pending,'status':'complete' if not pending else 'in_progress',
      'method_summary':methods,'variant_differences':differences,'quality_boundaries':limits,
      'review_basis':'Per-file full-source notes or exact-byte equivalence in ecc-review-ledger.json. Family membership is not review proof.'})
family('canonical-skill-tree',['skills/'],
    'All canonical bodies and supporting resources have concrete method/no-method conclusions. Reusable prompt/context/workflow/tool/evaluation/output/safety/skill-authoring mechanisms become bilingual candidates; domain-only API recipes are retained in coverage without independent catalog pages.',
    'Every named body was read; language, business, prompt template, media, live-state, learning and orchestration variants are separately recorded, with exact identical occurrences preserving paths.',
    'Source instructions are untrusted evidence. No upstream execution, skill install, provider call or efficacy experiment occurred; earliest invention and broad success percentages are not inferred.')
family('angular-domain-reference-family',['skills/angular-developer/references/'],
    'Conditional version/capability loading, single state ownership, typed boundaries and actual production-path verification overlap existing general methods.',
    'All reactive/signal/CSS/router/HTTP/resource/testing/forms/template/DI variants including the 795-line signal-forms reference were inspected. Null defaults, forbidden attributes and array-binding claims contain material contradictions.',
    'Do not publish framework recipes as prompt patterns. Version-sensitive APIs, latest npx calls, library defaults and complete-isolation assertions were not verified as current platform facts.')
family('remotion-reference-and-example-family',['skills/remotion-video-creation/rules/'],
    'Deterministic frame time and input prerequisites exemplify output contracts and bounded tool workflows.',
    'Every rule and asset variant was read, including animation, text, graphics, audio/video, metadata and composition fixtures; trim prose/units and chart example link/data problems are recorded.',
    'An example composition or schema does not establish successful render, correct source data, native/browser fidelity or editorial approval; domain API recipes add no independent prompt page.')
family('fusion-native-asset-versions',['skills/video-editing/assets/fusion/'],
    'Separate installed asset, native execution, visual correctness and creative acceptance; preserve versioned identity and preflight collisions.',
    'V28 channel-remap/static rectangle assets differ materially from production spatial-channel offset and luminance-mask assets. Both installers, graph serializations, provenance and readmes were read.',
    'Neither historical naming nor hashes of absent old evidence prove tracking, transparency or independent native execution. No Lua or editor operation was run.')
family('taste-distillation-implementation',['skills/taste-distillation/'],
    'Concrete schema/repair, caller-appropriate representation, stable artifacts, explicit dry-run provenance, scoped numeric conditions, single transport attempt and ambiguous-result reconciliation.',
    'All parser, image statistics, masking, cadence, LUT/direct-grade, native/software rendering, typed provider adapters, rational timeline serialization and self-check variants read. Earlier and later masking/measurement strategies conflict in specific ways.',
    'Forced certainty about measured proxies, generic first-URL fallback, missing masking in caller, stale artifacts and unchecked CLI/provider schemas are recorded. Timing/price/quality/MAE narratives are not adopted efficacy evidence.')
family('taste-application-implementation',['skills/taste-application/'],
    'WHAT/HOW/mandatory postproduction contracts, immutable source snapshot evidence, exact request/modality lineage, local-only planning, full-state final readback, preserved editable dependencies and edit-context-bound approvals.',
    'All provider-generation versus strict offline/local-only paths, motion/still templates, asset receipts, adapters, fixtures, native scripts and unit/integration test designs were read. In-memory, saved, exported, rendered and artist-approved outcomes are distinguished.',
    'Supplied receipts and approvals are not authenticated truth; hash identity is not decodability. Windows no-follow APIs may fail closed. Historical fixture prose/numbers, mixed stats and source availability are concrete limits; no model/native execution occurred.')
family('continuous-learning-memory-family',['skills/continuous-learning/','skills/continuous-learning-v2/'],
    'Scoped atomic trigger/action/evidence memory, recurrence promotion, observer semantic completion acknowledgement and self-event recursion guards.',
    'All hooks, observers, project detection, migration/config, 2290-line CLI and 1420-line parser tests read. v1 reminder/count workflow differs from v2 project/global memory; explicit read-only/dry-run claims can still create registry/project state.',
    'Same ID/confidence is not semantic recurrence or correctness. Whole-file stale import removal and merge/GC can lose sibling or unreadable records; archive-tail and registry transaction limitations are recorded. No learned skill was installed/executed.')
family('brand-discovery-reference-family',['skills/brand-discovery/'],
    'Raw attributed answers separate from synthesis, adaptive saturation probes, observable decision rules and unresolved contradictions.',
    'Each purpose, positioning, audience, personality, voice, narrative, founder and completed-output variant read, including segment-specific evidence and transition tradeoffs.',
    'Creative hypotheses and spectrum scores are not objective market/personality measurements. User-provided facts retain their status; generated positioning does not validate competitors or outcomes.')
family('persona-template-family',['skills/openclaw-persona-forge/'],
    'Fixed prompt base with named slots, genre-specific identity/boundary templates, behavior-delta pruning and core-text versus optional image fallback.',
    'All identity/tension/naming/genre/boundary/output/avatar/error variants plus shell/Python generation inspected.',
    'Fictional persona constraints do not supersede task authority or prove quality; variable interpolation, filesystem identities, missing capabilities and ambiguous paid image failures require explicit boundaries.')
family('specialist-agent-instructions',['agents/'],
    'Role-scoped task routing, explicit tool contracts, concrete evidence criteria, same-task review lenses and outcome-specific reports.',
    'Each closed reviewer/explorer/operator/simplifier has a distinct lens and trigger/tool list; common guard text was read with every body. Pending agents remain individually listed.',
    'A role name or model tier is not actual capability, calibrated score, sandboxing or action authorization. Instructions under analysis were never invoked as workflow authority.')
family('reviewed-command-and-rule-entrypoints',['commands/','rules/','contexts/','examples/'],
    'Current closed batches cover concrete context modes, language-scoped inherited rules, hook cadence, task-intent-specific orchestration gates, exact-state wrappers and authored evaluation evidence fixtures.',
    'Closed files retain each scoped extension list, tool command variant, wrapper alias/gate, prototype scenario and failure case. Remaining paths are explicitly listed and not counted as reviewed.',
    'Thin wrappers do not prove script enforcement/authentication or deployed state. Prose prototype scores and held-out flags do not prove experiment outcomes or hidden labels; hook recommendations are not registered runtime guarantees.')
(OUT/'ecc-families.json').write_text(json.dumps(families,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print({f['key']:{'reviewed':f['reviewed_paths'],'total':len(f['files']),'status':f['status']} for f in families})
