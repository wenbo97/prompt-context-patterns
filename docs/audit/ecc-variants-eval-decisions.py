"""Persist the six eval translations after complete semantic/prompt/example reading."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
rows=[]
for locale in ('zh-CN','ja-JP','es','ko-KR','tr','zh-TW'):
    reason='Read complete translated eval skill, all fenced grader prompts/definitions/reports/shell commands and current canonical text. Retains pre-defined capability/regression/baseline evals, code/model/human graders, attempt-success versus all-trials-success distinction, versioned artifacts and staged report. '
    if locale in ('ja-JP','zh-TW'):reason+='Older version omits activation section and ProductEvals rule-grader/overfit/cost-latency/flaky-checker/extra artifact guidance. '
    elif locale=='es':reason+='Condensed version omits full authentication worked example, ProductEvals framing/rule-grader list and minimal release-artifact layout, but retains retry/reliability and overfit/cost/flaky-checker anti-patterns. '
    else:reason+='ProductEvals rule-grader, overfit/cost-latency/flaky-checker and release-artifact sections retained. '
    reason+='All six omit current LocalFrameworkUtilities and refusal of candidate execution absent reviewed OS containment, including receipt/static-warning-versus-promotion proof boundary. No safe execution implied. grep presence is not behavior; echo FAIL can still exit zero. Example pass@ percentages/90%/100% thresholds are targets or fabricated reports, not empirical model reliability; repeated independent-trial evidence is required.'
    keys=['ecc-eval-before-build','ecc-reliability-metrics','ecc-protected-acceptance','ecc-live-state-proof']
    if locale=='zh-CN':
        reason+=' Chinese example translates report command verb at L211 unlike canonical literal report; absent verified localized grammar, do not claim command equivalence.'
        keys.append('ecc-variants-localization-symbol-integrity')
    rows.append({'path':f'docs/{locale}/skills/eval-harness/SKILL.md','reason':reason,'candidate_keys':keys,'existing_ids':[52,53,119,175,177]})
(out/'ecc-variants-eval-decisions.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
