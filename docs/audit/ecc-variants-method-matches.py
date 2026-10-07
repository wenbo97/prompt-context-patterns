"""Locate identical method prose for bounded delta review, without closing paths."""
import pathlib,json,re,collections,difflib
out=pathlib.Path(__file__).resolve().parent;b=pathlib.Path('D:/Projects/open-skills/affaan-m/ECC')
s=json.loads((out/'ecc-variants-state.json').read_text(encoding='utf8'))
def parts(path):
    lines=(b/path).read_text(encoding='utf-8-sig').replace('\r\n','\n').splitlines()
    wrapper=[]
    if lines and lines[0]=='---':
        end=next((i for i,v in enumerate(lines[1:],1) if v=='---'),None)
        if end is not None:wrapper=lines[:end+1];lines=lines[end+1:]
    prose=[];code=[];fence=None;keep=True
    for line in lines:
        m=re.match(r'^\s*(`{3,}|~{3,})([^\s]*)',line)
        if m:
            marker=m.group(1)
            if fence is None:
                fence=(marker[0],len(marker));keep=m.group(2).lower() in ('','text','txt','plain','plaintext','markdown','md','prompt','xml','yaml','yml','json','jsonc','jsonl','ndjson','dot','mermaid','bash','sh','shell','powershell')
            elif marker[0]==fence[0] and len(marker)>=fence[1]:fence=None;keep=True
        if keep or fence is None:
            if line.strip():prose.append(line)
        else:code.append(line)
    return wrapper,prose,code
matches=[]
for r in s['coverage']:
    if r['disposition']!='pending' or not r['counterpart']:continue
    try:w,prose,code=parts(r['path']);cw,cp,cc=parts(r['counterpart'])
    except (OSError,UnicodeError):continue
    if prose==cp:
        matches.append({'path':r['path'],'counterpart':r['counterpart'],'wrapper':w,'canonical_wrapper':cw,'code_delta':list(difflib.unified_diff(cc,code,n=2)),'prose_line_count':len(prose)})
(out/'ecc-variants-method-matches.json').write_bytes((json.dumps(matches,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
print('Pending exact method prose:',len(matches));print(collections.Counter(m['path'].split('/')[1] for m in matches))
print('\n'.join(m['path']+' '+str(len(m['code_delta']))+' delta lines' for m in matches))
