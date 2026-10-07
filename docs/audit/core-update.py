from pathlib import Path
import json, subprocess, hashlib, copy, collections

OUT=Path('D:/Projects/prompt-context-patterns-refresh/docs/audit')
INVENTORY=json.loads((OUT/'source-inventory.json').read_text(encoding='utf-8'))
DATA=json.loads((OUT/'harvest-core.json').read_text(encoding='utf-8'))
BY_REPO={r['repo']:r for r in INVENTORY['repositories']}
LEGACY=json.loads((OUT/'legacy-review.json').read_text(encoding='utf-8'))

def blob(repo,path):
    meta=next(f for f in BY_REPO[repo]['files'] if f['path']==path)
    root=Path('D:/Projects/open-skills')/repo
    return subprocess.check_output(['git','-C',str(root),'cat-file','blob',meta['blob']]).decode('utf-8')

def src(repo,path,start,end,section):
    commit=BY_REPO[repo]['commit'];text=blob(repo,path)
    assert 1<=start<=end<=len(text.splitlines()),(repo,path,start,end,len(text.splitlines()))
    names={f['path'] for f in BY_REPO[repo]['files']};parent=Path(path).parent;license_path=None;license='no-explicit-license'
    while True:
        for name in ['LICENSE','LICENSE.md','LICENSE.txt']:
            p=str(parent/name).replace('\\','/')
            if p in names:license_path=p;break
        if license_path or str(parent)=='.':break
        parent=parent.parent
    if license_path:
        l=blob(repo,license_path)
        license='Apache-2.0' if 'Apache License' in l else ('MIT' if 'MIT License' in l or 'Permission is hereby granted, free of charge' in l else 'source-available / inspect local license')
    elif 'license: MIT' in text or repo=='multica-ai/andrej-karpathy-skills':license='MIT declaration; no standalone root license'
    return dict(repo=repo,commit=commit,path=path,line_start=start,line_end=end,section=section,license=license,license_path=license_path,role='observed-example',url=f'https://github.com/{repo}/blob/{commit}/{path}#L{start}-L{end}')

def add(key,en,zh,cat,sources,en8,zh8,ids=None,legacy_keys=None,status=None):
    fields=['description','scenario','mechanism','bad','good','why','expected','boundaries']
    assert len(en8)==len(zh8)==8
    ids=ids or [];key='core-'+key
    candidate=dict(key=key,name={'en':en,'zh':zh},category=cat,tags=[cat]+list(dict.fromkeys(s[0].split('/')[0] for s in sources)),status=status or ('merged' if ids else 'active'),reason='Same mechanism as the named existing entry; source evidence enriches it.' if ids else 'Distinct reusable mechanism with concrete editorial contrast and observable limits.',suggested_existing_ids=ids,suggested_existing_keys=legacy_keys or [],content={'en':dict(zip(fields,en8)),'zh':dict(zip(fields,zh8))},sources=[src(*s) for s in sources],example_origin='project-authored-teaching-construction',scores={'scenario':2,'mechanism':2,'contrast':2,'observable':2,'boundaries':2},quality_total=10,efficacy_status='editorial-review-only',original_origin_status='earliest-origin-not-established')
    DATA['candidates']=[c for c in DATA['candidates'] if c['key']!=key]+[candidate]
    return key

def merged(key,id,sources):
    row=next(p for p in LEGACY['patterns'] if p['id']==id)
    if 'content' in row:content=copy.deepcopy(row['content'])
    else:
        cases=json.loads((OUT/'core-legacy-cases.json').read_text(encoding='utf-8'));case=cases[str(id)]
        desc_en=case[2]
        desc_zh=case[7]
        content={'en':{'description':desc_en,'scenario':case[0],'bad':case[1],'good':case[2],'mechanism':case[2],'why':'The required behavior is explicit instead of relying on an unsupported assumption.','expected':case[3],'boundaries':case[4]},'zh':{'description':desc_zh,'scenario':case[5],'bad':case[6],'good':case[7],'mechanism':case[7],'why':'所需行为被明确写出，而非依赖未证实的假设。','expected':case[8],'boundaries':case[9]}}
    fields=['description','scenario','mechanism','bad','good','why','expected','boundaries']
    return add(key,row['name_en'],row['name_zh'],row['category'],sources,[content['en'][k] for k in fields],[content['zh'][k] for k in fields],ids=[id])

