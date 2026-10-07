"""Parse packaging/deployment data and display actual purpose/relationship scope."""
import json,pathlib,sys,yaml,tomllib,re
sys.stdout.reconfigure(encoding='utf-8')
OUT=pathlib.Path('D:/Projects/prompt-context-patterns-refresh')
blobs=json.loads((OUT/'.tools/ecc/support-blobs.json').read_text(encoding='utf-8'))
rows=[]
for r in blobs:
 p=r['path'];suffix=pathlib.PurePosixPath(p).suffix
 if not(suffix in ('.yaml','.yml','.toml','.example') or pathlib.PurePosixPath(p).name in ('Dockerfile','CODEOWNERS','VERSION','.gitattributes','.gitignore','.gitleaksignore','.npmignore','.prettierrc','.tool-versions','.yarnrc.yml')):continue
 obj=yaml.safe_load(r['text']) if suffix in ('.yaml','.yml') else tomllib.loads(r['text']) if suffix=='.toml' else None
 keys=[];scalars=[]
 def walk(v,pointer=''):
  if isinstance(v,dict):
   for k,val in v.items():keys.append(str(k));walk(val,pointer+'/'+str(k))
  elif isinstance(v,list):
   for i,val in enumerate(v):walk(val,pointer+'/'+str(i))
  elif isinstance(v,str):scalars.append({'pointer':pointer,'text':v})
 if obj is not None:walk(obj)
 lines=r['text'].splitlines()
 row={'path':p,'sha256':r['sha256'],'lines':r['lines'],'opening':'\n'.join(lines[:30]),'keys':list(dict.fromkeys(keys)),'relationships':[s for s in scalars if s['pointer'].endswith(('/uses','/name','/run','/command','/content','/instructions','/permissions'))],'declarations':[{'line':i,'text':l} for i,l in enumerate(lines,1) if re.match(r'^(FROM|ENTRYPOINT|CMD|COPY|USER|WORKDIR|RUN|\[.*\]|#+|[^\s#][^:]*:)',l)]}
 rows.append(row)
(OUT/'.tools/ecc/metadata-shapes.json').write_text(json.dumps(rows,ensure_ascii=False),encoding='utf-8')
for r in rows:
 if len(sys.argv)>1 and sys.argv[1]=='compact':
  print(r['path']+' | '+r['opening'].replace('\n',' ')[:150]+' | fields='+','.join(r['keys'][:25])+' | relationships='+'; '.join(s['pointer']+'='+s['text'].replace('\n',' ')[:100] for s in r['relationships'][:12]))
  continue
 print('\n###',r['path'],'\n'+r['opening'])
 print('KEYS',','.join(r['keys'][:70]))
 print('RELATIONSHIPS','; '.join(s['pointer']+'='+s['text'].replace('\n',' ')[:200] for s in r['relationships'][:30]))
 print('DECLARATIONS',r['declarations'][:8])
