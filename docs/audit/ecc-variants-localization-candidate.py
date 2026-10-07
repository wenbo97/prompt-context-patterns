"""Author a symbol-integrity lesson from fully read translated glossary instructions."""
import pathlib,json
out=pathlib.Path(__file__).resolve().parent
s=json.loads((out/'ecc-variants-state.json').read_text(encoding='utf8'))
commit=s['commit']
candidate={
'key':'ecc-variants-localization-symbol-integrity',
'name_en':'Preserve Executable Identifiers Across Localization',
'name_zh':'本地化时保留可执行标识符',
'category':'skill-authoring',
'tags':['localization','literal-identifiers','adapter-metadata','reference-integrity'],
'summary_en':'Translate narrative while retaining the literal skill names, command invocations, paths and schema keys that the consuming harness resolves.',
'summary_zh':'翻译说明文字，同时保留宿主实际解析的技能名、调用命令、路径和元数据字段名。',
'status':'active','origin_status':'unknown','example_origin':'teaching-construction','validation_status':'editorial-review-only',
'scores':{'scenario':2,'mechanism':2,'contrast':2,'observable':2,'boundaries':2},
'suggested_existing_ids':[],'related_existing_ids':[166,171,172,190],
'related_candidate_keys':['ecc-variants-invocation-literal-boundary'],
'content':{
'en':{
'description':'Separate translated explanation from literal symbols used by an instruction loader or reference resolver.',
'scenario':'Localize a skill whose known identity is name: release-check, invocation is $release-check, and reference is references/checklist.md. The task authorizes translation, not renaming.',
'mechanism':'List the executable identifiers and schema keys first; translate prose around that literal set. Compare the localized parsed identity, invocation and reference target against the original.',
'bad':'Translate this release-check skill into Chinese, including name: release-check as 名称: 发布检查 and references/checklist.md as 参考/检查表.md. Keep the existing files and launcher unchanged.',
'good':'Translate this release-check skill into Chinese. Keep name: release-check, $release-check, references/checklist.md and YAML field keys literal. Translate description and narrative. Report whether parsed name and reference target still equal the originals.',
'why':'A translated label is readable to people, but changing a machine-resolved key or path can redirect or break discovery despite an otherwise accurate translation.',
'expected':'The narrative is Chinese, the loader still sees release-check, and the existing reference resolves. These comparisons are inspectable acceptance checks; the example was not executed.',
'boundaries':'Protect actual machine-resolved identifiers, not every English technical word. An authorized rename needs a separate migration of consumers and references. Do not infer runtime activation solely from a syntactically valid document.'},
'zh':{
'description':'将可翻译的说明与加载器、引用解析器实际使用的字面标识符分开。',
'scenario':'将技能翻译成中文：已知身份为 name: release-check，调用为 $release-check，引用为 references/checklist.md；任务只授权翻译，没有授权改名。',
'mechanism':'先列出可执行标识符和元数据字段名，再翻译该集合之外的说明。将本地化后的解析身份、调用名和引用目标与原文逐项比较。',
'bad':'将 release-check 技能全部翻译成中文，把 name: release-check 改为 名称: 发布检查，把 references/checklist.md 改为 参考/检查表.md。保留现有文件和启动器。',
'good':'将 release-check 技能说明翻译成中文。保留 name: release-check、$release-check、references/checklist.md 和 YAML 字段名。翻译 description 的值和正文说明，报告解析名称及引用目标是否仍与原文一致。',
'why':'翻译后的名称适合阅读，但机器解析的字段或路径变化可能改变发现行为，即使其他说明翻译准确。',
'expected':'说明是中文，加载器仍读取 release-check，现有引用仍可解析。这些是可检查的验收条件，教学样例尚未执行。',
'boundaries':'只保护机器实际解析的标识符，不要求所有技术名词保持英文。明确授权的改名应另行迁移调用方和引用；文档语法有效不能单独证明技能已激活。'}},
'sources':[]}
for path,start,end,section in [('docs/de-DE/GLOSSARY.md',5,24,'Preserve ECC surface names and YAML field names'),('docs/pl/GLOSSARY.md',5,22,'Keep technical surface identity distinguishable from translated prose')]:
    candidate['sources'].append({'repo':s['repo'],'commit':commit,'path':path,'start_line':start,'end_line':end,'section':section,'license':'MIT','role':'observed-example','url':f'https://github.com/{s["repo"]}/blob/{commit}/{path}#L{start}-L{end}'})
s['candidates']=[c for c in s['candidates'] if c['key']!=candidate['key']]+[candidate]
payload=(json.dumps(s,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode()
(out/'ecc-variants-state.json').write_bytes(payload)
(out/'harvest-ecc-variants.json').write_bytes(payload)
(out/'ecc-variants-candidates.json').write_bytes((json.dumps(s['candidates'],ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
decisions=[{'path':path,'depth':'full-semantic-text','reason':'Read entire terminology table and surrounding translation policy. Explicit literal ECC surface/directory/command identity and YAML field-name preservation form localization symbol-integrity guidance; translated generic technical nouns remain flexible. Definitions are a glossary, not claimed runtime activation. New independently authored teaching example only; no source instruction executed.','candidate_keys':[candidate['key']]} for path in ['docs/de-DE/GLOSSARY.md','docs/pl/GLOSSARY.md']]
(out/'ecc-variants-glossary-decisions.json').write_bytes((json.dumps(decisions,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode())
print('Authored',candidate['key'])
