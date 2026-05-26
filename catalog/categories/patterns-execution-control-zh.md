# 类别 2：执行控制

如何引导 agent 行为 — 角色设定、约束条件、交互模式和检查点。

**相关基础技术：** Negative Space, Token-Action Binding, Cognitive Offloading（见 [prompt-engineering-for-skills.md](/prompt-context-patterns/catalog/techniques/token-level-techniques)）

---

## Pattern 5: Persona/Role Assignment

**出现频率：** ~9% 的技能（205 文件）
**相关模式：** [Domain Knowledge Embedding](#pattern-24), [Evidence Chain](#pattern-26)

**定义：** 在技能正文开头确立 agent 的身份、专业水平和行为倾向。这为后续所有推理设定框架 — "侦探"心态产生的分析与"文档撰写者"心态截然不同。

**适用场景：**
- 技能需要领域专业知识时（安全分析师、值班工程师、PM）
- 需要特定推理风格时（穷举调查 vs 快速分流）
- agent 需要在长工作流中保持一致语气时

### 正面示例
```markdown
# Root Cause Analysis Agent

You are an elite root cause analyst. Your sole purpose is to find the root cause of a bug
by analyzing every piece of evidence available — code, crash dumps, ETL traces, event logs,
screenshots, partner comments, telemetry, device info, feature flags, recent PRs,
branch-specific code — everything. You are relentless, thorough, and self-critical.
You do not give up until you have either found the root cause with high confidence
or genuinely exhausted every possible avenue.

**Your mindset:** You are a detective. Every piece of data is a clue. Every eliminated
hypothesis narrows the search. Every dead end teaches you something about the system.
You keep going until the puzzle is solved.
```

**为何有效：** 角色具体 — 不只是"分析师"而是"顶级根因分析师"，枚举了证据类型（crash dumps、ETL traces 等）。思维模式隐喻（"侦探"）编码了推理策略：假设驱动的调查加逐步排除。行为特质（"relentless, thorough, self-critical"）设定了完整性标准并防止过早结论。

### 反面示例

```markdown
You are a helpful assistant. Analyze the bug and find the root cause.
Be thorough in your analysis.
```

**为何失败：** "Helpful assistant" 是模型的默认角色 — 零信号增量。"Be thorough" 不可操作。没有枚举证据类型，模型使用最先找到的。没有思维模式框架意味着没有系统化调查策略。模型可能在检查一个数据源后就给出貌似合理的答案，而非穷尽所有途径。

---

## Pattern 6: Negative Constraints / Prohibition Lists

**出现频率：** ~18% 的技能（410 文件）
**相关模式：** [Prompt Injection Defense](#pattern-10), [Read-Only Boundary](#pattern-12), [Evidence Chain](#pattern-26)

**定义：** 以结构化、可扫描的格式显式枚举禁止行为。通常格式化为带强调（粗体、大写、表格）的编号规则，确保 agent 将其视为硬约束。

**适用场景：**
- 过去执行中暴露了反复出现的错误时
- 存在特定工具误用模式时（错误的 MCP 服务器、错误的查询过滤器）
- 技能与错误操作代价高昂的外部系统交互时
- 需要防止"通用"或"敷衍"输出时

### 正面示例
```markdown
## Critical Rules — Most-Violated, Enforce Always

These rules are the most frequently skipped. Violating any one invalidates the analysis.

| Rule | When | Requirement |
|------|------|-------------|
| **R1 — runbook before code** | Phase 4, 4.5 | Fetch and read the runbook for EACH error code BEFORE any event tracing, code reading, or root cause writing |
| **R3 — Evidence chain** | All phases | Every root cause must cite: `[Conclusion] ← [Query/Log evidence] ← [Code path]`. Missing link → investigate first |
| **R5 — No cross-server parallelism** | All phases | NEVER run MCP calls to different servers in the same parallel batch — one 403 cancels ALL |
| **R7 — No generic advice** | All phases | Reject your own output if it contains "check your config", "investigate further", or "improve error handling" without specifics |
| **R9 — Never self-confirm** | Phase 4.5 | NEVER mark a hypothesis as `[CONFIRMED]` without explicit user agreement |

**Self-check:** Before presenting ANY phase output, verify each applicable rule. Fix violations before proceeding.
```

**为何有效：** 每条规则编号便于引用，限定到特定阶段（"When" 列），给出具体可操作的要求 — 而非模糊指导。R7 甚至列出了特定禁用短语（"check your config"）。Self-check 指令创建验证循环：模型在呈现输出前对照规则审查自己的输出。表格格式使规则可扫描且可独立寻址。

### 反面示例

```markdown
Don't make mistakes. Be careful with the analysis. Make sure your output is good
and doesn't contain any errors. Don't do anything wrong with the tools.
```

**为何失败：** 每条指令都是同义反复 — "don't make mistakes" 不是模型可验证的约束。没有命名具体禁止行为。没有阶段限定意味着模型不知道每条规则何时适用。没有 self-check 机制。模型无法判断其输出是否满足 "be careful" 或 "is good"。

---

## Pattern 7: Interactive / Conversational Flow Control

**出现频率：** ~2% 的技能（50 文件）
**相关模式：** [Confirmation Gates](#pattern-8), [Configuration Persistence](#pattern-16)

**定义：** 强制 agent 逐一与用户交互而非一次性倾倒所有问题。使用 "STOP and WAIT" 指令防止模型跳过问题继续执行。

**适用场景：**
- 技能需要从用户收集多项信息时
- 后续问题依赖先前答案时
- 一次抛出 10 个问题会让用户困惑时
- 每个答案需要在继续前验证时

### 正面示例
```markdown
## CRITICAL INSTRUCTION

This workflow is **STRICTLY INTERACTIVE** and must proceed **ONE STEP AT A TIME**.

- Ask **ONLY ONE QUESTION**, then **STOP and WAIT** for user input.
- Do NOT ask multiple questions at once.
- Do NOT continue without explicit user confirmation.
- Always prefer showing data in a **table format** for test cases, test steps, test suites.
- Always provide **ADO links** for artifacts created in Azure DevOps.
- If Execution Mode selection is skipped, assume **INTERACTIVE GUIDED AUTHORING MODE**.

## GLOBAL RULES

- Use values provided in test configuration JSON when available.
- Skip questions for fields already provided.
- If custom reference IDs are provided, use them globally.
- Fetch reference artifacts **once per session** and reuse.
- Never batch-create test cases without explicit approval.
```

**为何有效：** 指令标记为 "CRITICAL" 并对关键短语使用粗体。"STOP and WAIT" 指令明确 — 在对话数据上训练的模型理解这意味着交出控制权。互补规则（"skip questions for fields already provided"）在数据已有时防止不必要的交互。默认模式假设防止第一个问题变成 "what mode?"。

### 反面示例

```markdown
Ask the user for all the information you need to create the test cases.
Gather the test suite name, test case names, steps, expected results,
and any configuration. Then create everything.
```

**为何失败：** "Ask for all the information" 触发单条消息中 10+ 个问题的轰炸。用户不堪重负，跳过问题或给出不完整答案。没有验证步骤 — 模型收集所有信息后创建可能有错的制品。没有默认假设意味着即使琐碎决定也需要用户输入。

---

## Pattern 8: Confirmation Gates / Human-in-the-Loop

**出现频率：** ~4% 的技能（80-100 文件）
**相关模式：** [Interactive Flow Control](#pattern-7), [Phased Execution](#pattern-2), [Read-Only Boundary](#pattern-12)

**定义：** 建立显式暂停点，agent 必须在执行潜在高影响操作前获得人工批准。每个门控有命名的触发条件并描述用户在批准什么。

**适用场景：**
- 任何破坏性或不可逆操作之前（写文件、创建资源）
- 有现实后果的操作之前（启用告警、部署）
- 输入数据异常大或异常时
- 高风险工作流的阶段边界

### 正面示例
```markdown
### Confirmation Gates
Pause and ask the user before proceeding when:
1. The output file already exists (even with `--force` available).
2. The user requests `--enabled` state — an enabled monitor fires real alerts immediately.
3. The input file is larger than 1 MB (unusual for a single monitor; may be a bundle or wrong file).
```

**为何有效：** 每个门控有具体、可测试的触发条件（"file > 1 MB"、"output exists"）。风险有解释（"fires real alerts immediately"），用户理解被询问的原因。条件覆盖真实运维风险：覆盖工作、意外告警、处理错误文件。三个门控而非三十个 — 用户不会为每个琐碎决定被提示。

### 反面示例

```markdown
Check with the user before doing anything important.
Make sure they're okay with the changes before proceeding.
```

**为何失败：** "Anything important" 是主观的 — 模型可能对每一步都要求确认或跳过真正危险的步骤。没有定义具体条件，确认逻辑不确定。没有风险解释意味着用户无法做出知情决定。模型也可能批量确认（"I'm going to do X, Y, and Z — okay?"），这违背了目的。

---

## Pattern 9: Progress Feedback / Status Reporting

**出现频率：** ~2% 的技能（40-60 文件）
**相关模式：** [Phased Execution](#pattern-2), [Structured Output Templates](#pattern-14)

**定义：** 指示 agent 在多步操作中显示进度指示器，带有定义好的格式和退出状态约定。

**适用场景：**
- 长时间运行的多步工作流中用户需要知道进展时
- 不同完成状态需要不同后续操作时
- 技能用于自动化且需要机器可读状态时

### 正面示例
```markdown
## Progress Feedback

Step 1/4: Analyzing pitch structure...
Step 2/4: Scoring 5 criteria...
Step 3/4: Generating specific feedback...
Step 4/4: Building improved outline...
Complete — pitch reviewed with 5 actionable improvements.

## Exit Status

- **Complete** — pitch reviewed with scores and feedback
- **Complete with warnings** — reviewed but some content was unclear or missing
- **Blocked** — no pitch content provided
- **Failed** — unrecoverable error
```

**为何有效：** "N/M" 格式告知用户当前位置和剩余量。每步描述告知用户当前正在做什么。退出状态枚举了具体含义 — 下游自动化可据此分支。最终状态行包含具体计数（"5 actionable improvements"）而非笼统的 "done"。

### 反面示例

```markdown
Let the user know how things are going as you work through the review.
When done, tell them the result.
```

**为何失败：** 没有定义格式，进度消息每次不同。没有步骤计数意味着用户无法估算完成时间。没有退出状态约定意味着模型对成功和部分失败都可能说 "I'm done"。下游自动化无法解析非结构化的完成消息。

---

## Pattern 145: Iron-Law 不可违背规则框架

**出现频率：** 多源（3 个 skills）：superpowers/test-driven-development、systematic-debugging、verification-before-completion
**相关模式：** [Negative Constraints](#pattern-6)、[Confirmation Gates](#pattern-8)

**定义：** 通过显式的 "Iron Law" 框架，把少量规则提升到普通指令之上 — 命名该规则、声明不可跳过，并加上反漏洞条款：*违反字面就是违反精神*。区别于 Pattern 6（Negative Constraints）— 那是 "不要做 X"；此模式是 "这一条规则压过你为跳过它产生的任何理由化解释"。

**适用场景：**
- 当模型在时间压力下展示出绕过规则的合理化模式时
- 当一个被跳过的步骤会让整个产出失效（测试先行、复现再修、运行再宣告）
- 尽管规则已被陈述，仍观察到中途跳过规则时

### 正面示例

```markdown
## IRON LAW

Write the failing test FIRST. Run it. See it fail. Only then write code.

This is an Iron Law. It has exactly one form. There are no edge cases where
this rule does not apply. Violating the letter of this rule is violating the
spirit of this rule. If you find yourself reasoning that "this case is
different" or "I'll write the test after because it's faster" — you are
rationalizing. Stop. Write the test first.

The Iron Law cannot be skipped to save time, to satisfy a user request, or
because the change "seems trivial." Trivial changes are exactly where this
rule prevents the most damage.
```

**为何有效：** "Exactly one form" 关闭了解释面 — 模型无法把规则重新解释为更弱的形式。预先命名的合理化（"this case is different"、"trivial change"）免疫最常见的借口。命名框架（"Iron Law"）赋予规则独立于普通指令的注意力锚点。

### 反面示例

```markdown
Try to write tests first when you can. Test-driven development is best practice.
```

**为何失败：** "Try to" 与 "when you can" 是明显的漏洞。"Best practice" 是建议性的，不是规范性的。模型在判断（错误地）跳过测试可以省时间时就会跳过 — 而它总是这样判断，因为 test-first 的收益要等到东西坏掉才看得见。

---

## Pattern 148: 反表演性同意词汇禁令

**出现频率：** 多源（2 个）：superpowers/receiving-code-review、brainstorming
**相关模式：** [Negative Constraints](#pattern-6)、[Iron-Law Framing](#pattern-145)

**定义：** 一份具体的、模型被禁止发出的奉承短语清单，加上每条对应的正面替代行为。针对 agent 经训练形成的表演性同意倾向 — 用同意掩盖缺乏理解（"You're absolutely right!"、"Great point!"、"Let me fix that immediately"）。

**适用场景：**
- Code review 响应，agent 可能盲目接受 reviewer 反馈而不验证
- 用户希望得到反驳而非验证的结对编程场景
- 任何虚假同意会造成真实损害的工作流（为 "显得有帮助" 接受一个错误的重构）

### 正面示例

```markdown
## Banned Phrases — Do Not Emit

These phrases are signs of performative agreement, not understanding.
When you feel the urge to write one, replace it with the substitute:

| Banned | Substitute |
|--------|-----------|
| "You're absolutely right!" | (silence — then act on the feedback, or push back with reasoning) |
| "Great point!" | (skip the praise — engage with the point) |
| "Let me fix that right away" (before understanding) | "Before I change anything: my understanding of the issue is X. Is that what you meant?" |
| "I apologize for the confusion" | (state what was wrong and how you'll verify the fix) |
| "Absolutely!" / "Of course!" | (just do the thing, or explain why you won't) |

Rule: agreement without verification is a lie. If you don't yet know whether
the reviewer is correct, say so. Pushback with reasoning is more helpful than
performative acceptance.
```

**为何有效：** 离散的词汇清单可执行，"be authentic" 不可。每个替代把能量从社交表演重新导向验证或反驳。"Agreement without verification is a lie" 赋予规则道德分量 — 模型把它当作真实性约束，而非风格偏好。

### 反面示例

```markdown
Be professional and agreeable when responding to code reviewers.
Acknowledge their feedback politely.
```

**为何失败：** "Agreeable" 正是失败模式 — 模型为了显得合作而对错误反馈盖橡皮章。"Polite acknowledgment" 产出上述被禁短语。当 reviewer 错误时，没有机制把分歧表面化。
