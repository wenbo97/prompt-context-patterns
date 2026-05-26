# Claude Code Skill 与 Plugin 的 Prompt 工程实践

基于 LLM 实际处理 token 方式的稳定、可预测 skill prompt 编写指南。

---

## 核心原则：降低条件熵

LLM 生成的每个 token 都是候选项上的概率分布。**你的 prompt 结构直接控制每个决策点分布的尖锐或弥散程度。**

- 尖锐分布（低熵）→ 确定性行为
- 弥散分布（高熵）→ 不稳定、不可预测的行为

**以下所有技术都是为了在关键时刻锐化分布。**

### "条件熵"的实际含义

每次模型生成 token 时，它面对一组候选项，每个有一个概率。如果概率均匀分布（如10个候选项各10%），模型在"犹豫"——高熵。如果一个候选项占90%其余可忽略，模型"确定"——低熵。

**你编写 prompt 的方式直接决定模型在关键决策点是犹豫还是坚定。**

### 具体示例

假设你的 skill 需要根据环境决定是否询问用户输入。

**散文版本：**

```
If running in CI with no arguments, use defaults.
If interactive with arguments, run directly.
If interactive without arguments, ask the user.
```

读完后，模型需要生成下一个动作。注意力内部发生的事：

```
"CI"              → 第1行，开头     ← 注意力必须回溯
"no arguments"    → 第1行，中间     ← 注意力必须回溯
"use defaults"    → 第1行，末尾     ← 注意力必须回溯
"interactive"     → 第2行，开头     ← 也在争夺注意力
"ask the user"    → 第3行，末尾     ← 也在争夺注意力

5个条件分散在3行——应该关注哪个？
```

注意力分散在多个位置 → 没有单个条件获得足够权重 → 模型不确定走哪条路 → **高熵 → 不稳定行为**。

**树版本：**

```
## CI environment?
├─ YES
│  └─ Has arguments?
│     ├─ YES → use arguments, execute
│     └─ NO  → use defaults, execute
└─ NO (interactive)
   └─ Has arguments?
      ├─ YES → use arguments, execute
      └─ NO  → ask user
```

模型确定"CI = YES"且"arguments = NO"后，注意力在此：

```
│     └─ NO  → use defaults, execute
              ↑
              注意力集中在这一行
```

"use defaults, execute" token **紧邻游标**。无需回溯任何位置。模型几乎100%确定下一步做什么 → **极低熵 → 确定性行为**。

### 用数字感受

散文版本——决策点的概率分布：

```
use arguments, execute:  35%
use defaults, execute:   30%
ask user:                25%
other:                   10%
```

三个选项概率接近。运行10次，大约3次可能出错。

树版本——在正确分支叶节点：

```
use defaults, execute:   92%
use arguments, execute:   5%
other:                    3%
```

一个选项主导。运行10次，0-1次偏差。

### 为什么缩进是信息

```
└─ NO (interactive)
   └─ Has arguments?
      └─ NO  → ask user
```

缩进（0空格、3空格、6空格）在分词后变成空白 token。这些空白 token 编码**层级**——模型在训练中见过大量缩进结构（源代码、YAML、目录树），已学会：更深缩进 = 父条件的子级。

散文没有这种空间编码。在"If interactive but arguments provided"中——"interactive"和"arguments provided"之间的从属关系必须仅从自然语言语法推断。推断本身消耗注意力并引入不确定性。

### 一句话总结

> 树让模型看几个附近 token 就知道做什么。散文迫使它扫描整个段落拼凑答案。搜索半径越小，结果越确定。

---

## 1. 可视决策树优于散文

Claude 遵循可视树结构比同一逻辑的散文描述更可靠，因为每个分支都以明确动作终止。

### 原理

散文将条件分散在句子中。模型必须同时关注多个远距离 token，稀释注意力。树将相关条件与其动作在 token 序列中相邻放置——模型只需看附近 token 就知道做什么。

### 差: 散文

```
If running in CI with no arguments, use defaults. If interactive with arguments,
run directly. If interactive without arguments, ask the user.
```

### 好: 决策树

