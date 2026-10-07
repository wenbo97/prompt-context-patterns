"""Record eleven individually read Japanese Python/TypeScript method files."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
rows=[r for r in json.loads((out/'ecc-variants-zh-domain-2.json').read_text(encoding='utf8')) if '/python/' in r['path']]
rows += [r for r in json.loads((out/'ecc-variants-zh-domain-3.json').read_text(encoding='utf8')) if '/typescript/' in r['path']]
for row in rows:
    row['path']=row['path'].replace('docs/zh-CN/','docs/ja-JP/')
    row['reason']='Complete Japanese semantic comparison to the previously fully read same canonical method fields: '+row['reason']
    row['reason']+=' Individually read Japanese prose, predicates, resource pointers and shell commands; no material method control/pointer delta found. Application-language implementation examples explicitly excluded domain detail.'
rows.append({'path':'docs/ja-JP/rules/python/fastapi.md','reason':'Complete Japanese and canonical method prose/path predicates/reference read. Same scoped FastAPI-plus-general rules, create_app/thin-router/dependency session/auth, async I/O, distinct input/update/response schemas and nonsecret response fields, contextual CORS/JWT/rate/log policy and exact dependency override with cleanup after tests. Domain FastAPI API implementation excluded from new prompt-method authorship; configured rules are not actual runtime capability/security proof. No new variant mechanism.','existing_ids':[23,53]})
(out/'ecc-variants-jp-domain-3.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
