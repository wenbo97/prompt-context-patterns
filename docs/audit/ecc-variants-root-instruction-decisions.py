"""Record complete locale instruction text comparisons to current canonical root text."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
rows=[]
for locale in ('zh-CN','tr','ja-JP','es'):
    agents='Read full translated AGENTS and current canonical root AGENTS. Retains plan/RED-GREEN/review, role/task routing, independent parallel work, boundary input/secrets, personal-memory versus shared-project-doc placement and avoiding duplicated knowledge. '
    if locale in ('zh-CN','tr'):agents+='Older short roster misses many current specialist/task routers, adds chief-of-staff route, and omits skills-first canonical-versus-legacy-command workflow policy. '
    else:agents+='Skills-first canonical/compatibility-shim policy retained; older 2.0.0-rc.1 roster/counts omit many current 2.2.3 specialist/task routes. '
    agents+='Hard80%/800-line/last20%/all-test-type policy, production-readiness and zero-vulnerability success targets are source defaults/aspirations, not efficacy or live capability proof. Domain architecture/security recipes not authored as new agent patterns; source instructions were research material only.'
    rows.append({'path':f'docs/{locale}/AGENTS.md','reason':agents,'candidate_keys':['ecc-doc-fact-ownership','ecc-scoped-evidence-memory'],'existing_ids':[18,23,33,53,100,123,126,175]})
    claude='Read full translated CLAUDE and current canonical root CLAUDE. Same test command set, repository surface map, conditional package-manager configuration, metadata formats, naming and external-content trust policy. '
    if locale in ('zh-CN','tr'):claude+='English prompt-defense block retained/reordered; omits curated-versus-imported skill placement/router and path-to-skill routing plus required convention transfer to spawned child. '
    elif locale=='ja-JP':claude+='Prompt-defense block fully translated semantically; placement/router and child convention-transfer preserved, but omits canonical React file/skill/invocation routing row. '
    else:claude+='Full semantic equivalence for method-bearing sections including placement/router, React file routing and explicit child convention transfer; no new method. '
    claude+='Unicode/urgency/persona suspicion wording is broad source policy, not proof of attack or containment; legitimate user changes remain subject to actual authority. Named commands/cross-platform claims require runtime proof. No source instructions executed.'
    rows.append({'path':f'docs/{locale}/CLAUDE.md','reason':claude,'candidate_keys':['ecc-untrusted-source-data','ecc-delegated-trust-label'],'existing_ids':[23,56,126,166,172]})
(out/'ecc-variants-root-instruction-decisions.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