```
## Is $ARGUMENTS non-empty?
├─ YES → parse arguments, execute directly, no interaction
└─ NO
   ## Is $CI or $CLAUDE_NONINTERACTIVE set?
   ├─ YES → use values from <defaults>, execute directly
   └─ NO  → ask user for missing parameters, then execute
```

### 为什么缩进重要

缩进 token 编码层级。模型在训练中见过大量缩进结构（代码、YAML、目录树），已学会更深缩进 = 父条件的子级。散文没有这种空间编码——模型必须从自然语言语法推断嵌套，消耗注意力并引入不确定性。

---

## 2. 锚定 (Grounding)

给模型一个具体起点，而非让它从无限空间采样。

### 差: 无锚定

```
Generate a deployment script.
```

### 好: 用模板锚定

```
Generate a deployment script based on this template:
<template>
#!/bin/bash
set -euo pipefail
ENV="${1:?Usage: deploy.sh <env>}"
# ... your steps here
</template>
```

**原理:** 模板 token 直接参与注意力——模型输出被"拉向"模板分布，而非从"部署脚本"的通用概念采样。

---

## 3. 认知卸载

将模型原本需要隐式执行的推理步骤外化。

### 差: 需要隐式推理

```
Analyze this code's performance issues and fix them.
```

### 好: 提供显式步骤

```
<analysis_steps>
1. Identify all loops and recursion
2. Annotate each with time complexity
3. Flag anything O(n²) or higher
4. Propose optimization for each flagged section
</analysis_steps>
Execute these steps in order.
```

**原理:** LLM 没有真正的工作记忆。每个推理步骤消耗上下文窗口的注意力资源。写出中间步骤提供"外部记忆"——每步只需关注上一步输出，无需从零推导所有内容。

决策树 = 分支逻辑的认知卸载。
思维链 = 推理的认知卸载。
同一原则，不同应用。

---

## 4. 注意力局部性

相关信息应在 token 序列中靠近。实践中更近的 token 获得更高注意力权重。

### 差: 规则远离目标

```
<rules>Never delete production databases</rules>
... (500 tokens of other content) ...
<task>Clean up expired data</task>
```

### 好: 规则紧邻目标

```
<task>
Clean up expired data
<constraint>Never delete production databases</constraint>
</task>
```

**原理:** Transformer 注意力理论上全局但有位置偏差——附近 token 获得更强注意力分数。将约束放在其约束的动作旁边，而非放在远处的"通用规则"部分。

---

## 5. Token-Action 绑定

每条指令应尽可能直接映射到一个可执行动作。

### 差: 单句多个隐式动作

```
Check code style issues and fix them then run tests and make sure they pass.
```

### 好: 一条指令 = 一个动作

```
1. Run: `eslint --fix src/`
2. Run: `npm test`
3. If tests fail → read error output, fix the issue, go to step 2
```

**原理:** 模型将单条清晰指令序列映射到单个工具调用远比从一个连写句中提取多个隐含动作可靠。

---

## 6. Schema Priming

给模型一个输出"形状"，它会填充内容。

### 差: 开放式

```
Analyze this PR's risk.
```

### 好: Schema 约束

```
<output_schema>
- risk_level: high | medium | low
- affected_files: [list]
- rollback_plan: [string]
- requires_review: true | false
</output_schema>
```

**原理:** Schema token 在解码时充当"轨道"。生成每个字段值时，模型注意力被 schema 键名强引导，大幅减少漂移。

---

## 7. 负空间（显式替代）

告诉模型不要做什么时，始终提供应该做什么。

### 差: 只有否定

```
Don't modify the database directly.
Don't skip tests.
Don't use sudo.
```

### 好: 否定 + 替代路径

```
<boundaries>
- Database changes → generate a migration file, never execute raw SQL
- Validation needed → run full test suite before continuing, never skip
- Elevated permissions → request user confirmation, never use sudo
</boundaries>
```

**原理:** "Don't do X"只抑制某些 token 序列但不提升任何替代。模型知道哪里不能去但不知道该去哪 → 不稳定。提供替代同时抑制错误路径并提升正确路径。

---

## 8. XML 标签作为语义边界

Claude 训练数据中包含 XML 标签。使用它们划分 prompt 部分。

### 推荐的 skill prompt 结构

