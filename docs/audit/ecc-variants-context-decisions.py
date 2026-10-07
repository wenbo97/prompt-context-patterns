"""Record all twelve fully read translated context modes."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
notes={
'dev':'Development mode prioritizes working/correct/clean output, code-first explanation order, atomic commits and changes-followed-by-tests with edit/write/build/search tool preferences. This is a context specialization of task-mode routing; it does not authorize unrequested writes or establish a test result.',
'research':'Research mode uses question→source exploration→hypothesis→evidence→finding sequence, clarification and incremental notes, and findings before recommendations. Named web/explorer tools are conditional host capabilities, not proof that they exist; unclear understanding is not a measured gate.',
'review':'Review mode uses complete contextual reading, severity-ranked issues with fix suggestions, explicit logic/edge/error/security/performance/readability/test checklist and file-grouped findings. This prompt alone does not enforce read-only capability or establish vulnerability absence.'}
rows=[]
for locale in ('zh-CN','ja-JP','es','tr'):
    for mode,note in notes.items():
        rows.append({'path':f'docs/{locale}/contexts/{mode}.md','reason':'Read entire translated context and canonical counterpart; complete method semantic/structural equivalence, only language/spacing changes. '+note,'existing_ids':[3,20,53]})
(out/'ecc-variants-context-decisions.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
