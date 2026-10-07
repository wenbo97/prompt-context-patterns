"""Reconcile missing counterpart paths without resetting completed review records."""
import json,pathlib
OUT=pathlib.Path(__file__).resolve().parent;state=json.loads((OUT/'ecc-variants-state.json').read_text(encoding='utf-8'))
inventory=json.loads((OUT/'source-inventory.json').read_text(encoding='utf-8'));repo=next(r for r in inventory['repositories'] if r['repo']==state['repo']);paths={f['path'] for f in repo['files']}
changes=0
for r in state['coverage']:
    if r['counterpart']:continue
    p=r['path'];parts=p.split('/')
    if parts[0] in ('.cursor','.kiro') and len(parts)>2 and parts[1] in ('rules','steering'):
        name=parts[-1].removesuffix('.mdc').removesuffix('.md');language,sep,rule=name.partition('-');c=f'rules/{language}/{rule}.md'
        if c in paths:r['counterpart']=c;changes+=1
    if parts[0]=='.opencode' and parts[1]=='prompts' and parts[2]=='agents':
        c='agents/'+'/'.join(parts[3:]);c=c.removesuffix('.txt')+'.md' if c.endswith('.txt') else c
        if c in paths:r['counterpart']=c;changes+=1
    if parts[0]=='docs' and len(parts)==4 and parts[2]=='rules':
        c='rules/common/'+parts[-1]
        if c in paths:r['counterpart']=c;changes+=1
payload=(json.dumps(state,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode();(OUT/'ecc-variants-state.json').write_bytes(payload);(OUT/'harvest-ecc-variants.json').write_bytes(payload)
print('Reconciled',changes,'counterparts')
