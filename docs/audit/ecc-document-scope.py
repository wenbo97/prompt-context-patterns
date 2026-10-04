"""Display scope evidence for archival/product metadata prose, not semantic closure."""
import json,pathlib,re,sys,hashlib
sys.stdout.reconfigure(encoding='utf-8')
OUT=pathlib.Path('D:/Projects/prompt-context-patterns-refresh')
rows=[]
for r in json.loads((OUT/'.tools/ecc/support-blobs.json').read_text(encoding='utf-8')):
 if not r['path'].endswith('.md'):continue
 lines=r['text'].splitlines();sections=[]
 for i,l in enumerate(lines,1):
  if l.startswith('#'):
   next_i=next((j for j in range(i,len(lines)) if lines[j].startswith('#')),len(lines))
   body='\n'.join(lines[i:next_i]).strip()
   sections.append({'line':i,'end':next_i,'heading':l,'opening':body[:450],'section_hash':hashlib.sha256(body.encode()).hexdigest()})
 rows.append({'path':r['path'],'sha256':r['sha256'],'lines':r['lines'],'opening':'\n'.join(lines[:22]),'sections':sections,'links':re.findall(r'\]\(([^\)]+)\)',r['text'])})
(OUT/'.tools/ecc/document-shapes.json').write_text(json.dumps(rows,ensure_ascii=False),encoding='utf-8')
prefix=sys.argv[1] if len(sys.argv)>1 else ''
mode=sys.argv[2] if len(sys.argv)>2 else 'sections'
for r in rows:
 if not r['path'].startswith(prefix):continue
 if mode=='compact':
  print(r['path']+' | '+r['opening'].replace('\n',' ')[:260]+' | '+'; '.join(str(s['line'])+':'+s['heading'] for s in r['sections']))
  continue
 print('\n###',r['path'],'\n'+r['opening'][:500])
 print('SECTIONS','; '.join(str(s['line'])+':'+s['heading']+' '+s['opening'].replace('\n',' ')[:150] for s in r['sections']))
