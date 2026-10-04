"""Persist completed Chinese/canonical TypeScript, Java, Kotlin and Rust reads."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
notes={
'typescript':{
'coding-style':'Same four TS/JS paths, explicit public types/local inference, unknown narrowing, named React props, JSDoc/runtime parity, immutable update/error/schema and logging policy. Language implementation examples excluded; shallow spread is not deep immutability.',
'hooks':'Same after-edit formatter/tsc/reminder and modified-files Stop audit. Reminder versus actual blocking must be distinguished; source registration/config prose not runtime proof.',
'patterns':'Same common pointer and domain TS response/React debounce/repository code recipes; no additional prose mechanism. Application implementations excluded from agent catalog.',
'security':'Same required-secret domain example and security-reviewer router. Both canonical and translation call a reviewer agent a skill; capability type must be verified before invocation, not invented.',
'testing':'Same scoped Playwright critical-flow runner and e2e-runner role pointer. Domain tool selection is a frozen project default, not available/tested capability proof.'},
'java':{
'coding-style':'Same Java scope, project indentation, records/defensive copies, version-conditioned modern features, Optional and contextual errors/streams plus Java/JPA routers. Domain Java code excluded from prompt-method extraction.',
'hooks':'Same Java/Maven/Gradle scope, formatting/checkstyle and wrapper compilation verification; prose does not register callbacks and actual detected build-tool choice is prerequisite.',
'patterns':'Same repository/service/constructor/DTO/builder/sealed-state/response recipes. Translation Quarkus pointer says Camel/Panache where canonical says REST/Panache/messaging; altered domain routing description, not a new prompt mechanism.',
'security':'Same secret/input/SQL/auth/dependency and safe-client/detailed-server-error policy; Spring/Quarkus/general routers retained. Dependency tree is inventory, not a vulnerability scan result.',
'testing':'Same JUnit/Mockito/Testcontainers, layer-mirrored/behavior-named tests and coverage. Translation Quarkus resource description says Camel tests where canonical says Dev Services; pointer still same skill. 80%/skip-trivial rules are project defaults, not behavior proof.'},
'kotlin':{
'coding-style':'Same kt/kts scope, immutable-value preference/naming/null/sealed/scope-function and cancellation-rethrow rules. Domain language API code excluded. Read-only collection interface and shallow copy do not guarantee deep immutability.',
'hooks':'Same kt/kts/Gradle scope, after-edit formatter/static analysis/build verification. No actual registration, runner detection or successful build inferred.',
'patterns':'Same constructor/one-way-state/repository/use-case/platform/coroutine/DSL recipes and coroutine/Android routers. Child-failure independence is an application concurrency recipe, not agent delegation evidence.',
'security':'Same Android/iOS secret/network/input/auth/release/WebView domain policy, including release-byte tests and conditional JavaScript. BuildConfig is embedded release data, not confidential secret storage; numeric/code/API guidance not promoted as verified security.',
'testing':'Same configured KMP/Android frameworks, handwritten fakes, virtual-time coroutine, mock engine/memory DB, behavior names and layer organization. Framework time/isolation claims are source examples requiring runtime proof; no new agent method.'},
'rust':{
'coding-style':'Same rs scope, formatter/clippy, ownership/context errors, domain-organized/private/public API policy and Rust router. Language implementation code excluded from prompt-pattern authorship.',
'hooks':'Same rs/Cargo scope, after-edit formatter/clippy/check. Source faster-than-build claim not measured; config text is not callback/result proof.',
'patterns':'Same trait/repository/service/newtype/exhaustive state/builder/sealed trait/response recipes and Rust router. Domain type-system/architecture implementation excluded from new agent mechanism.',
'security':'Same required-secret, parameterized query, typed boundary parse, unsafe-invariant comment/review, dependency scanning and safe-client/server error policy. Commentary on unsafe invariant is a claim to check, not safety proof; no security guidance endorsed solely from prose.',
'testing':'Same unit/integration placement, parametrization/proptest/mock/async, behavior names and domain-target coverage/command routers. Source80% is a project threshold, not adequacy; test outcomes not executed or inferred.'}
}
rows=[]
for language,files in notes.items():
    for name,note in files.items():
        rows.append({'path':f'docs/zh-CN/rules/{language}/{name}.md','reason':'Read complete translated and canonical method prose, all path predicates, resource pointers and shell/XML examples; semantic comparison recorded. '+note,'existing_ids':[69,177] if name=='hooks' else [23,53]})
(out/'ecc-variants-zh-domain-3.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
