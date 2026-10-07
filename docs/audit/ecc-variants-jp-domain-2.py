"""Decisions after individual Japanese PHP, Perl and Swift method-body reads."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
rows=[r for r in json.loads((out/'ecc-variants-zh-domain-2.json').read_text(encoding='utf8')) if r['path'].split('/')[3] in ('php','perl','swift')]
for row in rows:
    row['path']=row['path'].replace('docs/zh-CN/','docs/ja-JP/')
    row['reason']='Complete Japanese semantic comparison to the previously fully read same canonical counterpart: '+row['reason']
    row['reason']+=' All Japanese method prose/path predicates/common and skill pointers/shell examples read; no material control/pointer delta. Programming-language application code excluded as domain detail, not assumed body duplication.'
(out/'ecc-variants-jp-domain-2.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
