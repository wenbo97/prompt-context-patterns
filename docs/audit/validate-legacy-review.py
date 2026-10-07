"""Validate the audit's coverage, content contracts and pinned evidence."""
import json,pathlib,re,subprocess,hashlib,collections
ROOT=pathlib.Path(__file__).resolve().parents[2];OUT=ROOT/'docs/audit';BASE=pathlib.Path('D:/Projects/open-skills')
d=json.loads((OUT/'legacy-review.json').read_text(encoding='utf-8'));ps=d['patterns'];numeric=[p for p in ps if isinstance(p['id'],int)]
assert sorted(p['id'] for p in numeric)==list(range(1,207))
assert sorted(p['id'] for p in ps if isinstance(p['id'],str))==['K1','K2','K3','K4','K5','K6']
by={p['id']:p for p in ps};fields={'description','scenario','mechanism','bad','good','why','expected','boundaries'};spans=[]
for p in ps:
    assert p['status'] in ('active','merged','removed','new'),p['id']
    assert set(p['scores'])=={'scenario','mechanism','contrast','observable','boundaries'}
    assert all(v in (0,1,2) for v in p['scores'].values())
    if p['status'] in ('active','new'):
        assert sum(p['scores'].values())>=8 and all(p['scores'][x]==2 for x in ('scenario','mechanism','contrast'))
        for lang in ('en','zh'):
            c=p['content'][lang];assert set(c)==fields,(p['id'],lang,set(c))
            assert all(isinstance(v,str) and v.strip() for v in c.values()),p['id']
            assert c['bad']!=c['good'],p['id']
            assert not any('^' in v or '~The ' in v for v in c.values()),p['id']
        if p['trace_status']=='untraced':assert 'source-unconfirmed' in p['tags']
        if p['status']=='new':assert p['candidate_key'].startswith('core-karpathy-')
    if p['status']=='merged':
        assert by[p['merged_into']]['status']=='active',p['id']
    assert all(by[id]['status']=='active' for id in p.get('related_ids',[])),p['id']
    assert p['origin_status']=='unknown',p['id']
    assert bool(p['sources'])==(p['trace_status']=='traced'),p['id']
    for s in p['sources']:
        assert re.fullmatch('[0-9a-f]{40}',s['commit']),s
        repo=BASE/s['repo'];head=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip();assert head==s['commit']
        f=repo/s['path'];lines=f.read_text(encoding='utf-8-sig').splitlines()
        assert 1<=s['start_line']<=s['end_line']<=len(lines),s
        assert s['url']==f"https://github.com/{s['repo']}/blob/{s['commit']}/{s['path']}#L{s['start_line']}-L{s['end_line']}"
        assert s['role']=='observed-example' and s['license']
        spans.append((s['repo'],s['path'],s['start_line'],s['end_line']))
result={'passed':True,'numeric_ids':206,'karpathy_aliases':6,'active_numeric':sum(p['status']=='active' for p in numeric),'unique_karpathy_candidates':len({p['candidate_key'] for p in ps if p['status']=='new'}),'validated_source_records':len(spans),'distinct_source_ranges':len(set(spans)),'bilingual_fields_per_retained_entry':16,'nonpattern_pages':len(d['nonpattern_pages']),'status_counts':dict(collections.Counter(p['status'] for p in ps))}
(OUT/'legacy-validation.json').write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8'))
print(json.dumps(result,ensure_ascii=False))
