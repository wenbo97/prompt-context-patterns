from pathlib import Path
import json,collections
n={'__name__':'core_helpers'};exec(Path(__file__).with_name('core-update.py').read_text(encoding='utf-8'),n)
queue=[]
for rr in n['DATA']['repositories']:
 if rr.get('external_owner')=='root':continue
 inv={f['path']:f for f in n['BY_REPO'][rr['repo']]['files']}
 for row in rr['coverage']:
  if row['disposition']=='pending':continue
  meta=inv[row['path']]
  source={'repo':rr['repo'],'commit':rr['commit'],'path':row['path'],'blob':meta['blob'],'hash':meta['hash']}
  evidence=row.get('review_evidence',{'frozen_source':source,'content_role_and_conclusion':row.get('semantic_conclusion','')})
  evidence['frozen_source']=source
  if 'exact_line_reuse' in row:
   row['review_kind']='difference-review';evidence['line_difference_ledger']=row['exact_line_reuse']
  elif 'exact_block_review' in row:
   row['review_kind']='full-semantic';evidence['exact_block_ledger']=row['exact_block_review']
  elif 'duplicate_of' in row or 'scope_inspection_source' in row:
   proof=row.get('duplicate_of',row.get('scope_inspection_source'))
   if isinstance(proof,str):proof={'repo':rr['repo'],'commit':rr['commit'],'path':proof,'hash':meta['hash']}
   row['review_kind']='verified-equivalence';evidence['equivalence_proof']=proof
  elif row.get('review_kind'):
   pass
  elif row['disposition']=='analyzed':
   row['review_kind']='full-semantic' if 'rendered' in row.get('depth','') or meta['classification'] not in ['license'] else 'scoped-relevance'
   evidence['existing_review_record']='harvest-core.json repositories['+rr['repo']+'].coverage['+row['path']+']; concrete per-path semantic conclusion retained'
  else:
   row['review_kind']='scoped-relevance'
   # Do not disguise old coarse path/type-only classifications as content inspection.
   queue.append({'repo':rr['repo'],'commit':rr['commit'],'path':row['path'],'hash':row['hash'],'reason':row['reason'],'prior_conclusion':row.get('semantic_conclusion','')})
   evidence['refresh_required']='Actual content/declaration/reference or artifact role inspection must supplement the former scope exclusion before final delivery.'
  row['review_evidence']=evidence
 # Source classification stays intact, but completion cannot outrun a new evidence requirement.
 missing=[q for q in queue if q['repo']==rr['repo']]
 if missing:
  rr['summary']['evidence_refresh_pending']=len(missing)
  rr['summary']['status']='in_progress'
(n['OUT']/'core-scope-refresh-queue.json').write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
n['save']();print('KINDS',collections.Counter(f.get('review_kind') for r in n['DATA']['repositories'] if r.get('external_owner')!='root' for f in r['coverage'] if f['disposition']!='pending'));print('REFRESH',collections.Counter(q['repo'] for q in queue))
