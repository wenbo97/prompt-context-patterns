"""Six full legacy-learning translation bodies compared, with retirement drift retained."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
rows=[]
for locale in ('zh-CN','ja-JP','zh-TW','es','tr','ko-KR'):
    reason='Read complete translated v1 learning prose/config/hook/examples against canonical current file. Retains end-of-session→qualifying-message gate→reusable correction/error/workaround/technique/project lessons→learned-skill store, ignores trivial/one-off patterns and keeps auto_approve=false. '
    if locale=='es':reason+='Spanish preserves current deprecated/archival top-level v2 router and older supported-status prose inside archived section; removes longform source link. '
    else:reason+='Omits canonical deprecated/archival top-level v2 migration router; presents old v1 extraction as active guidance. '
    if locale in ('ja-JP','zh-TW'):reason+='Also omits activation section. '
    if locale=='ko-KR':reason+='Adds duplicate config/hook examples and changes spec pointer to a relative Markdown link; no new mechanism. '
    reason+='Global-only storage is not project-scoped authority, hook configuration is not capture/extraction proof, and Stop need not mean exactly one whole session. 50–80%/100% reliability, complete-transcript/no-latency and strict-superset claims are unverified source narration. No hook/script/learned-file mutation executed.'
    rows.append({'path':f'docs/{locale}/skills/continuous-learning/SKILL.md','reason':reason,'candidate_keys':['ecc-atomic-learning','ecc-evidence-promotion','ecc-retirement-context'],'existing_ids':[42,69,95,155]})
(out/'ecc-variants-learning-v1-decisions.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
