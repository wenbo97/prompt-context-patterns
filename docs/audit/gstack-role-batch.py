"""Display actual support structures for scoped review; records are not full-body reads."""
import argparse
import json
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('prefix', nargs='?', default='bin/')
p.add_argument('--mark-last', action='store_true')
p.add_argument('--cap', type=int, default=18000)
p.add_argument('--compact', action='store_true')
p.add_argument('--terse', action='store_true')
p.add_argument('--tests-brief', action='store_true')
a=p.parse_args()
state_path=Path('docs/audit/gstack-support-role-review.json')
state=json.loads(state_path.read_text('utf-8')) if state_path.exists() else {'repo':'garrytan/gstack','commit':'f30b7b788a210d217ea3125bf3001b29cbc2a463','depth':'Scoped content/structure inspection; no full runtime correctness audit. Embedded prompts and method contracts are reviewed separately.','role_reviewed':{}}
last=Path('.tools/gstack/current-roles.json')
if a.mark_last:
    state['role_reviewed'].update(json.loads(last.read_text('utf-8')))
    state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n','utf-8',newline='')
full_files={r['path'] for r in json.loads(Path('docs/audit/harvest-gstack.json').read_text('utf-8'))['coverage'] if r['disposition']=='analyzed'}
data_path=Path('docs/audit/gstack-data-review.json')
data_files=set(json.loads(data_path.read_text('utf-8'))['containers']) if data_path.exists() else set()
todo=[r for r in json.loads(Path('.tools/gstack/support-shapes.json').read_text('utf-8')) if r['path'].startswith(a.prefix) and r['path'] not in state['role_reviewed'] and r['path'] not in full_files and r['path'] not in data_files]
chosen={}; chunks=[];size=0
for r in todo:
    literals=r.get('literals',[])
    display={k:r[k] for k in ['path','bytes','kind','first_lines','leading_comment','imports','symbols','checks','parse_errors','magic_hex'] if k in r}
    if len(display.get('symbols',[]))>25: display['symbols']={'count':len(display['symbols']),'first25':display['symbols'][:25]}
    if len(display.get('checks',[]))>15: display['checks']={'count':len(display['checks']),'first15':display['checks'][:15]}
    display['embedded_input_literals']=sum(l.get('agentOwner',False) for l in literals)
    display['other_long_literals']=[{'start':l['start'],'owners':l['owners'],'chars':l['chars'],'begins':l['text'][:100]} for l in literals if not l.get('agentOwner') and l['chars']>=120][:8]
    display['other_long_literal_count']=sum(not l.get('agentOwner') and l['chars']>=120 for l in literals)
    if a.tests_brief:
        value=json.dumps({'path':r['path'],'source_opening':r.get('first_lines','')[:200],
                         'imports':r.get('imports',[])[:4],'declarations':r.get('symbols',[])[:5],
                         'contracts':r.get('checks',[])[:6],'contract_count':len(r.get('checks',[])),
                         'embedded_inputs':display['embedded_input_literals'],
                         'other_values':[(l['start'],l['owners'],l['text'][:55]) for l in literals if not l.get('agentOwner')][:2]},ensure_ascii=False,separators=(',',':'))+'\n'
    elif a.terse:
        value=json.dumps({'path':r['path'],'bytes':r['bytes'],
                         'source_opening':r.get('first_lines','')[:380],
                         'imports':r.get('imports',[])[:5],
                         'declarations':r.get('symbols',[])[:8],
                         'test_contracts':r.get('checks',[])[:8],
                         'test_contract_count':len(r.get('checks',[])),
                         'embedded_input_literals':display['embedded_input_literals'],
                         'long_value_roles':[(l['start'],l['owners'],l['text'][:75]) for l in literals if not l.get('agentOwner')][:5],
                         'magic':r.get('magic_hex')},ensure_ascii=False,separators=(',',':'))+'\n'
    elif a.compact:
        display={k:v for k,v in display.items() if k not in ['parse_errors','other_long_literals']}
        # Compact source structures are scoped relevance evidence only. Essential
        # contracts and embedded methods must still be read in their own ledgers.
        display['first_lines']=display.get('first_lines','')[:750]
        if display.get('leading_comment'): display['leading_comment']=display['leading_comment'][:1000]
        value=json.dumps(display,ensure_ascii=False,separators=(',',':'))+'\n'
    else:
        value=json.dumps(display,ensure_ascii=False,indent=2)+'\n'
    if chosen and size+len(value)>a.cap:break
    size+=len(value);chunks.append(value)
    chosen[r['path']]={'sha256':r['sha256'],'git_oid':r['git_oid'],'bytes':r['bytes'],'inspection':'Selected frozen source opening, imports/declarations, test-call roles, binary signature and literal ownership inspected. The AST extraction is a structural inventory; displayed samples and separately reviewed literals support scoped relevance, never full-file semantic completion.','display_mode':'tests-brief' if a.tests_brief else 'terse' if a.terse else 'compact' if a.compact else 'expanded','embedded_literal_hashes':[l['sha256'] for l in literals if l.get('agentOwner')],'structural_evidence':{k:display[k] for k in ['kind','imports','symbols','checks','parse_errors','magic_hex'] if k in display}}
last.write_text(json.dumps(chosen,ensure_ascii=False),'utf-8')
print(json.dumps({'prefix':a.prefix,'pending_role_rows':len(todo),'displayed':len(chosen),'chars':size}))
print(''.join(chunks))
