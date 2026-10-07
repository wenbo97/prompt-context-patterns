"""Pin actual achieved-mode omissions in translated evaluator instructions."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
s=json.loads((out/'ecc-variants-state.json').read_text(encoding='utf8'))
row=next(r for r in s['coverage'] if r['path']=='docs/zh-CN/agents/gan-evaluator.md')
row['proof']=[]
for path,start,end,section in [('agents/gan-evaluator.md',36,42,'Actual available evaluation mode before testing'),('agents/gan-evaluator.md',129,144,'Achieved mode in feedback'),('docs/zh-CN/agents/gan-evaluator.md',28,38,'Translated workflow lacks mode preflight'),('docs/zh-CN/agents/gan-evaluator.md',124,141,'Translated feedback jumps from scores to verdict without achieved mode')]:
    row['proof'].append({'repo':s['repo'],'commit':s['commit'],'path':path,'start_line':start,'end_line':end,'section':section,'role':'comparison-context','url':f'https://github.com/{s["repo"]}/blob/{s["commit"]}/{path}#L{start}-L{end}'})
payload=(json.dumps(s,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode()
(out/'ecc-variants-state.json').write_bytes(payload)
(out/'harvest-ecc-variants.json').write_bytes(payload)
