"""Display embedded agent-input literals, with exact ownership/location; no file closure."""
import argparse
import json
from pathlib import Path
p = argparse.ArgumentParser()
p.add_argument('--mark-last', action='store_true')
p.add_argument('--cap', type=int, default=25000)
p.add_argument('--prefix', default='test/')
p.add_argument('--all-literals', action='store_true')
p.add_argument('--skip-runtime-markup', action='store_true')
a=p.parse_args()
report=json.loads(Path('docs/audit/harvest-gstack.json').read_text('utf-8'))
full_files={r['path'] for r in report['coverage'] if r['disposition']=='analyzed'}
state_path=Path('docs/audit/gstack-embedded-review.json')
state=json.loads(state_path.read_text('utf-8')) if state_path.exists() else {'repo':'garrytan/gstack','commit':'f30b7b788a210d217ea3125bf3001b29cbc2a463','read_literals':{},'scope':'Embedded literal review only; not full source-file review.'}
last=Path('.tools/gstack/current-literals.json')
if a.mark_last:
    state['read_literals'].update(json.loads(last.read_text('utf-8')))
    state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n','utf-8',newline='')
todo={}
for r in json.loads(Path('.tools/gstack/support-shapes.json').read_text('utf-8')):
    if not r['path'].startswith(a.prefix): continue
    if r['path'] in full_files: continue # Full-body review already covers every literal.
    for l in r.get('literals',[]):
        if a.skip_runtime_markup and l['text'].lstrip('`\"\' \n').lower().startswith(('<!doctype','<div','<li','<html')):
            continue # Runtime HTML construction is covered by the source-role ledger.
        if (l.get('agentOwner') or a.all_literals) and l['sha256'] not in state['read_literals']:
            todo.setdefault(l['sha256'],{'text':l['text'],'locations':[]})['locations'].append({'path':r['path'],'start':l['start'],'end':l['end'],'owners':l['owners']})
out=[]; chosen={}; size=0
for h,item in todo.items():
    value='\nLITERAL '+h+'\n'+str(item['locations'][0])+'; exact occurrences='+str(len(item['locations']))+'\n'+item['text']+'\n'
    if chosen and size+len(value)>a.cap: break
    size+=len(value);out.append(value);chosen[h]={'locations':item['locations'],'review':'Complete literal read; enclosing source role and other inputs reviewed separately.'}
last.write_text(json.dumps(chosen,ensure_ascii=False),'utf-8')
print(json.dumps({'pending_unique_literals':len(todo),'displayed':len(chosen),'chars':size}))
print(''.join(out))
