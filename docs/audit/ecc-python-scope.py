"""Python AST purpose/literal inventory. Reads source as data, never imports ECC."""
import ast,json,pathlib,sys,hashlib
sys.stdout.reconfigure(encoding='utf-8')
OUT=pathlib.Path('D:/Projects/prompt-context-patterns-refresh')
rows=[]
for r in json.loads((OUT/'.tools/ecc/support-blobs.json').read_text(encoding='utf-8')):
 if not r['path'].endswith('.py'):continue
 tree=ast.parse(r['text'],filename=r['path']);imports=[];symbols=[];literals=[]
 for n in ast.walk(tree):
  if isinstance(n,(ast.Import,ast.ImportFrom)):imports.extend((n.module or '')+'.'+a.name if isinstance(n,ast.ImportFrom) else a.name for a in n.names)
  if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):symbols.append({'name':n.name,'start':n.lineno,'end':n.end_lineno,'doc':ast.get_docstring(n)})
  if isinstance(n,ast.Constant) and isinstance(n.value,str) and len(n.value)>=100:literals.append({'start':n.lineno,'end':n.end_lineno,'chars':len(n.value),'sha256':hashlib.sha256(n.value.encode()).hexdigest(),'text':n.value})
 row={'path':r['path'],'sha256':r['sha256'],'lines':r['lines'],'doc':ast.get_docstring(tree),'imports':imports,'symbols':symbols,'literals':literals}
 rows.append(row)
(OUT/'.tools/ecc/python-shapes.json').write_text(json.dumps(rows,ensure_ascii=False),encoding='utf-8')
for r in rows:print(r['path']+' | '+str(r['doc'] or '')[:170].replace('\n',' ')+' | imports='+','.join(r['imports'][:10])+' | symbols='+','.join(s['name'] for s in r['symbols'])+' | literals='+str(len(r['literals'])))
print('PYTHON FILES',len(rows),'LONG LITERALS',sum(len(r['literals']) for r in rows))
