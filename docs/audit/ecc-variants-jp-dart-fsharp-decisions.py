"""Record ten complete translated/canonical method comparisons, truncations repaired."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
notes={
'dart':{
'coding-style':'Same Dart/project-config predicates, conditional null-crash/intentional detached Future, explicit generated-file commit-or-ignore policy and canonical generator-only edits. Language/API implementations excluded; format/naming/version defaults are frozen project policy, not current standard or behavior proof.',
'hooks':'Same full formatter/analyzer/affected-test/precommit workflow and JSON matcher/command sample. Unquoted CLAUDE_FILE_PATHS string and matcher-object syntax do not prove safe argv or accepted host schema. Regeneration/upgrades mutate state and optional test reminders are not executed checks.',
'patterns':'Same domain repository/state/DI/use-case/generated-state/layer graph and navigation recipes plus review/KMP references. Application Dart framework code excluded from new prompt mechanism; declared pure-domain layering is a project choice, not universal requirement.',
'security':'Same compile-time-config-is-not-secret warning, backend proxy versus runtime platform store, URL scheme/host/path validation, permissions, intentional JavaScript gate and actual release analysis. Domain platform/library implementation excluded; fixed framework versions, FLAG_SECURE and obfuscation labels are not proof of end-to-end secret containment.',
'testing':'Same unit/widget/golden/device separation, controlled time/fakes, intentional visual-only baseline update, behavior names/state transitions and CI coverage gate. Domain testing implementation excluded; no golden/coverage update executed and80% threshold does not establish complete behavioral proof.'},
'fsharp':{
'coding-style':'Same fs/fsx scope, conditionally mutable interop/performance exception, typed union/record/Option/Result, cancellation propagation, focused functions and ordered namespace sections. Domain F# implementation excluded; no new prompt method.',
'hooks':'Same source/project/solution/build-props predicates and after-edit formatter/build/nearest test plus broad-session final build/config warning. --no-build needs corresponding fresh artifacts; declared hook is not accepted registration or executed check.',
'patterns':'Same expected-error Result, missing-value Option, explicit domain variants, qualified module/collision avoidance and functional dependency injection. These are language/application recipes excluded from agent-method catalog, not new variant mechanisms.',
'security':'Same secret/config/input/typed-boundary/parameterized-query/authorization and safe-client-versus-server-error policy with reviewer router. Domain security implementations excluded; no runtime protection or library/standard compatibility inferred.',
'testing':'Same project/source test organization, behavior names, property tests, real infrastructure and HTTP middleware/auth boundary route. Domain FsCheck/framework implementation excluded;80% and package choices are source defaults, not model or program outcome evidence.'}}
rows=[]
for language,files in notes.items():
    for name,note in files.items():
        rows.append({'path':f'docs/ja-JP/rules/{language}/{name}.md','reason':'Read complete Japanese method prose/predicates/pointers and all shell/JSON/XML/template examples against complete canonical text; repaired truncated canonical Dart sections before disposition. Semantic equivalence of method fields, no material translation control delta. '+note,'existing_ids':[69,177] if name=='hooks' else [23,53]})
(out/'ecc-variants-jp-dart-fsharp-decisions.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
