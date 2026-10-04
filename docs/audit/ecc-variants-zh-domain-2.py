"""Decisions only for four fully read Chinese/canonical language rule pairs."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
notes={
'php':{
'coding-style':'Same PHP/Composer scope, PSR/strict types/immutable DTO policy, validated domain input and versioned same-local/CI scripts; backend-patterns router preserved. Domain language conventions excluded; no extra prompt mechanism.',
'hooks':'Same PHP/config path predicates, after-edit format/static/behavior-change targeted tests and debug/rawSQL/session-protection warnings. Warning is not a block and configuration prose is not a registered callback.',
'patterns':'Same thin-controller/domain-service/DTO/adapter/constructor-contract recipes and API/Laravel routers. Application architecture examples not treated as new prompt/context methods.',
'security':'Same boundary input/output escape and rawHTML exception, uploaded-metadata distrust, writable-field allowlist, dependency/secret/session safeguards and Laravel router. These are domain policies, not complete security proof.',
'testing':'Same configured-Pest-over-default-PHPUnit selection, checked CI coverage settings, factory fixtures, transport-versus-business tests, conditional Inertia assertions and two skill pointers. Runner selection is a domain instance of capability-aware routing.'},
'python':{
'coding-style':'Same py/pyi scope/common pointer, PEP8/types, immutable DTO examples and format/import/lint tools with Python router. Domain implementation recipes excluded; no new agent method.',
'hooks':'Same scoped after-edit formatter/typechecker and print reminder. Host settings/tool availability must be established separately; reminder is not enforcement.',
'patterns':'Same protocols/dataclass DTO/context-manager/lazy-generator language examples plus Python router. Domain code examples excluded from prompt-pattern catalog.',
'security':'Same scope, required-secret/scanner and Django-conditional reference. bandit command on src is illustrative scan coverage, not whole-repository or runtime safety proof.',
'testing':'Same pytest runner, example src coverage and test categorization with python-testing router. Wrong project source target can invalidate measurement; no new method.'},
'perl':{
'coding-style':'Same five Perl path predicates, v5.36/signatures, readonly Moo attribute conditional exception, formatting options/lint theme and Perl router. Language/OO rules are domain examples, not new prompt instructions.',
'hooks':'Same after-edit perltidy/perlcritic and non-script print warning; exact common reference retained. Config prose does not prove registration or block behavior.',
'patterns':'Same DBI repository/typed DTO/safe-file/module export/reproducible-carton recipes and Perl router. Domain API examples excluded; shell example remains read, not executed.',
'security':'Same taint/environment/allowlist/list-form-process/SQL-placeholder and scanner rules. Shell-free argument principle already exists; realpath alone is not a root-containment proof. Domain snippets not endorsed as complete security.',
'testing':'Same Test2/prove lib-path requirement, repeated runner options, coverage/mocks/done_testing and Perl router. Fixed80% and eight jobs are source defaults, not adequacy or speed evidence.'},
'swift':{
'coding-style':'Same Swift/package scope, value semantics, role naming, typed errors and actor/Sendable/structured-concurrency domain choices. Vendor link retained; no current API facts inferred beyond frozen source.',
'hooks':'Same after-edit formatter/linter/build and production-print reminder. Callback prose is not actual execution; build result not inferred.',
'patterns':'Same protocols/associated-state/value/actor and dependency-injected mocks, actor-persistence/DI-test routers. Domain code details excluded from new prompt-method authoring.',
'security':'Same Keychain/build-secret/ATS/certificate/input-boundary advice. Application security policy is conditional domain guidance, not proof of complete protection or suitable pinning on every endpoint.',
'testing':'Same testing framework/isolation/parameterization/coverage command and DI-mock router. Fresh-instance statement is a source recipe, not guaranteed isolation of static/global/shared external state.'}
}
rows=[]
for language,files in notes.items():
    for name,note in files.items():
        rows.append({'path':f'docs/zh-CN/rules/{language}/{name}.md','reason':'Complete translated and corresponding canonical method prose/predicates/pointers/shell text read; semantically equivalent for these fields. '+note,'existing_ids':[69,177] if name=='hooks' else [23,53]})
(out/'ecc-variants-zh-domain-2.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
