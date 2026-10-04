"""Record bounded consumer-function cross-reads without closing the parent-owned utility file."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
s=json.loads((out/'ecc-variants-state.json').read_text(encoding='utf8'))
rows={r['path']:r for r in s['coverage']}
def proof(path,start,end,section):
    return {'repo':s['repo'],'commit':s['commit'],'path':path,'start_line':start,'end_line':end,'section':section,'role':'comparison-context','url':f'https://github.com/{s["repo"]}/blob/{s["commit"]}/{path}#L{start}-L{end}'}
for path in ('docs/zh-CN/commands/save-session.md','docs/zh-CN/commands/sessions.md'):
    rows[path]['proof']=[proof('scripts/lib/session-manager.js',267,292,'Consumer metadata labels are exact English regex literals'),proof('commands/save-session.md',73,75,'Canonical producer metadata labels'),proof('docs/zh-CN/commands/save-session.md',73,75,'Localized metadata labels differ from consumer grammar'),proof('scripts/lib/session-manager.js',295,308,'Checkbox-section grammar for item statistics')]
s.setdefault('bounded_cross_reads',{})['scripts/lib/session-manager.js']={'ranges':[[237,325],[334,356]],'depth':'complete-specific-functions-only','reason':'Read parseSessionMetadata and getSessionStats for translated producer/consumer comparison; the rest of this root-owned file remains unreviewed here. Static inference only, no source execution.'}
payload=(json.dumps(s,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode()
(out/'ecc-variants-state.json').write_bytes(payload)
(out/'harvest-ecc-variants.json').write_bytes(payload)
print('Pinned2 locale producer/consumer comparisons; bounded cross-read recorded, no root utility closure')
