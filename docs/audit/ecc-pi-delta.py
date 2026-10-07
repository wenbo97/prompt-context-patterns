import difflib, importlib.util, json, pathlib, sys
out=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('ecc_corpus',out/'ecc-corpus.py')
corpus=importlib.util.module_from_spec(spec)
sys.argv=[sys.argv[0],'library']
spec.loader.exec_module(corpus)
ledger=json.loads((out/'ecc-review-ledger.json').read_text(encoding='utf-8'))
inventory=json.loads((out/'ecc-inventory.json').read_text(encoding='utf-8'))
files={r['path']:r for r in inventory}
results=[]
for p in ledger['pending_partitions']['other']:
    if not p.startswith('pi/core/') or not p.endswith('.md'): continue
    suffix=p.removeprefix('pi/core/')
    source=suffix.replace('skills/ecc-council/','skills/council/')
    if source not in files: continue
    if source not in ledger['reviews']:
        raise ValueError('Canonical source not semantically reviewed: '+source)
    original=corpus.text(source).splitlines()
    variant=corpus.text(p).splitlines()
    changes=list(difflib.unified_diff(original,variant,fromfile=source,tofile=p,n=3))
    results.append({'path':p,'hash':files[p]['hash'],'canonical':source,
                    'canonical_hash':files[source]['hash'],'canonical_review_depth':ledger['reviews'][source]['depth'],
                    'source_lines':len(original),'variant_lines':len(variant),'delta':changes})
    print('\n### '+p+' compared with '+source)
    print('\n'.join(changes) if changes else 'Exact complete line equality')
(out/'ecc-pi-deltas.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Compared',len(results),'complete files')
