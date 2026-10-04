"""Explicitly reuse decisions after reading these fifteen Japanese method bodies."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
rows=json.loads((out/'ecc-variants-zh-domain-1.json').read_text(encoding='utf8'))
for row in rows:
    row['path']=row['path'].replace('docs/zh-CN/','docs/ja-JP/')
    row['reason']=row['reason'].replace('Simplified Chinese','Japanese')
    row['reason']+=' Japanese predicates, literal commands and resources were individually read; no material prose/pointer/control delta found. Programming-language application examples remain explicitly excluded domain detail, not a claimed full-body duplicate.'
(out/'ecc-variants-jp-domain-1.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
