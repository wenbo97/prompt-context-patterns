from pathlib import Path
import json,collections
p=Path(__file__).parent
d=json.loads((p/'harvest-core.json').read_text(encoding='utf-8'));inv=json.loads((p/'source-inventory.json').read_text(encoding='utf-8'));repos={r['repo']:r for r in inv['repositories']}
ci=json.loads((p/'harvest-composio.json').read_text(encoding='utf-8'));keys={c['key'] for c in d['candidates']}|{c['key'] for c in ci['candidates']}
fields=['description','scenario','mechanism','bad','good','why','expected','boundaries'];issues=[]
for c in d['candidates']:
 for lang in ['en','zh']:
  for f in fields:
   if not isinstance(c.get('content',{}).get(lang,{}).get(f),str) or not c['content'][lang][f].strip():issues.append((c['key'],lang,f))
 if c['status'] in ['active','merged']:
  if sum(c['scores'].values())<8 or any(c['scores'][x]!=2 for x in ['scenario','mechanism','contrast']):issues.append((c['key'],'admission'))
 if len(c['sources'])==0:issues.append((c['key'],'sources'))
 for s in c['sources']:
  rr=repos[s['repo']];f=next(x for x in rr['files'] if x['path']==s['path'])
  if s['commit']!=rr['commit'] or len(s['commit'])!=40:issues.append((c['key'],'commit'))
  a=s.get('line_start',s.get('start_line'));z=s.get('line_end',s.get('end_line'))
  if not isinstance(a,int) or not isinstance(z,int) or not(1<=a<=z<=f['lines']):issues.append((c['key'],'lines',s))
  if s['role']!='observed-example' or s['url']!=f"https://github.com/{s['repo']}/blob/{s['commit']}/{s['path']}#L{a}-L{z}":issues.append((c['key'],'locator'))
 if '\ufffd' in json.dumps(c,ensure_ascii=False):issues.append((c['key'],'replacement-character'))
for rr in d['repositories']:
 meta={f['path']:f for f in repos[rr['repo']]['files']}
 if set(meta)!={f['path'] for f in rr['coverage']}:issues.append((rr['repo'],'tree-coverage'))
 for f in rr['coverage']:
  if f['hash']!=meta[f['path']]['hash']:issues.append((rr['repo'],f['path'],'hash'))
  if f['disposition']!='pending':
   if not f.get('semantic_conclusion') or not f.get('reason') or not f.get('depth'):issues.append((rr['repo'],f['path'],'disposition-evidence'))
   for k in f.get('candidate_keys',[]):
    if k not in keys:issues.append((rr['repo'],f['path'],'unknown-candidate',k))
  if f['disposition']=='duplicate':
   b=f['duplicate_of'];b={'path':b,'repo':rr['repo']} if isinstance(b,str) else b
   m=next(x for x in repos[b.get('repo',rr['repo'])]['files'] if x['path']==b['path'])
   if m['hash']!=f['hash']:issues.append((rr['repo'],f['path'],'duplicate-hash'))
 if rr['summary']['status']=='complete' and any(f['disposition']=='pending' for f in rr['coverage']):issues.append((rr['repo'],'false-completion'))
ledger=json.loads((p/'core-anthro-api-blocks.json').read_text(encoding='utf-8'))
for rr in d['repositories']:
 if rr['repo']=='anthropics/skills':
  for f in rr['coverage']:
   if 'exact_block_review' in f:
    ids={o['block_id'] for o in ledger['occurrences'] if o['path']==f['path']}
    if any(ledger['blocks'][i]['status']!='read' for i in ids):issues.append((f['path'],'unread-block-claim'))
print(json.dumps({'issues':issues,'owned_pending':d['summary']['owned_pending_count'],'candidates':d['summary']['candidate_counts'],'api_unique_blocks':dict(collections.Counter(b['status'] for b in ledger['blocks']))},ensure_ascii=False,indent=2))
assert not issues
