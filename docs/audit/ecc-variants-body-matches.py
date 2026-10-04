"""Find exact body copies without claiming wrapper or translation equivalence."""
import pathlib,json,hashlib,collections
out=pathlib.Path(__file__).resolve().parent;b=pathlib.Path('D:/Projects/open-skills/affaan-m/ECC')
s=json.loads((out/'ecc-variants-state.json').read_text(encoding='utf8'))
def split(path):
    text=(b/path).read_text(encoding='utf-8-sig').replace('\r\n','\n')
    lines=text.splitlines()
    if lines and lines[0]=='---':
        end=next((i for i,v in enumerate(lines[1:],1) if v=='---'),None)
        if end is not None:return '\n'.join(lines[:end+1]),'\n'.join(lines[end+1:]).strip()
    return '',text.strip()
matches=[]
for r in s['coverage']:
    if r['disposition']!='pending' or not r['counterpart']:continue
    try:w,body=split(r['path']);cw,cb=split(r['counterpart'])
    except (UnicodeError,OSError):continue
    if body==cb:
        matches.append({'path':r['path'],'counterpart':r['counterpart'],'body_hash':hashlib.sha256(body.encode()).hexdigest(),'wrapper':w,'canonical_wrapper':cw})
(out/'ecc-variants-body-matches.json').write_bytes((json.dumps(matches,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
print('Exact bodies pending:',len(matches));print(collections.Counter(r['path'].split('/')[1] for r in matches))
print(json.dumps(matches,ensure_ascii=False))
