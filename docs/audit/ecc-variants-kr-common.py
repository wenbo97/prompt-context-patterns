"""Record the completed Korean common-rule full semantic batch."""
import json,pathlib
out=pathlib.Path(__file__).resolve().parent
rows=json.loads((out/'ecc-variants-common-pt.json').read_text(encoding='utf8'))
for r in rows:
    r['path']=r['path'].replace('docs/pt-BR/','docs/ko-KR/')
    r['reason']=r['reason'].replace('Portuguese','Korean')
    if r['path'].endswith('/agents.md'):r['reason']='Complete Korean semantic comparison retains role/task routing, independent parallel reviews and diverse lenses, adding database/Go role examples to old user agent directory. Omits current plugin namespace/router and delegated-result completion/collection/depth contract. Domain role selection is a specialization, not a new method; presence is not usable dispatch proof.'
(out/'ecc-variants-common-kr.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
