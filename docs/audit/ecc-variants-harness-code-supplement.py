"""Record the bounded follow-up on method-bearing programming example deltas."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
s=json.loads((out/'ecc-variants-state.json').read_text(encoding='utf8'))
paths={r['path']:r for r in s['coverage']}
equal={
'.agents/skills/eval-harness/SKILL.md':'No excluded programming-language block; all shell/JSON grading instructions were in the original full method review.',
'.agents/skills/unified-memory/SKILL.md':'No excluded programming-language block; all typed memory/prompt/state instructions were read originally.',
'.cursor/skills/unified-memory/SKILL.md':'No excluded programming-language block; original complete typed memory/prompt/state comparison stands.',
'.kiro/skills/autonomous-loops/SKILL.md':'All ten programming-example lines match canonical after blank-line exclusion; unchanged body belongs to canonical reviewer, no distinct executable variant.',
'.agents/skills/dmux-workflows/SKILL.md':'No excluded programming-language block; all ownership/parallel/handoff instructions were included in initial review.',
'.agents/skills/tdd-workflow/SKILL.md':'All164 programming-example lines exactly match canonical after blank-line exclusion; no extra variant mechanism hidden in removed code projection.',
'.agents/skills/verification-loop/SKILL.md':'No excluded programming-language block; shell gates/verification were read originally.',
'.kiro/skills/verification-loop/SKILL.md':'No excluded programming-language block; complete shell gate deltas were read originally.'}
different={
'.kiro/skills/tdd-workflow/SKILL.md':'Complete programming-code delta read: removes canonical Bun test-import/empty-input/similarity-order example while other examples remain same. This reinforces runner-discovery omission; score-only sorted comparison does not establish an unspecified tie-order oracle. Domain tests not copied as proven behavioral coverage.',
'.agents/skills/security-review/SKILL.md':'Complete programming-code delta read: errors property differs from canonical issues; raw query retains PostgreSQL numbered placeholder where canonical generic sample has question-mark plus driver caveat; CSP source lacks base/object/frame fields and adds unsafe-eval/unsafe-inline strings. These are domain/config differences, not universal safe snippets; invocation-literal candidate must preserve actual driver syntax.',
'.kiro/skills/security-review/SKILL.md':'Complete programming-code delta read: same older errors field, PostgreSQL numbered placeholder and changed CSP fields/unsafe-eval/unsafe-inline as Codex mirror. No current library/browser runtime facts inferred; configuration correctness depends on actual consumer and threat model, and sample was not executed.'}
for path,note in (equal|different).items():
    paths[path].setdefault('supplemental_reviews',[]).append({'depth':'complete-programming-example-delta','reason':note})
payload=(json.dumps(s,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode()
(out/'ecc-variants-state.json').write_bytes(payload)
(out/'harvest-ecc-variants.json').write_bytes(payload)
print('Recorded',len(equal)+len(different),'supplemental code checks; dispositions unchanged')
