"""Emit line-preserving method text or complete canonical deltas for review."""
import json,pathlib,re,difflib,sys
OUT=pathlib.Path(__file__).resolve().parent;BASE=pathlib.Path('D:/Projects/open-skills/affaan-m/ECC')
state=json.loads((OUT/'ecc-variants-state.json').read_text(encoding='utf-8'))
def read(p):return (BASE/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').splitlines()
def method(lines):
    # Preserve prompt/plaintext fenced examples. Programming-language API examples
    # are identifiable domain detail and counted separately, never mistaken for prose.
    out=[];fence=None;keep=True
    for i,line in enumerate(lines,1):
        m=re.match(r'^\s*(`{3,}|~{3,})([^\s]*)',line)
        if m:
            marker=m.group(1)
            if fence is None:
                fence=(marker[0],len(marker));keep=m.group(2).lower() in ('','text','txt','plain','plaintext','markdown','md','prompt','xml','yaml','yml','json','jsonc','jsonl','ndjson','dot','mermaid','bash','sh','shell','powershell')
            elif marker[0]==fence[0] and len(marker)>=fence[1]:fence=None;keep=True
            if keep:out.append((i,line))
            continue
        if fence is None or keep:
            if line.strip():out.append((i,line))
    return out
mode=sys.argv[1];include_reviewed=mode.startswith('all:');mode=mode.removeprefix('all:');prefix=sys.argv[2];start=int(sys.argv[3]) if len(sys.argv)>3 else 0;size=int(sys.argv[4]) if len(sys.argv)>4 else 10
rows=[r for r in state['coverage'] if r['path'].startswith(prefix) and (include_reviewed or r['disposition']=='pending')][start:start+size]
for r in rows:
    path=r['path'];lines=read(path);c=r['counterpart'];print(f'\n### {path} ({len(lines)} lines) canonical={c}')
    if mode in ('codefull','canoncodefull'):
        raw=read(c) if mode=='canoncodefull' and c else lines
        retained={i for i,_ in method(raw)}
        print('\n'.join(f'{i}: {line}' for i,line in enumerate(raw,1) if i not in retained and line.strip()))
    elif mode=='codediff' and c:
        canon=read(c);cm={i for i,_ in method(canon)};vm={i for i,_ in method(lines)}
        canonical_code=[v for i,v in enumerate(canon,1) if i not in cm and v.strip()]
        variant_code=[v for i,v in enumerate(lines,1) if i not in vm and v.strip()]
        print('Programming-code blocks equal after blank-line exclusion:',canonical_code==variant_code)
        print('Programming-code line counts:',len(canonical_code),len(variant_code))
        for line in difflib.unified_diff(canonical_code,variant_code,fromfile=c,tofile=path,n=3):print(line)
    elif mode=='canonfull' and c:
        print('\n'.join(f'{i}: {line}' for i,line in method(read(c))))
    elif mode=='jsondiff' and path.endswith('.json') and '/agents/' in path:
        obj=json.loads('\n'.join(lines));prompt=obj.pop('prompt','');print('Complete config:',json.dumps(obj,ensure_ascii=False))
        paired=path.removesuffix('.json')+'.md';paired_lines=read(paired)
        if paired_lines and paired_lines[0]=='---':
            end=next(i for i,line in enumerate(paired_lines[1:],1) if line=='---');paired_lines=paired_lines[end+1:]
        left='\n'.join(paired_lines).strip();right=prompt.strip()
        print('Embedded prompt exact match to paired markdown (outer whitespace only):',left==right)
        if left!=right:
            for line in difflib.unified_diff([v for _,v in method(left.splitlines())],[v for _,v in method(right.splitlines())],fromfile=paired,tofile=path+'#prompt',n=2):print(line)
    elif mode in ('diff','methoddiff','jsondiff') and c:
        canon=read(c)
        if mode in ('methoddiff','jsondiff'):
            canonical_method=method(canon);variant_method=method(lines)
            print(f'Excluded domain code lines: canonical={len(canon)-len(canonical_method)} variant={len(lines)-len(variant_method)}; retained all prompt/plaintext/YAML/JSON/shell fences')
            canon=[v for _,v in canonical_method];lines=[v for _,v in variant_method]
        for line in difflib.unified_diff(canon,lines,fromfile=c,tofile=path,n=2):print(line)
    else:
        print('\n'.join(f'{i}: {line}' for i,line in method(lines)))
print('\nREVIEWED-PATHS:',json.dumps([r['path'] for r in rows]))
