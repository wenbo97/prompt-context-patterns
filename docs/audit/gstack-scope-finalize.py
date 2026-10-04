"""Close only evidenced reads; support inspection never becomes a full audit."""
import collections
import json
from pathlib import Path

def read(name):
    return json.loads(Path(name).read_text('utf-8'))

report = read('docs/audit/harvest-gstack.json')
roles = read('docs/audit/gstack-support-role-review.json')['role_reviewed']
shapes = {r['path']: r for r in read('.tools/gstack/support-shapes.json')}
blocks = {r['path']: r for r in read('.tools/gstack/blocks.json')['files']}
state = read('docs/audit/gstack-review-state.json')
literals = read('docs/audit/gstack-embedded-review.json')['read_literals']
direct_path = Path('docs/audit/gstack-direct-full-review.json')
direct = read(direct_path) if direct_path.exists() else {}
data_path=Path('docs/audit/gstack-data-review.json')
data=read(data_path)['containers'] if data_path.exists() else {}

for row in report['coverage']:
    name = row['path']
    # Preserve previously closed exclusions and exact duplicates. The role
    # ledger spans more paths than the pending-only support-shapes cache, so
    # reprocessing every historical row can index a shape that was never
    # collected for that already-closed path.
    if row['disposition'] in ('excluded', 'duplicate'):
        continue
    if name in direct:
        proof = direct[name]
        if proof['hash'] != row['hash']: raise ValueError('Direct-read hash mismatch: '+name)
        row.update(disposition='analyzed', classification='method-example-or-prompt-builder',
                   review_kind='full-semantic', review_depth='complete-frozen-body-read-for-pattern-relevance',
                   reason=proof['conclusion'], review_evidence={'ledger':str(direct_path).replace('\\','/'),'path':name,'source_hash':row['hash']})
        continue
    if row['disposition'] == 'analyzed':
        body = blocks.get(name)
        if body:
            changed = [h for h in body['blocks'] if h in state.get('delta_reads', {}) or h in state['parameter_block_aliases']]
            row['review_kind'] = 'difference-review' if changed else 'full-semantic'
            row['review_evidence'] = {'ledger': 'docs/audit/gstack-review-state.json', 'path': name,
                                      'body_block_count': len(body['blocks']), 'difference_block_count': len(changed),
                                      'source_hash': row['hash'], 'notes': 'Complete body blocks or verified shared content plus all displayed differences; source observations are in gstack-observations.md.'}
        continue
    if name in data:
        proof=data[name]
        if proof['source_hash'] != row['hash']: raise ValueError('Data scope hash mismatch: '+name)
        fields=', '.join(k for k,n in proof['field_roles'][:10]) or 'empty array'
        row.update(disposition='excluded',classification='parsed-runtime-metadata-or-observation-data',review_kind='scoped-relevance',
                   review_depth='whole-container-structure-and-purpose-with-separate-method-field-review',
                   reason='Actual JSON field roles inspected: '+fields+'. Container is runtime metadata, passive source/section indexing, domain fixture or captured observation data. It supports the separately reviewed workflow/consumer rather than adding an independently admitted prompt/context mechanism. Historical failures and synthetic controls do not become efficacy evidence; embedded method fields are separately fully read.',
                   review_evidence={'ledger':str(data_path).replace('\\','/'),'path':name,'source_hash':row['hash'],
                                    'method_ledger':'docs/audit/gstack-data-method-review.json','method_field_count':len(proof['method_fields']),
                                    'scope':'Structural parser inventory plus actual displayed field roles/provenance; not full semantic review of every raw observation.'})
        continue
    if name not in roles:
        continue
    shape = shapes[name]
    if shape['sha256'] != row['hash']:
        raise ValueError('Scope hash mismatch: ' + name)
    symbols = shape.get('symbols', [])
    checks = shape.get('checks', [])
    imports = shape.get('imports', [])
    facts = []
    if checks: facts.append('test contracts include ' + '; '.join(checks[:3]))
    if symbols: facts.append('declares ' + ', '.join(symbols[:5]))
    if imports: facts.append('depends on ' + ', '.join(imports[:3]))
    if shape['kind'] == 'binary': facts.append('binary asset signature ' + shape['magic_hex'][:16])
    if not facts:
        opening = shape.get('first_lines', '').splitlines()
        facts.append('source-opening role/content: ' + ' '.join(opening[:5])[:230])
    reviewed = [l['sha256'] for l in shape.get('literals', []) if l['sha256'] in literals]
    row.update(disposition='excluded', classification='implementation-test-or-domain-support',
               review_kind='scoped-relevance', review_depth='purpose-and-relationship-with-separate-embedded-method-review',
               reason='Content/structure inspected: ' + '; '.join(facts) + '. Runtime plumbing, regression assertions or domain data is excluded as a separate reusable prompt/context pattern. Embedded method inputs reviewed separately are identified in the evidence; no comprehensive correctness, security or performance audit is claimed.',
               review_evidence={'role_ledger': 'docs/audit/gstack-support-role-review.json', 'path': name,
                                'source_hash': row['hash'], 'embedded_ledger': 'docs/audit/gstack-embedded-review.json',
                                'fully_read_literal_hashes': reviewed,
                                'scope': 'Selected source opening and AST structures support purpose/relationship review; extraction counts are not semantic completion.'})

by_path={r['path']:r for r in report['coverage']}
by_hash={}
for r in shapes.values():by_hash.setdefault(r['sha256'],[]).append(r)
blobs={r['path']:r for r in read('.tools/gstack/support-blobs.json')}
for group in by_hash.values():
    if len(group)<2:continue
    base=next((r for r in group if by_path[r['path']]['disposition'] in ['analyzed','excluded']),None)
    if not base:continue
    for r in group:
        if r['path']==base['path']:continue
        if blobs[r['path']].get('text') != blobs[base['path']].get('text'):raise ValueError('Hash equality without byte-text equality')
        row=by_path[r['path']]
        row.update(disposition='duplicate',review_kind='verified-equivalence',review_depth='exact-frozen-byte-equivalence-to-reviewed-base',
                   reason='Exact frozen bytes and Git blob identity verified equal to '+base['path']+'; reuse that reviewed '+by_path[base['path']]['review_kind']+' relevance conclusion without promoting it to a full implementation audit.',
                   review_evidence={'base_path':base['path'],'base_hash':base['sha256'],'base_review_kind':by_path[base['path']]['review_kind'],'same_git_blob':r['git_oid']==base['git_oid'],'full_text_equal':True})
counts = collections.Counter(r['disposition'] for r in report['coverage'])
report['summary'].update(status='in_progress' if counts['pending'] else 'complete', coverage_counts=dict(counts),
                         files_analyzed=counts['analyzed'],
                         review_kind_counts=dict(collections.Counter(r.get('review_kind','pending') for r in report['coverage'])))
Path('docs/audit/harvest-gstack.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n','utf-8',newline='')
print(json.dumps(report['summary'], ensure_ascii=False))
