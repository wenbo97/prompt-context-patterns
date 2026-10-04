"""Legacy audit preparation and validation; never modifies product files."""
import json, re, pathlib, sys, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/audit'
def sections(path):
    lines=path.read_text(encoding='utf-8-sig').splitlines()
    starts=[]; fence=None
    for i,line in enumerate(lines):
        m=re.match(r'^\s*(`{3,}|~{3,})',line)
        if m:
            marker=m.group(1)
            if fence is None: fence=(marker[0],len(marker))
            elif marker[0]==fence[0] and len(marker)>=fence[1]: fence=None
            continue
        if fence is None:
            m=re.match(r'^## (?:Meta-)?Pattern (K?\d+):',line)
            if m: starts.append((i,m.group(1)))
    return [{'id':p,'path':path.relative_to(ROOT).as_posix(),'start_line':i+1,'end_line':(starts[k+1][0] if k+1<len(starts) else len(lines)),'body':'\n'.join(lines[i:(starts[k+1][0] if k+1<len(starts) else len(lines))])} for k,(i,p) in enumerate(starts)]
def prepare():
    items=[]
    for p in sorted((ROOT/'catalog/categories').glob('*.md')):
        if not p.stem.endswith('-zh'): items+=sections(p)
    meta=json.loads((ROOT/'_data/patterns.json').read_text(encoding='utf-8-sig'))
    harvest=json.loads((ROOT/'eval/tools/patterns-harvest.json').read_text(encoding='utf-8-sig'))
    d={'sections':items,'metadata':meta,'harvest':harvest}
    (OUT/'legacy-prepared.json').write_text(json.dumps(d,ensure_ascii=False,indent=2).replace('\n','\r\n'),encoding='utf-8')
    print(f'Prepared {len(items)} real sections, {len(meta)} metadata records')
def read(a,b):
    d=json.loads((OUT/'legacy-prepared.json').read_text(encoding='utf-8'))
    for s in d['sections']:
        if s['id'].isdigit() and a<=int(s['id'])<=b:
            print(f"\n=== {s['path']}:{s['start_line']}-{s['end_line']} ===\n{s['body']}")
if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='read':read(int(sys.argv[2]),int(sys.argv[3]))
    else:prepare()
