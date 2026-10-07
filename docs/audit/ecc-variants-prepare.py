"""Prepare Git-authoritative variant coverage and exact duplicate maps."""
import json,pathlib,hashlib,collections,re,difflib
OUT=pathlib.Path(__file__).resolve().parent;ROOT=OUT.parents[1];BASE=pathlib.Path('D:/Projects/open-skills/affaan-m/ECC')
snapshot=json.loads((OUT/'source-inventory.json').read_text(encoding='utf-8'));repo=next(x for x in snapshot['repositories'] if x['repo']=='affaan-m/ECC')
locales={'ja-JP','zh-CN','zh-TW','es','tr','ko-KR','pt-BR','de-DE','pl','ru','th','uk-UA','ur','vi-VN'}
def selected(p):
    parts=p.split('/');return parts[0] in {'.agents','.cursor','.kiro','.opencode'} or (parts[0]=='docs' and len(parts)>2 and parts[1] in locales)
files={f['path']:f for f in repo['files']};assigned=[p for p in files if selected(p)]
def text(p):return (BASE/p).read_bytes().decode('utf-8-sig',errors='replace').replace('\r\n','\n')
def hash(p):return hashlib.sha256((BASE/p).read_bytes()).hexdigest()
def normhash(p):return hashlib.sha256(text(p).encode()).hexdigest()
hashmap=collections.defaultdict(list)
for p,f in files.items():
    if not f.get('binary'):hashmap[normhash(p)].append(p)
def counterpart(p):
    parts=p.split('/')
    if parts[0]=='docs':c='/'.join(parts[2:]);return c if c in files else ('docs/'+c if 'docs/'+c in files else None)
    c='/'.join(parts[1:])
    if c in files:return c
    if parts[0]=='.opencode' and parts[1]=='prompts':
        c='agents/'+'/'.join(parts[2:]);return c if c in files else None
    if parts[0]=='.kiro' and parts[1]=='agents':
        c='agents/'+'/'.join(parts[2:]);return c if c in files else None
    if parts[0] in ('.kiro','.cursor') and parts[1] in ('rules','steering'):
        name=parts[-1].removesuffix('.mdc').removesuffix('.md')
        if name.startswith('common-'):c='rules/common/'+name[7:]+'.md'
        elif name.startswith('typescript-'):c='rules/typescript/'+name[11:]+'.md'
        elif name.startswith('python-'):c='rules/python/'+name[7:]+'.md'
        elif name.startswith('golang-'):c='rules/golang/'+name[7:]+'.md'
        elif name.startswith('go-'):c='rules/golang/'+name[3:]+'.md'
        else:c='rules/common/'+name+'.md'
        if c in files:return c
    return None
def projection(p):
    lines=text(p).splitlines();out=[];fence=None
    for i,line in enumerate(lines,1):
        m=re.match(r'^\s*(`{3,}|~{3,})',line)
        if m:
            mark=m.group(1)
            if fence is None:fence=(mark[0],len(mark))
            elif mark[0]==fence[0] and len(mark)>=fence[1]:fence=None
            continue
        if fence is None and line.strip():out.append((i,line))
    return out
coverage=[]
for p in assigned:
    f=files[p];c=counterpart(p);h=normhash(p)
    duplicate=next((other for other in hashmap[h] if other!=p and not selected(other)),None)
    if duplicate is None:duplicate=next((other for other in hashmap[h] if other!=p and other<p),None)
    status='duplicate' if duplicate else 'pending'
    record={'path':p,'git_blob':f['blob'],'hash':hash(p),'normalized_hash':h,'classification':f['classification'],'disposition':status,'depth':'exact-content-comparison' if duplicate else 'pending','reason':'Exact LF-normalized content matches a recorded Git path; retain occurrence and target.' if duplicate else 'Requires full method-bearing text or semantic delta review.','candidate_keys':[],'counterpart':c,'duplicate_of':duplicate,'line_count':f['lines']}
    if p.endswith(('package-lock.json','.npmignore','tsconfig.json')):
        record.update(disposition='excluded',depth='data-structure-inspection',reason='Dependency lock, publish exclusion list or compiler configuration is packaging data; no prompt/context workflow text. Review executable adapters separately.')
    coverage.append(record)
state={'repo':repo['repo'],'commit':repo['commit'],'partition':{'locales':sorted(locales),'harnesses':['.agents','.cursor','.kiro','.opencode']},'coverage':coverage,'candidates':[],'summary':{'status':'in_progress','total':len(coverage),'pending':sum(r['disposition']=='pending' for r in coverage),'duplicates':sum(r['disposition']=='duplicate' for r in coverage),'excluded':sum(r['disposition']=='excluded' for r in coverage)}}
(OUT/'ecc-variants-state.json').write_bytes((json.dumps(state,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
print(json.dumps(state['summary']));print('Pending by prefix',collections.Counter('/'.join(r['path'].split('/')[:2]) for r in coverage if r['disposition']=='pending'))
def emit(paths):
    for p in paths:
        print('\n###',p)
        print('\n'.join(f'{i}: {line}' for i,line in projection(p)))
if __name__=='__main__':pass
