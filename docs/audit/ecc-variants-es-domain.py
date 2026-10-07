"""Persist all fifteen individually read Spanish language-rule bodies plus index."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
rows=[r for r in json.loads((out/'ecc-variants-zh-domain-1.json').read_text(encoding='utf8')) if '/golang/' in r['path']]
rows += [r for r in json.loads((out/'ecc-variants-zh-domain-2.json').read_text(encoding='utf8')) if '/python/' in r['path']]
rows += [r for r in json.loads((out/'ecc-variants-zh-domain-3.json').read_text(encoding='utf8')) if '/typescript/' in r['path']]
for row in rows:
    row['path']=row['path'].replace('docs/zh-CN/','docs/es/')
    row['reason']='Complete Spanish method prose/path predicates/common and skill pointers/shell commands read and semantically compared to previously fully read current canonical counterpart. '+row['reason']
    row['reason']+=' No material method-control/reference delta; programming-language application examples explicitly excluded domain detail, not assumed translated-body equality.'
    if row['path'].endswith(('golang/coding-style.md','python/coding-style.md')):row['reason']+=' Final idioms description is mistranslated as idiomas (languages), without changing the target skill identifier.'
rows.append({'path':'docs/es/rules/README.md','reason':'Read complete Spanish rules overview and compare to fully read canonical index. Wholesale condensed rewrite inventories common/Go/Python/TS topics and declares common/language/path-based behavior, but omits actual install commands, whole-directory hierarchy warning, ECC-owned user/project namespace and specific-over-general precedence/new-language authoring policy. Auto-loaded/applied statement needs actual installed host proof. No complete index equivalence or new method; canonical owner reference is prose code path, not verified installation.','existing_ids':[23,114,172,177]})
(out/'ecc-variants-es-domain.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
