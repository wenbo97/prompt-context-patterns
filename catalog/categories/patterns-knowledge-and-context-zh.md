# 类别 6：知识与上下文

信息管理方式 — 参考文件、领域知识、示例和证据要求。

**相关基础技术：** Grounding/Anchoring, Few-Shot with Embedded Reasoning, Attention Locality（见 [prompt-engineering-for-skills.md](/prompt-context-patterns/catalog/techniques/token-level-techniques)）

---

## Pattern 23: Reference File / Knowledge Base Injection

**出现频率：** ~17% 的技能（390 文件）
**相关模式：** [Domain Knowledge Embedding](#pattern-24), [Few-Shot Examples](#pattern-25), [Tool Routing Tables](#pattern-21)

**定义：** 指向外部参考文件（JSON、markdown、KQL 模板、查找表），这些文件包含技能在运行时需要的领域知识。技能指示 agent 在继续之前读取特定文件，而非将所有知识内联嵌入。

**适用场景：**
- 领域知识量大到适合作为独立文件维护时
- 知识跨多个技能共享（DRY）时
- 知识更新独立于技能逻辑时
- 查找表会让技能文件过于臃肿时

### 正面示例
```markdown
## Routing Tables

All team routing data is in **`references/team-routing-tables.md`**. Read that file before
attempting any match. It contains three lookup tables:

- **Table 1 — Team Descriptions**: Match team names or problem descriptions against the
  incident management path and Description columns.
- **Table 2 — InternalService to Incident Team**: Match InternalService service or application names
  to their owning incident team.
- **Table 3 — Process to Incident Team**: Match crashing process names to their owning incident team.

## Steps

### Step 1 — Match input to incident management path

Read `references/team-routing-tables.md` and apply the appropriate lookup:

1. If the user provides a **team name** → match directly against Table 1 incident management path column
2. If the user describes a **problem** → match keywords against Table 1 Description column
3. If the user names an **InternalService service** → look up in Table 2
4. If the user names a **crashing process** → look up in Table 3

If the input is ambiguous, present the top candidate matches and ask the user to confirm.
```
```markdown
## Reference Files

All in `references/` relative to this skill:

| Reference | Contents |
|-----------|----------|
| `mas-standards.json` | 16 MAS standards — _DID, _DetectionPatterns, _FixPrinciples, _CommonPatterns |
| `01-perceivable.md` | Code examples for alt text, semantic HTML, contrast, color |
| `02-operable.md` | Code examples for keyboard, focus, tab order, target size |
| `03-understandable.md` | Code examples for labels, errors, language, predictability |
| `04-robust.md` | Code examples for ARIA, roles, states, live regions |
```

**为何有效：** 文件路径精确 — 模型无需搜索。内容摘要告知模型每个文件包含什么，以便决定读取哪个。Step 1 中的路由逻辑将输入类型映射到特定表，防止模型对每次查询扫描所有表。无障碍示例使用参考索引模式：一个 JSON 文件用于结构化数据，独立的 markdown 文件用于代码示例，按 WCAG 类别组织。

### 反面示例

```markdown
Look up the correct team routing information. There should be some reference
data available somewhere in the project. Check if there are any tables you can use.
```

**为何失败：** "Somewhere in the project" 强制模型搜索目录树。"Some reference data" 没有标识文件或格式。"Check if there are tables" 让知识库变成可选 — 模型可能跳过它。没有从输入类型到表的映射意味着模型在所有数据上使用暴力匹配。每次运行可能读取不同文件或完全跳过查找。

---

## Pattern 24: Domain Knowledge Embedding

**出现频率：** ~22% 的技能（500+ 文件）
**相关模式：** [Reference File Injection](#pattern-23), [Few-Shot Examples](#pattern-25), [Scoring Rubrics](#pattern-27)

**定义：** 将详细的领域特定知识直接嵌入提示词 — schema 定义、API 字段映射、查询语法、分类规则或命令参考。与 Pattern 23 不同，知识是内联的而非外部文件。

**适用场景：**
- 知识足够紧凑可以嵌入（低于 ~100 行）时
- 知识与技能逻辑紧密耦合（不可复用）时
- 模型需要知识在其即时注意力窗口中时
- 外部文件读取会为小量参考数据增加延迟时

### 正面示例
```markdown
## Key Schema Fields

| Field | Description |
|-------|-------------|
| `DeploymentConfigurationItemType` | Type of override — determines its effect |
| `StartVersion` | Build version the override starts applying from |
| `EndVersion` | Build version the override stops applying (inclusive) |
| `TargetFilterExpression` | Scope: which machines/rings/roles it applies to |
| `IsDeleted` | `false` = currently active |
| `WhenCreated` | When the override was created |
| `CreatedBy` | Who created it |
| `Reason` | Why it was created |

## Blocking Override Types

These types are checked by the deployment gate system `DeploymentBlockRule`:

| DeploymentConfigurationItemType value | Effect |
|---------------------------------------|--------|
| `BlockAll` | Blocks all deployment to matching machines |
| `BlockProvisionedMachines` | Blocks deployment to provisioned machines |
| `Halt` | Halts deployment of specific version range |
| `HaltAndStop` | Halts and stops any in-progress deployment |
| `Purge` | Rolls back to previous version |
| `PurgePreferSxSRollback` | Rolls back using side-by-side method |

## Common Filters

| Filter | KQL |
|--------|-----|
| Active only | `where IsDeleted == false` |
| Blocking types only | `where DeploymentConfigurationItemType in ("BlockAll",...)` |
| By start version | `where StartVersion == "1.2.3456.007"` |
| By ring | `where TargetFilterExpression has "global"` |
```

**为何有效：** Schema 字段带类型和描述文档化 — 模型能构造有效查询。阻断覆盖类型穷举列出带效果说明 — 无需猜测哪些类型是 "blocking"。常用过滤器提供现成 KQL 片段供模型组合。知识结构化为表格，模型可高效扫描。每个字段名是数据源中使用的精确字符串 — 无需映射。

### 反面示例

```markdown
Query the deployment overrides table in Kusto to find blocking overrides.
The table has various fields for tracking deployments.
Use appropriate filters to find what you need.
```

**为何失败：** 没有字段名 — 模型发明看似合理但错误的列名。没有枚举阻断类型 — 模型可能过滤 `Type == "Block"` 而非实际值。没有查询模式 — 每次运行生成不同 KQL 语法。"Appropriate filters" 将整个查询设计委托给不了解 schema 的模型。

---

## Pattern 25: Few-Shot Examples

**出现频率：** ~21% 的技能（482 文件）
**相关模式：** [Structured Output Templates](#pattern-14), [Scoring Rubrics](#pattern-27), [Domain Knowledge Embedding](#pattern-24)

**定义：** 在技能中包含完整的输入/输出示例来演示预期行为。最佳示例同时包含正常路径和失败路径，完整输出展示精确格式。

**适用场景：**
- 输出格式复杂时（多章节报告、评分卡、JSON）
- 展示"好的样子"比描述更有效时
- 技能有非显而易见的行为需要通过示例演示时
- 需要展示代码前后对比变换时

### 正面示例
```markdown
### Input

Review this pitch for "CodePilot" (3 minutes):

Slide 1: "CodePilot — AI Pair Programming"
Slide 2: "Problem: Code reviews take 2-3 days on average"
Slide 3: Demo — shows GPT-4 suggesting refactors in VS Code
Slide 4: "Architecture: VS Code extension → GPT-4 API → GitHub PR comments"
Slide 5: "Thank you!"

### Output

# Pitch Review — CodePilot

**Format:** 5 slides, ~3 minutes | **Overall:** 16/25 (Adequate)

## Scorecard

| Criterion | Score | Feedback |
|-----------|-------|----------|
| Hook | 2/5 | Title slide alone is not a hook. Start with a pain point: "Your PR has been waiting 3 days. Sound familiar?" |
| Problem / Solution | 4/5 | Problem is clear and quantified. Add one metric: "reduces review time by 60%." |
| Demo Flow | 4/5 | Live demo is strong. Add a before/after comparison to make impact visible. |
| Technical Clarity | 4/5 | Architecture diagram is clear. Mention latency and cost for credibility. |
| Call to Action | 2/5 | "Thank you" is not a CTA. End with: "Try it today — install from marketplace." |
```
```markdown
Output for each fix:

### MAS XX.XX.XX — Criterion Name

**File:** `path/to/file.ext` (line N)
**Standard:** [_Requirement text]

**Before:**
[offending code]

**After:**
[fixed code]

**Fix applied:** [from _FixPrinciples — issue type + principle]
```

**为何有效：** Pitch 评审示例展示完整的输入/输出对 — 模型看到从 5 张幻灯片输入到评分输出的精确变换。分数具体（2/5、4/5）带可操作反馈而非笼统赞扬。无障碍示例展示了 before/after 代码模板，教模型每个修复的预期结构。两个示例足够具体可模仿，又足够通用可适配。

### 反面示例

```markdown
Here's an example: if someone gives you a pitch about a coding tool,
review it and give it a score. Make sure to provide helpful feedback.
```

**为何失败：** 没有实际输出展示 — 模型看不到输出 token 序列。"Give it a score" 没有展示评分表格式。"Helpful feedback" 可以是段落、列表或单句。模型没有可模仿的模板，每次运行产生不同结构。没看到评分示例，模型不知道预期分数分布（16/25 常见吗？）。

---

## Pattern 26: Evidence Chain / Proof-of-Work

**出现频率：** ~5% 的技能（100-150 文件）
**相关模式：** [Persona/Role Assignment](#pattern-5), [Negative Constraints](#pattern-6), [Self-Critique](#pattern-28)

**定义：** 要求 agent 展示推理过程 — 引用来源、为结论提供证据、维护审计轨迹。防止模型在未实际调查的情况下生成貌似合理的结论。

**适用场景：**
- 根因分析中结论必须可追溯时
- 任何产出他人将据以行动的建议的技能
- 事件响应中调查记录对事后复盘重要时
- 分析数据的技能中模型可能虚构发现时

### 正面示例
```markdown
| **R3 — Evidence chain** | All phases | Every root cause must cite:
`[Conclusion] <- [Query/Log evidence] <- [Code path]`. Missing link → investigate first |
```
```markdown
## PROOF OF WORK — Mandatory Checkpoint Before Any Hypothesis

After completing Phase 1, you MUST output a **Download & Analysis Manifest** listing:

1. **Every attachment URL** from the bug's relations array — with download status
   (SUCCESS / FAILED + reason)
2. **Every file extracted** from archives — with file type and size
3. **Every CDB command run** on every `.dmp` / `.mdmp` file — with the output file path
4. **Every ETL converted** — with the output file path
5. **Key findings per file** — 1-2 lines summarizing what each file revealed

**If the manifest shows ZERO dumps analyzed and the bug has dump attachments → your
investigation is INVALID. Go back to Phase 1.**

**If you formed a hypothesis before completing this manifest → STOP. Delete the hypothesis.
Complete Phase 1 first.**
```

**为何有效：** R3 定义了证据链的精确格式：`Conclusion ← Evidence ← Code path`。每个环节必须存在 — "missing link" 触发调查而非假设。Manifest 更强：模型必须在形成任何假设之前证明它分析了每个附件。"Delete the hypothesis" 指令防止确认偏差 — 如果模型已有想法，可能选择性寻找确认证据。

### 反面示例

```markdown
Make sure your analysis is thorough and well-supported. Include evidence for your
conclusions. Don't make assumptions.
```

**为何失败：** "Well-supported" 是主观的 — 模型可能引用一行日志就认为"有支撑"。没有必需的证据格式意味着有些运行产生有据可查的证据链，其他则产生无依据断言。"Don't make assumptions" 在没有强制检查点的情况下模型无法自我验证。模型可能真诚地认为自己有证据，实际上却在虚构。
