# 类别 5：Agent 编排

多个 agent 如何协调 — 拓扑结构、技能组合、意图路由、工具映射和共识机制。

**相关基础技术：** Cognitive Offloading, Token-Action Binding（见 [prompt-engineering-for-skills.md](/prompt-context-patterns/catalog/techniques/token-level-techniques)）

---

## Pattern 18: Multi-Agent Orchestration / Agent Topologies

**出现频率：** ~2% 的技能（857 个引用 agent 的文件中仅 30-50 个是真正的编排）
**相关模式：** [Skill Composition](#pattern-19), [Deduplication/Consensus](#pattern-22), [Tool Routing Tables](#pattern-21)

**定义：** 定义多个 AI agent 如何协调 — 生成子 agent、agent 间路由、建立通信协议、合并结果。拓扑定义了 agent 图的形状。

**适用场景：**
- 单个 agent 无法产生可靠结果时（使用跨模型共识）
- 任务有独立维度可从并行分析受益时
- 对抗性验证能提高输出质量时（一个 agent 挑战另一个）
- 规模要求（并行审查 100+ 文件）时

### 正面示例
```markdown
## Architecture Overview

This skill uses a **multi-agent ensemble architecture** that combines cross-model
diversity (Tier 3) with adversarial validation (Tier 2):

Orchestrator (this agent — Opus)
  |
  +- Phase 0: Setup & Context Gathering
  |
  +- Phase 1: Spawn 8 parallel dimension pipelines
  |    |
  |    +- Per dimension (x8 in parallel):
  |         +- 2 Context Builders (Sonnet + Gemini) — gather relevant code, union merge
  |         +- 3 Analyzers in parallel:
  |         |    +- Model A: Claude Opus
  |         |    +- Model B: GPT-5.2-Codex
  |         |    +- Model C: Gemini Pro
  |         +- Validator (Opus) — adversarial consensus judge
  |
  +- Phase 2: Synthesis Ensemble
  |    +- 3 Synthesizers in parallel (Opus, GPT-5.2-Codex, Gemini Pro)
  |    +- Synthesizer Validator (Opus) — consensus merge & dedup
  |
  +- Phase 3: Report Writer (Opus) — final Markdown report
  |
  +- Phase 4: Action Mode (if mode="act") — fix, commit, push

**Total agents per review: ~55**

### Consensus Scoring

| Agreement | Action |
|-----------|--------|
| 3/3 models | `[high]` confidence — almost certainly real |
| 2/3 models | Accept — verify specifics, `[medium]`+ confidence |
| 1/3 models | Adversarially challenge — keep only if it survives scrutiny |
```

**为何有效：** 拓扑可视化为树形图 — 编排器能看到 agent 图的完整形状。每个节点指定运行的模型，创造跨模型多样性（Claude、GPT、Gemini）。共识评分表给出确定性的分歧合并规则。Agent 数量已声明，编排器知道预期规模。分阶段结构防止 agent 冲突 — 上下文构建在分析开始前完成。

### 反面示例

```markdown
Use multiple agents to review the code. Have them analyze different aspects and then
combine the results. Make sure they don't duplicate findings.
```

**为何失败：** 没有定义拓扑 — 模型不知道多少 agent、什么角色、什么模型。"Different aspects" 没有枚举维度。"Combine the results" 没有合并策略。"Don't duplicate" 没有去重算法。编排器将生成任意数量的 agent，范围重叠且无共识机制。每次运行产生不同的 agent 图。

---

## Pattern 19: Skill Composition / Cross-Skill Invocation

**出现频率：** ~4% 的技能（100+ 文件）
**相关模式：** [Multi-Agent Orchestration](#pattern-18), [Intent Classification](#pattern-20), [Activation Scope](#pattern-13)

**定义：** 一个技能显式调用或委托给另一个技能，创建工作流管线，每个技能处理更大任务的特定阶段。

**适用场景：**
- 功能已存在于另一个技能中（DRY 原则）时
- 工作流的不同阶段由不同技能专门处理时
- 需要一个路由技能分发到专家技能时
- 将不同插件的技能组合成管线时

### 正面示例
```markdown
## Execution Workflow

### PHASE 1: THREAT MODELING (Automatic)

**Action:** Invoke the `security-threat-modeler` skill from ai-starter-pack plugin

**Instructions:**
1. Change working directory to the repository path provided
2. Invoke the skill: `security-threat-modeler`
3. The ai-starter-pack's security-threat-modeler will:
   - Analyze codebase architecture
   - Generate comprehensive STRIDE threat model
   - Identify trust boundaries and data flows
   - Output threat model to `{repo_name}_Threats.csv`
4. Read the generated threat model CSV into memory for Phase 2

**Expected Output from security-threat-modeler:**
- Threat model CSV file with all identified threats
- Each threat includes: Title, Category, Priority, Description, Affected Component,
  Mitigation, CVSS Score, Location

**Important:** DO NOT duplicate the security-threat-modeler functionality. Always invoke
the existing skill from ai-starter-pack.
```

**为何有效：** 委托明确 — 命名了确切的技能和插件。预期输出已文档化，本技能知道消费什么。"DO NOT duplicate" 指令防止模型内联重新实现威胁建模。工作目录设置确保被调用技能有正确上下文。输出文件路径已指定，Phase 2 知道从哪里读取。

### 反面示例

```markdown
First do threat modeling, then do security review. You might want to use some
existing tools for the threat modeling part.
```

**为何失败：** "Might want to use existing tools" 不是委托 — 模型会尝试自己做威胁建模。没有技能名、插件名、预期输出格式。模型要么（差劲地）重新实现威胁建模，要么跳过。没有输出交接机制意味着安全审查阶段不知道威胁建模阶段有什么数据可用。

---

## Pattern 20: Intent Classification / Smart Routing

**出现频率：** ~6% 的技能（100-150 文件）
**相关模式：** [Workflow Mode Branching](#pattern-3), [Activation Scope](#pattern-13), [$ARGUMENTS Pattern](#pattern-4)

**定义：** 分析用户输入并根据关键词匹配、URL 解析、内容分析或语言检测路由到适当的子技能、工作流模式或管线。

**适用场景：**
- 单一技能入口服务多个子工作流时
- 路由取决于分析输入（不仅仅是标志）时
- 不同编程语言需要不同分析管线时
- 技能需要解析 URL 来确定目标平台（ADO vs GitHub）时

### 正面示例
```markdown
# Enhanced SAST Security Review V2 Command

This command auto-detects the project's primary language and routes to the appropriate
workflow:

- **C# projects** → Agent-driven taint analysis with CodeQL verification + critic re-triage
- **PowerShell projects** → Parallel security analysis with critic re-triage

## Phase 0: Language Detection

**Goal**: Determine the project's primary language to route to the correct pipeline

**Actions**:
1. Invoke `detect-project-language` skill
2. Read `.shield_security/detect_project_language/language_detection.json`
3. If `primaryLanguage == "csharp"` → proceed to **C# Pipeline**
4. If `primaryLanguage == "powershell"` → proceed to **PowerShell Pipeline**
5. If `primaryLanguage == "unknown"` → stop and report to user
```

**为何有效：** 路由是确定性的 — 读取 JSON 文件、检查字段、分支到命名管线。"unknown" 情况已处理（停止并报告，不是猜测）。路由发生在 Phase 0，在任何分析开始前，不浪费工作。每个管线是完整指定的工作流（C# 有 8 个阶段，PowerShell 有自己的）。检测委托给专门技能而非使用启发式。

### 反面示例

```markdown
Figure out what kind of project this is and analyze it appropriately.
Use the right tools for the language.
```

**为何失败：** "Figure out what kind" 要求模型从头实现语言检测。"Appropriately" 未按语言定义。没有分支结构意味着模型可能对 PowerShell 代码应用 C# 分析。未识别语言没有处理意味着模型要么猜测，要么静默产生垃圾结果。

---

## Pattern 21: Tool Routing Tables

**出现频率：** ~16% 的技能（358 文件引用 `allowed-tools`；200+ 有内部路由）
**相关模式：** [Negative Constraints](#pattern-6), [YAML Frontmatter](#pattern-1), [Multi-Agent Orchestration](#pattern-18)

**定义：** 将任务映射到特定工具的查找表，带有显式的 "NOT these" 列列出禁止的替代方案。防止 agent 对给定操作使用错误工具。

**适用场景：**
- 多个工具表面上能处理相同任务但可靠性不同时
- 通用 Q&A 工具与精确查询工具并存时
- 过去的失败由使用错误工具导致时
- 技能与多个 MCP 服务器交互时

### 正面示例
```markdown
## Tool Routing — MANDATORY

Use ONLY the tools listed below for each task. Do NOT use `mcp__workiq__ask_work_iq`,
`es_chat`, or any general-purpose Q&A tool as a substitute — they return unreliable,
unstructured results.

| Task | Tool(s) | NOT these |
|------|---------|-----------|
| **Search code by keyword** | `mcp__bluebird__search_file_content` | workiq, es_chat, WebSearch |
| **Read source files** | `mcp__bluebird__get_file_content` | workiq |
| **Find files by path** | `mcp__bluebird__search_file_paths` | workiq |
| **Search commits** | `mcp__ado__repo_search_commits` | workiq |
| **Fetch PRs** | `mcp__ado__repo_list_pull_requests_by_repo_or_project` | workiq |
| **Fetch bug data** | `mcp__ado__wit_get_work_item` | workiq |
| **Download attachments** | `Bash` (curl with ADO bearer token) | workiq |
| **Analyze crash dumps** | `Bash` (CDB — see Phase 1c) | workiq |
| **View screenshots** | `Read` (supports PNG, JPG) | workiq |
```

**为何有效：** 三列表（Task / Tool / NOT these）使路由毫不含糊。"NOT these" 列显式阻止模型使用返回不可靠结果的通用工具（workiq、es_chat）的倾向。理由在前面陈述（"unreliable, unstructured results"）。工具名使用精确 MCP 标识符而非描述。连不显而易见的工具也包含在内（截图 → `Read`，crash dumps → `Bash` with CDB）。

### 反面示例

```markdown
Use the appropriate tools to investigate the bug. You have access to code search,
work item tracking, and various other tools. Pick the best one for each task.
```

**为何失败：** "Appropriate" 和 "best" 要求模型评估工具质量 — 它会默认使用熟悉的通用工具（workiq），即使精确工具存在。没有禁止工具意味着模型自由使用不可靠的 Q&A 端点进行结构化查询。没有映射意味着模型可能用工作项搜索工具搜索代码，或用代码搜索工具查找 PR。

---

## Pattern 22: Deduplication / Consensus Algorithms

**出现频率：** ~1% 的技能（20-30 文件）
**相关模式：** [Multi-Agent Orchestration](#pattern-18), [Scoring Rubrics](#pattern-27)

**定义：** 定义显式算法用于跨多个 agent 或分析轮次去重发现，通常使用带定义阈值的加权相似度评分。

**适用场景：**
- 多 agent 审查中 agent 可能报告相同问题时
- 跨批次分析中发现需要合并时
- 需要与现有评论/发现对比以避免重复时
- 任何产出需要去重的发现的工作流

### 正面示例
```markdown
### Dedup Algorithm (Multi-Signal Fingerprinting)

Used wherever two findings are compared. Compute a match score:

| Signal | Weight | Match Criteria |
|--------|--------|---------------|
| File + Line proximity | 0.35 | Same file AND line within +/-5 lines |
| Code symbol reference | 0.25 | Both reference the same function/variable/class name |
| Issue category | 0.25 | Both address the same concern type (null-handling, security, perf) |
| Text similarity | 0.15 | Jaccard similarity on significant words (exclude stop words) |

**Thresholds (consistent everywhere):**
- **>= 0.7:** DUPLICATE — skip / do not post
- **0.5 – 0.7:** RELATED — reply to existing thread, or merge findings
- **< 0.5:** NEW — distinct finding

**Precedence:** Micy self-dedup (exact file+line within +/-3 lines + same severity + same
category) is a **HARD DUPLICATE** regardless of text similarity score. This deterministic
check runs FIRST, before the weighted scoring.

**Dedup execution order** (deterministic):
1. **Cross-batch dedup** (Step 5.3) — after all batches, MERGE duplicates across batches
2. **Cross-agent dedup** (Step 6) — MERGE duplicates across the 5 agents
3. **Vs-existing-comments dedup** (Step 6.75) — classify against existing PR threads
```

**为何有效：** 算法完全指定：信号、权重、匹配标准、阈值和执行顺序。模型可以确定性地计算分数 — 无需"靠判断"。Hard duplicate 优先级防止加权算法保留明显重复。执行顺序防止顺序依赖结果（先跨批次再跨 agent 再对比现有）。阈值含义已定义（skip vs merge vs keep）。

### 反面示例

```markdown
Remove duplicate findings. If two agents report the same issue, only include it once.
Make sure related findings are grouped together.
```

**为何失败：** "Same issue" 未定义 — 同文件？同类别？同措辞？"Related" 没有阈值。没有算法意味着每次运行去重方式不同。有些运行会激进合并不同发现；其他则保留近似重复。没有执行顺序意味着去重结果取决于哪个 agent 的发现先被处理。没有区分 "duplicate"（跳过）和 "related"（合并）。
