"""Inspect JSON metadata, embedded instruction fields and fixture relationships."""
import json,pathlib,sys,hashlib,collections
sys.stdout.reconfigure(encoding='utf-8')
OUT=pathlib.Path('D:/Projects/prompt-context-patterns-refresh')
blobs=json.loads((OUT/'.tools/ecc/support-blobs.json').read_text(encoding='utf-8'))
rows=[];virtual=[]
for r in blobs:
 if not r['path'].endswith('.json'):continue
 obj=json.loads(r['text']);keys=collections.Counter();strings=[]
 def walk(value,pointer=''):
  if isinstance(value,dict):
   keys.update(value.keys())
   for k,v in value.items():walk(v,pointer+'/'+str(k))
  elif isinstance(value,list):
   for i,v in enumerate(value):walk(v,pointer+'/'+str(i))
  elif isinstance(value,str):strings.append({'pointer':pointer,'text':value,'chars':len(value),'hash':hashlib.sha256(value.encode()).hexdigest()})
 walk(obj)
 method=[];code=[]
 for s in strings:
  pointer=s['pointer'];leaf=pointer.rsplit('/',1)[-1]
  if '/files/' in pointer or leaf in ('check','code') or leaf.endswith(('.js','.cjs','.mjs','.ts','.py')):
   code.append({k:s[k] for k in ('pointer','chars','hash')})
   if leaf in ('check','code') or leaf.endswith(('.js','.cjs','.mjs','.ts','.py')):virtual.append({'path':r['path']+'#'+pointer,'parent_path':r['path'],'sha256':s['hash'],'bytes':len(s['text'].encode()),'lines':s['text'].count('\n')+1,'text':s['text'],'magic_hex':None})
  elif leaf in ('query','sampling','note','instructions','system','prompt','defaultPrompt','description','longDescription','shortDescription','purpose','expectedBlock','rule','limitations') or 'expectedIds' in pointer:
   method.append(s)
 row={'path':r['path'],'sha256':r['sha256'],'top_keys':list(obj) if isinstance(obj,dict) else '[array]','all_keys':dict(keys),'string_count':len(strings),'method_fields':method,'embedded_code':code,'long_data_fields':[s['pointer'] for s in strings if s['chars']>=100 and s not in method]}
 rows.append(row)
(OUT/'.tools/ecc/json-shapes.json').write_text(json.dumps(rows,ensure_ascii=False),encoding='utf-8')
(OUT/'.tools/ecc/json-virtual-blobs.json').write_text(json.dumps(virtual,ensure_ascii=False),encoding='utf-8')
mode=sys.argv[1] if len(sys.argv)>1 else 'roles'
prefix=sys.argv[2] if len(sys.argv)>2 else ''
for r in rows:
 if not r['path'].startswith(prefix):continue
 print('\n###',r['path'],'TOP',r['top_keys'],'FIELDS',','.join(r['all_keys']),'strings',r['string_count'],'embedded',len(r['embedded_code']))
 if mode=='methods':
  for s in r['method_fields']:print(s['pointer']+': '+s['text'])
 elif r['method_fields']:print('Representative content:',r['method_fields'][0]['pointer'],r['method_fields'][0]['text'][:200])
print('JSON files',len(rows),'embedded source units',len(virtual))
