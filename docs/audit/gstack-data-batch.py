"""Display actual parsed container roles. Marking records scoped review only."""
import argparse
import json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--mark-last',action='store_true');p.add_argument('--cap',type=int,default=27000);a=p.parse_args()
target=Path('docs/audit/gstack-data-review.json');last=Path('.tools/gstack/current-data.json')
state=json.loads(target.read_text('utf-8')) if target.exists() else {'scope':'Parsed field roles, declared provenance and embedded method fields; not full semantic review of raw observations.','containers':{}}
if a.mark_last:
    state['containers'].update(json.loads(last.read_text('utf-8')))
    target.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n','utf-8',newline='')
shapes=json.loads(Path('.tools/gstack/support-data-shapes.json').read_text('utf-8'))
chosen={};out=[];size=0
for name,r in shapes.items():
    if name in state['containers']:continue
    shown={'path':name,'top_keys':r['top_keys'],'field_roles':r['field_roles'][:8],'value_types':r['value_types'],'purpose_notes':r['purpose_notes'][:1],
           'method_fields':[{'path':m['path'],'sha256':m['sha256'],'chars':m['chars']} for m in r['method_fields']]}
    text=json.dumps(shown,ensure_ascii=False,separators=(',',':'))+'\n'
    if chosen and size+len(text)>a.cap:break
    size+=len(text);out.append(text)
    chosen[name]={'source_hash':r['sha256'],'git_oid':r['git_oid'],'inspection':'Whole JSON parsed structurally; displayed field roles/provenance reviewed. Raw domain observations are scoped, embedded method fields separately read.','top_keys':r['top_keys'],'field_roles':r['field_roles'],'value_types':r['value_types'],
                  'method_fields':[{'path':m['path'],'sha256':m['sha256'],'chars':m['chars']} for m in r['method_fields']]}
last.write_text(json.dumps(chosen,ensure_ascii=False),'utf-8')
print(json.dumps({'remaining':len(shapes)-len(state['containers']),'displayed':len(chosen),'chars':size}));print(''.join(out))