```markdown
<context>
Background information the model needs to understand the domain.
</context>

<parameters>
Inputs with types, defaults, and sources.
</parameters>

<decision_tree>
Visual branching logic with explicit leaf actions.
</decision_tree>

<examples>
<example>
<input>...</input>
<thinking>Step-by-step reasoning the model should follow</thinking>
<output>...</output>
</example>
</examples>

<boundaries>
What not to do + what to do instead.
</boundaries>

<output_schema>
Expected output shape.
</output_schema>
```

**原理:** XML 标签创建硬语义边界。模型将不同标签内的内容视为独立部分，减少指令、示例和约束之间的交叉污染。

---

## 9. 带嵌入推理的 Few-Shot

展示模型如何思考，而非只展示输出什么。

### 差: 只有输入/输出对

```
<example>
<input>deploy staging</input>
<output>Deployed to staging.</output>
</example>
```

### 好: 输入 + 思考 + 输出

```
<example>
<input>deploy staging</input>
<thinking>
1. Arguments provided: "staging" → non-empty → skip user interaction
2. Environment "staging" is valid (matches staging|production)
3. No CI variable detected → but args present → proceed silently
4. Execute deployment to staging
</thinking>
<output>Deployed to staging successfully.</output>
</example>
```

**原理:** few-shot 示例中的 `<thinking>` 模式被泛化到模型自身的扩展思考块中。它学到的是推理模式，而非仅仅是输出模式。

---

## 综合运用：Skill Prompt 模板

```markdown
---
name: my-skill
description: One line that tells Claude WHEN to activate this skill
context: default
allowed-tools: Bash(specific-commands*), Write, Edit
---

<context>
What this skill does and why it exists.
Domain-specific background if needed.
</context>

<parameters>
- target: from $ARGUMENTS, or ask user
- env_mode: from $CI or $CLAUDE_NONINTERACTIVE, default "interactive"
</parameters>

<decision_tree>
## Has $ARGUMENTS?
├─ YES → parse into `target`, skip interaction
└─ NO
   ## Is env_mode non-interactive?
   ├─ YES → use defaults from <defaults>, proceed
   └─ NO  → ask user for `target`, then proceed
</decision_tree>

<defaults>
- target: "staging"
</defaults>

<steps>
1. Validate `target` against allowed values (staging | production)
2. Run preflight checks: `npm test`
3. If tests fail → stop, report error, do NOT proceed
4. Execute deployment to `target`
5. Verify deployment health
</steps>

<examples>
<example>
<input>/my-skill production</input>
<thinking>
1. $ARGUMENTS = "production" → non-empty → use directly
2. target = "production" → valid
3. Run tests → pass
4. Deploy to production
</thinking>
<output>Deployed to production. Health check passed.</output>
</example>
</examples>

<boundaries>
- Never deploy without passing tests → run `npm test` first, abort on failure
- Never modify .env files → read config from environment variables only
- Never run with sudo → request user confirmation for elevated actions
</boundaries>
```

---

## 关系总结

```
行为稳定性
      ↑
决策点的低条件熵
      ↑
尖锐的注意力分布
      ↑
Prompt 中 Token 的空间排列
      ↑
┌─────────────┬──────────────┬───────────────┬──────────────┐
│ Decision    │ Attention    │ Cognitive     │ Schema       │
│ Trees       │ Locality     │ Offloading    │ Priming      │
├─────────────┼──────────────┼───────────────┼──────────────┤
│ Grounding   │ Token-Action │ Negative      │ XML          │
│ (Anchoring) │ Binding      │ Space         │ Boundaries   │
├─────────────┼──────────────┼───────────────┼──────────────┤
│ Few-Shot w/ │              │               │              │
│ Reasoning   │              │               │              │
└─────────────┴──────────────┴───────────────┴──────────────┘

所有技术操控的是同一件事：
生成时注意力如何分布在 token 上。
```

---

## 参考文献

- Anthropic Prompting Best Practices: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
- Anthropic Context Engineering: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- XML Tags Guide: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags
- Claude Code Skills Docs: https://code.claude.com/docs/en/skills
- Claude Code System Prompts (community): https://github.com/Piebald-AI/claude-code-system-prompts
- Awesome Claude Skills: https://github.com/travisvn/awesome-claude-skills
