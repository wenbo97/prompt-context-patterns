"""Display scoped structural evidence and selected literals for human review."""
import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8')
OUT=pathlib.Path('D:/Projects/prompt-context-patterns-refresh')
rows=json.loads((OUT/'.tools/ecc/support-shapes.json').read_text(encoding='utf-8'))
mode=sys.argv[1];prefix=sys.argv[2] if len(sys.argv)>2 else ''
selected=[r for r in rows if r['path'].startswith(prefix)]
if mode=='entryroles':
 selected=[r for r in selected if not r['path'].startswith('scripts/lib/') and 'parse_errors' in r]
 mode='roles'
if mode in ('shapes','compact','roles'):
 lo=int(sys.argv[3]) if len(sys.argv)>3 else 0;hi=int(sys.argv[4]) if len(sys.argv)>4 else len(selected)
 for r in selected[lo:hi]:
  if mode=='roles':
   relationships=[x for x in r.get('imports',[]) if x.startswith('.')]
   print(r['path']+' | '+r.get('leading_comment',r.get('first_lines','')).replace('\n',' ')[:90]+' | calls='+','.join(relationships[:5])+' | declarations='+','.join(x['name'] for x in r.get('symbols',[])[:3])+' | example-check='+';'.join(r.get('checks',[])[:1])+' | literals='+str(len(r.get('literals',[]))))
   continue
  if mode=='compact':
   print('\n###',r['path'],'lines',r['lines'],'parse_errors',len(r.get('parse_errors',[])))
   print('CONTRACT',r.get('leading_comment',r.get('first_lines','')).replace('\n',' ')[:350])
   print('IMPORTS',','.join(r.get('imports',[])))
   print('SYMBOLS',','.join(x['name'] for x in r.get('symbols',[])))
   print('CHECKS','; '.join(r.get('checks',[]))[:900])
   continue
  print('\n###',r['path'],r['sha256'],'lines',r['lines'],'parse_errors',r.get('parse_errors'))
  print('CONTRACT',r.get('leading_comment',r.get('first_lines','')))
  print('IMPORTS',','.join(r.get('imports',[])))
  print('SYMBOLS','; '.join(x['name']+'@'+str(x['start'])+'-'+str(x['end']) for x in r.get('symbols',[])))
  print('CHECKS','; '.join(r.get('checks',[])))
elif mode in ('literals','literal-index'):
 minimum=int(sys.argv[3]) if len(sys.argv)>3 else 100;lo=int(sys.argv[4]) if len(sys.argv)>4 else 0;hi=int(sys.argv[5]) if len(sys.argv)>5 else 100000
 seen={};values=[]
 for r in selected:
  for l in r.get('literals',[]):
   if l['chars']<minimum:continue
   if l['sha256'] in seen:continue
   seen[l['sha256']]=r['path'];values.append((r,l))
 print('Unique selected',len(values),'chars',sum(l['chars'] for r,l in values))
 for i,(r,l) in enumerate(values[lo:hi],lo):print('\n###',i,r['path'],str(l['start'])+'-'+str(l['end']),l['sha256'],','.join(l['owners'])+'\n'+(l['text'] if mode=='literals' else l['text'][:350].replace('\n',' ')+' [chars='+str(l['chars'])+']'))
elif mode=='nonast':
 for r in selected:
  if 'literals' not in r:print(r['path'],r['lines'],r['bytes'])
