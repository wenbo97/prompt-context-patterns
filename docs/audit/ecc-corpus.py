"""Read-only ECC corpus review helper. It never executes upstream code."""
import collections, functools, hashlib, json, pathlib, re, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path('D:/Projects/open-skills/affaan-m/ECC')
OUT = pathlib.Path('D:/Projects/prompt-context-patterns-refresh/docs/audit')
COMMIT='ef648e01899ba3e8dc6371642deaaf64b4477775'
SOURCE_ROWS=next(x for x in json.loads((OUT/'source-inventory.json').read_text(encoding='utf-8'))['repositories'] if x['repo']=='affaan-m/ECC')['files']
SOURCE_MAP={x['path']:x for x in SOURCE_ROWS}

def paths():
    return subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', COMMIT], cwd=ROOT, text=True).splitlines()

@functools.lru_cache(maxsize=1024)
def text(path):
    expected=SOURCE_MAP[path]
    try: raw=(ROOT/path).read_bytes()
    except OSError: raw=b''
    hashed=raw if expected['binary'] else raw.replace(b'\r\n',b'\n')
    if hashlib.sha256(hashed).hexdigest()!=expected['hash']:
        raw=subprocess.check_output(['git','show',f'{COMMIT}:{path}'],cwd=ROOT)
    return raw.decode('utf-8',errors='replace').replace('\r\n','\n')

def excerpt(path, maximum=900):
    body = text(path)
    lines = body.splitlines()
    description = re.search(r'^description:\s*(.+)$', body, re.M)
    headings = [l for l in lines if l.startswith('#')]
    instructions=[]
    fenced=False
    for i,line in enumerate(lines,1):
        if line.startswith('```'):
            fenced=not fenced
        elif not fenced and re.search(r'\b(must|never|do not|only|before|stop|evidence|approval|verify|unknown|uncertain|context|prompt|retry|handoff|source|scope|budget|trust|contradict|confidence|reference|schema|gate)\b',line,re.I):
            instructions.append(f'{i}:{line.strip()}')
    instructions=[l for l in instructions if ':description:' not in l]
    result=' | '.join(([description.group(1)[:230]] if description else []) + headings[:20] + instructions)
    return result[:maximum]

if sys.argv[1]=='skills':
    selected=[p for p in paths() if p.startswith('skills/') and p.endswith('SKILL.md')]
    lo=int(sys.argv[2]); hi=int(sys.argv[3]); maximum=int(sys.argv[4]) if len(sys.argv)>4 else 1200
    for p in selected[lo:hi]: print(p+'\n'+excerpt(p,maximum)+'\n')
elif sys.argv[1]=='inventory':
    records=[]
    seen={}
    for p in paths():
        raw=(ROOT/p).read_bytes()
        h=hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest()
        record={'path':p,'hash':h,'bytes':len(raw),'lines':raw.count(b'\n')+1}
        if h in seen: record['duplicate_of']=seen[h]
        else: seen[h]=p
        records.append(record)
    (OUT/'ecc-inventory.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'tracked':len(records),'unique_normalized_hashes':len(seen)}))
elif sys.argv[1]=='read':
    for p in sys.argv[2:]:
        print('\n### '+p)
        for i,l in enumerate(text(p).splitlines(),1): print(f'{i}: {l}')
elif sys.argv[1]=='range':
    p=sys.argv[2]; start=int(sys.argv[3]); end=int(sys.argv[4])
    print('\n### '+p+' '+str(start)+'..'+str(end))
    for i,l in enumerate(text(p).splitlines(),1):
        if start<=i<=end: print(f'{i}: {l}')
elif sys.argv[1]=='digest':
    selected=[p for p in paths() if p.startswith(sys.argv[2]) and p.endswith(('.md','.txt','.js','.py','.ts','.sh','.json','.yaml','.yml'))]
    for p in selected[int(sys.argv[3]):int(sys.argv[4])]: print(p+'\n'+excerpt(p,int(sys.argv[5]))+'\n')
elif sys.argv[1] in ('pending','pending_refs','pending_owned','pending_other'):
    state=json.loads((OUT/'ecc-review-ledger.json').read_text(encoding='utf-8'))
    mode=sys.argv[1]
    rows=state['pending_partitions']['canonical_skills'] if mode=='pending' else state['pending_partitions']['canonical_references'] if mode=='pending_refs' else state['pending_partitions']['other'] if mode=='pending_other' else [x['path'] for x in state['pending'] if x['path'].startswith(('commands/','agents/','rules/','contexts/','examples/'))]
    if len(sys.argv)>3: rows=[p for p in rows if p.startswith(sys.argv[3])]
    rows.sort(key=lambda p:len(text(p)))
    budget=int(sys.argv[2]); batch=[]; used=0
    for p in rows:
        size=len(text(p))
        if used+size>budget and batch: break
        batch.append(p); used+=size
    (OUT/'ecc-current-batch.json').write_text(json.dumps(batch,indent=2),encoding='utf-8')
    print('BATCH',json.dumps(batch),'source_chars',used)
    for p in batch:
        print('\n### '+p)
        for i,l in enumerate(text(p).splitlines(),1): print(f'{i}: {l}')
