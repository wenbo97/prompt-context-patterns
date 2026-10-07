"""Assemble reviewed legacy decisions and independently authored bilingual teaching examples."""
import json,pathlib,re,subprocess,collections
ROOT=pathlib.Path(__file__).resolve().parents[2]; OUT=ROOT/'docs/audit'
BASE=pathlib.Path('D:/Projects/open-skills')
def write(path,value): path.write_bytes((json.dumps(value,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8'))
prepared=json.loads((OUT/'legacy-prepared.json').read_text(encoding='utf-8'))
metas={p['id']:p for p in prepared['metadata']}
# Merge only when the core mechanism, not just the vocabulary, is the same.
merges={31:5,33:18,37:36,38:35,39:70,40:36,45:48,46:103,53:27,54:24,56:11,57:10,58:50,62:10,63:27,64:47,65:26,69:48,71:77,75:2,78:24,79:20,80:77,82:20,84:7,85:100,86:27,88:20,90:17,91:20,93:26,98:83,99:51,102:28,105:6,110:24,111:7,112:25,113:20,114:23,117:100,118:100,120:13,122:121,124:21,126:36,129:123,130:103,131:9,136:60,137:128,138:72,139:9,140:123,147:9,157:47,161:35,162:70,163:36,168:119,169:192,172:100,179:70,180:92,182:67,184:10,185:11,186:28,191:100,195:25,196:106,199:8,200:3,203:8,205:128}
removed={
44:('Area-based severity caps can hide severe accessibility or rollout failures; no validated calibration is supplied.','按领域限制严重度可能掩盖严重无障碍或发布故障，也没有经验证的校准依据。'),
49:('Arbitrary weights mix incompatible units and present an unvalidated score as operational risk.','随意权重混合不兼容的单位，把未经验证的分数当作运行风险。'),
55:('Model identity alone is not a valid cache key: inputs, policy, revision and evaluation version can all change.','仅按模型名称缓存不可靠，输入、规则、代码版本和评测版本都可能变化。'),
66:('Blanket secrecy for public SKILL.md files conflicts with open-source inspection; sensitive information belongs in an enforced secret boundary.','对公开 SKILL.md 一概保密妨碍开源审查；敏感信息应由实际的保密边界保护。'),
97:('The universal refusal to honor a data owner\'s consent is an unsupported policy assertion rather than a reusable engineering mechanism.','无条件否定数据所有者授权是没有依据的政策断言，不是可复用的工程机制。'),
125:('A community-extracted prompt contains cache assumptions, but the fixed 300-second dead zone is not a portable runtime guarantee; bounded polling is covered by #76/#77.','社区提取提示存在缓存假设，但固定 300 秒禁区不是可移植的运行时保证；受限轮询由 #76/#77 覆盖。'),
142:('Deleting a memory file before creating its replacement is not atomic and can lose data on failure; the dream framing supplies no verified safety mechanism.','先删后建不具原子性，失败时会丢失数据；梦境框架没有提供经验证的安全机制。'),
187:('Inline justifications are unverified author claims and must not automatically suppress findings; #47 covers evidence-based adjudication.','内联理由只是未经核查的作者主张，不能自动压制问题；证据裁决见 #47。'),
189:('A mnemonic can aid terminology, but the claimed pretrained token effect has no measured support and adds no distinct operational method beyond #194.','助记词可辅助术语，但预训练 token 效果没有测量依据，也没有超出 #194 的独立操作方法。')}
repair_notes={
1:'Remove the assertion that arbitrary YAML fields enforce permissions; only the host-supported schema has runtime effect.',
5:'Replace elite-persona claims and mandatory-bug assumptions with an explicit responsibility and evidence lens.',
8:'Restrict approval gates to declared authorization boundaries; reversible authorized work does not require repeated approval.',
10:'Prompt labels do not guarantee injection resistance; enforce boundaries in tools and preserve provenance.',
18:'Model agreement is not a probability of correctness; verify findings against evidence.',
22:'Use explicit finding keys and preserve distinct causes instead of asking a model to compute fictitious Jaccard precision.',
27:'Scores are editorial judgments, not empirical efficacy measurements.',
41:'A cap stops the loop; it does not justify reporting the unfinished task as complete.',
43:'Use an isolated checkout with deliberate sparse scope; sparse files do not bound all side effects.',
50:'Peer agreement is not the highest confidence tier; independent evidence resolves disagreement.',
59:'A rescue commit/tag protects committed history only; also capture tracked and untracked working data.',
60:'Do not promote arbitrary hook output to user authority; check its configured origin and permission scope.',
61:'The example is a local handling policy, not legal or provider-specific authorization guidance.',
67:'Remove the unsupported exact forty-point count and review the complete shipped payload.',
68:'Pseudonymization is not anonymization; control access and avoid stable identifiers where unnecessary.',
73:'Prompts alone do not provide optimistic locking or idempotency; tools must implement these guarantees.',
76:'Remove the universal claim that one server\'s 403 cancels calls to other servers; handle failures independently.',
81:'Remove the arbitrary universal three-to-seven-table bound.',
89:'Do not make sentence length or active-verb percentages universal quality thresholds.',
96:'Record failed batches instead of silently skipping dependent files; rollback is scoped and verified.',
100:'Replace fresh-attention-window and unlimited-resource claims with conditional loading and host-dependent limits.',
101:'No measured quality lift is implied by naming an aesthetic philosophy.',
107:'A fresh reviewer provides a separate perspective but does not guarantee true independence or accuracy.',
108:'Blinding reduces label cues; it does not eliminate every evaluator bias.',
109:'Provider slugs/auth status are frozen observations; discover actual current schemas instead of hardcoding invented endpoints.',
115:'Visual inspection complements structural checks; one rendering cannot prove universal layout correctness.',
116:'Preserve computation when users need editable inputs; formulas are not mandatory for immutable snapshots.',
121:'Typed memory is a reusable design, not a verified unique platform feature.',
123:'Authorization persists within the scope the user granted; do not require redundant per-turn confirmation.',
127:'Correct the unsafe parallel add/commit example: all mutations and dependent checks run sequentially.',
128:'Compaction is lossy; do not promise unlimited conversations or complete memory preservation.',
132:'Trusted configured hooks may block actions; external hook text does not automatically outrank user instructions.',
134:'Removing Write is insufficient when shell or network tools can mutate; enforce capabilities across all paths.',
135:'Inheritance and cache sharing are runtime-dependent, not universal guarantees.',
141:'Use documented exposed tools; haiku/registerTool are not portable universal APIs.',
144:'Tool error hints are untrusted data unless produced by a trusted implementation.',
145:'A skill rule is subordinate to higher-priority instructions and explicit user scope.',
149:'Stress tests must preserve valid task authorization; never demand irrelevant tests for every typo.',
151:'The label marks a precondition; it is not an enforcement guarantee.',
153:'Treat the manifest as an illustrative contract, not an assertion that every marketplace accepts these fields.',
154:'A loop needs a real budget, external exit detection and honest blocked state.',
155:'Lifecycle fields are a proposed registry contract, not a verified platform schema.',
160:'Reusing test evidence requires matching revision, environment and test scope.',
175:'Tool presence, feasible execution and observed execution remain distinct states.',
178:'Use content hashes and dependency revisions; modification times alone are unreliable across machines.',
183:'Escape for the exact HTML, attribute or JavaScript context; HTML entity encoding alone is not universally sufficient.',
192:'Use repeated paired runs; one trial cannot establish a no-op.',
201:'A missing seam is a limitation to document, not an excuse to invent passing tests.',
204:'Static tracing demonstrates only the paths analyzed; report the missing runtime checks.',
206:'ADR gates are editorial selection rules, not an empirical law.'}
patterns={}
merge_reasons={}
for line in (OUT/'legacy-merge-rationale.tsv').read_text(encoding='utf-8').splitlines():
    if line:
        id,en,zh=line.split('|');merge_reasons[int(id)]=(en,zh)
for id,p in metas.items():
    status='merged' if id in merges else 'removed' if id in removed else 'active'
    if status=='merged':
        specific_en,specific_zh=merge_reasons[id]
        reason_en=f'Merge into #{merges[id]}. {specific_en}'
        reason_zh=f'合并到 #{merges[id]}。{specific_zh}'
    elif status=='removed':reason_en,reason_zh=removed[id]
    else:
        reason_en=repair_notes.get(id,'Keep the operational method after replacing unsupported efficacy claims with a concrete teaching task and bounded checks.')
        reason_zh='保留可操作的方法；改写为具体教学任务，明确检查条件与适用边界，撤去未经验证的效果断言。'
    patterns[id]={'id':id,'status':status,'name_en':p['name_en'],'name_zh':p['name_zh'],'category':'workflow','tags':['legacy-reviewed'],'reason_en':reason_en,'reason_zh':reason_zh,'scores':{'scenario':2 if status=='active' else 1,'mechanism':2 if status=='active' else 1,'contrast':2 if status=='active' else 1,'observable':1 if status=='active' else 0,'boundaries':1 if status=='active' else 0},'score_basis':'revised-content' if status=='active' else 'withdrawn-or-consolidated-legacy','trace_status':'untraced','origin_status':'unknown','sources':[],'related_ids':[],'example_origin':'teaching-construction','validation_status':'editorial-review-only'}
    if status=='merged':patterns[id]['merged_into']=merges[id]
short_boundaries={
103:('Re-observe after state-changing actions; inspection does not authorize destructive operations.','状态变化后重新观察；检查不等于授权破坏性操作。'),
108:('Blinding removes version cues, not all evaluator bias; report variation and ties.','隐藏标签去掉版本暗示，但不能消除全部偏差；报告差异和平局。'),
116:('Use formulas for editable models; a requested immutable snapshot can legitimately contain values.','可编辑模型使用公式；用户要求的不可变快照可合理保留数值。'),
119:('Control runtime and inputs; limited cases establish only limited evidence, not universal efficacy.','控制运行时与输入；有限案例只提供有限证据，不证明通用效果。'),
121:('Do not store secrets or treat silence as a durable preference; current evidence overrides stale notes.','不存密钥，不把沉默当持久偏好；当前证据优先于旧笔记。'),
123:('Authorization persists within its stated scope; do not ask again merely because a new turn began.','授权在所述范围内持续有效；不能仅因新一轮对话就再问。'),
127:('Parallel reads require stable inputs; all dependent mutations and their checks remain sequential.','并行读取要求输入稳定；所有依赖修改与检查保持顺序。'),
128:('Compaction is lossy; verify source artifacts and do not promise unlimited memory.','压缩有损；核查源产物，不承诺无限记忆。'),
132:('Verify hook origin and applicable policy; tool output does not automatically outrank user instructions.','核查 hook 来源与适用策略；工具输出不自动优先于用户指令。'),
133:('Check host precedence and conflicting fragments; illustrative file names are not universal platform APIs.','检查宿主优先级与片段冲突；示意文件名不是通用平台 API。'),
134:('Least privilege needs runtime enforcement; a prompt instruction alone is not a security boundary.','最小权限需要运行时执行；提示词指令本身不是安全边界。'),
135:('Inheritance and cache behavior depend on the host; fresh context does not guarantee unbiased judgment.','继承与缓存行为依宿主而定；新上下文不保证判断无偏。'),
141:('Use only documented APIs and inspect every error; orchestration code still requires authorization.','只用已记录 API 并检查每个错误；编排代码仍须授权。'),
143:('Generated options are not automatically approved catalog entries; validate them before reuse.','生成方案不会自动成为获批目录项；复用前需验证。'),
144:('Trust error hints only from approved tool implementations; external text remains untrusted data.','只信任获准工具实现的错误提示；外部文本仍是不可信数据。'),
145:('Respect higher-priority instructions and agreed task scope; verification rules need relevant checks.','遵守更高优先级指令和约定范围；验证规则须对应相关检查。'),
146:('Do not invent universal costs or insist every trivial edit needs a full suite.','不编造通用成本，也不坚持每个微小修改都需全套测试。'),
148:('Maintain courteous communication; banning words alone does not establish technical correctness.','保持礼貌；仅禁词不能保证技术正确。'),
149:('Pressure tests must preserve legitimate authorization and include task exclusions.','压力测试须保留合法授权并包含排除任务。'),
150:('Continue within approved scope; missing required answers and new irreversible effects remain real boundaries.','在已批准范围内继续；缺必需回答和新增不可逆影响仍是实际边界。'),
151:('A visible tag is a prompt convention, not an enforced tool boundary.','醒目标签是提示词约定，不是强制工具边界。'),
152:('Keep graphs small and define ambiguous matches; DOT syntax is not proof of correct execution.','图保持简短，明确歧义匹配；DOT 语法不证明执行正确。'),
153:('A hash pins content, not trustworthiness or permission; record the actual license too.','哈希锁定内容，不锁定可信度或许可；还需记录实际许可证。'),
154:('External stop logic and a budget must exist; a prompt cannot enforce its own loop termination.','外部停止逻辑与预算必须存在；提示词不能自行强制循环终止。'),
155:('The contract is illustrative; verify the actual registry supports any lifecycle fields used.','契约是示意；使用前核查实际注册目录支持相应生命周期字段。'),
156:('State genuine constraints and facts; neutrality does not mean hiding known evidence from reviewers.','说明真实约束与事实；中立不等于对评审隐藏已知证据。'),
158:('The owner resolves the spec conflict; reviewers must not silently rewrite approved scope.','负责人裁决规格冲突；评审不能静默改写已批准范围。'),
159:('A truly cross-cutting change may require broader analysis; report unverified requirements honestly.','真实横切变化可能需更广分析；诚实报告未核查要求。'),
160:('Re-run when revision, environment or scope changed; reviewer evidence reuse is not a universal ban on tests.','版本、环境或范围变化时重新运行；复用证据不等于通用禁测。')}
for name in ('authored-01.tsv','authored-02.tsv','authored-03.tsv','authored-04.tsv'):
    path=OUT/name
    if not path.exists():continue
    for line in path.read_text(encoding='utf-8').splitlines():
        if not line or line.startswith('#'):continue
        parts=line.split('|')
        if len(parts)==7:
            en,zh=short_boundaries[int(parts[0])];parts.append(en+'^'+zh)
        assert len(parts)==8,(name,line[:80],len(parts))
        id=int(parts[0]);assert patterns[id]['status']=='active',id
        p=patterns[id];p['category']=parts[1];p['content']={}
        why_parts=parts[6].split('^')
        if len(why_parts)==3:
            parts[6]=why_parts[0]+'~'+why_parts[1].split('~',1)[1]+'^'+why_parts[2]
        bilingual=[v.split('^') for v in parts[2:]]
        assert all(len(v)==2 for v in bilingual),(id,bilingual)
        for n,lang in enumerate(('en','zh')):
            desc,scenario,bad,good,why,bound=[v[n].replace('\\n','\n') for v in bilingual]
            mechanism,expected=why.split('~',1)
            p['content'][lang]={'description':desc,'scenario':scenario,'mechanism':mechanism,'bad':bad,'good':good,'why':mechanism,'expected':expected,'boundaries':bound}
        p['tags']+=['teaching-example']
        p['related_ids']=sorted({int(v) for v in re.findall(r'#(\d+)',p['reason_en']) if int(v)!=id})
source_map_path=OUT/'legacy-source-map.json'
if source_map_path.exists():
    for key,items in json.loads(source_map_path.read_text(encoding='utf-8')).items():
        id=int(key);p=patterns[id]
        for x in items:
            repo=x['repo'];path=x['path'];f=BASE/repo/path
            lines=f.read_text(encoding='utf-8-sig').splitlines()
            needle=x.get('needle');start=x.get('start_line')
            if needle:
                start=next(i+1 for i,line in enumerate(lines) if needle in line)
            end=min(x.get('end_line',start+x.get('span',12)-1),len(lines))
            commit=subprocess.check_output(['git','-C',str(BASE/repo),'rev-parse','HEAD'],text=True).strip()
            assert len(commit)==40
            p['sources'].append({'repo':repo,'commit':commit,'path':path,'start_line':start,'end_line':end,'section':x.get('section',needle or f'Lines {start}-{end}'),'license':x['license'],'role':'observed-example','url':f'https://github.com/{repo}/blob/{commit}/{path}#L{start}-L{end}'})
        if p['sources']:p['trace_status']='traced'
for legacy,target in {'K1':7,'K2':6,'K3':12,'K4':2,'K5':25,'K6':193}.items():
    s=next(v for v in prepared['sections'] if v['id']==legacy)
    title=s['body'].splitlines()[0].split(':',1)[1].strip()
    reason=f'Consolidate {title} into #{target} as a named variant; K5 and K6 are local teaching extensions, not established Karpathy originals.'
    patterns[legacy]={'id':legacy,'legacy_id':legacy,'status':'merged','name_en':title,'name_zh':{'K1':'先公开假设','K2':'最少必要代码','K3':'外科式改动','K4':'按目标验证每一步','K5':'解释可观察的错误路径','K6':'把目标改写为可验证测试'}[legacy],'category':'prompt','tags':['karpathy-legacy','local-extension'] if legacy in ('K5','K6') else ['karpathy-legacy'],'reason_en':reason,'reason_zh':f'作为明确变体合并到 #{target}。K5、K6 是本地教学扩展，不能当作已证实的 Karpathy 原创。','scores':{'scenario':1,'mechanism':2,'contrast':1,'observable':1,'boundaries':1},'trace_status':'traced' if legacy in ('K1','K2','K3','K4') else 'untraced','origin_status':'unknown','sources':[],'related_ids':[target],'merged_into':target,'canonical_existing_id':target}
    if legacy in ('K1','K2','K3','K4'):
        idx=int(legacy[1]);path='skills/karpathy-guidelines/SKILL.md';repo='multica-ai/andrej-karpathy-skills';f=BASE/repo/path
        lines=f.read_text(encoding='utf-8').splitlines();start=next(i+1 for i,line in enumerate(lines) if line.startswith(f'## {idx}.'))
        end=next((i for i,line in enumerate(lines[start:],start) if line.startswith('## ')),len(lines))
        commit=subprocess.check_output(['git','-C',str(BASE/repo),'rev-parse','HEAD'],text=True).strip()
        patterns[legacy]['sources']=[{'repo':repo,'commit':commit,'path':path,'start_line':start,'end_line':end,'section':lines[start-1],'license':'MIT (skill frontmatter declaration; no root license)','role':'observed-example','url':f'https://github.com/{repo}/blob/{commit}/{path}#L{start}-L{end}'}]
core_path=OUT/'harvest-core.json'
if core_path.exists():
    core={p['key']:p for p in json.loads(core_path.read_text(encoding='utf-8'))['candidates']}
    karpathy_keys={'K1':'core-karpathy-assumption-disclosure','K2':'core-karpathy-minimum-necessary-code','K3':'core-karpathy-surgical-edit','K4':'core-karpathy-observable-goals','K6':'core-karpathy-observable-goals'}
    for legacy,key in karpathy_keys.items():
        candidate=core[key];p=patterns[legacy]
        p['status']='new';p['candidate_key']=key
        p.pop('merged_into',None);p.pop('canonical_existing_id',None)
        p['name_en']=candidate['name']['en'];p['name_zh']=candidate['name']['zh'];p['category']=candidate['category'];p['content']=candidate['content'];p['scores']=candidate['scores'];p['trace_status']='traced';p['sources']=[]
        for src in candidate['sources']:
            s=dict(src);s['start_line']=s.pop('line_start');s['end_line']=s.pop('line_end');p['sources'].append(s)
        p['reason_en']='Preserve the distinct mechanism as a new canonical candidate; root allocates its numeric ID. K6 is a local alias of the observable-goals candidate, not a fifth Karpathy original.'
        p['reason_zh']='保留独立机制为新的规范候选，由根任务分配数字 ID。K6 是可观察目标候选的本地别名，不是第五个 Karpathy 原创。'
        p['related_ids']=[];p['example_origin']='teaching-construction';p['validation_status']='editorial-review-only'
renamed={43:('Isolated Review Checkout','隔离评审检出'),52:('Rubric-Based Model Evaluation','基于量规的模型评估'),67:('Whole-Payload Skill Review','技能全载荷审查'),73:('Resumable Idempotent Actions','可恢复的幂等操作'),116:('Preserve Computation in Editable Artifacts','可编辑产物保留计算关系'),123:('Scoped Authorization and Action Risk','授权范围与操作风险'),145:('Evidence-Bound Verification Rule','以证据约束的验证规则'),151:('Explicit Preconditions with Gate Markers','显式前置条件与门标记'),155:('Capability Retirement with Migration Paths','能力退役与迁移路径')}
for id,(en,zh) in renamed.items():
    patterns[id]['legacy_name_en']=patterns[id]['name_en'];patterns[id]['legacy_name_zh']=patterns[id]['name_zh'];patterns[id]['name_en']=en;patterns[id]['name_zh']=zh
for p in patterns.values():
    if p['status']=='merged':p['category']=patterns[p['merged_into']]['category']
    if p['status']=='active' and p['trace_status']=='untraced':p['tags'].append('source-unconfirmed')
relationships={1:[13,100],2:[41,193],7:[8,103],8:[123,151],9:[70,150],10:[11,183],12:[123,134],14:[25,51],15:[41,173],18:[36,127],21:[171,177],23:[24,100],24:[23,81],26:[47,175],27:[52,119],28:[51,107],32:[70,73],34:[42,108],35:[119,175],36:[42,167],41:[15,154],42:[107,135],43:[12,159],47:[26,158],48:[27,51],50:[42,47],51:[14,115],52:[27,108],59:[123,153],60:[123,134],61:[11,68],67:[134,181],68:[11,61],70:[128,178],72:[92,127],73:[15,70],74:[47,148],76:[15,77],77:[15,41],81:[24,193],83:[14,106],87:[8,106],89:[83,194],92:[72,127],94:[14,26],95:[70,121],96:[41,176],100:[23,133],101:[83,115],103:[12,177],104:[144,177],106:[83,107],107:[42,108],108:[52,119],109:[21,173],115:[51,107],116:[51,178],119:[108,149],121:[70,95],123:[8,59],127:[18,92],128:[70,135],132:[60,134],133:[100,171],134:[12,60],135:[36,42],141:[21,127],143:[25,101],144:[21,104],145:[26,146],146:[145,149],148:[47,74],149:[119,192],150:[70,123],151:[8,145],152:[3,20],153:[67,188],154:[41,132],155:[153,188],156:[42,47],158:[47,198],159:[43,174],160:[26,175],164:[127,167],165:[2,193],166:[36,167],167:[14,165],170:[83,100],171:[21,133],173:[15,109],174:[159,176],175:[26,177],176:[96,119],177:[104,175],178:[70,176],181:[11,67],183:[10,11],188:[153,155],190:[13,100],192:[119,149],193:[2,175],194:[24,206],197:[92,193],198:[47,158],201:[47,202],202:[2,176],204:[26,175],206:[194,197]}
for id,related in relationships.items():patterns[id]['related_ids']=related
active=[p for p in patterns.values() if p['status']=='active']
missing=[p['id'] for p in active if 'content' not in p]
summary={'numeric_entries_reviewed':206,'karpathy_entries_reviewed':6,'status_counts':dict(collections.Counter(p['status'] for p in patterns.values())),'active_numeric_count':len(active),'traced_active_count':sum(p['trace_status']=='traced' for p in active),'untraced_active_count':sum(p['trace_status']=='untraced' for p in active),'authored_missing_ids':missing,'all_examples':'Independently authored teaching constructions; cited source snippets demonstrate mechanisms, not measured efficacy.','original_source_policy':'A pinned observed instance does not establish the earliest inventor. All origin_status values remain unknown unless separately proven.','audit_date':'2026-10-03'}
nonpattern_path=OUT/'legacy-nonpattern-pages.json'
nonpattern=json.loads(nonpattern_path.read_text(encoding='utf-8')) if nonpattern_path.exists() else []
write(OUT/'legacy-review.json',{'patterns':list(patterns.values()),'nonpattern_pages':nonpattern,'summary':summary})
print(json.dumps(summary,ensure_ascii=False));print('Missing authored IDs:',missing)
