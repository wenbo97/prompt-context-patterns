"""Persist completed Turkish common-rule semantic comparison decisions."""
import json,pathlib
out=pathlib.Path(__file__).resolve().parent
rows=json.loads((out/'ecc-variants-common-pt.json').read_text(encoding='utf8'))
for r in rows:
    r['path']=r['path'].replace('docs/pt-BR/rules/','docs/tr/rules/common/')
    r['reason']=r['reason'].replace('Portuguese','Turkish')
    name=r['path'].split('/')[-1]
    if name=='agents.md':r['reason']='Full Turkish semantic comparison retains plugin namespace/router, role/task routing including Rust, independent parallel reviews and diverse lenses. Omits current HarmonyOS row and delegated-result completion/collection/depth contract. No new mechanism; namespace presence is not usable-capability proof.'
    if name=='git-workflow.md':r['reason']='Complete Turkish semantic equivalent of full-history/triple-dot PR summary, commit format, explicit attribution choice and real development-workflow relative router. TODO test plan is planned rather than executed evidence.'
development=next(r for r in json.loads((out/'ecc-variants-common-zh.json').read_text(encoding='utf8')) if r['path'].endswith('/development-workflow.md'))
development['path']=development['path'].replace('docs/zh-CN/','docs/tr/')
development['reason']=development['reason'].replace('Complete comparison','Complete Turkish semantic comparison')
rows.append(development)
(out/'ecc-variants-common-tr.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