def review(repo,path,conclusion,keys=None,excluded=None,duplicate_of=None):
    rr=next(r for r in DATA['repositories'] if r['repo']==repo);row=next(f for f in rr['coverage'] if f['path']==path)
    row.update(disposition='excluded' if excluded else ('duplicate' if duplicate_of else 'analyzed'),reason=excluded or conclusion,semantic_conclusion=conclusion,candidate_keys=keys or [],depth='scope-exclusion' if excluded else 'semantic-procedure-and-contract-review')
    if duplicate_of:row['duplicate_of']=duplicate_of
    row['review_kind']='scoped-relevance' if excluded else ('verified-equivalence' if duplicate_of else 'full-semantic')
    row['review_evidence']={'frozen_source':{'repo':repo,'commit':rr['commit'],'path':path,'hash':row['hash'],'blob':row.get('blob')},'content_role_and_conclusion':conclusion}
    if duplicate_of:row['review_evidence']['equivalence_proof']=duplicate_of

def finish_repo(repo,families,notes):
    rr=next(r for r in DATA['repositories'] if r['repo']==repo)
    assert not [f for f in rr['coverage'] if f['disposition']=='pending'],repo
    rr['families']=families;rr['summary']={'status':'complete','coverage_counts':dict(collections.Counter(f['disposition'] for f in rr['coverage'])),'notes':notes}

def save():
    owned=[r for r in DATA['repositories'] if r.get('external_owner')!='root']
    completed=[r['repo'] for r in owned if r['summary']['status']=='complete']
    DATA['summary'].update(status='complete' if len(completed)==len(owned) else 'in_progress',completed_repositories=completed,coverage_counts=dict(collections.Counter(f['disposition'] for r in DATA['repositories'] for f in r['coverage'])),owned_coverage_counts=dict(collections.Counter(f['disposition'] for r in owned for f in r['coverage'])),owned_pending_count=sum(f['disposition']=='pending' for r in owned for f in r['coverage']),candidate_counts=dict(collections.Counter(c['status'] for c in DATA['candidates'])),original_source_scripts_executed=False)
    (OUT/'harvest-core.json').write_text(json.dumps(DATA,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    md=['# Eight-repository skill-pattern harvest','',f'Status: **{DATA["summary"]["status"]}**. Completed: {len(completed)}/{len(owned)} owned repositories; gstack is assigned to the root separate report. Pending coverage is not represented as semantic analysis.','', '## Repository coverage','']
    for rr in DATA['repositories']:
        counts=dict(collections.Counter(f['disposition'] for f in rr['coverage']))
        md.append(f'- [{rr["repo"]}](https://github.com/{rr["repo"]}/tree/{rr["commit"]}): {rr["summary"]["status"]}; {counts}.')
        for note in rr['summary'].get('notes',[]):md.append('  - '+note)
    md+=['','## Source quality and limits','', 'Repository content is evidence of an observed instruction, not authority for its claimed causal explanation. Numeric efficacy, current host/API behavior, model pricing and earliest invention remain unestablished unless separately supported.','']
    for rr in DATA['repositories']:
        for flaw in rr.get('source_flaw_evidence',[]):md.append('- **'+rr['repo']+'**: '+flaw['claim']+' '+'; '.join('['+s['path']+']('+s['url']+')' for s in flaw['sources'])+'.')
    md+=['','## Mechanisms reviewed','']
    for c in DATA['candidates']:
        md.append('- **'+c['name']['en']+' / '+c['name']['zh']+'** ('+c['status']+'): '+c['content']['en']['description']+' '+'; '.join('['+s['path']+']('+s['url']+')' for s in c['sources'])+'.')
    md+=['','All examples are independently authored teaching constructions. Source snippets and manifests are frozen observations; they do not establish current API behavior, earliest invention or measured efficacy.','']
    (OUT/'harvest-core.md').write_text('\n'.join(md),encoding='utf-8')

if __name__=='__main__':save()
