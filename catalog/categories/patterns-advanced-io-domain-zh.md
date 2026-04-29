# 高级输入/输出、领域与通信模式

数据转换、领域知识编码、可视化、交互式推理、文体转换和受众适配的深度模式 — 在 500+ 插件中发现的生产级架构，扩展了基础 I/O 模式（14-17）和知识模式（23-26）。

**来源研究：** 从 DevOps、安全、迁移和事件响应领域的 500+ 生产级 AI agent 插件分析中提取。

---

## Pattern 81: Natural Language to Relational Schema Decomposition

**出现频率：** <1% 的插件
**相关模式：** [Domain Knowledge Embedding](#pattern-24), [Phased Execution](#pattern-2)

**定义：** 一个强制性的中间推理步骤，迫使模型在任何代码生成之前将自然语言主题分解为正式的关系结构。五步流程（识别实体、分类、定义关系、确定生成顺序、约束复杂度）作为结构化推理支架。

### 正面示例

```markdown
Decompose ${input:subject} into a normalized relational model.
This is a mandatory first step before any code generation.

1. Identify Entities: List all distinct real-world objects or concepts
2. Classify Each Entity:
   - Lookup/Dimension tables: Relatively static reference data
   - Fact/Transaction tables: Event-driven records that reference lookups
3. Define Relationships: For every pair of related entities, specify:
   - Relationship type: one-to-one, one-to-many, or many-to-many
   - The foreign key column and which table it references
4. Determine Generation Order: Build a dependency graph so parent/lookup
   tables are generated before child/fact tables
5. Aim for 3-7 tables depending on domain complexity.

| Subject | Entities (Tables) | Key Relationships |
| Hospital patient records | Patients, Doctors, Departments, Visits, Diagnoses | Visits->Patients (FK) |
| E-commerce sales | Customers, Products, Categories, Orders, OrderItems | Orders->Customers (FK) |
```

**为什么有效：** 与 Pattern 24（嵌入静态 schema）不同，这里教模型*如何从*非结构化概念*推导* schema。实体分类（Lookup vs Fact）提供分类法。依赖图确保正确的生成顺序。3-7 表的约束防止过度分解和过度设计。

### 反面示例

```markdown
Generate a database schema for ${input:subject}.
Create all necessary tables with appropriate columns and relationships.
Make sure to include primary keys and foreign keys.
```

**为什么失败：** 没有分解流程意味着模型临时发明表，常出现过多（15+ 张表用于简单领域）或过少（单一平表）的情况。没有实体分类（Lookup vs Fact）就没有生成顺序，子表可能引用尚不存在的父表。缺少复杂度约束意味着没有停止添加表的信号。

---

## Pattern 82: Chart Decision Tree with Anti-Pattern Guards

**出现频率：** <1% 的插件
**相关模式：** [Tool Routing Tables](#pattern-21), [Negative Constraints](#pattern-6)

**定义：** 一个多分支决策树，将*数据形态*映射到*可视化类型*，带有基数守卫（cardinality guards）和内联反模式防护。

### 正面示例

```markdown
Category comparison → bar or horizontal_bar (Plotly)
Value over time → time_series (Plotly)
Distribution → histogram or box_plot (Plotly)
Part-to-whole (2-7 categories) → pie (Plotly)
Distribution across groups (20+ points/group) → violin (Plotly)
Change decomposition (3-20 factors) → waterfall (Plotly)

## Two-Variable Routing
Two numeric columns?
  +-- Meaningful third numeric (size)? 5-100 entities? → bubble_scatter
  +-- Population shape/density? Row count >500? → density_2d
  +-- Individual points with selection? → scatter_brush (D3)
  +-- Grouped by category?
        +-- >20 pts/group? → violin
        +-- <20 pts/group? → box_plot

## Anti-Patterns — Avoid:
1. Pie chart with more than 7 slices — becomes unreadable
2. 3D charts — distort perception of values
3. Dual y-axes — confuse readers about axis mapping
4. Truncated y-axis on bar charts — exaggerates differences
5. Too many series on one line chart — >7 lines become spaghetti
6. Rainbow color palettes — lack perceptual ordering, fail for colorblind
```

**为什么有效：** 三层结构：简单情况的平面查找、模糊情况的多分支决策树、以及短路错误决定的反模式。基数守卫（pie: 2-7 类别, violin: 20+ 点/组）防止选择渲染效果差的图表。

### 反面示例

```markdown
Choose the best chart type for the data.
Options: bar, line, pie, scatter, histogram, box plot, violin, waterfall.
Pick whichever seems most appropriate for the user's data.
```

**为什么失败：** 没有选择标准意味着模型无论数据形态都默认选择柱状图或折线图。没有基数守卫，它会毫无顾忌地生成 50 片的饼图或 3 个数据点的 violin plot。缺少反模式列表意味着无法阻止双 y 轴或 3D 图表。

---

## Pattern 83: Audience-Purpose-Driven Content Calibration

**出现频率：** 约 1% 的插件
**相关模式：** [Workflow Mode Branching](#pattern-3), [Structured Output Templates](#pattern-14)

**定义：** 将受众和目的作为一等输入，决定所有下游关于输出格式、详细程度和展示风格的决策。

### 正面示例

```markdown
### Step 1: Understand the Report

Ask about context before selecting charts:
- Audience — who reads this? (technical team, management, external stakeholders)
- Purpose — what kind? (investigation, monitoring, comparison, status update)
- Key questions — what should the reader learn?

These answers drive chart selection and level of detail:
- Audit trail needs → chart_table_query (shows visualization + raw query results)
- Summary KPI metrics → kpi_query (headline numbers with source query)
- Investigation findings → narrative (multi-paragraph explanatory text)
```

**为什么有效：** 受众/目的框架传播到每个下游决策。审计团队受众获得原始数据和可视化；管理层获得关键数字；调查人员获得叙述性解释。这是将语调/受众适配应用于数据可视化，而非仅限于文字。

### 反面示例

```markdown
### Step 1: Create the Report

Generate a report with appropriate charts and tables.
Include relevant KPIs and findings.
Use a professional tone suitable for business stakeholders.
```

**为什么失败：** 硬编码"business stakeholders"将所有受众区分折叠为一个。审计团队需要每张图表旁的原始查询结果；高管需要单一 KPI 标题。不询问目的（调查 vs 监控 vs 状态更新），模型会产出一个不服务于任何受众的通用仪表板。

---

## Pattern 84: Socratic Investigation Loop with Active Research

**出现频率：** <1% 的插件
**相关模式：** [Interactive Flow Control](#pattern-7), [Evidence Chain](#pattern-26)

**定义：** 模型在*主动工具研究*（读代码、搜索模式）和*苏格拉底式提问*之间交替，使用研究发现来提出越来越精确的问题。故意不直接给出解决方案，帮助用户自己发现洞察。

### 正面示例

```markdown
This is NOT classic rubber duck debugging where you sit silently.
You are a full research partner who:
- Actively investigates the codebase using tools (Grep, Read, Task agents)
- Asks informed questions based on what you discover
- Guides them to insights through interactive exploration

### Investigation Loop
1. Research Before Asking
   - Evaluate relevance: which leads are "hot trail" vs "cold trail"?
   - Follow hot trail (1-3 most relevant sources)
   - Acknowledge cold leads: "I also see X, Y, Z — should I explore those?"
2. Brief Analysis (1-3 sentences)
3. Ask a Thoughtful Question (2-4 specific options based on research)
4. Process the Answer

Session guard: After 8-10 questions without converging, check in:
"We've explored quite a bit — should we keep digging or move forward?"
```

**为什么有效：** 热/冷线索分诊防止在提出单个问题前进行穷举研究，保持对话节奏。模型故意不给答案 — 引导式发现比直接给答案产生更深的理解。收敛守卫防止无限探索。

### 反面示例

```markdown
Help the user debug their issue using the Socratic method.
Ask clarifying questions to understand the problem.
Guide them toward the solution without giving the answer directly.
Use available tools to read code when needed.
```

**为什么失败：** 没有调查循环结构意味着模型要么在不读代码的情况下提出浅层问题，要么在提问前读完整个代码库。没有热/冷线索分诊，每条线索获得同等关注。缺少收敛守卫（8-10 个问题检查点）让会话陷入无限提问而没有解决。

---

## Pattern 85: Knowledge Base Index with Intent-to-Source Routing

**出现频率：** 约 2% 的插件
**相关模式：** [Reference File Injection](#pattern-23), [Intent Classification](#pattern-20)

**定义：** 两层检索系统：每次调用时读取轻量级索引文件（低 token 成本），然后仅选择性深度读取匹配的知识库文件。每个数据源有消歧表处理重叠领域。

### 正面示例

```markdown
1. Read <knowledge base>/INDEX.md — lightweight index with keywords & descriptions
2. Match user's question against index entries' keywords/descriptions
3. Only then read matching knowledge base file(s) in full
4. If no match: fall back to Grep across all .md files

INDEX.md structure:
| File | Data Source | Keywords | Description |
| get-active-action-items.md | GetActiveActionItems() | SFI, action items, person | Individual SFI queries |
| s360-active-action-items.md | ComplianceDashboard ActiveActionItems | SFI, action items, overdue | Aggregate SFI tracking |

Per-source disambiguation (inside each KB file):
| Need | Use |
| Individual action items for a person | GetActiveActionItems() (this) |
| Aggregated counts by KPI/wave | SFIFactTable or ComplianceDashboardSFISnapshot |
| Org-leader-level rollups | ActiveActionItems (turbologsna) |
```

**为什么有效：** 两层检索最小化 token 成本 — 始终读索引，选择性读完整文件。每数据源消歧表处理最难的情况：多个来源关键词重叠但适用场景不同。

### 反面示例

```markdown
Read all knowledge base files at the start of every conversation.
Match the user's question against the full content of each file.
If multiple files match, combine their guidance into a single answer.
```

**为什么失败：** 每次调用读取所有 KB 文件在不相关内容上浪费 token。没有索引层，匹配完整文件内容慢且不精确。合并重叠来源的指导而没有消歧表，在两个来源覆盖同一关键词但用于不同场景时会产生矛盾建议。

---

## Pattern 86: Heuristic Scoring with Signal Detection

**出现频率：** <1% 的插件
**相关模式：** [Scoring Rubrics](#pattern-27)

**定义：** 评分标准中每个分值级别指定*机器可检测信号* — 字数、正则模式、结构标记 — 而非主观描述词。

### 正面示例

```markdown
### Problem Statement (1-5)
| Score | Heuristic Signals |
| 1 | No section matching "problem", "background", "overview", "context" |
| 2 | Section found but <30 words, no user focus |
| 3 | Has user focus (mentions user/customer/developer) OR >80 words |
| 4 | Has specific numbers OR research evidence, AND user focus |
| 5 | Has research evidence AND >=2 specific numbers AND user focus |

Research evidence patterns: "interviewed N", "surveyed N", "research shows",
"based on data/research/feedback", "support ticket", "NPS score"

Scoring philosophy:
- AI-generated boilerplate caps at 2-3; real substance required for 4-5
- Near-perfect (48-55) requires: user research, competitive analysis, metrics with baselines
```

**为什么有效：** 可测试条件（字数、模式匹配、AND/OR 逻辑）替代主观标签。"AI boilerplate caps at 2-3"规则明确约束通用内容的评分。

### 反面示例

```markdown
### Problem Statement (1-5)
| Score | Description |
| 1 | Poor — missing or very weak problem statement |
| 2 | Below average — problem statement lacks depth |
| 3 | Adequate — reasonable problem statement |
| 4 | Good — strong problem statement with clear user focus |
| 5 | Excellent — comprehensive, evidence-backed problem statement |
```

**为什么失败：** 每个描述词都是主观的 — "lacks depth"、"reasonable"和"strong"没有可测量定义。模型无法在没有字数或证据模式等具体信号的情况下区分 3 分和 4 分。AI 生成的模板文字读起来"reasonable"，评 3 分，实际应该限制在 2 分。

---

## Pattern 87: Eager Incremental Materialization

**出现频率：** <1% 的插件
**相关模式：** [Interactive Flow Control](#pattern-7), [Confirmation Gates](#pattern-8)

**定义：** 指示模型在对话*过程中*（而非之后）创建制品，使用工具调用作为实时反馈通道。

### 正面示例

```markdown
EAGER TOOL INVOCATION (CRITICAL)
Do NOT wait until the end to create plan items. Instead:
1. Create plan shell IMMEDIATELY when user provides product name
2. Create epics AS THEY EMERGE during discussion
3. Add features AS THEY'RE DEFINED

Why: Each tool call triggers a real-time WIP spinner in the plan tray,
giving immediate visual feedback that the plan is taking shape.

You CAN and SHOULD create items while still asking clarifying questions.
```

**为什么有效：** 反转默认的"收集所有信息再行动"行为。工具调用成为沟通通道 — 用户看到他们的话立即产出制品。允许"在提问的同时创建条目"覆盖了模型等待完整信息的倾向。

### 反面示例

```markdown
Gather all requirements from the user first.
Once you have a complete picture, create the plan with all epics and features.
Make sure everything is finalized before making any tool calls.
```

**为什么失败：** "先收集所有需求"强化了模型将所有操作推迟到对话结束的默认行为。用户在漫长的需求讨论中看不到可见进展，失去参与感，且没有机会根据部分制品进行纠偏。

---

## Pattern 88: Data Shape to Query Pattern Detection

**出现频率：** <1% 的插件
**相关模式：** [Intent Classification](#pattern-20), [Domain Knowledge Embedding](#pattern-24)

**定义：** 从数据制品推断可视化意图 — 检查 DataFrame 列名和原始查询文本，检测映射到特定图表类型的模式并附带置信度分数。

### 正面示例

```markdown
When source_type is "kusto", run pattern detection:

| Pattern Signal | Chart Type | Confidence |
| AD_score/AD_flag columns | time_series with anomaly highlights | high |
| Percentile columns (p50, p95, p99) | time_series with threshold highlights | high |
| render areachart in query | area or stacked_area | 0.9 (ADX hint) |
| Grouped continuous data (>50 rows) | violin (requires 20+ pts/group) | medium |
| Mixed pos/neg deltas (3-20 rows) | waterfall | medium |
| Source/target columns (<50 rows) | mermaid diagram | low |

Present ALL matches with confidence. Auto-populate from highest match.
User confirms, overrides, or rejects before proceeding.
```

**为什么有效：** 双信号方法（列名 + 查询文本）比单一信号提供更高准确度。置信度分数允许排名建议而非单一猜测。这从*数据结构*分类意图，而非从用户文本。

### 反面示例

```markdown
Analyze the data and choose the best chart type.
Consider the number of rows and columns to determine
whether a bar chart, line chart, or scatter plot is appropriate.
```

**为什么失败：** 忽略列名和查询文本丢弃了图表选择的最强信号。"行数和列数"太粗糙 — 100 行 3 列的数据集可能是时间序列、类别对比或分布，取决于列代表什么。没有置信度分数，模型锁定一种图表类型而不是呈现排名替代方案供用户确认。

---

## Pattern 89: Writability Rules and Linguistic Substitution Tables

**出现频率：** <1% 的插件
**相关模式：** [Negative Constraints](#pattern-6), [Self-Critique](#pattern-28)

**定义：** 完整的文体转换引擎：替换表（术语→简单词）、检测启发式（被动语态"by zombies"测试）、量化目标（15-20 词平均句长、80% 主动动词）和自验证清单。

### 正面示例

```markdown
### Passive voice detection
Can you add "by zombies" after the verb and it still makes sense? → passive

### Jargon substitution (26 entries)
| Instead of | Use |
| commence | start, begin |
| comply with | keep to, follow |
| ensure | make sure |
| utilise | use |

### Nominalisation detection
Words ending in -tion, -sion, -ment, -ence, -ance with a simpler verb inside:
| Avoid | Use |
| We made an arrangement | We arranged |
| We reached an agreement | We agreed |

### Quality targets
- Average sentence length: 15-20 words
- Active verbs: ≥80%
- Zero remaining jargon with simpler alternatives
```

**为什么有效：** 替换表给模型一个穷举查找。检测启发式（"by zombies"测试、后缀模式）教*如何*检测问题。量化目标使合规可测量。可被其他 skills 复用为后处理器。

### 反面示例

```markdown
Write in plain English. Avoid jargon and complex language.
Use short sentences and active voice where possible.
Keep the tone professional but accessible.
```

**为什么失败：** "Avoid jargon"没有替换表意味着模型必须对每个词自行判断是否为术语 — 它会漏掉"utilise"和"commence"同时标记没有更简单替代词的技术术语。"Short sentences"和"active voice where possible"没有量化，无法验证合规。模型没有检测被动语态或名词化的方法。

---

## Pattern 90: Cross-Platform Surface Compatibility Matrix

**出现频率：** <1% 的插件
**相关模式：** [Cross-Platform Handling](#pattern-17), [Error Handling](#pattern-15)

**定义：** 兼容性降级矩阵，将源/目标平台对映射到具体的功能损失和自动化解决路径，结合有界重试语义。

### 正面示例

```markdown
| Source Surface | Target Surface | Issues | Resolution |
| Teams (v1.5+) | Outlook (v1.4) | Table, Carousel unsupported | transform_card with downgrade to 1.4 |
| Generic (v1.6) | Windows (v1.3) | Action.Execute, Table | transform_card with downgrade to 1.3 |

Bounded retry:
- Max 2 retry cycles for fix-and-revalidate loops
- MCP server unreachable → do NOT attempt to hand-write card JSON
- Tool-call budget: max 3 primary calls per user request
```

**为什么有效：** 平台对有具体的解决命令 — 无需猜测。"do not hand-write JSON"规则防止模型绕过工具的常见失败模式。有界重试防止无限修复-验证循环。

### 反面示例

```markdown
Ensure the card is compatible with the target platform.
If validation fails, fix the card and try again.
If the MCP server is unavailable, generate the card JSON directly.
```

**为什么失败：** "Ensure compatibility"没有平台对矩阵迫使模型猜测哪些功能在哪个平台降级。无界的"fix and try again"在同一验证错误反复出现时创建无限重试循环。允许在服务器不可用时手写 JSON 完全绕过 schema 验证，产出在目标平台上静默失败的畸形 card。

---

## Pattern 91: Hub-Spoke Domain Router with Overlap Resolution

**出现频率：** 约 1% 的插件
**相关模式：** [Intent Classification](#pattern-20), [Skill Composition](#pattern-19)

**定义：** 多级特异性级联，用于消歧关键词空间重叠的专业插件。上下文相关的路由规则，同一关键词根据共现词不同路由到不同目标。

### 正面示例

```markdown
## Overlap Resolution (specificity-first)

1. Specific product area named (ProductA, ProductB, ProductC) → domain plugin
2. "Flight" + "ProductC bug" → productc-investigation (has flight classification rules)
   "Flight" standalone → flight-investigation
3. General Excel telemetry → kql-reference
4. Bug ID mentioned → classify by tag/title pattern:
   - BugTracker/Triage → fetch-bug
   - ProductC → productc-investigation
   - Unknown → ask user
5. "Pipeline" → "CI/CD health" vs "ADF query" → ask if unclear
6. Still ambiguous → present top 2-3 candidates and ask user to pick

If target plugin not installed:
"The {domain} capability requires {plugin-name}.
Install with: /plugin install {plugin-name}@marketplace"
```

**为什么有效：** 六级特异性级联提供确定性消歧。上下文相关规则（规则 2："flight"根据共现的"ProductC bug"含义不同）处理实际歧义。优雅降级将路由失败转为可操作的安装指引。

### 反面示例

```markdown
Route the user's request to the most relevant plugin.
If the request mentions a product name, use that product's plugin.
If unclear, ask the user which plugin they want.
```

**为什么失败：** 没有特异性级联意味着重叠关键词（如"flight"同时出现在 Shield 和 flight-investigation 上下文中）由模型先想到的插件解决。任何歧义直接跳到"ask the user"将消歧负担推给可能不知道有哪些插件的用户。缺少安装指引意味着未安装的插件静默失败而非产出可操作的下一步。
