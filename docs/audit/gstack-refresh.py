"""Refresh occurrence coverage from the explicit, actually-read block ledger."""
import json
from pathlib import Path

def read(path):
    return json.loads(Path(path).read_text('utf-8'))

state = read('docs/audit/gstack-review-state.json')
cache = read('.tools/gstack/blocks.json')
report = read('docs/audit/harvest-gstack.json')
seen = set(state['read_blocks']) | set(state['parameter_block_aliases'])
closed = {f['path']: f for f in cache['files'] if all(h in seen for h in f['blocks'])}
for row in report['coverage']:
    if row['path'] not in closed:
        continue
    if row['disposition'] == 'excluded':
        continue
    row.update(disposition='analyzed', classification='normative-skill-or-template' if row['path'].endswith(('SKILL.md','SKILL.md.tmpl')) else 'prose-or-reference',
               reason=state['file_notes'].get(row['path'],
                   'Every heading block reviewed, including source-specific deltas and exact shared lines; entry routing, required outputs, fallbacks and authority/measurement limitations examined. Referenced files are separately tracked.'),
               review_depth='full-body-via-exact-blocks-and-reviewed-line-deltas')
report['summary'].update(status='in_progress', files_analyzed=sum(r['disposition']=='analyzed' for r in report['coverage']),
                         reviewed_unique_blocks=len(state['read_blocks']), parameter_alias_blocks=len(state['parameter_block_aliases']),
                         delta_reads=len(state.get('delta_reads',{})),
                         coverage_counts={d:sum(r['disposition']==d for r in report['coverage']) for d in ['analyzed','duplicate','excluded','pending']})
Path('docs/audit/harvest-gstack.json').write_text(json.dumps(report,ensure_ascii=False,indent=2).replace('\n','\r\n')+'\r\n','utf-8', newline='')
print(json.dumps(report['summary']))
