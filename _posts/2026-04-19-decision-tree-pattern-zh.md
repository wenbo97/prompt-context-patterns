---
layout: post
title: "模式：决策树比自然语言更适合 AI 提示词中的分支逻辑"
date: 2026-04-19
categories: [patterns, decision-tree]
lang: zh
---

大多数时候，用一段自然语言告诉 AI 该做什么就够了。可一旦逻辑开始分叉（"如果 X 就 Y，不然就 Z"），麻烦就来了：哪怕输入一模一样，多跑几次，自然语言提示词给出的输出也会**前后不一致**。

**决策树正好能解决这件事。** 把分支逻辑画成一棵可视化的树，模型执行起来就稳定、确定了。

---

## 问题

举个例子，一个事故响应系统：AI 得判断严重等级、安排响应人员、挑选缓解措施，最后生成一份结构化的响应计划。规则并不简单 — 4 个严重等级、6 种根因类别、按层级分配人员，还有升级条件和通信截止时间。

我们给同一个任务写了两版提示词，一版是自然语言段落（约 140 行），一版是决策树（约 260 行），然后在输入完全相同的前提下，用 `claude -p` 各跑了 **20 次**。

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

自然语言的次要措施可复现性是 **0%** — 每一次运行都憋出一个全新的句子。

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

其实两种方式**决策都没错** — SEV2、启用优雅降级、派 4 名响应人员。真正的差别，在于**输出稳不稳定**。

如果下游代码这样写：

```python
if response["mitigation_plan"]["primary_action"]["action"] == "enable_graceful_degradation":
    execute_graceful_degradation()
```

- **决策树提示词**：20/20 次匹配成功
- **自然语言提示词**：**0/20 次匹配成功**（action 是自由句子，永远不会精确匹配）

这可不是纸上谈兵。任何要解析 AI 输出的系统 — 自动化流水线、agent 编排、工具调用 — 只要输出格式没法预测，迟早会崩。

## 模式

思路很简单：把这样的写法：

```
如果根因是部署问题且服务支持即时回滚，优先选择回滚，因为它能以最小风险恢复到最后已知良好状态。
如果根因是部署问题但回滚不可用，则考虑关闭功能标志（如果变更在功能标志后面）。
如果没有功能标志，则进行热修复。
```

换成这样：

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

逻辑一模一样。区别在于，树在每个叶子节点都写好了**精确的输出字符串**，而缩进本身就把决策路径画了出来。

## 为什么有效

1. **一步步收窄注意力。** 模型每次只看一个条件，不用把所有规则一起扛在脑子里。
2. **直接给出要输出的文本。** 叶子节点写的就是字面量 action 字符串 — 模型照抄即可，不用自己再造句。
3. **用空间关系表达层级。** 缩进这些空白字符，本身就编码了父子关系。这种模式，LLM 早在训练时就从数百万份代码文件、YAML 配置和目录树里学会了。

## 什么时候用 / 什么时候不用

**该用决策树：**
- 提示词里有分支逻辑（if/else、switch/case）
- 输出要交给代码解析（JSON 字段、action 名称、状态值）
- 你需要多次运行都保持一致
- 你在搭建 agent 编排或自动化流水线

**不用决策树：**
- 开放式的创意任务（有变化反而更好）
- 根本没有分支逻辑
- 输出只给人看（用词换换无所谓）

## 自己试试

把仓库克隆下来，然后运行：

```bash
cd eval/decision-tree-ab
bash run.sh 20           # 20 次运行，默认模型
bash run.sh 10 haiku     # 10 次运行，haiku 模型
python3 analyze.py       # 分析结果
```

里面有三个场景：简单（部署控制器）、歧义（未知服务器状态）、复杂（200+ 行的事故响应提示词）。

## 延伸阅读

- [Anthropic: Prompt Engineering Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)
- [Anthropic: Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
