from pathlib import Path
_namespace={'__name__':'core_helpers'}
exec(compile(Path(__file__).with_name('core-update.py').read_text(encoding='utf-8'),'core-update.py','exec'),_namespace)
globals().update({k:v for k,v in _namespace.items() if not k.startswith('__')})
R='obra/superpowers';rr=next(r for r in DATA['repositories'] if r['repo']==R)
current={
 '.opencode/plugins/superpowers.js':'Full383-line runtime body reviewed, not executed: action mappings vary by host, cached frontmatter/body, structural parentID child classification, validated envelope/identity, no cache on lookup failure, bounded cache, transient bootstrap dedup/compaction and per-skill registration isolation. Marker substring guard can be spoofed by quoted content; cache lifetime and fail-open behavior are source design choices.',
 '.pi/extensions/superpowers.ts':'Full121-line runtime body reviewed, not executed: native skills, lifecycle flag, compaction-aware insertion, cached source, marker guard and inline tool mapping. Optional capability fallbacks differ from actual native Skill invocation; parsed frontmatter currently assumes LF.',
 'skills/systematic-debugging/condition-based-waiting-example.ts':'Full158-line example body/comments reviewed, not executed: fresh event getter and type/count/predicate helpers with timeout. Old events can satisfy an unscoped predicate; instance/correlation identity is needed. Claimed universal success and pass/speed gains are not independently verified.',
 'skills/systematic-debugging/find-polluter.sh':'Full72-line helper reviewed, not executed: sequential per-test runs with before/after pollution path observation. Despite its bisection label it is linear; pre-existing pollution makes all tests skipped but final message still says clean, and whitespace-delimited filenames are fragile. No clean-result guarantee extracted.',
 'README.md':'Full399-line README reviewed: overview/routes/install mappings and source library/philosophy; no additional reusable mechanism beyond normative skill bodies. Summary drift includes outdated minute-sized/full-code plans and discard menu; product/version/telemetry claims are frozen statements.'
}
for path,note in current.items():review(R,path,note,['core-superpowers-harness-reference-routing'] if path.startswith(('.opencode/','.pi/')) else [])

special={
 'docs/superpowers/specs/2026-06-10-positive-instruction-redesign-design.md':'Full178-line historical method/results narrative reviewed: variant/control microtests, manual false-positive scoring checks, independently assessed recognition/composition forms and no-op stop when controls lack a failure. Reported small-sample effects/prices and generalizations are not adopted as current model guarantees.',
 'docs/superpowers/specs/2026-06-10-strict-cost-sdd-design.md':'Full265-line historical experimental ladder reviewed, including reread of truncation gap: quality and judgment gates precede cost optimization, preregistered rejection, controlled fixture confound reattribution, negative results and distinct task/review model responsibilities. Reported costs/rates are self-report snapshots; no raw run revalidation or current price claims.',
 'docs/superpowers/specs/2026-07-06-sdd-plan-scoped-workspace-eval-results.md':'Method/scenarios/results/quoted evidence/limitations and scenario prompt reviewed; Appendix A widget/Git fixture implementation is domain-only and excluded from semantic code reading. Validity controls exposed fake hashes/stub content and baseline no-op; report explicitly retracts error-rate and call-count improvements. Numeric table arithmetic is inspectable, raw artifacts are outside this repository.'
}
for path,note in special.items():review(R,path,note,['core-plan-owned-resumption-ledger'] if 'workspace' in path else [])

for row in rr['coverage']:
    p=row['path']
    if row['disposition']!='pending':continue
    if p.startswith(('docs/plans/','docs/superpowers/')) and p.endswith('.md'):
        title=blob(R,p).splitlines()[0].lstrip('# ').strip()
        review(R,p,'Scope reviewed by dated title, objective/architecture and section inventory; current corresponding skill/ref/runtime mechanisms have been semantically reviewed. Historical artifact: '+title,excluded='Repository-specific historical implementation/design of '+title+'; code changes, past acceptance details and superseded policies are excluded rather than presented as current agent instructions. Normative successor bodies carry transferable mechanisms.')
    elif p in ['RELEASE-NOTES.md','CODE_OF_CONDUCT.md']:
        review(R,p,'Scope reviewed: release chronology or community conduct policy, not a skill/ref/procedural prompt body.',excluded='Release history/community governance; no standalone prompt/context workflow extracted from this non-runtime document.')
    elif p.startswith('tests/'):
        review(R,p,'Scope assessed against corresponding current skill/reference: repository-specific automated fixture/assertion/harness wiring.',excluded='Plugin/runtime or historical CLI integration implementation/tests; transferable testing/pressure/oracle methods are reviewed in normative authoring/debugging references. No source tests executed.')
    elif p.startswith('skills/brainstorming/scripts/') or p.endswith('render-graphs.js'):
        review(R,p,'Scope assessed via referenced helper contracts and file type; serves/renders the already-reviewed visual/graph workflow.',excluded='Domain browser UI/HTTP/WebSocket/rendering implementation, not an additional prompt or context procedure. User-facing event/lifecycle and validation method are covered by visual-companion and porting references.')
    else:
        review(R,p,'Scope assessed from tracked path/type and normative references; package metadata, installer/release or CI support for reviewed runtime.',excluded='Repository support, package/version/CI/installer metadata or code; no distinct method-bearing instruction body. Current harness/bootstrap/authoring contracts were reviewed in full.')

families=[{'key':'superpowers-current-skills','count':15,'summary':'All15 SKILL bodies fully read with graphs/examples. Inline/delegated execution share ledger but differ in task review/fix policy; this difference remains explicit.','candidate_keys':[c['key'] for c in DATA['candidates'] if any(s['repo']==R for s in c['sources'])]}, {'key':'superpowers-diagnostic-lenses','summary':'All7 dimension prompts plus common, similar-session, scrub/audit, discovery/redaction/context refs and case/report/issue/bundle templates semantically reviewed. Common role/contract blocks do not erase dimension-specific differences.'}, {'key':'superpowers-harness-adapters','summary':'All7 harness refs plus Kimi/OpenCode guides, porting guide and actual OpenCode/Pi/bootstrap/helper runtime read. Tool/callback/object shapes and fallback differences preserved, stale claims qualified.'}, {'key':'superpowers-historical-domain-artifacts','summary':'Dated implementation/spec history scope-reviewed and excluded where normative successors cover the methods; selected microtest/cost/workspace evidence narratives reviewed separately. Excluded code is not claimed as semantically read.'}]
finish_repo(R,families,['No original source scripts or live evals executed. Root MIT license reviewed; source material treated as evidence, never task instructions.','Unsupported cost/pass-rate/impossibility claims and weakened sample oracles/path checks recorded in per-file conclusions.','Historical project-specific plans/specs, runtime UI/math/installer/CI code and fixtures excluded explicitly after scope review, not labeled semantic duplicates or full reads.'])
save()
