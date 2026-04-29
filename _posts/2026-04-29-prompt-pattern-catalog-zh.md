---
layout: post
title: "142 个 AI Agent 提示词模式"
date: 2026-04-29
categories: [patterns, catalog]
lang: zh
---

从 500+ 个真实 AI agent 插件中提炼的 142 个提示词工程模式。不是理论，每个模式都有名字、解决的问题、和可直接使用的 prompt 片段。

---

## 为什么做这个

市面上的"awesome prompts"集合大多面向 ChatGPT 用户的一次性问答。**这个目录面向构建 AI agent 和多步骤插件的开发者** — prompt 稳定性、技能间协调、防御性模式才是关键。

这些模式来自对 500+ 个生产插件的分析，涵盖：DevOps 自动化、安全分析、代码迁移、事件响应、部署编排等。每个模式至少在 3 个独立插件中出现才被收录。

---

## 目录结构

```
catalog/
├── catalog-index.md              ← 总索引（全部 142 个模式）
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

还有补充分类：Karpathy 行为模式、Claude Code 平台模式、开源技能模式、Gap-fill 模式。

---

## 举例：模式 23 — 带上限的修复循环

**问题：** AI agent 修复构建错误时可能无限循环，或者太早放弃。

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

**为什么有效：** 消除了 agent 合理化提前退出的倾向。穷举表格不留歧义 — agent 无法发明第 4 个停止条件。

---

## 举例：模式 45 — 指令式写前审查

**问题：** Agent 写入错误的配置变更，破坏生产行为。

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

**为什么有效：** 在"决定做什么"和"执行"之间强制暂停。表格格式让每项检查独立可评估 — agent 无法在连续叙述中跳过某一项。

---

## 技巧亮点

### Token 级技巧（9 个）

基于 LLM 实际处理 token 的方式 — 不是直觉。例如：**决策树在分支逻辑上优于自然语言**，因为树结构把注意力集中在一条路径上，而自然语言同时分散注意力到所有条件。

### 防偷懒策略（8 种）

Agent 会跳过引用文件的阅读、把多步流程压缩成捷径、"记住"而不是重新读取。防偷懒指南记录了 8 种系统性防御，从强制读取门控到渐进式披露。

### Prompt 评审框架

9 个维度（清晰度、确定性、安全性、可测试性……）的结构化评审流程，配合 P0/P1/P2 严重度分级。设计用于 agent prompt 的同行评审。

---

## 如何使用

1. **构建新技能？** 浏览[目录索引](/prompt-context-patterns/catalog/)找到匹配的模式
2. **调试不稳定行为？** 查看[执行控制](/prompt-context-patterns/catalog/categories/patterns-execution-control-zh)和[防偷懒](/prompt-context-patterns/catalog/techniques/anti-laziness-zh)
3. **评审别人的 prompt？** 使用[评审清单](/prompt-context-patterns/catalog/standards/review-checklist-zh)
4. **学习 prompt 工程？** 从 [Token 级技巧](/prompt-context-patterns/catalog/techniques/token-level-techniques-zh)开始

---

## 许可

MIT。可自由用于你的 agent、插件和项目。
