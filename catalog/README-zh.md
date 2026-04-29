# 提示词工程示例与模式目录

一套用于编写稳定、可预测的 Claude Code 技能和插件提示词的参考库。包含从 500+ 生产级 AI Agent 插件（社区插件市场）、Anthropic 官方技能仓库和社区开源技能中提取的 **120 个提示词工程模式**。

## 内容概览

### 理论与深度分析

| 文件 | 说明 |
|------|------|
| [prompt-engineering-for-skills.md](/prompt-context-patterns/catalog/techniques/token-level-techniques) | 基于条件熵和注意力分布的 9 个基础技术 |
| [template.md](/prompt-context-patterns/catalog/techniques/good-vs-bad-template) | BAD vs GOOD 提示词对比，含逐行分析 |
| [skill-reference-laziness-analysis.md](/prompt-context-patterns/catalog/techniques/anti-laziness) | 防止 Agent 跳过 Tier 3 参考文件读取的 8 种策略，含决策框架 |
| [reference-skip-playbook.md](/prompt-context-patterns/catalog/techniques/reference-skip-playbook) | 针对参考跳过问题的 11 种解决模式，按 3 种失败模式分类（裸跳转、预满足、可选框架），含决策矩阵 |

### 模式目录（120 个模式）

从 [pattern-catalog-index.md](/prompt-context-patterns/catalog/catalog-index) 的快速参考表开始查找所有模式。

#### 基础模式（1-30）

| 文件 | 分类 | 模式 |
|------|------|------|
| [patterns-structural-scaffolding.md](/prompt-context-patterns/catalog/categories/patterns-structural-scaffolding) | 结构脚手架 | YAML frontmatter、分阶段执行、工作流模式分支、`$ARGUMENTS` |
| [patterns-execution-control.md](/prompt-context-patterns/catalog/categories/patterns-execution-control) | 执行控制 | 角色/人设、否定约束、交互式流程、确认门控、进度反馈 |
| [patterns-safety-and-trust.md](/prompt-context-patterns/catalog/categories/patterns-safety-and-trust) | 安全与信任 | 注入防御、数据脱敏、只读边界、激活范围 |
| [patterns-input-output-contracts.md](/prompt-context-patterns/catalog/categories/patterns-input-output-contracts) | 输入/输出契约 | 结构化输出模板、错误处理、配置持久化、跨平台 |
| [patterns-agent-orchestration.md](/prompt-context-patterns/catalog/categories/patterns-agent-orchestration) | Agent 编排 | 多 Agent 拓扑、技能组合、意图路由、工具映射、共识 |
| [patterns-knowledge-and-context.md](/prompt-context-patterns/catalog/categories/patterns-knowledge-and-context) | 知识与上下文 | 参考文件、领域知识、示例、证据要求 |
| [patterns-quality-and-feedback.md](/prompt-context-patterns/catalog/categories/patterns-quality-and-feedback) | 质量与反馈 | 评分标准、自我批评、反馈循环、版本管理 |

#### 高级模式（31-99）

| 文件 | 模式 | 关注点 |
|------|------|--------|
| [patterns-advanced-orchestration.md](/prompt-context-patterns/catalog/categories/patterns-advanced-orchestration) | 31-44 | Agent 编排与多 Agent 协调 |
| [patterns-advanced-quality.md](/prompt-context-patterns/catalog/categories/patterns-advanced-quality) | 45-55 | 质量、评审与评估 |
| [patterns-advanced-safety.md](/prompt-context-patterns/catalog/categories/patterns-advanced-safety) | 56-69 | 安全、信任与合规 |
| [patterns-advanced-workflow.md](/prompt-context-patterns/catalog/categories/patterns-advanced-workflow) | 70-80 | 工作流、执行与自主性 |
| [patterns-advanced-io-domain.md](/prompt-context-patterns/catalog/categories/patterns-advanced-io-domain) | 81-91 | 输入/输出、领域与通信 |
| [patterns-gap-fills.md](/prompt-context-patterns/catalog/categories/patterns-gap-fills) | 92-99 | 入职、生产力、迁移与创意 |

#### 开源模式（100-120）

| 文件 | 模式 | 来源 |
|------|------|------|
| [patterns-open-source-skills.md](/prompt-context-patterns/catalog/categories/patterns-open-source-skills) | 100-120 | Anthropic 官方技能仓库 + ComposioHQ 社区技能 |

### 架构

| 文件 | 说明 |
|------|------|
| [skill-architecture-patterns.md](/prompt-context-patterns/catalog/techniques/skill-architecture) | 技能打包、组合、子 Agent、市场模式与参考组织 |

## 使用方法

1. **构建新技能？** 扫描[快速参考表](/prompt-context-patterns/catalog/catalog-index#quick-reference-table)，找到与你的场景相关的模式。
2. **评审现有技能？** 检查它使用了哪些模式，遗漏了哪些。
3. **学习提示词工程？** 从[理论](/prompt-context-patterns/catalog/techniques/token-level-techniques)开始，然后按顺序阅读基础分类文件。

## 数据来源

| 来源 | 规模 | 提取日期 |
|------|------|----------|
| 社区插件市场 | 500+ 插件，2,293 个 SKILL.md 文件 | 2026-04-13/14 |
| `skills`（Anthropic 官方） | 17 个技能 + 35 个参考文件 | 2026-04-15 |
| `awesome-claude-skills`（社区） | 32 个独立技能 + 832 个 Composio 技能 | 2026-04-15 |
