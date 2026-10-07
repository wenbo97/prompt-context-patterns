"""Parse domain/support containers as data; this is scope evidence, not semantic completion."""
import collections
import hashlib
import json
from pathlib import Path

rows = json.loads(Path('.tools/gstack/support-blobs.json').read_text('utf-8'))
out = {}
for r in rows:
    if r['kind'] != 'text': continue
    text = r['text']
    if not text.lstrip().startswith(('{','[')): continue
    try: value = json.loads(text)
    except (ValueError, TypeError): continue
    keys = collections.Counter()
    kinds = collections.Counter()
    methods = []
    notes = []
    def visit(v, p='$'):
        kinds[type(v).__name__] += 1
        if isinstance(v, dict):
            for key, child in v.items():
                keys[key] += 1
                child_path = p + '.' + key
                if isinstance(child,str) and key in ['prompt','system','instructions','default_prompt','method','reviewMethod']:
                    methods.append({'path':child_path,'chars':len(child),'sha256':hashlib.sha256(child.encode()).hexdigest(),'text':child})
                if isinstance(child,str) and key in ['qualification','note','source','rule','originalOutcome','actualOutcome','observedOutcome','originalPaidOutcome','description'] and len(notes)<6:
                    notes.append({'path':child_path,'text':child[:280]})
                visit(child,child_path)
        elif isinstance(v,list):
            for index,child in enumerate(v): visit(child,p+f'[{index}]')
    visit(value)
    out[r['path']]={'sha256':r['sha256'],'git_oid':r['git_oid'],'bytes':r['bytes'],
                    'top_keys':list(value)[:24] if isinstance(value,dict) else {'array_length':len(value)},
                    'field_roles':keys.most_common(18),'value_types':dict(kinds),'purpose_notes':notes,'method_fields':methods}
Path('.tools/gstack/support-data-shapes.json').write_text(json.dumps(out,ensure_ascii=False),'utf-8')
print(json.dumps({'containers':len(out),'method_fields':sum(len(r['method_fields']) for r in out.values())}))
