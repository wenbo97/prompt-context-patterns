"""Record reviewed variant batches with explicit depth and rationale."""
import pathlib,json,sys
OUT=pathlib.Path(__file__).resolve().parent
state=json.loads((OUT/'ecc-variants-state.json').read_text(encoding='utf-8'))
harvest=json.loads((OUT/'harvest-ecc.json').read_text(encoding='utf-8'))
keys={}
for c in harvest['candidates']:
    for source in c.get('sources',[]):keys.setdefault(source['path'],[]).append(c['key'])
prefix=sys.argv[1];start=int(sys.argv[2]);size=int(sys.argv[3]);reason=sys.argv[4]
rows=[r for r in state['coverage'] if r['path'].startswith(prefix) and r['disposition']=='pending'][start:start+size]
for r in rows:
    r.update(disposition='analyzed',depth='full-canonical-delta' if r['counterpart'] else 'full-method-text',reason=reason,candidate_keys=sorted(set(keys.get(r['counterpart'],[]))))
    if r['path'].endswith('agents/openai.yaml'):
        r['candidate_keys']=['legacy-190']
        r['reason']='Full seven-field adapter read: display labels, color and default explicit skill invocation plus allow_implicit_invocation=true. This specializes host-specific invocation metadata (#190); it adds no new task mechanism.'
counts={status:sum(r['disposition']==status for r in state['coverage']) for status in ('analyzed','duplicate','excluded','pending')}
state['summary'].update(counts)
state['summary']['status']='complete' if counts['pending']==0 else 'in_progress'
payload=(json.dumps(state,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode()
(OUT/'ecc-variants-state.json').write_bytes(payload)
(OUT/'harvest-ecc-variants.json').write_bytes(payload)
print('Recorded',len(rows),'paths;',state['summary'])
