from pathlib import Path
import json,collections
n={'__name__':'core_helpers'};exec(Path(__file__).with_name('core-update.py').read_text(encoding='utf-8'),n)
r='nextlevelbuilder/ui-ux-pro-max-skill';out=n['OUT'];by=collections.defaultdict(list)
completed=[x for x in n['DATA']['repositories'] if x.get('external_owner')!='root' and x['summary']['status']=='complete']
comp=json.loads((out/'harvest-composio.json').read_text(encoding='utf-8'));completed.append(comp)
for rr in completed:
 inv={f['path']:f for f in n['BY_REPO'][rr['repo']]['files']}
 for f in rr['coverage']:
  if f['disposition'] not in ['analyzed','excluded']:continue
  by[inv[f['path']]['hash']].append({'repo':rr['repo'],'commit':rr['commit'],'path':f['path'],'hash':inv[f['path']]['hash'],'review':f})
matches=[]
for meta in n['BY_REPO'][r]['files']:
 if meta['hash'] not in by:continue
 canon=sorted(by[meta['hash']],key=lambda x:(x['review']['disposition']!='analyzed',x['repo'],x['path']))[0]
 old=canon['review'];proof={k:canon[k] for k in ['repo','commit','path','hash']};proof['proof']='Git-blob SHA-256 equality at both frozen trees'
 matches.append({'path':meta['path'],'hash':meta['hash'],'canonical':proof,'review':old})
 note=('Locally scoped legal-license text, byte-identical to the recorded canonical source; no operational method.' if old['classification']=='license' else (old['reason'] if old['disposition']=='excluded' else old.get('semantic_conclusion',old['reason'])))
 if old['disposition']=='excluded':
  n['review'](r,meta['path'],note,excluded='Byte-identical to a previously content/role-inspected scope exclusion: '+old['reason'])
  row=next(x for rr in n['DATA']['repositories'] if rr['repo']==r for x in rr['coverage'] if x['path']==meta['path']);row['scope_inspection_source']=proof
 else:
  n['review'](r,meta['path'],note,keys=old.get('candidate_keys',[]),duplicate_of=proof)
  row=next(x for rr in n['DATA']['repositories'] if rr['repo']==r for x in rr['coverage'] if x['path']==meta['path']);row['depth']='byte-identical-external-semantic-review'
(out/'core-nextlevel-matches.json').write_text(json.dumps(matches,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
n['save']();print('NEXTLEVEL IDENTITIES',len(matches),collections.Counter(m['review']['disposition'] for m in matches))
