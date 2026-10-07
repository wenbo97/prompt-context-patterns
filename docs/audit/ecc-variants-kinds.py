"""Backfill honest review labels and link existing explicit decision/compare ledgers."""
import pathlib,json,collections
OUT=pathlib.Path(__file__).resolve().parent
state=json.loads((OUT/'ecc-variants-state.json').read_text(encoding='utf8'))
lookup={}
def visit(value,filename):
    if isinstance(value,list):
        for x in value:visit(x,filename)
    elif isinstance(value,dict):
        if isinstance(value.get('path'),str) and isinstance(value.get('reason'),str):
            lookup.setdefault((value['path'],value['reason']),[]).append('docs/audit/'+filename+'#'+value['path'])
        for k,v in value.items():
            if isinstance(k,str) and '/' in k and isinstance(v,str):
                lookup.setdefault((k,v),[]).append('docs/audit/'+filename+'#'+k)
            elif isinstance(v,(dict,list)):visit(v,filename)
for p in OUT.glob('ecc-variants-*.json'):
    if p.name in ['ecc-variants-state.json','ecc-variants-validation.json','ecc-variants-review-evidence.json']:continue
    try:visit(json.loads(p.read_text(encoding='utf8')),p.name)
    except (ValueError,UnicodeError):pass
for row in state['coverage']:
    if row['disposition']=='pending':
        row['review_kind']=None;row['review_evidence']=[];continue
    # Correct a previous batch-level note accidentally repeated on unrelated files.
    stale='Backend mirror retains per-process limiter removed from canonical, so record stale domain implementation, not semantic equivalence or a new prompt method. '
    if row['path']!='.agents/skills/backend-patterns/SKILL.md' and stale in row['reason']:
        row['reason']=row['reason'].replace(stale,'')
        row['note_correction']='Removed irrelevant batch-level backend note; actual canonical-delta read and metadata decision unchanged.'
    d=row['depth']
    if row['disposition']=='duplicate' or 'exact-body' in d or d.startswith('verified-method-equivalence'):
        kind='verified-equivalence'
    elif row['disposition']=='excluded' or d in ['data-structure-inspection','full-stub-text','full-nonpattern-text']:
        kind='scoped-relevance'
    elif 'delta' in d or 'comparison' in d or row.get('counterpart'):
        kind='difference-review'
    else:kind='full-semantic'
    row['review_kind']=kind
    evidence=lookup.get((row['path'],row['reason']),[])
    row['review_evidence']=sorted(set(evidence)) or ['docs/audit/ecc-variants-state.json#coverage/'+row['path']]
    if row.get('body_duplicate_of') or row.get('duplicate_of'):
        row['review_evidence'].append('docs/audit/ecc-variants-state.json#duplicate-proof/'+row['path'])
    if row.get('comparison_proof'):
        row['review_evidence'].append('docs/audit/ecc-variants-state.json#comparison-proof/'+row['path'])
counts=collections.Counter(r['review_kind'] for r in state['coverage'] if r['disposition']!='pending')
state['summary']['review_kinds']=dict(counts)
state['summary']['review_kind_policy']='Labels describe actual method/difference/equivalence/relevance work; depth is preserved. Evidence links explicit read/compare decisions, not executed upstream behavior.'
proof={'repo':state['repo'],'commit':state['commit'],'coverage':[{k:r.get(k) for k in ['path','hash','git_blob','disposition','depth','review_kind','review_evidence','reason','note_correction']} for r in state['coverage']],'summary':{'closed':sum(counts.values()),'pending':state['summary']['pending'],'review_kinds':dict(counts)}}
for name,obj in [('ecc-variants-state.json',state),('harvest-ecc-variants.json',state),('ecc-variants-review-evidence.json',proof)]:
    (OUT/name).write_bytes((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
print(json.dumps(proof['summary'],ensure_ascii=False))
