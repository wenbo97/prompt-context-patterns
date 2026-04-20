---
layout: post
title: "模式：决策树比自然语言更适合 AI 提示词中的分支逻辑"
date: 2026-04-19
categories: [patterns, decision-tree]
lang: zh
---

用自然语言段落告诉 AI 该做什么，大多数时候能用。但当逻辑有分支（"如果 X 就 Y，否则 Z"），自然语言提示词在多次运行中会产生**不一致的输出** — 即使输入完全相同。

**决策树能解决这个问题。** 用可视化的树结构替代自然语言的分支逻辑，模型就能确定性地执行。

---

## 问题

考虑一个事故响应系统：AI 需要判断严重等级、分配响应人员、选择缓解措施、生成结构化的响应计划。规则很复杂：4 个严重等级、6 种根因类别、基于层级的人员分配、升级条件、通信截止时间。

我们为同一个任务写了两种提示词 — 一种是自然语言段落（约 140 行），一种是决策树（约 260 行）— 用 `claude -p` 各跑了 **20 次**，输入完全相同。

## 结果（各 20 次运行）

### 主要缓解措施

| 自然语言 | 决策树 |
|---------|--------|
| 20 次中有 **15 种不同写法** | 20 次中只有 **1 种写法** |

自然语言输出 — 每次都不同：

```
第 1 次:  "Enable graceful degradation on Cosmos DB (cached responses, reduced functionality) while investigating root cause"
第 2 次:  "Enable graceful degradation on Cosmos DB (cached responses, reduced functionality for non-critical read paths)"
第 3 次:  "Enable graceful degradation mode on Cosmos DB East US 2"
第 4 次:  "Enable graceful degradation on Cosmos DB East US 2 to serve cached/reduced-functionality responses while..."
...共 15 种不同表达
```

决策树输出 — 每次相同：

```
第 1-20 次:  "enable_graceful_degradation"
```

### 次要措施

| 自然语言 | 决策树 |
|---------|--------|
| **20 种不同写法**（零重复） | **2 种**（19 次 `hotfix`，1 次 `failover_to_secondary`） |

自然语言的次要措施达到了 **0% 的可复现性** — 每一次运行都产生独特的句子。

### 完整对比

| 维度 | 自然语言（20 次） | 决策树（20 次） |
|------|-----------------|----------------|
| 严重等级 | 20/20 SEV2 | 20/20 SEV2 |
| 主要措施（唯一值数量） | **15** | **1** |
| 次要措施（唯一值数量） | **20** | **2** |
| 响应人员角色组合 | 2 种（大小写不一致：`on-call` vs `On-Call`） | 1 种（一致） |
| "避免操作"数量 | 不一致（16 次 2 项，4 次 3 项） | 一致（20 次都是 2 项） |
| 升级触发条件 | 3 条，一致 | 3 条，一致 |

## 这意味着什么

两种方式都做出了**正确的决策** — SEV2、启用优雅降级、分配 4 名响应人员。差异在于**输出的确定性**。

如果下游代码这样写：

```python
if response["mitigation_plan"]["primary_action"]["action"] == "enable_graceful_degradation":
    execute_graceful_degradation()
```

- **决策树提示词**：20/20 次匹配成功
- **自然语言提示词**：**0/20 次匹配成功**（action 是自由句子，永远不会精确匹配）

这不是理论问题。任何解析 AI 输出的系统 — 自动化流水线、agent 编排、工具调用 — 都会因为输出格式不可预测而崩溃。

## 模式

核心思路：把这种写法：

```
如果根因是部署问题且服务支持即时回滚，优先选择回滚，因为它能以最小风险恢复到最后已知良好状态。
如果根因是部署问题但回滚不可用，则考虑关闭功能标志（如果变更在功能标志后面）。
如果没有功能标志，则进行热修复。
```

替换成这种：

```
根因类别？
├─ 部署问题
│   └─ 服务支持即时回滚？
│       ├─ 是 → action: "rollback"
│       └─ 否
│           └─ 变更在功能标志后面？
│               ├─ 是 → action: "disable_feature_flag"
│               └─ 否 → action: "hotfix"
```

同样的逻辑。树版本在每个叶子节点给出了**精确的输出字符串**，缩进编码了决策路径。

## 为什么有效

1. **逐步收窄注意力。** 模型每次只评估一个条件，而不是同时持有所有规则。
2. **提供精确的输出文本。** 叶子节点包含字面量 action 字符串 — 模型直接复制，而不是自己编写新句子。
3. **用空间编码层级关系。** 缩进 token（空白字符）编码了父子关系。LLM 在训练中从数百万份代码文件、YAML 配置、目录树中学到了这种模式。

## 什么时候用 / 什么时候不用

**用决策树：**
- 提示词有分支逻辑（if/else、switch/case）
- 输出要被代码解析（JSON 字段、action 名称、状态值）
- 需要多次运行的一致性
- 构建 agent 编排或自动化流水线

**不需要决策树：**
- 开放式创意任务（变化是好事）
- 没有分支逻辑
- 输出只给人类阅读（措辞变化无所谓）

## 自己试试

克隆仓库然后运行：

```bash
cd eval/decision-tree-ab
bash run.sh 20           # 20 次运行，默认模型
bash run.sh 10 haiku     # 10 次运行，haiku 模型
python3 analyze.py       # 分析结果
```

包含三个场景：简单（部署控制器）、歧义（未知服务器状态）、复杂（200+ 行的事故响应提示词）。

## 延伸阅读

- [Anthropic: Prompt Engineering Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)
- [Anthropic: Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
