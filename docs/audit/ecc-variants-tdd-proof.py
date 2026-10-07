"""Pin the retry-success versus all-trials-success translation error."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
s=json.loads((out/'ecc-variants-state.json').read_text(encoding='utf8'))
row=next(r for r in s['coverage'] if r['path']=='docs/zh-CN/agents/tdd-guide.md')
row['proof']=[]
for path,start,end,section in [('agents/tdd-guide.md',91,100,'Release-critical pass^3 requirement'),('docs/zh-CN/agents/tdd-guide.md',87,96,'Translated release gate says pass@3')]:
    row['proof'].append({'repo':s['repo'],'commit':s['commit'],'path':path,'start_line':start,'end_line':end,'section':section,'role':'comparison-context','url':f'https://github.com/{s["repo"]}/blob/{s["commit"]}/{path}#L{start}-L{end}'})
payload=(json.dumps(s,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode()
(out/'ecc-variants-state.json').write_bytes(payload)
(out/'harvest-ecc-variants.json').write_bytes(payload)
