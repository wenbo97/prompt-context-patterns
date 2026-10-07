"""Record explicit reviewed path decisions; never closes a family from its name."""
import pathlib,json,sys,collections
OUT=pathlib.Path(__file__).resolve().parent
state=json.loads((OUT/'ecc-variants-state.json').read_text(encoding='utf8'))
harvest=json.loads((OUT/'harvest-ecc.json').read_text(encoding='utf8'))
source_keys={}
for candidate in harvest['candidates']:
    for source in candidate.get('sources',[]):
        source_keys.setdefault(source['path'],set()).add(candidate['key'])
decisions=json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf8'))
indexed={r['path']:r for r in state['coverage']}
for decision in decisions:
    row=indexed[decision['path']]
    assert row['disposition']=='pending',row['path']
    row.update(disposition=decision.get('disposition','analyzed'),depth=decision.get('depth','full-semantic-comparison'),reason=decision['reason'])
    row['candidate_keys']=sorted(set(decision.get('candidate_keys',[]))|source_keys.get(row['counterpart'],set()))
    if 'existing_ids' in decision:row['existing_ids']=decision['existing_ids']
    for field in ('body_duplicate_of','body_hash','wrapper_review'):
        if field in decision:row[field]=decision[field]
counts=collections.Counter(r['disposition'] for r in state['coverage'])
state['summary'].update(dict(counts))
state['summary']['status']='complete' if not counts['pending'] else 'in_progress'
payload=(json.dumps(state,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode()
(OUT/'ecc-variants-state.json').write_bytes(payload)
(OUT/'harvest-ecc-variants.json').write_bytes(payload)
print('Recorded',len(decisions),'explicit decisions;',dict(counts))
