"""Pin exact canonical and translated line ranges for completed web/layout delta records."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
s=json.loads((out/'ecc-variants-state.json').read_text(encoding='utf8'))
by_path={r['path']:r for r in s['coverage']}
def proof(path,start,end,section):
    return {'repo':s['repo'],'commit':s['commit'],'path':path,'start_line':start,'end_line':end,'section':section,'role':'comparison-context','url':f'https://github.com/{s["repo"]}/blob/{s["commit"]}/{path}#L{start}-L{end}'}
for name in ('coding-style','design-quality','hooks','patterns','performance','security','testing'):
    path=f'docs/ja-JP/rules/web/{name}.md'
    by_path[path]['proof']=[proof(f'rules/web/{name}.md',1,12,'Canonical conditional path metadata'),proof(path,1,5,'Translated file starts directly with prose; metadata absent')]
by_path['docs/ja-JP/rules/web/hooks.md']['proof'] += [proof('rules/web/hooks.md',57,80,'Incremental/time-bounded checker source claims'),proof('rules/web/hooks.md',100,116,'Validate proposed Write payload'),proof('docs/ja-JP/rules/web/hooks.md',88,104,'Translated proposed-content guard')]
for locale in ('ja-JP','zh-CN'):
    path=f'docs/{locale}/rules/README.md'
    by_path[path]['proof']=[proof('rules/README.md',60,100,'Preserved hierarchy and ECC-owned user/project install namespace'),proof(path,40 if locale=='ja-JP' else 44,57 if locale=='ja-JP' else 62,'Older non-namespaced manual layout')]
payload=(json.dumps(s,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode()
(out/'ecc-variants-state.json').write_bytes(payload)
(out/'harvest-ecc-variants.json').write_bytes(payload)
print('Pinned9 layout/web delta records')
