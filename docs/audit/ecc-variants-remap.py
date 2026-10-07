"""Refresh evidence mappings without changing any review disposition."""
import pathlib,json,collections
out=pathlib.Path(__file__).resolve().parent
s=json.loads((out/'ecc-variants-state.json').read_text(encoding='utf8'))
h=json.loads((out/'harvest-ecc.json').read_text(encoding='utf8'))
valid={c['key'] for c in h['candidates']}|{c['key'] for c in s['candidates']}
by_source={}
for c in h['candidates']+s['candidates']:
    for source in c.get('sources',[]):by_source.setdefault(source['path'],set()).add(c['key'])
for r in s['coverage']:
    if r['disposition']=='pending':continue
    legacy=[int(k.split('-')[1]) for k in r['candidate_keys'] if k.startswith('legacy-')]
    if legacy:r['existing_ids']=sorted(set(r.get('existing_ids',[])+legacy))
    keys={k for k in r['candidate_keys'] if k in valid}
    keys|=by_source.get(r['path'],set())|by_source.get(r['counterpart'],set())
    r['candidate_keys']=sorted(keys)
    if r['path'].startswith('docs/') and r['depth']=='full-canonical-delta':r['depth']='full-semantic-comparison'
counts=collections.Counter(r['disposition'] for r in s['coverage'])
s['summary'].pop('duplicates',None)
s['summary'].update(dict(counts))
s['summary']['status']='complete' if counts['pending']==0 else 'in_progress'
s['summary']['remaining_by_locale']=dict(collections.Counter(r['path'].split('/')[1] for r in s['coverage'] if r['disposition']=='pending'))
s['summary']['harness_status']='complete' if not any(r['disposition']=='pending' and any(r['path'].startswith(h+'/') for h in s['partition']['harnesses']) for r in s['coverage']) else 'in_progress'
s['summary']['candidate_count']=len(s['candidates'])
s['summary']['body_duplicate_wrapper_reviews']=sum('body_duplicate_of' in r for r in s['coverage'])
s['summary']['coverage_candidate_links_role']='Comparison targets, not source proof. Reasons distinguish mechanisms retained and omitted; only candidate sources are pinned positive provenance.'
payload=(json.dumps(s,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode()
(out/'ecc-variants-state.json').write_bytes(payload)
(out/'harvest-ecc-variants.json').write_bytes(payload)
print(json.dumps(s['summary'],ensure_ascii=False))
