"""Persist individually read Japanese Java/Kotlin/Rust semantic comparisons."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
rows=[r for r in json.loads((out/'ecc-variants-zh-domain-3.json').read_text(encoding='utf8')) if r['path'].split('/')[3] in ('java','kotlin','rust')]
overrides={
'java/patterns.md':'Same repository/service/constructor/DTO/builder/sealed-state/response recipes; all Java/Spring/Quarkus/JPA routers preserved and Japanese Quarkus description correctly retains current REST/Panache/messaging, unlike Chinese Camel wording. Application Java code excluded from new prompt method.',
'java/testing.md':'Same JUnit/Mockito/Testcontainers, layer-mirrored and behavior-named tests and coverage/source routers. Japanese Quarkus pointer retains canonical RESTAssured/DevServices wording, unlike Chinese Camel wording. Fixed80%/skip-trivial defaults are not behavior proof.'}
for row in rows:
    row['path']=row['path'].replace('docs/zh-CN/','docs/ja-JP/')
    key='/'.join(row['path'].split('/')[-2:])
    if key in overrides:row['reason']=overrides[key]
    row['reason']='Full Japanese method prose/predicates/pointers/shell/XML/templates read and compared with previously completely read same canonical fields. '+row['reason']
    row['reason']+=' Domain implementation examples excluded from prompt-method authorship; no whole-body duplicate claim or source execution.'
(out/'ecc-variants-jp-domain-4.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
