"""Read frozen nextlevel partition as data. No upstream code import/execution."""
import json,pathlib,hashlib,subprocess,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
OUT=pathlib.Path('D:/Projects/prompt-context-patterns-refresh')
ROOT=pathlib.Path('D:/Projects/open-skills/nextlevelbuilder/ui-ux-pro-max-skill')
plan=json.loads((OUT/'docs/audit/core-nextlevel-partition.json').read_text(encoding='utf-8'))
COMMIT=plan['commit'];groups={}
for r in plan['transfer_support_template_data_partition']:groups.setdefault(r['hash'],[]).append(r)
private=OUT/'.tools/core-nextlevel';private.mkdir(parents=True,exist_ok=True)
def raw(row):
 value=subprocess.check_output(['git','-C',str(ROOT),'show',COMMIT+':'+row['path']])
 hashed=value if row['binary'] else value.replace(b'\r\n',b'\n')
 assert hashlib.sha256(hashed).hexdigest()==row['hash'],row['path']
 return value
def content(row):return raw(row).decode('utf-8').replace('\r\n','\n')
mode=sys.argv[1] if len(sys.argv)>1 else 'summary'
if mode=='freeze':
 rows=[]
 for hash_value,occurrences in groups.items():
  row=occurrences[0];value=raw(row)
  rows.append({'path':row['path'],'sha256':hash_value,'bytes':row['bytes'],'lines':row['lines'],'binary':row['binary'],'mode':row['mode'],'blob':row['blob'],'occurrences':occurrences,'text':None if row['binary'] else value.decode('utf-8').replace('\r\n','\n'),'magic_hex':value[:32].hex() if row['binary'] else None})
 (private/'blobs.json').write_text(json.dumps(rows,ensure_ascii=False),encoding='utf-8')
 print(json.dumps({'commit':COMMIT,'occurrences':sum(len(v) for v in groups.values()),'canonical_hash_groups':len(rows),'bytes':sum(r['bytes'] for r in rows)}))
elif mode=='read':
 index={r['path']:r for rows in groups.values() for r in rows}
 for path in sys.argv[2:]:
  print('\n###',path)
  for i,line in enumerate(content(index[path]).splitlines(),1):print(str(i)+': '+line)
elif mode=='range':
 index={r['path']:r for rows in groups.values() for r in rows};path=sys.argv[2];lo=int(sys.argv[3]);hi=int(sys.argv[4])
 print('\n###',path,str(lo)+'..'+str(hi))
 for i,line in enumerate(content(index[path]).splitlines(),1):
  if lo<=i<=hi:print(str(i)+': '+line)
else:
 print(json.dumps({'commit':COMMIT,'owned_occurrences':sum(len(v) for v in groups.values()),'canonical_hash_groups':len(groups),'classifications':dict(collections.Counter(r['classification'] for v in groups.values() for r in v))}))
