"""Shell/PowerShell structural and heredoc inventory, never execute source."""
import re,json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8')
OUT=pathlib.Path('D:/Projects/prompt-context-patterns-refresh')
rows=[]
for r in json.loads((OUT/'.tools/ecc/support-blobs.json').read_text(encoding='utf-8')):
 if not (r['path'].endswith(('.sh','.ps1')) or r['path'].startswith('scripts/codex-git-hooks/')):continue
 lines=r['text'].splitlines();symbols=[];heredocs=[]
 for i,l in enumerate(lines,1):
  if re.match(r'^(?:function\s+)?[A-Za-z_][A-Za-z0-9_-]*(?:\s*\(\s*\))?\s*\{',l):symbols.append({'line':i,'declaration':l})
  h=re.search(r'<<-?\s*[\'\"]?([A-Za-z_][A-Za-z0-9_]*)[\'\"]?',l)
  if h:
   end=next((j for j in range(i,len(lines)) if lines[j].strip()==h[1]),None)
   if end is not None:heredocs.append({'start':i,'end':end+1,'declaration':l,'text':'\n'.join(lines[i:end])})
 row={'path':r['path'],'sha256':r['sha256'],'lines':r['lines'],'first_lines':'\n'.join(lines[:30]),'symbols':symbols,'heredocs':heredocs,'calls':[{ 'line':i,'text':l.strip()} for i,l in enumerate(lines,1) if re.match(r'^\s*(?:exec\s+)?(?:node|python\S*|git|npm|pnpm|claude|codex|gh|bash|powershell)\b',l)]}
 rows.append(row)
(OUT/'.tools/ecc/shell-shapes.json').write_text(json.dumps(rows,ensure_ascii=False),encoding='utf-8')
mode=sys.argv[1] if len(sys.argv)>1 else 'roles'
for r in rows:
 print('\n###',r['path'],'lines',r['lines'],'\n'+r['first_lines'])
 print('DECLARATIONS',r['symbols'],'CALLS',r['calls'][:15])
 if mode=='heredocs':
  for h in r['heredocs']:print('HEREDOC',h['start'],h['end'],h['declaration'],'\n'+h['text'])
 else:print('HEREDOC ranges',[(h['start'],h['end'],h['declaration']) for h in r['heredocs']])
