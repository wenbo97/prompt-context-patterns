"""Explicit decisions for three language rule trees read with their canonical prose."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
notes={
'cpp':{
'coding-style':'Same seven C++/CMake path predicates, common-rule pointer, modern features/RAII/ownership/project naming and formatter plus cpp-coding-standards router. Domain resource/naming recipes do not add a prompt method.',
'hooks':'Same before-commit format/static/build/test checks and ordered CI pipeline. Fixed src globs/std=c++17 are illustrative assumptions, not project discovery; prose does not register a runtime hook.',
'patterns':'Same common pointer, RAII/zero-five/value-semantics/result-type recipe and skill router. C++ implementation excluded as domain detail; no additional agent mechanism.',
'security':'Same scoped paths, unsafe-memory/string/UB checks, sanitizer/static-analysis commands and skill router. Domain security recipes do not prove complete protection or actual check execution.',
'testing':'Same GoogleTest/CMake/CTest, build-before-test, coverage/sanitizer commands and cpp-testing router. Workflow is configured validation, not test-result proof; domain runner details add no new mechanism.'},
'csharp':{
'coding-style':'Same cs/csx scope, record/entity/interface distinction, immutable update, cancellation propagation and explicit async/errors/formatter. Domain C# API examples excluded from new prompt methods.',
'hooks':'Same expanded project/solution/build-props scope, after-edit formatter/build/nearest-relevant-test and broad-session final build/config-secrets warning. No runtime registration or built-artifact freshness proof merely from test --no-build.',
'patterns':'Same cs/csx scope/common pointer, typed API/repository/options and deliberate DI lifetimes. Domain application patterns excluded from extra prompt-method authorship.',
'security':'Same source/project/appsettings scope, secret management, parameters/dynamic-field validation, DTO/auth boundary and safe client versus detailed server errors; same security-review router. No new mechanism from domain security advice.',
'testing':'Same behavior-named test organization, real-infrastructure integration, HTTP auth/middleware path and targeted domain/failure coverage. Supports alternate-path fidelity concept, but no new variant; 80% is unverified project threshold.'},
'golang':{
'coding-style':'Same go/mod/sum path scope/common pointer, gofmt/goimports, consumer-small-interface and contextual error policy plus golang-patterns router. Application code conventions excluded from new prompt pattern.',
'hooks':'Same scoped after-edit formatter/vet/staticcheck mapping and common hook pointer. Event prose is not actual registration or enforcement proof.',
'patterns':'Same functional options, consumer interface and constructor injection with golang-patterns router. Domain Go implementations excluded; no agent mechanism added.',
'security':'Same scope/common pointer, required-secret and gosec/context-timeout domain recipes. Tool-specific scanning example is not complete security or execution evidence.',
'testing':'Same scope/common pointer, table-driven standard runner, race/coverage commands and golang-testing router. Actual race detection applicability/results must be verified per project; no new prompt mechanism.'}
}
rows=[]
for language,files in notes.items():
    for name,note in files.items():
        rows.append({'path':f'docs/zh-CN/rules/{language}/{name}.md','reason':'Read complete Simplified Chinese method prose, predicates, pointers and shell examples plus corresponding complete canonical method text; semantically equivalent for these fields. '+note,'existing_ids':[69,177] if name=='hooks' else [23,53]})
(out/'ecc-variants-zh-domain-1.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
