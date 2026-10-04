"""Persist sixteen Turkish rule files only after complete individual method reading."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
rows=json.loads((out/'ecc-variants-es-domain.json').read_text(encoding='utf8'))
for row in rows:
    row['path']=row['path'].replace('docs/es/','docs/tr/')
    row['reason']=row['reason'].replace('Spanish','Turkish')
    row['reason']=row['reason'].replace(' Final idioms description is mistranslated as idiomas (languages), without changing the target skill identifier.','')
(out/'ecc-variants-tr-domain.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
