"""Persist decisions after complete Japanese/common semantic reads."""
import json,pathlib
out=pathlib.Path(__file__).resolve().parent
rows=json.loads((out/'ecc-variants-common-zh.json').read_text(encoding='utf8'))
overrides={
'agents.md':'Complete Japanese semantic comparison: plugin namespace, resource router, task routing, independent parallel reviews and diverse lenses retained. Omits current Rust/HarmonyOS roster rows and delegation result-collection/depth/completion contract. No new mechanism; spawning a child alone is not task completion.',
'code-review.md':'Complete semantic comparison retains CI/conflict/base pre-review gate and severity/report/router workflow. Security trigger translates use-agent without canonical STOP. Hard 800-line rule omits current soft source-role exception; HIGH warning versus other role blocking remains source inconsistency. Domain checklists and source numeric thresholds are not calibrated proof.',
'coding-style.md':'Complete semantic comparison retains immutable contrast, schema boundary validation, explicit errors and completion checklist; omits canonical KISS/DRY/YAGNI, language-dependent naming and soft source-size/test/generated exceptions. No distinct prompt method from domain style policy.',
'development-workflow.md':'Complete Japanese semantic equivalent includes repository-first reuse, version-grounded primary docs, registry search, dependency planning, RED/GREEN, code review and final CI/conflict/base pre-review gate. Source 80% defaults and mandatory named agents are frozen project assumptions, not efficacy or live capability evidence.',
'git-workflow.md':'Complete comparison preserves full-history/triple-dot PR summary, commit format and explicit user attribution choice, but embeds older feature/TDD/review workflow instead of canonical router to separate development-workflow. This duplication can drift; TODO tests are planned rather than observed validation.',
'performance.md':'Complete semantic comparison retains complexity model tiers, context headroom, multiple critique lenses and incremental build verification. Pins Haiku4.5/Sonnet5/Opus5 where canonical uses generic families. 90% capability, one-third cost, last20% and 31,999 default are unverified source assertions, not current vendor facts.',
}
for r in rows:
    r['path']=r['path'].replace('docs/zh-CN/','docs/ja-JP/')
    name=r['path'].split('/')[-1]
    if name in overrides:r['reason']=overrides[name]
    else:r['reason']='Complete Japanese semantic comparison: '+r['reason'].split(': ',1)[-1]
(out/'ecc-variants-common-jp.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
