---
layout: post
title: "155 个 AI Agent 提示词模式"
date: 2026-05-26
categories: [patterns, catalog]
lang: zh
---

这 155 个提示词工程模式，是从 500+ 个真实 AI agent 插件、开源 skill 仓库和 Claude Code 系统提示里一点点提炼出来的。它们不讲空理论——每个模式都有自己的名字、要解决的具体问题，还有一段拿来就能用的 prompt 片段。

> **2026-05-26 更新**：从 `awesome-claude-skills`、`superpowers`、`andrej-karpathy-skills`、`claude-plugins-official` 这几个来源又收割了 13 个新模式（143–155），顺手就地优化了 14 个已有模式。完整列表见[目录索引](/prompt-context-patterns/catalog/catalog-index-zh)。

---

## 为什么做这个

网上的"awesome prompts"集合，大多是给 ChatGPT 用户准备的一次性问答。**而这个目录，是给那些在构建 AI agent 和多步骤插件的开发者看的**——对他们来说，真正要紧的是 prompt 够不够稳、技能之间能不能协调、有没有足够的防御性设计。

这些模式来自对 500+ 个生产插件的梳理，横跨 DevOps 自动化、安全分析、代码迁移、事件响应、部署编排等场景。一个模式只有在至少 3 个独立插件里都出现过，才会被收进来。

---

## 目录结构

```
catalog/
├── catalog-index.md              ← 总索引（全部 155 个模式）
├── categories/                   ← 按功能分组
│   ├── patterns-structural-scaffolding.md
│   ├── patterns-input-output-contracts.md
│   ├── patterns-execution-control.md
│   ├── patterns-knowledge-and-context.md
│   ├── patterns-agent-orchestration.md
│   ├── patterns-safety-and-trust.md
│   ├── patterns-quality-and-feedback.md
│   └── ...（共 18 个文件）
├── techniques/                   ← 深度指南
│   ├── token-level-techniques.md    ← 基于熵理论的 9 个技巧
│   ├── anti-laziness.md             ← 防止 agent 偷懒的 8 种策略
│   ├── skill-architecture.md        ← 技能打包与组合
│   ├── branching-stability.md       ← 分支逻辑的可靠性
│   ├── reference-skip-playbook.md   ← 强制 agent 阅读引用文件
│   └── good-vs-bad-template.md      ← 好坏 prompt 对比
└── standards/                    ← 评审框架
    ├── quality-standards.md         ← P0/P1/P2 严重度分级
    └── review-checklist.md          ← 9 维度 prompt 评审
```

---

## 12 个模式分类

| # | 分类 | 模式数 | 覆盖内容 |
|---|------|--------|----------|
| 1 | 结构脚手架 | 15 | 阶段门控、决策树、边界标签 |
| 2 | 输入/输出契约 | 12 | Schema 约束、格式锁定、校验 |
| 3 | 执行控制 | 14 | 尝试上限、停止条件、重试逻辑 |
| 4 | 知识与上下文 | 12 | SSOT 注册表、按需加载、缓存层 |
| 5 | Agent 编排 | 11 | 子 agent 派发、并行执行、交接 |
| 6 | 安全与信任 | 10 | 护栏、禁止操作、升级门控 |
| 7 | 质量与反馈 | 9 | 自审查、证据门控、置信度评分 |
| 8 | 高级 I/O 与领域 | 10 | 领域路由、多模态、Schema 演进 |
| 9 | 高级编排 | 8 | DAG 执行、共识、群体模式 |
| 10 | 高级质量 | 7 | 回归检测、漂移监控 |
| 11 | 高级安全 | 8 | 数据分类、审计追踪、合规 |
| 12 | 高级工作流 | 10 | 部署门控、回滚、状态机 |

除此之外还有几组补充分类：Karpathy 行为模式、Claude Code 平台模式（121–142）、开源技能模式、Gap-fill 模式，以及 **2026-05 收割（143–155）** —— 覆盖 Iron-Law 规则框架、HARD-GATE 阻断标签、DOT 图决策流、市场源类型多态、插件生命周期状态机等。

---

## 举例：模式 23 — 带上限的修复循环

**问题：** AI agent 在修复构建错误时，要么陷进无限循环，要么太早就放弃了。

**模式：**

```markdown
## 停止条件（穷举）

修复循环只在以下条件满足时停止：

| 条件 | 动作 |
|------|------|
| (a) 构建成功 | 返回成功 |
| (b) 尝试次数达到 N | 返回失败，附带剩余错误 |
| (c) 会话死亡 | 返回 session_dead |

没有其他理由可以停止。"错误太多"不行，
"超出范围"不行，"无法修复"也不行。
```

**为什么有效：** 它掐掉了 agent 为提前退出找借口的空间。穷举式的表格没留任何模糊地带 — agent 没法再凭空造出第 4 个停止条件。

---

## 举例：模式 45 — 指令式写前审查

**问题：** Agent 写入了错误的配置变更，把生产行为搞坏了。

**模式：**

```markdown
每次编辑前，逐条检查护栏：

| # | 检查项 | 通过 | 失败 |
|---|--------|------|------|
| G1 | 抑制是否有范围？ | 在具体条目上 | 全局范围 |
| G2 | 覆写是否必要？ | 默认值不满足 | 默认值已经可以 |
| G3 | 是否创建了配套文件？ | 文件对存在 | 孤立条件 |

任何护栏返回"失败" → 不写入。先修正。
```

**为什么有效：** 它在"决定做什么"和"真正动手"之间硬塞进一个暂停。表格这种格式让每一项检查都能单独过一遍 — agent 没办法在一大段连续叙述里悄悄漏掉某一条。

---

## 技巧亮点

### Token 级技巧（9 个）

这些技巧建立在 LLM 真正处理 token 的方式上，而不是凭直觉。举个例子：**在分支逻辑上，决策树比自然语言更好用**——因为树结构会把注意力收拢到一条路径上，而自然语言会同时把注意力摊到所有条件上。

### 防偷懒策略（8 种）

Agent 会耍各种小聪明：跳过该读的引用文件、把多步流程偷偷压成捷径、凭"记忆"作答而不去重新读取。防偷懒指南把 8 种系统性的应对办法都记了下来，从强制读取门控一直讲到渐进式披露。

### Prompt 评审框架

围绕 9 个维度（清晰度、确定性、安全性、可测试性……）的一套结构化评审流程，再配上 P0/P1/P2 的严重度分级，专门用来给 agent prompt 做同行评审。

---

## 如何使用

1. **要构建新技能？** 到[目录索引](/prompt-context-patterns/catalog/)里翻一翻，找到对得上的模式
2. **在调试不稳定的行为？** 看看[执行控制](/prompt-context-patterns/catalog/categories/patterns-execution-control-zh)和[防偷懒](/prompt-context-patterns/catalog/techniques/anti-laziness-zh)
3. **要评审别人写的 prompt？** 用这份[评审清单](/prompt-context-patterns/catalog/standards/review-checklist-zh)
4. **想学 prompt 工程？** 从 [Token 级技巧](/prompt-context-patterns/catalog/techniques/token-level-techniques-zh)入手

---

## 许可

MIT。随便用，你的 agent、插件、项目都行。
