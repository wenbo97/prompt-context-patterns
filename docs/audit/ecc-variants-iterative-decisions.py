"""Close retrieval translations only after both prose and method-bearing JS were compared."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
rows=[]
for locale in ('zh-CN','ja-JP','ko-KR','zh-TW'):
    reason='Read all translated prose/agent prompts/examples and canonical counterpart, plus all54 method-bearing JavaScript lines (not excluded as domain code). Same dispatch→evaluate→gap/terminology/pattern refinement→bounded cycle, relevance reason/gap record, low-score exclusion, cumulative best-context and early-return predicate. '
    if locale=='zh-CN':reason+='Code exactly retains canonical English comments and controls; manual install agent-directory pointer is current. '
    elif locale=='ko-KR':reason+='All54 programming lines match canonical after blank-line exclusion; source agent-directory pointer is older unqualified ~/.claude/agents. '
    else:reason+='Complete translated JS comment delta preserves controls/symbols; activation section omitted and older ~/.claude/agents pointer replaces current install-conditional router. '
    reason+='Source score cutoffs/three-files/three-cycles are heuristics, not calibrated relevance or evidence completeness. Excluding tests can lose behavioral context, early return can omit earlier relevant files, and low relevance can change with new gaps; max-cycle return needs an explicit incomplete state. Prototype helper names have no implementation here. No new variant mechanism or retrieval/agent execution.'
    rows.append({'path':f'docs/{locale}/skills/iterative-retrieval/SKILL.md','depth':'full-semantic-and-method-code','reason':reason,'candidate_keys':['ecc-iterative-gap-retrieval'],'existing_ids':[23,36,41,100,175]})
(out/'ecc-variants-iterative-decisions.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
