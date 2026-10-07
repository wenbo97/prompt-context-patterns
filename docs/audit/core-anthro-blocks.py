from pathlib import Path
import hashlib,json,re,sys,collections
n={'__name__':'core_helpers'};exec(Path(__file__).with_name('core-update.py').read_text(encoding='utf-8'),n)
out=n['OUT'];repo='anthropics/skills';ledger_path=out/'core-anthro-api-blocks.json'
cache_path=out.parents[1]/'.tools/core-reading-cache/core-anthro-api-blocks.raw.json'
def public_write(data):
    public={**data,'private_reading_cache':'.tools/core-reading-cache/core-anthro-api-blocks.raw.json','raw_text_included':False}
    public['blocks']=[{k:v for k,v in b.items() if k!='text'} for b in data['blocks']]
    ledger_path.write_text(json.dumps(public,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def block_text(block,cache=None):
    if 'text' in block:return block['text']
    if cache is not None:
        old=cache['blocks'][block['id']]
        if old['hash']==block['hash'] and 'text' in old:
            raw=old['text']
            if hashlib.sha256(raw.encode()).hexdigest()==block['hash']:return raw
    raw=''.join(n['blob'](repo,block['path']).splitlines(keepends=True)[block['start_line']-1:block['end_line']])
    assert hashlib.sha256(raw.encode()).hexdigest()==block['hash']
    return raw
def make():
    blocks=[];seen={};occurrences=[]
    for f in n['BY_REPO'][repo]['files']:
        p=f['path']
        if not p.startswith('skills/claude-api/') or not p.endswith(('.md','.py','.mjs')):continue
        text=n['blob'](repo,p);lines=text.splitlines(keepends=True)
        starts=[];start=0;fence=None
        for i,line in enumerate(lines):
            marker=re.match(r'^\s*(`{3,}|~{3,})',line)
            if marker:
                token=marker.group(1)[0]
                if fence is None:fence=token
                elif fence==token:fence=None
            if not line.strip() and fence is None:
                if i>start:starts.append((start,i))
                start=i+1
        if start<len(lines):starts.append((start,len(lines)))
        for a,b in starts:
            raw=''.join(lines[a:b]);h=hashlib.sha256(raw.encode()).hexdigest()
            if h not in seen:
                seen[h]=len(blocks);blocks.append({'id':len(blocks),'hash':h,'path':p,'start_line':a+1,'end_line':b,'text':raw,'status':'pending'})
            occurrences.append({'path':p,'start_line':a+1,'end_line':b,'block_id':seen[h],'hash':h})
    # Exactly the first 98 lines of the body were read before this ledger.
    for block in blocks:
        if block['path']=='skills/claude-api/SKILL.md' and block['end_line']<=98:block['status']='read'
    data={'repo':repo,'commit':n['BY_REPO'][repo]['commit'],'proof':'Exact UTF-8 Git-blob paragraph/code-fence block SHA-256 equality; no normalization or similarity equivalence','blocks':blocks,'occurrences':occurrences,'cursor':0}
    cache_path.parent.mkdir(parents=True,exist_ok=True)
    cache_path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    public_write(data)
    print('CREATED',len(blocks),'unique',len(occurrences),'occurrences',sum(len(x['text']) for x in blocks),'chars',collections.Counter(x['status'] for x in blocks))
def show(start,limit=21000):
    data=json.loads(ledger_path.read_text(encoding='utf-8'));selected=[];size=0
    cache=json.loads(cache_path.read_text(encoding='utf-8')) if cache_path.exists() else None
    for b in data['blocks'][start:]:
        if b['status']=='read':continue
        raw=block_text(b,cache)
        if selected and size+len(raw)>limit:break
        if len(raw)>limit:
            print('OVERSIZED BLOCK',b['id'],b['path'],b['start_line'],b['end_line'],len(raw));break
        selected.append((b,raw));size+=len(raw)
    print('BATCH IDS',','.join(str(b['id']) for b,raw in selected),'CHARS',size)
    for b,raw in selected:
        print('\nBLOCK',b['id'],b['path'],f"L{b['start_line']}-{b['end_line']}")
        print(raw,end='')
def mark(ids):
    data=json.loads(ledger_path.read_text(encoding='utf-8'))
    for i in ids:data['blocks'][i]['status']='read'
    public_write(data)
    print('STATUS',collections.Counter(x['status'] for x in data['blocks']))
if __name__=='__main__':
    if sys.argv[1]=='make':make()
    elif sys.argv[1]=='show':show(int(sys.argv[2]),int(sys.argv[3]) if len(sys.argv)>3 else 21000)
    elif sys.argv[1]=='mark':mark([int(x) for x in sys.argv[2].split(',')])
