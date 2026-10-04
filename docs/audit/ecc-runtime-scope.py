"""Scope discovery only: preserve whole literal payloads and source-range identity.

Does not execute upstream code or mark any source semantically analyzed.
"""
import hashlib,importlib.util,json,pathlib,re,sys
out=pathlib.Path(__file__).parent
production_only='--production-literals' in sys.argv
requested=[v for v in sys.argv[1:] if v!='--production-literals'] or ['ecc2/src/config/mod.rs','ecc2/src/main.rs','ecc2/src/session/daemon.rs','ecc2/src/session/manager.rs','ecc2/src/session/store.rs','ecc2/src/tui/dashboard.rs']
spec=importlib.util.spec_from_file_location('ecc_corpus',out/'ecc-corpus.py')
corpus=importlib.util.module_from_spec(spec);sys.argv=[sys.argv[0],'library'];spec.loader.exec_module(corpus)
records=[]
literal=re.compile(r'(?P<comment>//[^\n]*|/\*[\s\S]*?\*/)|(?P<char>\'(?:\\.|[^\'\\\n])\')|r(?P<hashes>#{0,16})"(?P<raw>[\s\S]*?)"(?P=hashes)|"(?:\\.|[^"\\])*"')
for p in requested:
    body=corpus.text(p);lines=body.splitlines()
    declarations=[]
    for i,line in enumerate(lines,1):
        if re.match(r'^\s*(?:(?:pub(?:\([^)]*\))?|async|unsafe|const)\s+)*fn\s+',line):
            declarations.append({'line':i,'signature':line.strip()})
    long_literals=[]
    for m in literal.finditer(body):
        if m.group('comment') is not None or m.group('char') is not None:continue
        value=m.group('raw') if m.group('raw') is not None else m.group(0)[1:-1]
        if len(value)>=120 or '\\n' in value or '\n' in value:
            line=body.count('\n',0,m.start())+1
            long_literals.append({'start_line':line,'end_line':body.count('\n',0,m.end())+1,'literal':value})
    record={'path':p,'hash':hashlib.sha256(body.encode()).hexdigest(),'lines':len(lines),
            'header':lines[:38],'declarations':declarations,'long_literals':long_literals,'disposition':'pending','scope_only':True}
    records.append(record)
    print('\n###',p,'header and declarations')
    if not production_only:
        print('\n'.join(f'{i+1}: {s}' for i,s in enumerate(record['header'])))
        print('\n'.join(f"{r['line']}: {r['signature']}" for r in declarations))
    print('LONG LITERALS:')
    test_start=next((i for i,l in enumerate(lines,1) if l.strip()=='#[cfg(test)]' and i>800),len(lines)+1)
    for r in long_literals:
        if not production_only or r['start_line']<test_start:print(f"{r['start_line']}..{r['end_line']}: {r['literal']}")
artifact=out/'ecc-runtime-scope.json'
prior={r['path']:r for r in json.loads(artifact.read_text(encoding='utf-8'))} if artifact.exists() else {}
prior.update({r['path']:r for r in records})
artifact.write_text(json.dumps(list(prior.values()),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
