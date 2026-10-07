"""Decisions from the completed Spanish common-rule semantic batch."""
import json,pathlib
out=pathlib.Path(__file__).resolve().parent
rows=json.loads((out/'ecc-variants-common-pt.json').read_text(encoding='utf8'))
for r in rows:
    r['path']=r['path'].replace('docs/pt-BR/rules/','docs/es/rules/common/')
    r['reason']=r['reason'].replace('Portuguese','Spanish')
    name=r['path'].split('/')[-1]
    if name=='agents.md':r['reason']='Full Spanish semantic comparison retains current plugin namespace/router and full abbreviated roster, independent work and multiple lenses; omits delegation completion/result-collection/depth contract. No new mechanism and frozen namespace is not live capability proof.'
    if name=='coding-style.md':r['reason']='Full Spanish comparison retains KISS/DRY/YAGNI, immutable contrast, validation/error/quality checklist and smell explanations. Older hard800-line policy and JS-specific camelCase/PascalCase/use naming omit canonical language-dependent naming and soft source-role exceptions. These are application policy deltas, not new agent methods.'
    if name=='git-workflow.md':r['reason']='Complete semantic equivalent of full-history/triple-dot PR summary, commit format, user attribution choice and real relative development-workflow router. TODO test plan is planned rather than executed evidence.'
    if name=='performance.md':r['reason']='Full Spanish comparison retains complexity tiers, context headroom, critique lenses and iterative build verification; pinned model versions and default/token/90%/3x claims remain unverified. Bash-only budget cap omits canonical PowerShell form; actual host setting/capability needs separate proof.'
    if name=='testing.md':r['reason']='Complete Spanish semantic equivalent including intended-failure RED/minimal GREEN, wrong-test correction, isolation, Arrange-Act-Assert and descriptive behavior names. TS implementation examples are domain detail; universal80% and all-test-type defaults are not behavior assurance.'
development=next(r for r in json.loads((out/'ecc-variants-common-jp.json').read_text(encoding='utf8')) if r['path'].endswith('/development-workflow.md'))
development['path']=development['path'].replace('docs/ja-JP/','docs/es/')
development['reason']=development['reason'].replace('Japanese','Spanish')
rows.append(development)
(out/'ecc-variants-common-es.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
