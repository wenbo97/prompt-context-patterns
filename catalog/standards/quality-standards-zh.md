# 提示词工程质量标准

> **提示词编写技巧、反模式和风格指南的唯一权威来源（SSOT）。**
> 引用方：`commands/dev-prompt.md`、`commands/dev-prompt-review.md`。
> **示例：** 在编写或评审任何提示词之前，先阅读 @../prompt-examples/template.md 中详细的好/坏对比逐行分析。

这些标准将研究验证的提示词工程技巧落地到本插件的自主迁移 Agent。每条原则都包含 **为什么**（利用或规避的模型行为）、**何时用**（适用的插件场景）和 **怎么用**（具体模式）。

> **参考资料（编写或评审提示词之前建议深入阅读）：**
>
> | 来源 | 学什么 |
> |------|--------|
> | [Claude Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) | **主要参考。** 清晰原则、XML 结构、few-shot 设计、角色提示、长上下文排序、自适应思维、子 Agent 编排、并行工具调用，以及 Claude 4.6 特定迁移指导（减少反懒惰提示、避免过触发）。 |
> | [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices) | CLAUDE.md 设计（包含/排除什么、简洁规则）、验证优先开发、上下文窗口管理（首要约束）、子 Agent 委托实现上下文隔离、会话管理和并行扩展。 |
> | [Prompt Engineering Guide](https://www.promptingguide.ai/techniques) | 18 种技术目录。与本插件最相关的：few-shot、chain-of-thought、prompt chaining、ReAct（推理+行动循环）、reflexion（从过去失败中学习）、self-consistency（多推理路径）。 |
> | [Claude Code System Prompts](https://github.com/Piebald-AI/claude-code-system-prompts) | 110+ 模块化微提示词（每个 16-102 token）、对抗性验证专家模式、两层安全（评估器 + 策略引擎）、fork 安全委托（worker 不能再派生 worker）、按 Agent 角色条件组装提示词。 |
> | [Claude Code Sub-Agents](https://github.com/dl-ezo/claude-code-sub-agents) | 触发丰富的描述（每个 Agent 3-5 个触发场景）、窄范围单关注点 Agent、显式输出契约、主协调器模式（编排但不做专业工作）。 |
> | [Anthropic Prompt Engineering Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) | Few-shot 范例选择、chain-of-thought 激发、结构化输出强制、通过锚定减少幻觉。 |

---

## 原则 1：清晰直接 — 消除推断

**为什么有效：** Claude 响应显式指令。模糊提示迫使模型推断意图，导致不同运行间行为不一致。Anthropic 的黄金法则："把你的提示词给一个对任务了解很少的同事看，让他照着做。如果他会困惑，Claude 也会。"

**何时用：** 每个文件中的每条指令。

**怎么用：**

| 模式 | 不好（Agent 推断） | 好（Agent 执行） |
|------|-------------------|-----------------|
| 祈使语气 | "你可能想检查一下 csproj" | "读取目标 csproj。如果 `<TargetFrameworks>` 不存在，停止 — 这是一个旧式 CoreXT 项目。" |
| 精确格式 | "添加包" | "在 .NET Core 条件 ItemGroup (`!= '{conditionTFM}'`) 中添加 `<PackageReference Include=\"System.Configuration.ConfigurationManager\" />`。" |
| 显式回退 | "如果构建失败，处理它" | "如果 `build` 返回 `Build FAILED`，从输出中提取所有 CS*/MSB*/NU* 错误码。如果没找到错误码，分类为 `infra_error`。" |
| 上下文/动机 | "不要用 git amend" | "不要用 git amend — 构建修复循环可能失败并重试，amend 会破坏上一次提交的安全状态。" |

**Claude 4.6 注意事项：** Claude 4.6 对系统提示词的响应比之前的模型更灵敏。如果你的提示词是为了减少工具或技能的触发不足而设计的，请调低激进程度。之前可能写 "CRITICAL: You MUST use this tool when..." 的地方，用普通提示即可："Use this tool when..."

---

## 原则 2：Few-Shot 示例 — 展示，不要描述

**为什么有效：** 示例是引导输出格式、语气和结构最可靠的方式。3-5 个精心制作的示例能显著提升准确性和一致性。用 `<example>` 标签包裹示例，让 Claude 区分示例和指令。

**何时用：** 关键操作 — 带特定参数的工具调用、输出 JSON 格式、复杂分类决策、csproj XML 转换。

**如何构建示例：**

1. **相关** — 用真实迁移场景（非假设）。使用本插件中的真实包名、真实 csproj 结构、真实错误消息。
2. **多样** — 覆盖正常路径和至少一个边界情况。如果决策有 3 个分支，展示 2-3 个覆盖不同分支的示例。
3. **结构化** — 展示确切的 XML/JSON/命令，不是文字描述。

**好的 few-shot 示例（NU1701 处理）：**

```xml
<examples>
<example>
<scenario>OrchestrationSDK triggers NU1701 — no REPLACE mapping exists</scenario>
<before>
<ItemGroup>
  <PackageReference Include="OrchestrationSDK" />
</ItemGroup>
</before>
<after>
<ItemGroup Condition="'$(TargetFramework)' == 'net472'">
  <PackageReference Include="OrchestrationSDK" />
</ItemGroup>
<ItemGroup Condition="'$(TargetFramework)' != 'net472'">
  <!-- NU1701: OrchestrationSDK targets net472 only; suppress fallback warning -->
  <PackageReference Include="OrchestrationSDK" NoWarn="NU1701" PrivateAssets="all" />
</ItemGroup>
</after>
</example>
</examples>
```

**目标：** 每个示例 100-300 token。展示确切的输入/输出，不是抽象模式。

---

## 原则 3：思维链 — 结构化多步决策

**为什么有效：** 用散文描述的多步决策不可靠 — Agent 可能跳过步骤或改变顺序。带有每个决策点显式 if/else 的编号序列能强制顺序执行。

**何时用：** 错误分类、依赖解析、Tier 选择、状态路由。

**怎么用：** 结构化为编号步骤，每步有具体检查和显式分支：

```
1. Read the error code from build output.
2. If error code matches SUPPRESSIBLE (PackageReference) list per @../skills/error-handling-rules.md → add NoWarn at PackageReference level.
3. If error code matches SUPPRESSIBLE (PropertyGroup) list per @../skills/error-handling-rules.md → add <NoWarn> in .NET Core PropertyGroup.
4. If error code is CS* (except CS8981) → classify as MUST FIX. Proceed to Tier selection.
5. Otherwise → log "Unknown error code: {code}" and continue to next error.
```

**绝不：** "分类错误并应用适当的修复。"（Agent 必须推断分类逻辑）

---

## 原则 4：Prompt Chaining — 显式阶段契约

**为什么有效：** 每个阶段产生输出供下一阶段消费。未文档化的交接导致静默的字段名不匹配。在每个阶段的末尾文档化输出 schema，在下一阶段的开头文档化输入表。

**何时用：** 阶段转换（0→1→2→3→4）、Agent 边界（orchestrator→dotnet-migrator→build-repair-agent→ado-agent）、技能序列交接。

**怎么用：**

- 每个阶段/Agent/技能以 **Output** 部分结尾：字段名、类型、可能的值
- 每个阶段/Agent/技能以 **Input** 部分开头：参数名、类型、必需/可选、来源（哪个阶段/Agent 产生的）
- 使用 `rules/phase-data-contract.md` 中定义的契约 — 不要发明临时变量名

**自测：** 对每个 Output 字段，在下游消费者中搜索。如果消费者没有引用那个确切的字段名，契约就是断裂的。

---

## 原则 5：锚定 — 强制读取，不要依赖记忆

**为什么有效：** Claude 的上下文窗口随长度增加而退化。"记住"对话早期规则的 Agent 可能记错。在决策点强制读取权威文件能确保准确性。

**何时用：** 错误解决、包映射、依赖分类、状态路由。

**怎么用：**

- "在向任何 PackageReference 添加 NoWarn 之前，先读取 @../rules/nu1701-handling.md。"
- "在搜索 ADO 之前，先在 @../issue-and-solution/runtime-solution/issue-map-index.md 中检查此错误码。"
- 内联关键值并引用 SSOT：`NoWarn="NU1701" PrivateAssets="all" (per @nu1701-handling.md)`

**反模式：** "详见 @file"，但不内联关键值。Agent 需要跟踪 2+ 次跳转，可能跳过或即兴发挥。始终在使用点内联操作，然后引用来源。

---

## 原则 6：长上下文排序 — 数据在前，指令在后

**为什么有效：** Anthropic 测试显示，查询放在长上下文提示词末尾能将响应质量提升最多 30%。对本插件，将参考数据（包映射、项目映射、错误表）放在顶部，决策逻辑放在底部，能产生更准确的分类。

**何时用：** 加载大型参考文件的技能（package-map.md、project-map-list.md、issue-solutions.md）。

**怎么用：**

1. 在文件早期通过 `@` 引用加载参考数据
2. 在数据之后放置决策逻辑（编号步骤）
3. 对超过 200 行的技能：将数据拆分到独立文件，通过 `@` 引用组合

---

## 原则 7：自验证 — 每次检查都需要一条命令

**为什么有效：** 没有可执行的验证，Agent 会合理化成功："代码看起来正确"不是检查 — 是跳过。Claude Code 最佳实践："当 Claude 能验证自己的工作时，表现会显著提升。"

**何时用：** 每次构建后、每次 git 操作后、每次创建 PR 后、每次修改 csproj 后。

**怎么用：**

每个 `<self-check>` 项必须指定：
1. 要运行的**命令**（或调用的工具）
2. 构成 PASS 的**预期输出**
3. 输出不匹配时的**失败操作**

```
<self-check>
- [ ] Run `git status --porcelain` with pathspec from @git-exclusions.md — output shows modified files → PASS. Empty → exit with Aborted_NoChanges.
- [ ] Read the target csproj — contains `<TargetFrameworks>` with both `{previousTFM}` and `{netCoreTargets}` → PASS. Missing either → FAIL, stop and report.
</self-check>
```

**绝不：** "- [ ] Verify the csproj is valid"（没有命令、没有预期输出 — Agent 会跳过）

---

## 原则 8：角色提示 — 一句话，放在最前面

**为什么有效：** 第一句话中的角色声明能聚焦 Claude 的行为和语气。即使一句话也有效果（参见 Anthropic 文档）。

**何时用：** Agent 定义（frontmatter + 开场白）。技能不需要（技能是工具，不是人设）。

**怎么用：** "You are a {role} that {primary responsibility}." 保持一句话。角色为后续所有指令定调。

```
You are a diagnostic build engineer responsible for analyzing .NET build failures and applying fixes within 7 attempts.
```

**绝不：** 多段背景故事或激励文字。角色是框架设定，不是人物传记。

---

## 原则 9：Fork 安全委托 — 传递一切，不做假设

**为什么有效：** 子 Agent 和 fork 出的 Agent 以零父上下文启动。Claude Code 的系统提示词执行严格的委托层级：Main Agent → Coordinator → Worker（终端，不能再 fork）。Worker 以显式参数接收所有必需值。

**何时用：** 每个 orchestrator→agent 边界（Phase 1 → dotnet-migrator, Phase 3 → build-repair-agent, Phase 4 → ado-agent）。

**怎么用：**

- 将所有必需值作为显式参数传递 — 不要引用"Phase 0 的值"而不传递它
- 在使用点展示确切的工具调用和实际参数值
- "简短、命令式的提示词产生浅层、通用的工作" — 用上下文、约束和预期输出格式充分简报子 Agent

**测试：** 移除父对话上下文。子 Agent 能否仅凭其 Input 参数正确执行？如果不能，缺少了某个参数。

---

## 原则 10：行为防护栏 — 短小、分级、否定+肯定

**为什么有效：** Claude Code 内部的防护栏平均每条 47 token — 精确且有针对性。长散文段落在上下文压力下会被略读。表格和列表能被可靠解析。

**何时用：** 约束 Agent 范围、防止常见错误、执行"不伤害"规则。

**怎么用：**

1. 在说 Agent 必须做什么的同时，说明不能做什么
2. 每条防护栏控制在 30-60 token
3. 按严重性分级：MUST > SHOULD > PREFER（参见 `rules/never-always-rules.md`）
4. 用表格或列表，每行一条规则

**Claude 4.6 注意事项：** Claude 4.6 有过度工程化的倾向 — 创建额外文件、添加不必要的抽象。用显式范围约束应对："Only make changes that are directly requested. Do not add features, refactor code, or make 'improvements' beyond what was asked."

---

## 原则 11：自适应子 Agent 编排

**为什么有效：** Claude 4.6 的原生子 Agent 编排能力显著提升 — 它会主动委托工作而无需显式指令。但它可能在一个简单的 grep/read 更快的情况下派生子 Agent。

**何时用：** 编写编排器级提示词（CLAUDE.md、Agent 定义）。

**怎么用：**

- 对真正并行的任务，让 Claude 自然编排
- 添加显式指导防止过度委托："For simple file reads, single-file edits, or sequential operations, work directly rather than delegating to subagents."
- 为上下文隔离使用子 Agent（构建调查、代码库探索）— 保持主对话清洁
- 每个子 Agent 应该只负责一件事（参见 Claude Code Sub-Agents 模式）

---

## 原则 12：ReAct 模式 — 推理然后行动然后观察

**为什么有效：** build-repair-agent 已经隐式使用了这个模式：思考错误 → 应用修复 → 观察构建结果 → 重复。显式化可以防止 Agent 不做诊断就应用修复或跳过观察。

**何时用：** 构建修复循环、错误调查、搜索优先解决策略。

**怎么用：**

```
For each build error:
1. REASON: What is the root cause? Check issue-map-index.md, then ADO search.
2. ACT: Apply the specific fix (Tier 1/2/3/4 per code-fix-tiers.md).
3. OBSERVE: Rebuild. Parse the output for the same error code.
4. If error persists with same code → the fix was wrong. Try a different approach.
5. If error is gone but new errors appeared → continue to next error.
```

---

## 原则 13：Reflexion — 从历史会话失败中学习

**为什么有效：** `issue-map-index.md` 缓存本身就是一个 reflexion 循环 — 它存储来自以前迁移会话的修复方案，让未来的会话不必重复相同的调查。显式化这个模式能确保新的修复始终被记录。

**何时用：** Phase 3 构建修复 — 在 ADO 搜索前检查缓存、在循环完成后记录新修复。

**怎么用：**

- search-first-strategy.md 中的 Step 0：先检查缓存
- 构建循环完成后：按 issue-format-guide.md 记录新的 error/fix 对
- 用新条目取代无效的缓存修复（参见 issue-format-guide.md Rule 4）

---

## 反模式 — 导致 Agent 失败的原因

| 反模式 | 利用的模型行为 | 本插件中的具体失败 | 修复 |
|--------|---------------|-------------------|------|
| **模糊祈使句**（"考虑..."、"试试..."、"你可能..."） | Claude 将模棱两可的措辞视为可选；上下文压力下跳过 | Agent 跳过 NU1701 抑制，因为指令说"考虑添加 NoWarn" | 直接命令："Add `NoWarn=\"NU1701\"` to the PackageReference in the .NET Core group." |
| **缺少 else/otherwise** | 没有指定分支时 Claude 会发明回退行为 | Agent 遇到未知错误码，因为没有"otherwise"子句而发明修复 | 每个 `if/when` 必须有显式 `else/otherwise`："Otherwise, log the error and continue." |
| **未文档化的输出 schema** | 下游消费者猜测字段名和类型；静默不匹配 | Phase 3 返回 `buildStatus` 但 Phase 4 期望 `LocalBuildStatus` — 字段静默为 null | 每个 agent/skill 末尾有正式的 Output 表，包含字段名、类型、可能的值。 |
| **跳转引用不内联值**（"详见 @file"） | Agent 需要跟踪 2+ 次跳转；上下文压力下可能跳过 | Agent 跳过读取 nu1701-handling.md 并即兴将 NU1701 放在 common group | 在使用点内联关键值并引用来源：`NoWarn="NU1701" PrivateAssets="all" (per @nu1701-handling.md)` |
| **上下文继承假设** | Fork 出的 Agent 以零父上下文启动 | Build-repair-agent 不知道 `netCoreTargets` 因为 orchestrator 假设它从 Phase 0 继承了 | 将所有值作为显式 Input 参数传递。测试：Agent 能否仅凭 Input 表工作？ |
| **单体提示词（>300 行）** | Agent 优先处理早期内容，略读或忽略后面部分（上下文稀释） | 400 行技能文件后三分之一的规则被不一致地应用 | 拆分为通过 `@` 引用组合的专注文件。一个文件 = 一个关注点。目标：每文件 <200 行。 |
| **工具名但没参数**（"use search_code"） | Agent 猜测参数；使用错误的项目名或缺少过滤器 | Agent 用 `project: "ControlPlane"` 而非 `project: "O365 Core"` 调用 `search_code` | 展示确切的工具调用：`search_code(searchText: "WorkflowSDK AND TargetFrameworks ext:csproj", project: ["O365 Core"], repository: ["ControlPlane"], top: 15)` |
| **散文段落防护栏** | Agent 从表格/列表中可靠提取规则；会略读散文 | Agent 错过了埋在段落中的"不要添加包到 common group"规则 | 每行一条规则的表格或列表。每条 30-60 token。 |
| **跳过验证**（"代码看起来正确"） | Agent 不运行检查就合理化成功 | Agent 声称 csproj 有效但没解析它 — 损坏的 XML 传播到 PR | 每个 self-check：命令 + 预期输出 + 失败操作。没有"验证它能工作"而没有命令。 |
| **过度提示要求彻底**（Claude 4.6 特定） | Claude 4.6 比前代显著更主动；反懒惰提示导致过触发 | Agent 在 Phase 0 分析中读取 50+ 文件因为提示词说"要彻底" | 移除 "If in doubt, use [tool]" 表述。将笼统的 "Default to using [tool]" 替换为 "Use [tool] when it would enhance your understanding of the problem." |

---

## 可靠性冗余

某些指令受益于跨文件的**有意重复**，以确保 Agent 即使在 SSOT 文件未加载到上下文中时也能遵循。这与 SSOT 违规（**规则**的无意重复导致分歧）不同。

**应该重复的内容（使用点的值）：**
- 关键格式字符串（PR 标题、提交消息）— 内联确切格式并引用 SSOT
- 工具调用模式（哪个工具、哪些参数）— 在使用点展示确切调用
- 错误处理默认值（"记录并继续"、"停止并报告"）— 在每个决策点重述

**如何标记有意冗余：** 在内联值后添加 `(per @SSOT-file)` 归属标注。这向审阅者表明重复是有意的，如果它们分歧了，哪个文件具有权威性。

---

## 提示词风格指南

### 结构规则

| 规则 | 为什么（模型行为） | 怎么做 |
|------|-------------------|--------|
| **一个文件一个关注点** | 多关注点文件将无关内容强制放入上下文；Agent 按需加载文件 | `rules/nu1701-handling.md` 只处理 NU1701 — 不包含所有包警告 |
| **操作在前，上下文在后** | Claude 提取第一个祈使句，可能略读背景。"为什么"放在"做什么"前面会埋没指令。 | "Add `NoWarn=\"NU1701\"` to the PackageReference. This suppresses..." — 不要反过来 |
| **决策用表格不用散文** | 表格按行解析可靠；嵌入条件的散文段落在上下文压力下脆弱 | 状态处理器、错误分类、包映射 — 都使用表格。继续这个模式。 |
| **序列用编号步骤** | Claude 遵循编号序列的可靠性远高于段落内嵌入的序列 | "1. Read the csproj. 2. Find the ItemGroup. 3. Add the PackageReference." |
| **无序约束用列表符号** | 编号列表暗示序列；列表符号暗示"所有这些，任意顺序" | 防护栏、排除列表、"任一"条件使用列表符号 |
| **长数据在前，查询在后** | 查询放在长上下文提示词末尾能将响应质量提升最多 30%（Anthropic 测试） | 包映射、项目映射、错误表放顶部；决策逻辑放后面 |

### 提示词大小规范

| 文件类型 | 目标 | 硬性上限 | 超限处理 |
|----------|------|----------|----------|
| Agent 定义 (`agents/*.md`) | ≤200 行 | 260 行 | 将参考内容提取到 `rules/` 或技能资源文件；从 Agent 中 `@` 引用 |
| 命令定义 (`commands/*.md`) | ≤200 行 | 260 行 | 将参考内容提取到 `rules/` 或 `skills/` 资源文件；从命令中 `@` 引用 |
| 技能定义 (`skills/*/SKILL.md`) | ≤200 行 | 300 行 | 将数据表、示例或映射提取到技能文件夹内的兄弟资源文件；从 SKILL.md 中 `@` 引用 |
| 规则文件 (`rules/*.md`) | ≤200 行 | 300 行 | 按子主题拆分为专注文件；从父文件 `@` 引用 |

**提取模式：** 当文件超过限制时，识别最大的自包含部分（参考表、示例、质量标准、输出模板）。在自然归属目录创建新文件（`rules/` 用于共享内容，技能文件夹用于技能特定数据）。用简洁的 `@` 引用（1-3 行）替换该部分，说明引用文件包含什么以及何时读取。

### Token 经济

Claude Code 的行为防护栏平均每条 **47 token**。本插件应遵循相同的经济原则：

| 组件 | 目标长度 | 为什么 |
|------|----------|--------|
| 单条防护栏规则 | 30-60 token | 足够精确以消除歧义，足够短以在上下文压力下存活 |
| 技能描述（frontmatter） | 50-150 token | 必须包含触发短语、when-NOT-to-use 和一个使用示例 |
| Input/Output 参数行 | 每行 20-40 token | 名称、类型、必需、来源 — 不要散文 |
| Self-check 项 | 20-50 token | 命令 + 预期输出 + 失败操作 |
| Few-shot 示例 | 每个 100-300 token | 确切的输入/输出，不是抽象模式 |
| Agent 角色声明 | 15-30 token | 一句话。"You are a {role} that {responsibility}." |

### Agent 定义模式

```
1. Role statement (1 sentence — "You are a [role] that [primary responsibility].")
2. Context block (environment variables, @references, configuration)
3. Input block (parameters table — name, type, required, source)
4. Constraints block (guardrails as bullets/table, tiered MUST > SHOULD > PREFER)
5. Steps block (numbered instructions, decision tables with if/else at every branch)
6. Self-check block (postcondition checklist — command + expected output per item)
7. Output block (field table — name, type, possible values)
```

### 技能定义模式

```
1. Frontmatter (name, description with 3-5 trigger phrases and when-NOT-to-use)
2. Purpose (1-2 sentences — what this skill does and when it's a NO-OP)
3. Input parameters table (name, type, required/optional, source)
4. Steps (numbered, with explicit if/else at each decision point)
5. Examples (1-2 before/after — happy path + one edge case, using real package/project names)
6. Verification (command + expected output + failure action)
7. Output table (field name, type, possible values)
```

### 写作检查清单

在最终完成任何提示词文件之前，验证以下最低质量标准：

- [ ] 每个 `if/when` 都有显式的 `else/otherwise` — 无悬挂条件
- [ ] 每个 agent/skill 都有正式的 Input 和 Output 表 — 不靠猜测
- [ ] 每个关键操作至少有一个用真实值的 few-shot 示例 — 不是抽象的
- [ ] 每个多步决策使用编号步骤 — 不是散文段落
- [ ] 每条防护栏 ≤60 token 且使用祈使语气 — 不是"考虑"或"试试"
- [ ] 每个 `@` 引用已验证指向现有文件 — 用 Glob 检查
- [ ] 每个工具调用展示确切参数（工具名 + 每个必需参数 + 预期响应形状）
- [ ] 文件在大小限制内（参见上方提示词大小规范表）
- [ ] Description frontmatter 包含 3-5 个触发短语和 1-2 个 when-NOT-to-use 短语
- [ ] 每个 self-check 项都有要运行的命令和预期输出 — 没有"验证它能工作"
- [ ] 没有过度提示要求彻底 — 为 Claude 4.6 将 "MUST use this tool" 替换为自然指导
