# 来自开源 Skill 仓库的提示模式

**Patterns 100-120** -- 提取自 Anthropic 官方 `skills` 仓库（17 个 skill）和 ComposioHQ 的 `awesome-claude-skills` 仓库（32 个独立 skill + 832 个 Composio 自动化 skill）。

**数据来源:**
- Anthropic 官方 Agent Skills（17 个 SKILL.md 文件 + 35 个参考文件）
- 社区精选 skills（32 个 SKILL.md 文件 + 832 个 Composio skills）
- **提取日期:** 2026-04-15

**与现有目录的关系:** Patterns 1-99 从 500+ 生产插件中提取，覆盖 DevOps、安全、迁移和事件响应领域。这 21 个模式（100-120）来自开源生态，代表内部未观察到的全新技术或重要改进。

---

## 快速索引

| # | 模式 | 分类 | 来源仓库 | 核心收益 |
|---|------|------|---------|---------|
| 100 | [Progressive Disclosure Architecture](#pattern-100-progressive-disclosure-architecture) | Structural | skills (skill-creator) | 三层上下文加载最小化 token 浪费 |
| 101 | [Creative Philosophy Scaffolding](#pattern-101-creative-philosophy-scaffolding) | Creative | skills (canvas-design) | 强制在视觉执行前进行概念深化 |
| 102 | [Mandatory Refinement Pass](#pattern-102-mandatory-refinement-pass) | Quality | skills (canvas-design) | 带有特定批评话术的自我质量门控 |
| 103 | [Reconnaissance-Then-Action](#pattern-103-reconnaissance-then-action) | Execution | skills (webapp-testing) | 行动前先观察状态，防止盲目交互 |
| 104 | [Helper Script as Black Box](#pattern-104-helper-script-as-black-box) | Execution | skills (webapp-testing) | 脚本封装复杂性；模型先用 `--help` |
| 105 | [Anti-Slop Design Guidelines](#pattern-105-anti-slop-design-guidelines) | Quality | skills (frontend-design) | 明确列出要避免的"AI 审美"反模式 |
| 106 | [Section-by-Section Collaborative Drafting](#pattern-106-section-by-section-collaborative-drafting) | Workflow | skills (doc-coauthoring) | 逐章节迭代而非一次性生成全文 |
| 107 | [Reader Testing with Sub-Agent](#pattern-107-reader-testing-with-sub-agent) | Quality | skills (doc-coauthoring) | 生成独立的"新鲜眼睛"子 Agent 审查 |
| 108 | [Blind A/B Comparison](#pattern-108-blind-ab-comparison) | Evaluation | skills (skill-creator) | 双盲 Skill 评估消除确认偏差 |
| 109 | [Composio 3-Step SaaS Integration](#pattern-109-composio-3-step-saas-integration) | Integration | awesome (Composio) | Search -> Connect -> Execute 通用 SaaS API 模式 |
| 110 | [Algorithm-as-Domain Knowledge](#pattern-110-algorithm-as-domain-knowledge) | Knowledge | awesome (twitter-optimizer) | 将真实系统内部机制嵌入提示知识 |
| 111 | [Clarifying Questions Before Action](#pattern-111-clarifying-questions-before-action) | Execution | awesome (multiple) | 行动前的结构化问题列表 |
| 112 | [Output Format with Populated Example](#pattern-112-output-format-with-populated-example) | I/O | awesome (multiple) | 展示完整真实输出而非抽象 schema |
| 113 | [Multi-Workflow Routing by Input Type](#pattern-113-multi-workflow-routing-by-input-type) | Structural | skills (docx, pdf) | 同一 Skill 根据输入类型路由到创建/读取/编辑 |
| 114 | [Font/Asset Bundling with Directory Reference](#pattern-114-fontasset-bundling-with-directory-reference) | Knowledge | skills (canvas-design) | 通过相对路径引用捆绑资源 |
| 115 | [QA Sub-Agent with Visual Verification](#pattern-115-qa-sub-agent-with-visual-verification) | Quality | skills (pptx) | 生成子 Agent 截图并检查输出 |
| 116 | [Never-Hardcode Financial Rules](#pattern-116-never-hardcode-financial-rules) | Safety | skills (xlsx) | 所有计算值必须用公式，不能硬编码 |
| 117 | [Multi-Language SDK Routing](#pattern-117-multi-language-sdk-routing) | Structural | skills (claude-api) | 检测编程语言，加载对应 SDK 文档 |
| 118 | [Surface Selection by Architecture](#pattern-118-surface-selection-by-architecture) | Structural | skills (claude-api) | 按需求路由到单调用/工作流/Agent 模式 |
| 119 | [Eval-Driven Skill Improvement Loop](#pattern-119-eval-driven-skill-improvement-loop) | Quality | skills (skill-creator) | 写测试 -> 运行 -> 评分 -> 改进 -> 基准循环 |
| 120 | [Non-Anthropic Provider Guard](#pattern-120-non-anthropic-provider-guard) | Safety | skills (claude-api) | 检测到非 Anthropic 的 import 时提前退出 |

---

<a id="pattern-100-progressive-disclosure-architecture"></a>
## Pattern 100: Progressive Disclosure Architecture

**分类:** Structural Scaffolding
**来源:** `skills/skill-creator/SKILL.md`
**出现率:** Anthropic 官方 Skill 编写指南中记录为最佳实践

### 概念

按需分三层加载上下文，而非一次性全部加载。防止 token 膨胀。

### 三层结构

| 层 | 内容 | 加载时机 | 目标大小 |
|----|------|---------|---------|
| **Tier 1: Metadata** | YAML frontmatter (`name`, `description`) | 始终在上下文中（system prompt） | ~100 词 |
| **Tier 2: SKILL.md body** | 核心指令、工作流、边界 | Skill 被调用时 | <5,000 词 |
| **Tier 3: Bundled resources** | 参考文件、脚本、schema、示例 | 按需通过 Read 工具 | 无限制 |

### 正面示例：渐进式加载

```yaml
---
name: mcp-builder
description: Guide for creating MCP servers...
---

# MCP Server Builder

## Phase 1: Research
Read the framework documentation:
- TypeScript: Read `reference/node_mcp_server.md`
- Python: Read `reference/python_mcp_server.md`
```

模型仅在进入 Phase 1 时读取 Tier 3 文件。如果用户问题仅凭 Tier 2 就能回答，这些文件永远不会被加载。

### 反面示例：全部内联

```yaml
---
name: mcp-builder
description: Guide for creating MCP servers...
---

# MCP Server Builder

## TypeScript MCP Server Documentation
[... 2000 lines of TypeScript SDK docs ...]

## Python MCP Server Documentation
[... 1500 lines of Python SDK docs ...]
```

每次调用都支付全部 token 成本，即使用户只需要 TypeScript。

### 生效原因

Token 上下文有限。渐进式呈现将注意力集中在当前最相关的层。Tier 3 资源在需要时加载到新的注意力窗口（通过 Read 工具）-- 最大化注意力局部性。

### 在我们插件中的应用

我们的迁移插件使用此模式：CLAUDE.md（Tier 2，始终加载）通过 `@rules/...` 引用按需文件（Tier 3，进入阶段时读取）。CLAUDE.md 中的 `<always-loaded>` 和 `<on-demand>` 部分就是显式的 Progressive Disclosure Architecture。

---

<a id="pattern-101-creative-philosophy-scaffolding"></a>
## Pattern 101: Creative Philosophy Scaffolding

**分类:** Creative Workflow
**来源:** `skills/canvas-design/SKILL.md`, `skills/algorithmic-art/SKILL.md`
**出现率:** 2 个 skill（均为 Anthropic 官方）

### 概念

在产出创意输出前，强制模型阐述一个**设计哲学** -- 一个命名的美学运动及其原则。通过建立概念约束防止泛化输出。

### 正面示例：哲学优先

```markdown
## Step 1: Create Design Philosophy

Create a `.md` file articulating a visual philosophy/aesthetic movement:
- Give the movement a NAME (e.g., "Chromatic Language", "Geometric Silence")
- Articulate through: space, form, color, scale, rhythm, composition
- This is a PHILOSOPHY, not a layout description
- Use craftsmanship language throughout

## Step 2: Deduce the Subtle Reference
Identify the conceptual thread from the original request.
This becomes the "soul" of the piece.

## Step 3: Express Philosophy on Canvas
Apply the philosophy visually. Museum-quality output.
```

### 反面示例：直接生成

```markdown
## Step 1: Create the design
Make a beautiful poster based on the user's request.
Use good colors and layout.
```

### 生效原因

哲学步骤强制模型在执行前做出有意识的艺术选择。这创建了一个强先验约束后续所有生成 -- 降低了产出泛化"AI 水货"的概率。命名的运动作为注意力锚点。

---

<a id="pattern-102-mandatory-refinement-pass"></a>
## Pattern 102: Mandatory Refinement Pass

**分类:** Quality
**来源:** `skills/canvas-design/SKILL.md`
**出现率:** 3 个 skill

### 概念

在初始输出后，提示强制一个自我批评和打磨步骤，使用特定语言提升质量标准。

### 正面示例：显式精修配合情感锚定

```markdown
## Final Step: Refinement

Examine your work critically. Use this exact thought:
"It isn't perfect enough. It must be pristine."

Look for:
- Alignment issues (off by even 1 pixel)
- Color harmony (does every color earn its place?)
- Typography kerning and weight
- Negative space balance
- Overall composition from 3 feet away

Make corrections. Do NOT skip this step.
```

### 反面示例：可选质检

```markdown
## Optional: Review your work
If time permits, check for any issues.
```

### 生效原因

"It isn't perfect enough. It must be pristine." 这句话充当情感提示，将模型的生成分布推向更高质量的 token。具体的检查清单提供了明确的注意力目标。强制（非可选）防止模型跳过以"省力"。

---

<a id="pattern-103-reconnaissance-then-action"></a>
## Pattern 103: Reconnaissance-Then-Action

**分类:** Execution Control
**来源:** `skills/webapp-testing/SKILL.md`
**出现率:** 1 个 skill（但模式高度通用）

### 概念

与动态系统（浏览器、API、CLI）交互前，先观察当前状态。永远不要盲目行动。

### 正面示例：先观察

```markdown
## Reconnaissance-Then-Action Pattern

When testing any webpage:
1. **First:** Take a screenshot to see what the page actually looks like
2. **Second:** Inspect the DOM to identify precise selectors
3. **Third:** Identify the specific elements you need to interact with
4. **Fourth:** Execute your action using the identified selectors

NEVER click, type, or navigate without first observing the current state.
```

### 反面示例：立即行动

```markdown
## Testing
1. Click the login button
2. Type the username
3. Submit the form
```

### 生效原因

动态系统有模型无法从提示中预测的状态。侦察步骤提供了锚定 -- 用具体观察来约束后续行动。没有它，模型会幻想元素位置和状态。

### 更广泛的应用

此模式适用于浏览器测试之外的场景：
- **文件系统:** `ls` 在 `mv` 之前
- **Git:** `git status` 在 `git add` 之前
- **数据库:** `SELECT` 在 `UPDATE` 之前
- **API:** `GET` 在 `PUT` 之前

我们的 build-repair-agent 使用了一个变体：在应用修复前始终读取构建输出。

---

<a id="pattern-104-helper-script-as-black-box"></a>
## Pattern 104: Helper Script as Black Box

**分类:** Execution Control
**来源:** `skills/webapp-testing/SKILL.md`, `skills/web-artifacts-builder/SKILL.md`
**出现率:** 5 个 skill

### 概念

将复杂操作封装到脚本中。模型先用 `--help` 了解接口，然后将脚本当作黑盒使用，无需理解内部实现。

### 正面示例：脚本 + --help 发现

```markdown
## Helper Scripts

### scripts/with_server.py
Manages server lifecycle for testing. Always run `--help` first:
```bash
python scripts/with_server.py --help
```

Use it as a black box — do not modify the script or duplicate its logic.

### scripts/bundle-artifact.sh
Bundles React app into single HTML. Run directly:
```bash
bash scripts/bundle-artifact.sh
```
```

### 反面示例：内联所有逻辑

```markdown
## Starting the server
1. Check if port 3000 is in use
2. If yes, kill the process
3. Run `npm start` in background
4. Wait for server to be ready
5. Check health endpoint
6. If health fails, retry 3 times
...
```

### 生效原因

脚本提供认知卸载 -- 模型无需推理服务器生命周期管理，只需调用函数。`--help` 发现模式意味着模型适配脚本的实际接口而非猜测。

---

<a id="pattern-105-anti-slop-design-guidelines"></a>
## Pattern 105: Anti-Slop Design Guidelines

**分类:** Quality / Negative Space
**来源:** `skills/frontend-design/SKILL.md`, `skills/web-artifacts-builder/SKILL.md`
**出现率:** 2 个 skill（Anthropic 官方）

### 概念

明确命名 AI 倾向于生成的泛化模式并禁止它们。这是 Negative Constraints (Pattern 6) 在创意输出上的特化应用。

### 正面示例：命名反模式

```markdown
## Design Guidelines

Avoid these "AI slop" aesthetics:
- Excessive centered layouts (everything stacked vertically)
- Purple/blue gradient backgrounds (the default AI palette)
- Uniform rounded corners on everything
- Inter font everywhere
- Card-based layouts with no visual hierarchy
- Gratuitous animation with no purpose
- Stock photo placeholders

Instead:
- Use asymmetric layouts with intentional tension
- Choose colors that serve the content's mood
- Mix sharp and rounded corners deliberately
- Select typefaces that match the content's personality
```

### 反面示例：模糊的质量指令

```markdown
## Design
Make it look professional and modern.
```

### 生效原因

"Professional and modern"正是产出 AI 水货的分布 -- 它是模型见过的所有"好看"网站的统计平均。命名具体反模式抑制了这些模式，而替代方案提升了有特色的选择。

---

<a id="pattern-106-section-by-section-collaborative-drafting"></a>
## Pattern 106: Section-by-Section Collaborative Drafting

**分类:** Workflow
**来源:** `skills/doc-coauthoring/SKILL.md`
**出现率:** 1 个 skill

### 概念

不是一次生成完整文档，而是逐章节构建，每个阶段都有用户输入。每个章节经历：澄清 -> 头脑风暴 -> 筛选 -> 缺口检查 -> 草稿 -> 精修。

### 正面示例：逐章节迭代

```markdown
## Stage 2: Section-by-Section Building

For EACH section in the outline:

1. **Clarify:** "What's the main point you want this section to make?"
2. **Brainstorm:** Generate 3-5 possible approaches for this section
3. **Curate:** User picks the approach (or combines)
4. **Gap Check:** "What information am I missing to write this well?"
5. **Draft:** Write the section
6. **Refine:** User provides feedback, iterate until satisfied

Only move to the next section when the current one is approved.
```

### 反面示例：全文生成

```markdown
## Writing
Generate the complete document based on the outline.
Present it to the user for review.
```

### 生效原因

全文生成将注意力稀释到整篇文章上。逐章节集中模型注意力于一个连贯的单元。每个阶段的用户反馈在错误积累前提供方向修正。

---

<a id="pattern-107-reader-testing-with-sub-agent"></a>
## Pattern 107: Reader Testing with Sub-Agent

**分类:** Quality
**来源:** `skills/doc-coauthoring/SKILL.md`
**出现率:** 1 个 skill

### 概念

写完文档后，生成一个独立 Agent（子 Agent）作为零背景的读者审查。子 Agent 不了解写作过程 -- 只看到文档本身。提供真正的"新鲜眼睛"审查。

### 正面示例：子 Agent 作为零背景读者

```markdown
## Stage 3: Reader Testing

### With Sub-Agents (preferred)
Spawn a sub-agent with ONLY the document (no outline, no conversation history).
Give it these instructions:
- Read the document as if you've never seen it before
- Predict what each section will say BEFORE reading it (to test if structure is clear)
- Note any confusion, jargon, or missing context
- Rate each section's clarity on 1-5

### Without Sub-Agents (fallback)
Read the document as if for the first time.
For each section heading, predict its content before reading.
Note surprises — any surprise = a clarity issue.
```

### 反面示例：无隔离的自我审查

```markdown
## Review
After writing, re-read the document yourself and check for clarity issues.
```

作者 Agent 已经知道每句话背后的意图。无记忆隔离的自我审查产生虚假自信 -- Agent 从自己的上下文中填补空缺而非检测它们。

### 生效原因

主 Agent 见过整个写作过程 -- 无法成为零背景读者。具有记忆隔离（Pattern 42）的子 Agent 真的不知道前情。它的困惑是真实信号，不是模拟的。

---

<a id="pattern-108-blind-ab-comparison"></a>
## Pattern 108: Blind A/B Comparison

**分类:** Evaluation
**来源:** `skills/skill-creator/SKILL.md`, `skills/skill-creator/agents/comparator.md`
**出现率:** 1 个 skill（但深度开发）

### 概念

通过在相同输入上运行两个 Skill 版本，然后让盲评 Agent 在不知哪个版本产出了哪个结果的情况下评估输出来比较。消除确认偏差。

### 架构

```
1. Run Skill Version A on N test cases → collect outputs
2. Run Skill Version B on same N test cases → collect outputs
3. Randomly assign as "Output A" and "Output B" (blind)
4. Comparator agent reads both outputs + rubric
5. Comparator determines winner without knowing version labels
6. Analyzer agent extracts actionable improvements from winner
```

### Comparator 的 7 步流程

```markdown
1. Read both outputs without seeing skill content
2. Understand what the task asked for
3. Generate evaluation rubric (content + structure dimensions)
4. Evaluate each output against rubric
5. Check assertions (from test cases)
6. Determine winner with scores and reasoning
7. Write results as structured JSON
```

### 反面示例：作者选择赢家

```markdown
## Comparison
Run both versions, then decide which one you think is better
and explain why.
```

"改进"版本的作者对自己的修改有锚定偏差。没有双盲和结构化评分标准，评估者会可靠地选择他们预期更好的版本。

### 生效原因 -- 如果知道哪个版本是"新的"或"改进的"，会给它更高的评分。双盲完全消除了这种偏差。7 步流程为评估本身提供了认知卸载。

---

<a id="pattern-109-composio-3-step-saas-integration"></a>
## Pattern 109: Composio 3-Step SaaS Integration

**分类:** Integration
**来源:** `awesome-claude-skills/composio-skills/*`（832 个 skill）
**出现率:** 832 个 skill 使用完全相同的模式

### 概念

通过三个确定性步骤集成任何 SaaS API 的通用模板：Search -> Connect -> Execute。

### 模板

```markdown
## How to use this skill

1. **Search for available tools:**
   Use RUBE_SEARCH_TOOLS with toolkit name "{service}" to discover available actions.

2. **Check and establish connection:**
   Use RUBE_MANAGE_CONNECTIONS to verify or create the API connection.
   If no connection exists, provide the setup URL to the user.

3. **Execute the action:**
   Use RUBE_MULTI_EXECUTE_TOOL to run the discovered action.

## Known Pitfalls
- Always search for tools first — tool names change between versions
- Always verify connection before execution — expired tokens cause silent failures
```

### 反面示例：硬编码 API 调用

```markdown
## Slack Integration
Call `chat.postMessage` with the channel ID and message text.
Use the bot token from environment variable SLACK_TOKEN.
```

硬编码的 action 名称在 API 变更时会失效。硬编码的鉴权跳过了连接验证，在 token 过期时导致静默失败。

### 生效原因 -- 对 832+ 种不同 SaaS API 有效，因为它将所有服务特定的细节抽象到工具发现步骤中。模型无需了解 Slack 的 API 或 Jira 的 API -- 它在运行时发现可用操作。

---

<a id="pattern-110-algorithm-as-domain-knowledge"></a>
## Pattern 110: Algorithm-as-Domain Knowledge

**分类:** Knowledge
**来源:** `awesome-claude-skills/twitter-algorithm-optimizer/SKILL.md`
**出现率:** 1 个 skill（但技术广泛适用）

### 概念

将外部系统的真实内部机制（排名算法、评分模型、推荐引擎）作为结构化领域知识嵌入提示。模型据此对真实算法进行内容优化，而非猜测。

### 正面示例：真实的算法内部机制

```markdown
## Twitter's Core Ranking Models

1. **Real-graph:** Predicts interaction probability between user pairs
2. **SimClusters:** Community detection via user-topic embedding spaces
3. **TwHIN:** Knowledge graph embeddings (user-tweet-author triples)
4. **Tweepcred:** PageRank-style reputation scoring on social graph

## Engagement Signals (Weighted)
- Explicit: likes (1x), replies (3x), retweets (5x), quotes (10x)
- Implicit: profile visits, link clicks, dwell time, bookmarks
- Negative: block (-100x), mute (-50x), "not interested" (-20x)

## Optimization Strategy
For each tweet, map to algorithm components:
1. Will this trigger Real-graph? (personal relevance)
2. Does it fit SimClusters? (community resonance)
3. What signals will it maximize? (engagement weights)
```

### 反面示例：泛泛建议

```markdown
## How to write good tweets
- Be engaging
- Use hashtags
- Post at good times
```

### 生效原因

当嵌入的知识是真实系统内部机制而非人工摘要时，Domain Knowledge Embedding (Pattern 24) 效果大幅增强。模型可以针对具体机制（SimClusters, Real-graph）进行推理，而非模糊概念（"engagement"）。

---

<a id="pattern-111-clarifying-questions-before-action"></a>
## Pattern 111: Clarifying Questions Before Action

**分类:** Execution Control
**来源:** `awesome-claude-skills/file-organizer/SKILL.md` 等 10+ 个 skill
**出现率:** ~40% 的社区 skill

### 概念

在做任何工作之前，提出 3-5 个具体的澄清问题。不是开放式的"you want what?"，而是收集推进所需参数的针对性问题。

### 正面示例：针对性问题

```markdown
## Step 1: Understand the Scope

Before organizing ANY files, ask these questions:
1. Which directory should I focus on? (specific path)
2. What's the main problem? (duplicates / messy naming / wrong locations / all of the above)
3. Are there any files or folders I should NEVER touch?
4. How aggressive should I be? (suggest only / move files / delete duplicates)
```

### 反面示例：开放式或无问题

```markdown
## Step 1: Organize
Look at the user's files and organize them.
```

### 生效原因

每个问题约束一个否则会欠定的参数。这是 Schema Priming（Technique 6）的运行时应用 -- 问题在执行开始前定义了任务的"schema"。

### 出现率说明

这是社区 skill 中最常见的模式（~40%）。它出现在几乎每个非平凡 skill 的开头，表明这是 skill 作者独立发现的自然最佳实践。

---

<a id="pattern-112-output-format-with-populated-example"></a>
## Pattern 112: Output Format with Populated Example

**分类:** I/O Contracts
**来源:** `awesome-claude-skills/domain-name-brainstormer/SKILL.md` 等 10+ 个 skill
**出现率:** ~35% 的社区 skill

### 概念

展示一个包含真实数据的完整、现实的输出示例 -- 而非带占位符类型的抽象 schema。示例本身就是 schema。

### 正面示例：填充完整数据的示例

```markdown
## Example Output

### Available (.com)
| Domain | Status | Price |
|--------|--------|-------|
| codeflow.com | Available | ~$12/yr |
| devpulse.com | Available | ~$12/yr |

### Available (Alternative TLDs)
| Domain | Status | Price |
|--------|--------|-------|
| codeflow.dev | Available | ~$14/yr |
| codeflow.io | Available | ~$30/yr |

### Recommendations
**Top Pick:** codeflow.com — short, memorable, .com availability
**Runner-up:** devpulse.dev — modern TLD, developer audience signal
```

### 反面示例：抽象 schema

```markdown
## Output Format
Return a table with columns: domain, status, price.
Group by availability.
Include recommendations.
```

### 生效原因

填充示例比抽象 schema 提供了更强的锚定因为：
1. 模型看到精确的格式（表格对齐、标题、章节结构）
2. 数据分布被示范了（价格范围、TLD 多样性、推荐风格）
3. 语调被确立了（简洁描述、比较语言）

---

<a id="pattern-113-multi-workflow-routing-by-input-type"></a>
## Pattern 113: Multi-Workflow Routing by Input Type

**分类:** Structural
**来源:** `skills/docx/SKILL.md`, `skills/pdf/SKILL.md`, `skills/pptx/SKILL.md`
**出现率:** 4 个文档类 skill

### 概念

单个 Skill 通过根据用户提供的输入进行路由来处理多个根本不同的工作流（创建、读取、编辑）。

### 正面示例：输入类型路由

```markdown
## Workflow Selection

What does the user want?
├─ **Read/analyze** an existing document?
│  └─ Use `pandoc` to convert to markdown, then analyze
│
├─ **Create** a new document from scratch?
│  └─ Use docx-js (JavaScript) to build programmatically
│
├─ **Edit** an existing document (preserve formatting)?
│  └─ Unpack OOXML, edit XML directly, repack
│     (This is the only way to preserve styles, track changes, etc.)
```

### 反面示例：单一工作流

```markdown
## Creating Documents
Here's how to create Word documents...
(User who wants to EDIT is lost)
```

### 生效原因

这是 Intent Classification (Pattern 20) 的特化形式，但路由键是输入类型（无 vs 已有文件 vs 两者兼有），而非用户陈述的意图。决策树格式提供无歧义的确定性路由。

---

<a id="pattern-114-fontasset-bundling-with-directory-reference"></a>
## Pattern 114: Font/Asset Bundling with Directory Reference

**分类:** Knowledge / Context
**来源:** `skills/canvas-design/SKILL.md`（54 种字体）, `skills/algorithmic-art/SKILL.md`（模板）
**出现率:** 4 个 skill

### 概念

将物理资源（字体、模板、schema）与 Skill 捆绑在一起，通过相对路径引用。模型直接使用资源 -- 无需下载，无外部依赖。

### 正面示例：捆绑资源 + 路径引用

```markdown
## Available Fonts

Use fonts from the `./canvas-fonts` directory. Available families:
- Playfair Display (Regular, Bold, Italic)
- Space Mono (Regular, Bold)
- Crimson Text (Regular, Italic)
- ...

Always use absolute paths resolved from the skill directory.
Do NOT download fonts from the internet.
```

### 反面示例：运行时下载

```markdown
## Fonts
Download a font from Google Fonts that matches the design.
Use the URL: https://fonts.googleapis.com/css2?family=...
```

运行时下载引入网络故障、版本漂移和不可预测的可用性。模型还可能幻想出返回 404 的字体 URL。

### 生效原因 -- 模型无需检查字体是否存在或处理下载失败。相对路径引用创建了封闭系统 -- 所有资源在提示编写时已知。

---

<a id="pattern-115-qa-sub-agent-with-visual-verification"></a>
## Pattern 115: QA Sub-Agent with Visual Verification

**分类:** Quality
**来源:** `skills/pptx/SKILL.md`
**出现率:** 1 个 skill

### 概念

生成视觉输出（幻灯片、图像、PDF）后，生成一个子 Agent 对结果进行截图并验证是否满足质量标准。QA Agent 具有视觉检查能力。

### 正面示例：视觉 QA 循环

```markdown
## Quality Assurance

After generating slides:
1. Spawn a sub-agent with screenshot capability
2. Sub-agent opens each slide and takes screenshots
3. Sub-agent checks against these criteria:
   - No text overflow outside slide boundaries
   - No repeated layouts on consecutive slides
   - No accent lines under titles (anti-pattern)
   - Color palette consistency
   - Font size readability
4. Report issues → fix → re-verify
```

### 反面示例：纯文本审查

```markdown
## Quality Check
Review the generated slide XML to verify layout is correct.
Check that no text exceeds the slide boundaries.
```

幻灯片 XML 坐标是不透明的数字（EMU 单位）。纯文本的 XML 检查无法可靠地检测视觉溢出、错位或色彩冲突。

### 生效原因（溢出、对齐、色彩冲突）。子 Agent 提供真正的视觉反馈循环。这是 Reader Testing (Pattern 107) 和 Memory Isolation (Pattern 42) 的特化组合。

---

<a id="pattern-116-never-hardcode-financial-rules"></a>
## Pattern 116: Never-Hardcode Financial Rules

**分类:** Safety / Domain
**来源:** `skills/xlsx/SKILL.md`
**出现率:** 1 个 skill（但对任何数据 Skill 至关重要）

### 概念

对于电子表格/财务输出，所有计算值必须使用公式 -- 永远不能硬编码。确保输入变更时电子表格仍然有效。

### 正面示例：公式优先规则

```markdown
## Critical Rule: Formulas, Never Hardcoded Values

NEVER put a calculated number directly in a cell.
ALWAYS use an Excel formula.

✅ Cell C2: =A2*B2 (calculates price × quantity)
❌ Cell C2: 150 (hardcoded result of 10 × 15)

After creating the spreadsheet, MANDATORY: run LibreOffice recalculation
to verify all formulas produce correct results.
```

### 反面示例：单元格中放计算结果

```markdown
## Spreadsheet
Fill in the total column with the calculated values.
For row 2, the total is 150. For row 3, the total is 230.
```

硬编码结果产出"死"电子表格。任何输入变更后，合计值会静默过时而无错误提示。

### 生效原因 -- 此显式禁令配合公式优先的替代方案重新引导了这种倾向。强制重新计算步骤提供了验证门控。

### 更广泛的适用性

此模式泛化为：**当可以保留计算逻辑时，永远不要嵌入计算结果**。适用于：
- SQL view 而非物化快照
- 配置模板而非展开的配置
- 构建脚本而非提交的构建输出

---

<a id="pattern-117-multi-language-sdk-routing"></a>
## Pattern 117: Multi-Language SDK Routing

**分类:** Structural
**来源:** `skills/claude-api/SKILL.md`
**出现率:** 1 个 skill

### 概念

从 import/文件扩展名/显式声明中检测用户的编程语言，然后仅加载相关的 SDK 文档。

### 正面示例：语言检测 + 选择性加载

```markdown
## Language Detection

Determine the user's language:
├─ Python imports (`import anthropic`, `from anthropic`) → Read `python/claude-api/README.md`
├─ TypeScript imports (`import Anthropic`, `from @anthropic-ai/sdk`) → Read `typescript/claude-api/README.md`
├─ Java → Read `java/claude-api.md`
├─ Go → Read `go/claude-api.md`
├─ Ruby → Read `ruby/claude-api.md`
├─ C# → Read `csharp/claude-api.md`
├─ PHP → Read `php/claude-api.md`
├─ cURL / no code → Read `curl/examples.md`
└─ Unknown → Ask user

Always load `shared/models.md` regardless of language.
```

### 反面示例：加载所有语言文档

```markdown
## API Documentation
Here is the complete Claude API reference for all languages:
[... Python docs ...] [... TypeScript docs ...] [... Java docs ...]
[... Go docs ...] [... Ruby docs ...]
```

加载全部 7 种语言的 SDK 在 6 种不相关的语言上浪费 ~1800 行上下文。注意力稀释导致模型混淆语言特定的惯用法。

### 生效原因 -- 模型只加载 ~200 行语言特定文档而非 ~2000 行全语言文档。Token 节省直接通过集中注意力来提升输出质量。

---

<a id="pattern-118-surface-selection-by-architecture"></a>
## Pattern 118: Surface Selection by Architecture

**分类:** Structural
**来源:** `skills/claude-api/SKILL.md`
**出现率:** 1 个 skill

### 概念

确定语言后，确定用户需要的架构模式，仅加载该模式的文档。

### 正面示例：架构路由

```markdown
## Surface Selection

What is the user building?
├─ **Single API call** (classification, extraction, Q&A)
│  └─ Load: language-specific basic examples
├─ **Multi-step workflow** (pipelines, chains)
│  └─ Load: tool-use docs + streaming docs
├─ **Autonomous agent** (tool loop, planning)
│  └─ Load: tool-use + agent design docs
├─ **Managed agent** (Anthropic-hosted)
│  └─ Load: managed-agents docs (beta)
```

### 反面示例：所有用例使用单一模式

```markdown
## Claude API
Use messages.create() to call the Claude API.
Pass your prompt in the messages array.
```

单调用示例使构建 agent 或工作流的用户无所适从，缺少 tool use、streaming 或多轮交互的指导。

### 生效原因 -- 模型恰好加载正确的文档子集。Python 用户构建简单分类器加载 ~100 行。TypeScript 用户构建自主 Agent 加载 ~400 行。两者都不加载完整的 2000+ 行语料库。

---

<a id="pattern-119-eval-driven-skill-improvement-loop"></a>
## Pattern 119: Eval-Driven Skill Improvement Loop

**分类:** Quality / Evaluation
**来源:** `skills/skill-creator/SKILL.md`
**出现率:** 1 个 skill（Anthropic 官方）

### 概念

通过自动化评估改进 Skill 的结构化循环：编写测试用例 -> 运行 -> 评分 -> 提取改进点 -> 应用 -> 重新基准测试。

### 5 步 Eval 流程

```markdown
## Running Evaluations

1. **Create test cases** (`evals.json`):
   - 5+ prompts covering different scenarios
   - Each with expectations (MUST contain, MUST NOT contain, behavioral checks)

2. **Run tests:** Spawn sub-agent per test case
   - Sub-agent executes the skill with the test prompt
   - Captures full transcript + output

3. **Grade:** Spawn grader sub-agent
   - Reads expectations + transcript
   - Extracts claims, verifies each against evidence
   - PASS/FAIL per expectation with reasoning

4. **Analyze:** Spawn analyzer sub-agent
   - Surfaces per-assertion patterns (which expectations fail most?)
   - Cross-eval patterns (are failures correlated?)
   - Generates improvement suggestions

5. **Improve:** Apply suggestions to SKILL.md
   - Re-run evals to verify improvement
   - Benchmark: compare old vs new versions
```

### 反面示例：手动抽查

```markdown
## Testing
Try a few prompts and see if the output looks good.
If it does, ship it.
```

手动抽查捕获明显失败但遗漏边缘情况。没有持久的评估套件，提示修改会静默回退之前能用的场景。

### 生效原因 -- 评估套件捕获手动测试遗漏的回退。多 Agent 架构（executor、grader、analyzer）防止自我评估偏差。

---

<a id="pattern-120-non-anthropic-provider-guard"></a>
## Pattern 120: Non-Anthropic Provider Guard

**分类:** Safety / Activation Scope
**来源:** `skills/claude-api/SKILL.md`
**出现率:** 1 个 skill

### 概念

执行前检查用户代码是否使用了其他提供商（OpenAI、Google 等）。如果是，立即退出 -- 不尝试适配。

### 正面示例：提供商检测 + 提前退出

```markdown
## Non-Anthropic Detection (BEFORE anything else)

If the code imports or uses any of these, STOP and say
"This skill is for the Anthropic/Claude API. Your code uses {provider}.":

- `import openai` / `from openai`
- `import { OpenAI }` / `@google/generative-ai`
- `langchain` with non-Anthropic models
- Any `OPENAI_API_KEY` references

Do NOT try to adapt the code to work with Claude.
Do NOT suggest replacing the provider.
Just inform and stop.
```

### 反面示例：无提供商检查

```markdown
## Getting Started
Help the user write code that calls the Claude API.
```

不检测提供商，模型可能尝试将 OpenAI 代码适配到 Anthropic SDK，产出两个 API 都用不对的混合代码。

### 生效原因 -- 带有自动检测，Agent 无需依赖用户知道 Skill 何时适用。提前退出防止模型尝试不适合的转换，避免浪费 token 并产出错误输出。

---

## 跨领域观察

### 各仓库的模式分布

| 模式类别 | Anthropic `skills` | 社区 `awesome` | 两者都有 |
|---------|--------------------|--------------------|------|
| Progressive Disclosure | 强（多个 skill） | 少见 | - |
| Clarifying Questions | 中等 | 非常强（~40%） | 是 |
| Populated Examples | 中等 | 非常强（~35%） | 是 |
| Anti-Slop Guidelines | 存在 | 缺失 | - |
| Helper Scripts | 存在 | 缺失 | - |
| SaaS Integration | 缺失 | 832 个 skill | - |
| Algorithm Internals | 缺失 | 存在 | - |
| Eval-Driven Improvement | 深度（skill-creator） | 缺失 | - |

### 质量梯度

Anthropic 官方 skill 展现出显著更成熟的提示工程：
1. **多层上下文加载**（Progressive Disclosure）
2. **子 Agent 评估架构**（Blind A/B, Reader Testing）
3. **反模式命名**（Anti-Slop）
4. **领域特定安全规则**（Never-Hardcode Financial）

社区 skill 偏好更简单但广泛适用的模式：
1. **Clarifying Questions**（通用）
2. **Populated Examples**（通用）
3. **Step-by-step Instructions**（7-10 个编号步骤）
4. **Use Case Catalogs**（何时使用 / 示例工作流）

### 设计哲学差异

| 方面 | Anthropic 官方 | 社区 |
|------|---------------|------|
| 调用方式 | 隐式（描述触发） | 显式（用户须知道 skill 存在） |
| 上下文管理 | 渐进式呈现 | 全部内联 |
| 质量保证 | 子 Agent 验证 | 自检或无 |
| 错误处理 | 降级路径 | 很少提及 |
| 捆绑资源 | 脚本、schema、字体 | 极少 |
| Skill 大小 | 50-600 行 | 30-500 行 |
