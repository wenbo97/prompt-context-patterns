# 提示词模式目录 — 索引

从 500+ 生产级 AI Agent 插件（2,293 个 SKILL.md 文件）、2 个开源技能仓库和 Claude Code 系统提示词架构中提取的 **142 个提示词工程模式**目录。原始 30 个模式（1-30）包含正面/反面示例。高级 61 个模式（31-91）通过对完整插件集合的深度研究发现。8 个补充模式（92-99）来自针对覆盖不足类别的定向扫描。最后 21 个模式（100-120）提取自 Anthropic 官方技能仓库和 ComposioHQ 的 awesome-claude-skills 仓库。模式 121-142 涵盖 Claude Code 可组合系统提示词的平台级关注点。

**数据来源：**
提取自对 500+ 生产级 AI Agent 插件的分析，覆盖 DevOps、安全、迁移和事件响应领域。

**提取日期：** 2026-04-13（原始 30 个），2026-04-14（高级 31-91），2026-04-15（开源 100-120）

---

## 如何使用本目录

1. **构建新技能？** 扫描下方快速参考表，找到与你的场景相关的模式。
2. **评审现有技能？** 检查它使用了哪些模式，遗漏了哪些。
3. **学习提示词工程？** 按顺序阅读分类文件 — 从结构到编排到质量，层层递进。

### 配套文件

| 文件 | 涵盖内容 |
|------|----------|
| [prompt-engineering-for-skills.md](/prompt-context-patterns/catalog/techniques/token-level-techniques-zh) | **理论** — 基于条件熵/注意力分布的 9 个基础技术 |
| [template.md](/prompt-context-patterns/catalog/techniques/good-vs-bad-template-zh) | **深度分析** — 一个 BAD vs GOOD 对比，含逐行分析 |
| **本目录（模式 1-30）** | **基础模式** — 30 个模式，含正面/反面示例 |
| [patterns-advanced-orchestration.md](/prompt-context-patterns/catalog/categories/patterns-advanced-orchestration-zh) | **高级** — 14 个 Agent 编排与多 Agent 模式（31-44） |
| [patterns-advanced-quality.md](/prompt-context-patterns/catalog/categories/patterns-advanced-quality-zh) | **高级** — 11 个质量、评审与评估模式（45-55） |
| [patterns-advanced-safety.md](/prompt-context-patterns/catalog/categories/patterns-advanced-safety-zh) | **高级** — 14 个安全、信任与合规模式（56-69） |
| [patterns-advanced-workflow.md](/prompt-context-patterns/catalog/categories/patterns-advanced-workflow-zh) | **高级** — 11 个工作流、执行与自主性模式（70-80） |
| [patterns-advanced-io-domain.md](/prompt-context-patterns/catalog/categories/patterns-advanced-io-domain-zh) | **高级** — 11 个输入/输出、领域与通信模式（81-91） |
| [patterns-gap-fills.md](/prompt-context-patterns/catalog/categories/patterns-gap-fills-zh) | **补充** — 8 个入职、生产力、迁移与创意模式（92-99） |
| [patterns-open-source-skills.md](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh) | **开源** — 来自 Anthropic 官方 + 社区技能仓库的 21 个模式（100-120） |
| [patterns-karpathy-behavioral.md](/prompt-context-patterns/catalog/categories/patterns-karpathy-behavioral-zh) | **行为** — 5 个 Karpathy 衍生模式：暴露假设、最小可行代码、精准修改、逐步验证、叙述错误路径 |
| [patterns-claude-code-platform.md](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-zh) | **平台** — 12 个 Claude Code 平台模式：记忆、权限、调度、工具路由、Agent 调度（121-132） |
| [patterns-claude-code-platform-extended.md](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-extended-zh) | **平台扩展** — 10 个模式：组合装配、工具约束、安全监视器、团队协调、梦境记忆（133-142） |
| [skill-architecture-patterns.md](/prompt-context-patterns/catalog/techniques/skill-architecture-zh) | **架构** — 技能打包、组合、子 Agent、市场、参考组织 |
| [skill-reference-laziness-analysis.md](/prompt-context-patterns/catalog/techniques/anti-laziness-zh) | **深度分析** — 防止 Agent 在 Tier 3 参考读取中偷懒的 8 种策略，含风险分级决策框架 |
| [reference-skip-playbook.md](/prompt-context-patterns/catalog/techniques/reference-skip-playbook-zh) | **深度分析** — 参考跳过问题的 11 种解决模式：3 种失败模式（裸跳转、预满足、可选框架）、决策矩阵、反模式 |

---

## 快速参考表

| # | 模式 | 分类 | 普及率 | 核心价值 |
|---|------|------|--------|----------|
| 1 | [YAML Frontmatter Metadata](/prompt-context-patterns/catalog/categories/patterns-structural-scaffolding-zh#pattern-1-yaml-frontmatter-metadata-block) | 结构 | ~100% | 平台级身份标识和工具权限 |
| 2 | [Phased/Stepped Execution](/prompt-context-patterns/catalog/categories/patterns-structural-scaffolding-zh#pattern-2-phasedstepped-execution-flow) | 结构 | ~54% | 确定性排序，带阶段目标 |
| 3 | [Workflow Mode Branching](/prompt-context-patterns/catalog/categories/patterns-structural-scaffolding-zh#pattern-3-workflow-mode-branching) | 结构 | ~5% | 同一技能服务不同受众 |
| 4 | [$ARGUMENTS Variable](/prompt-context-patterns/catalog/categories/patterns-structural-scaffolding-zh#pattern-4-arguments-variable-pattern) | 结构 | ~7% | 解析带标志和选项的用户输入 |
| 5 | [Persona/Role Assignment](/prompt-context-patterns/catalog/categories/patterns-execution-control-zh#pattern-5-personarole-assignment) | 执行 | ~9% | 设定专业水平和推理风格 |
| 6 | [Negative Constraints](/prompt-context-patterns/catalog/categories/patterns-execution-control-zh#pattern-6-negative-constraints--prohibition-lists) | 执行 | ~18% | 防止已知的特定错误 |
| 7 | [Interactive Flow Control](/prompt-context-patterns/catalog/categories/patterns-execution-control-zh#pattern-7-interactive--conversational-flow-control) | 执行 | ~2% | 每次一个问题，STOP and WAIT |
| 8 | [Confirmation Gates](/prompt-context-patterns/catalog/categories/patterns-execution-control-zh#pattern-8-confirmation-gates--human-in-the-loop) | 执行 | ~4% | 高风险操作前需人工审批 |
| 9 | [Progress Feedback](/prompt-context-patterns/catalog/categories/patterns-execution-control-zh#pattern-9-progress-feedback--status-reporting) | 执行 | ~2% | Step N/M 状态 + 退出码 |
| 10 | [Prompt Injection Defense](/prompt-context-patterns/catalog/categories/patterns-safety-and-trust-zh#pattern-10-prompt-injection-defense) | 安全 | <1% | 外部内容视为不可信数据 |
| 11 | [Sensitive Data Redaction](/prompt-context-patterns/catalog/categories/patterns-safety-and-trust-zh#pattern-11-sensitive-data-redaction) | 安全 | ~2% | 命名数据类型 + 替换模式 |
| 12 | [Read-Only Boundary](/prompt-context-patterns/catalog/categories/patterns-safety-and-trust-zh#pattern-12-read-only--safety-boundary-declaration) | 安全 | ~4% | 声明操作范围限制 |
| 13 | [Activation Scope](/prompt-context-patterns/catalog/categories/patterns-safety-and-trust-zh#pattern-13-activation-scope-when-to-use--when-not-to-use) | 安全 | ~7% | When to Use / When NOT to Use + 重定向 |
| 14 | [Structured Output Templates](/prompt-context-patterns/catalog/categories/patterns-input-output-contracts-zh#pattern-14-structured-output-templates) | 输入/输出 | ~26% | 精确输出格式 + 填充示例 |
| 15 | [Error Handling / Degradation](/prompt-context-patterns/catalog/categories/patterns-input-output-contracts-zh#pattern-15-error-handling--graceful-degradation) | 输入/输出 | ~10% | 阶段特定的失败响应 |
| 16 | [Configuration Persistence](/prompt-context-patterns/catalog/categories/patterns-input-output-contracts-zh#pattern-16-configuration-persistence--first-time-setup) | 输入/输出 | ~4% | 检查-加载-设置-保存用户配置 |
| 17 | [Cross-Platform Handling](/prompt-context-patterns/catalog/categories/patterns-input-output-contracts-zh#pattern-17-cross-platform-handling) | 输入/输出 | ~3% | 平台特定的工具和路径 |
| 18 | [Multi-Agent Orchestration](/prompt-context-patterns/catalog/categories/patterns-agent-orchestration-zh#pattern-18-multi-agent-orchestration--agent-topologies) | 编排 | ~2% | Agent 拓扑 + 共识评分 |
| 19 | [Skill Composition](/prompt-context-patterns/catalog/categories/patterns-agent-orchestration-zh#pattern-19-skill-composition--cross-skill-invocation) | 编排 | ~4% | 委托给已有技能（DRY） |
| 20 | [Intent Classification](/prompt-context-patterns/catalog/categories/patterns-agent-orchestration-zh#pattern-20-intent-classification--smart-routing) | 编排 | ~6% | 将输入路由到正确的子工作流 |
| 21 | [Tool Routing Tables](/prompt-context-patterns/catalog/categories/patterns-agent-orchestration-zh#pattern-21-tool-routing-tables) | 编排 | ~16% | 任务→工具映射 + "不用这些" |
| 22 | [Deduplication / Consensus](/prompt-context-patterns/catalog/categories/patterns-agent-orchestration-zh#pattern-22-deduplication--consensus-algorithms) | 编排 | ~1% | 加权相似度 + 定义阈值 |
| 23 | [Reference File Injection](/prompt-context-patterns/catalog/categories/patterns-knowledge-and-context-zh#pattern-23-reference-file--knowledge-base-injection) | 知识 | ~17% | 指向外部知识文件 |
| 24 | [Domain Knowledge Embedding](/prompt-context-patterns/catalog/categories/patterns-knowledge-and-context-zh#pattern-24-domain-knowledge-embedding) | 知识 | ~22% | 内联 Schema、字段表、查询模板 |
| 25 | [Few-Shot Examples](/prompt-context-patterns/catalog/categories/patterns-knowledge-and-context-zh#pattern-25-few-shot-examples) | 知识 | ~21% | 完整的输入/输出对 |
| 26 | [Evidence Chain / Proof-of-Work](/prompt-context-patterns/catalog/categories/patterns-knowledge-and-context-zh#pattern-26-evidence-chain--proof-of-work) | 知识 | ~5% | 可追溯结论 + 强制清单 |
| 27 | [Scoring Rubrics](/prompt-context-patterns/catalog/categories/patterns-quality-and-feedback-zh#pattern-27-scoring-rubrics--quantitative-assessment) | 质量 | ~4% | 评分维度、分数范围、类别阈值 |
| 28 | [Self-Critique](/prompt-context-patterns/catalog/categories/patterns-quality-and-feedback-zh#pattern-28-self-critique--quality-self-check) | 质量 | ~2% | 对抗性弱点识别 |
| 29 | [Feedback Solicitation](/prompt-context-patterns/catalog/categories/patterns-quality-and-feedback-zh#pattern-29-feedback-solicitation) | 质量 | <1% | 按优先级分层的调查 + 会话去重 |
| 30 | [Version Check](/prompt-context-patterns/catalog/categories/patterns-quality-and-feedback-zh#pattern-30-version-check--update-notification) | 质量 | <1% | 非阻塞更新通知 |

---

## 高级模式快速参考表（31-80）

通过对 500+ 插件的深度研究发现，按类别分组。

### 第 8 类：高级 Agent 编排 (/prompt-context-patterns/catalog/categories/patterns-advanced-orchestration-zh)

| # | 模式 | 核心价值 |
|---|------|----------|
| 31 | [Adversarial Persona Framing](/prompt-context-patterns/catalog/categories/patterns-advanced-orchestration-zh#pattern-31-adversarial-persona-framing) | 攻击者思维发现真正的 Bug，而非表面问题 |
| 32 | [Hub-and-Spoke SDLC State Machine](/prompt-context-patterns/catalog/categories/patterns-advanced-orchestration-zh#pattern-32-hub-and-spoke-sdlc-state-machine) | 确定性推进开发生命周期 |
| 33 | [M x N Cross-Model Consensus Grid](/prompt-context-patterns/catalog/categories/patterns-advanced-orchestration-zh#pattern-33-m-x-n-cross-model-consensus-grid) | 跨模型多样性捕捉幻觉 |
| 34 | [Dual-Model Adversarial Planning](/prompt-context-patterns/catalog/categories/patterns-advanced-orchestration-zh#pattern-34-dual-model-adversarial-planning) | 独立计划减少单模型偏差 |
| 35 | [Cost-Optimized Model Routing](/prompt-context-patterns/catalog/categories/patterns-advanced-orchestration-zh#pattern-35-cost-optimized-model-routing) | 按任务选择模型，节省 60%+ 成本 |
| 36 | [Handoff Context Protocol](/prompt-context-patterns/catalog/categories/patterns-advanced-orchestration-zh#pattern-36-handoff-context-protocol) | Agent 间统一上下文传递 |
| 37 | [Context Efficiency Rule](/prompt-context-patterns/catalog/categories/patterns-advanced-orchestration-zh#pattern-37-context-efficiency-rule-orchestrator-reads-nothing) | 编排器上下文保持清洁 |
| 38 | [Complexity-Tiered Dispatch](/prompt-context-patterns/catalog/categories/patterns-advanced-orchestration-zh#pattern-38-complexity-tiered-dispatch) | 按任务复杂度匹配 Agent 管道 |
| 39 | [Persistent Team with Message Board](/prompt-context-patterns/catalog/categories/patterns-advanced-orchestration-zh#pattern-39-persistent-team-with-message-board) | 状态文件实现跨 Agent 讨论 |
| 40 | [Delegation to Cloud Agent](/prompt-context-patterns/catalog/categories/patterns-advanced-orchestration-zh#pattern-40-delegation-to-cloud-agent-via-work-item) | 工作项作为 Agent 分配机制 |
| 41 | [Loop Prevention with Max Iterations](/prompt-context-patterns/catalog/categories/patterns-advanced-orchestration-zh#pattern-41-loop-prevention-with-max-iterations) | 硬性停止防止无限 Agent 循环 |
| 42 | [Agent Memory Isolation](/prompt-context-patterns/catalog/categories/patterns-advanced-orchestration-zh#pattern-42-agent-memory-isolation) | 防止跨 Agent 影响和注入 |
| 43 | [Sparse Git Worktree for Review](/prompt-context-patterns/catalog/categories/patterns-advanced-orchestration-zh#pattern-43-sparse-git-worktree-for-isolated-review) | Monorepo 安全的隔离文件访问 |
| 44 | [Severity Promotion/Demotion by Area](/prompt-context-patterns/catalog/categories/patterns-advanced-orchestration-zh#pattern-44-severity-promotiondemotion-by-area) | 将组织风险偏好编入提示词 |

### 第 9 类：高级质量与评估 (/prompt-context-patterns/catalog/categories/patterns-advanced-quality-zh)

| # | 模式 | 核心价值 |
|---|------|----------|
| 45 | [Directive-Based Review with on_fail](/prompt-context-patterns/catalog/categories/patterns-advanced-quality-zh#pattern-45-directive-based-review-with-on_fail-classification) | 每个维度三向分类：Pass/Review/Fail |
| 46 | [Multi-Stage Repo Discovery Before Review](/prompt-context-patterns/catalog/categories/patterns-advanced-quality-zh#pattern-46-multi-stage-repo-discovery-before-review) | 评审校准到仓库惯例 |
| 47 | [Evidence-First Review](/prompt-context-patterns/catalog/categories/patterns-advanced-quality-zh#pattern-47-evidence-first-review-demonstrate-dont-cite-rules) | "展示，而非引用规则" — 可操作的 Bug |
| 48 | [Rule-Catalog Review (YAML)](/prompt-context-patterns/catalog/categories/patterns-advanced-quality-zh#pattern-48-rule-catalog-review-hierarchical-yaml) | 版本化、可审计、独立可更新的规则 |
| 49 | [Blast Radius & Impact Formulas](/prompt-context-patterns/catalog/categories/patterns-advanced-quality-zh#pattern-49-blast-radius--on-call-impact-formulas) | 量化运维影响评分 |
| 50 | [Adversarial Triad + Counterarguments](/prompt-context-patterns/catalog/categories/patterns-advanced-quality-zh#pattern-50-adversarial-triad-with-counterargument-phase) | 两轮评审消除群体思维 |
| 51 | [Schema Validation Gate](/prompt-context-patterns/catalog/categories/patterns-advanced-quality-zh#pattern-51-schema-validation-gate) | 机器强制的输出格式合规 |
| 52 | [LLM-as-Judge (8 Scenarios)](/prompt-context-patterns/catalog/categories/patterns-advanced-quality-zh#pattern-52-llm-as-judge-evaluation-scenarios-8-types) | 完整评估工具箱，含元评判 |
| 53 | [Retrospective Quality Rubric](/prompt-context-patterns/catalog/categories/patterns-advanced-quality-zh#pattern-53-retrospective-quality-rubric-incident-postmortem) | 事后复盘的反模式/模式对 |
| 54 | [Test Scaffolding + Convention Enforcement](/prompt-context-patterns/catalog/categories/patterns-advanced-quality-zh#pattern-54-test-scaffolding-with-convention-enforcement) | 完整测试生成 + 反模式表 |
| 55 | [Smart Triage-Skip with Model Tracking](/prompt-context-patterns/catalog/categories/patterns-advanced-quality-zh#pattern-55-smart-triage-skip-with-model-tracking) | 防止重复分诊，支持模型升级 |

### 第 10 类：高级安全与合规 (/prompt-context-patterns/catalog/categories/patterns-advanced-safety-zh)

| # | 模式 | 核心价值 |
|---|------|----------|
| 56 | [MCP-Response-as-Data Guardrail](/prompt-context-patterns/catalog/categories/patterns-advanced-safety-zh#pattern-56-mcp-response-as-data-guardrail) | 防止基础设施细节泄露 |
| 57 | [Prompt-Injection-as-Security-Finding](/prompt-context-patterns/catalog/categories/patterns-advanced-safety-zh#pattern-57-prompt-injection-as-security-finding) | 将攻击转化为可操作的评审发现 |
| 58 | [Prosecutor-Defender-Judge Architecture](/prompt-context-patterns/catalog/categories/patterns-advanced-safety-zh#pattern-58-prosecutor-defender-judge-architecture) | 对抗性审计 + 准确性指标 |
| 59 | [Rescue-Tag-Before-Destructive-Operation](/prompt-context-patterns/catalog/categories/patterns-advanced-safety-zh#pattern-59-rescue-tag-before-destructive-operation) | 所有破坏性操作自动创建撤销点 |
| 60 | [Tiered Permission Model (RED/DEFER/GREEN)](/prompt-context-patterns/catalog/categories/patterns-advanced-safety-zh#pattern-60-tiered-permission-model-red--defer--green) | 三级风险分类 + 预检分析 |
| 61 | [Data Classification Matrix (4-Level)](/prompt-context-patterns/catalog/categories/patterns-advanced-safety-zh#pattern-61-data-classification-matrix-4-level) | 明确的敏感度分类 + 工具特定规则 |
| 62 | [XPIA Defense Model](/prompt-context-patterns/catalog/categories/patterns-advanced-safety-zh#pattern-62-xpia-defense-model-cross-plugin-injection-attack) | 跨插件注入攻击的四层防御 |
| 63 | [Severity Rubric with Litmus Tests](/prompt-context-patterns/catalog/categories/patterns-advanced-safety-zh#pattern-63-severity-rubric-with-litmus-tests) | "凌晨 3 点你会叫人起来吗？" — 校准锚点 |
| 64 | [Security Posture Delta Analysis](/prompt-context-patterns/catalog/categories/patterns-advanced-safety-zh#pattern-64-security-posture-delta-analysis) | 代码 + 基础设施关联分析真实风险 |
| 65 | [Confidence-Gated Reporting](/prompt-context-patterns/catalog/categories/patterns-advanced-safety-zh#pattern-65-confidence-gated-reporting) | 非对称阈值：安全发现门槛更低 |
| 66 | [System-Prompt Non-Disclosure](/prompt-context-patterns/catalog/categories/patterns-advanced-safety-zh#pattern-66-system-prompt-non-disclosure) | 禁止泄露 Agent 配置 |
| 67 | [40-Point Skill Security Checklist](/prompt-context-patterns/catalog/categories/patterns-advanced-safety-zh#pattern-67-40-point-security-skill-review-checklist) | 插件市场的供应链防御 |
| 68 | [Orchestrator-Only (No Direct Data)](/prompt-context-patterns/catalog/categories/patterns-advanced-safety-zh#pattern-68-orchestrator-only-pattern-no-direct-data-processing) | LLM 永不接触原始 PII；由工具处理数据 |
| 69 | [Policy-as-Data (Declarative YAML)](/prompt-context-patterns/catalog/categories/patterns-advanced-safety-zh#pattern-69-policy-as-data-declarative-yaml-configs) | 合规规则与 Agent 代码解耦 |

### 第 11 类：高级工作流与自主性 (/prompt-context-patterns/catalog/categories/patterns-advanced-workflow-zh)

| # | 模式 | 核心价值 |
|---|------|----------|
| 70 | [State File as Sole Continuity](/prompt-context-patterns/catalog/categories/patterns-advanced-workflow-zh#pattern-70-state-file-as-sole-continuity-mechanism) | 桥接隔离的 Agent 上下文窗口 |
| 71 | [Zero-Questions Triage](/prompt-context-patterns/catalog/categories/patterns-advanced-workflow-zh#pattern-71-zero-questions-triage-maximum-autonomy) | 95 秒内完全自主分析 |
| 72 | [Pull-Based Kanban Orchestration](/prompt-context-patterns/catalog/categories/patterns-advanced-workflow-zh#pattern-72-pull-based-kanban-orchestration) | Agent 按亲和力拉取任务，范围蔓延时分叉 |
| 73 | [Deployment State Machine (Idempotent)](/prompt-context-patterns/catalog/categories/patterns-advanced-workflow-zh#pattern-73-deployment-state-machine-statelessre-entrantidempotent) | 崩溃可恢复的无状态部署处理器 |
| 74 | [Autonomous PR Feedback Resolution](/prompt-context-patterns/catalog/categories/patterns-advanced-workflow-zh#pattern-74-autonomous-pr-feedback-resolution) | Agent 实现或驳回评审意见 |
| 75 | [11-Phase Autonomous Dev Flow](/prompt-context-patterns/catalog/categories/patterns-advanced-workflow-zh#pattern-75-11-phase-autonomous-development-flow) | 从任务到部署的端到端流程，带防护栏 |
| 76 | [Staggered Burst Query + Rate Limits](/prompt-context-patterns/catalog/categories/patterns-advanced-workflow-zh#pattern-76-staggered-burst-query-with-rate-limit-respect) | 跨服务器反并行防止级联故障 |
| 77 | [Time-Boxed Investigation](/prompt-context-patterns/catalog/categories/patterns-advanced-workflow-zh#pattern-77-time-boxed-investigation-with-partial-results) | 硬性时间预算 + 部分结果报告 |
| 78 | [Deployment Override Knowledge Encoding](/prompt-context-patterns/catalog/categories/patterns-advanced-workflow-zh#pattern-78-deployment-override-knowledge-encoding) | 完整 override 分类用于精准查询 |
| 79 | [Incident Escalation Decision Matrix](/prompt-context-patterns/catalog/categories/patterns-advanced-workflow-zh#pattern-79-incident-escalation-decision-matrix) | 严重级别和升级的量化阈值 |
| 80 | [Scope Estimation Checkpoints](/prompt-context-patterns/catalog/categories/patterns-advanced-workflow-zh#pattern-80-scope-estimation-and-re-estimation-checkpoints) | 在 25/50/75% 时重新估算，捕捉范围蔓延 |

### 第 12 类：高级输入/输出与领域特化 (/prompt-context-patterns/catalog/categories/patterns-advanced-io-domain-zh)

| # | 模式 | 核心价值 |
|---|------|----------|
| 81 | [NL to Relational Schema Decomposition](/prompt-context-patterns/catalog/categories/patterns-advanced-io-domain-zh#pattern-81-natural-language-to-relational-schema-decomposition) | 教模型推导 Schema，而非仅嵌入 |
| 82 | [Chart Decision Tree + Anti-Pattern Guards](/prompt-context-patterns/catalog/categories/patterns-advanced-io-domain-zh#pattern-82-chart-decision-tree-with-anti-pattern-guards) | 数据形状到可视化 + 基数防护 |
| 83 | [Audience-Purpose Content Calibration](/prompt-context-patterns/catalog/categories/patterns-advanced-io-domain-zh#pattern-83-audience-purpose-driven-content-calibration) | 输出格式/详细度由受众和目的驱动 |
| 84 | [Socratic Investigation Loop](/prompt-context-patterns/catalog/categories/patterns-advanced-io-domain-zh#pattern-84-socratic-investigation-loop-with-active-research) | 主动研究 + 苏格拉底式提问引导发现 |
| 85 | [Knowledge Base Index + Intent Routing](/prompt-context-patterns/catalog/categories/patterns-advanced-io-domain-zh#pattern-85-knowledge-base-index-with-intent-to-source-routing) | 两级检索：轻量索引 → 选择性深读 |
| 86 | [Heuristic Scoring with Signal Detection](/prompt-context-patterns/catalog/categories/patterns-advanced-io-domain-zh#pattern-86-heuristic-scoring-with-signal-detection) | 机器可检测信号替代主观标签 |
| 87 | [Eager Incremental Materialization](/prompt-context-patterns/catalog/categories/patterns-advanced-io-domain-zh#pattern-87-eager-incremental-materialization) | 对话过程中就创建产出物，而非结束后 |
| 88 | [Data Shape to Query Pattern Detection](/prompt-context-patterns/catalog/categories/patterns-advanced-io-domain-zh#pattern-88-data-shape-to-query-pattern-detection) | 从数据列 + 查询文本推断可视化 |
| 89 | [Writability Rules + Substitution Tables](/prompt-context-patterns/catalog/categories/patterns-advanced-io-domain-zh#pattern-89-writability-rules-and-linguistic-substitution-tables) | 完整的风格转换 + 检测启发式 |
| 90 | [Cross-Platform Compatibility Matrix](/prompt-context-patterns/catalog/categories/patterns-advanced-io-domain-zh#pattern-90-cross-platform-surface-compatibility-matrix) | 来源/目标降级路径 + 有限重试 |
| 91 | [Hub-Spoke Router with Overlap Resolution](/prompt-context-patterns/catalog/categories/patterns-advanced-io-domain-zh#pattern-91-hub-spoke-domain-router-with-overlap-resolution) | 多级特异性级联用于消歧 |

### 第 13 类：补充 — 入职、生产力、迁移与创意 (/prompt-context-patterns/catalog/categories/patterns-gap-fills-zh)

| # | 模式 | 核心价值 |
|---|------|----------|
| 92 | [DAG Journey with Typed Gates](/prompt-context-patterns/catalog/categories/patterns-gap-fills-zh#pattern-92-dag-journey-with-typed-gates) | 非线性入职 + 手动门控和回填 |
| 93 | [Multi-Source Evidence Harvest + Goal Synthesis](/prompt-context-patterns/catalog/categories/patterns-gap-fills-zh#pattern-93-multi-source-evidence-harvest-with-goal-aligned-synthesis) | 6+ 源并行采集 + 受众分层输出 |
| 94 | [Promise Detection and KB Sync](/prompt-context-patterns/catalog/categories/patterns-gap-fills-zh#pattern-94-promise-detection-and-knowledge-base-sync) | 从对话中提取隐含承诺 |
| 95 | [Mandatory Self-Learning After Failure](/prompt-context-patterns/catalog/categories/patterns-gap-fills-zh#pattern-95-mandatory-self-learning-after-failure-resolution) | 每次错误解决后知识库都会增长 |
| 96 | [Risk-Ordered Batch Migration + Build-Verify](/prompt-context-patterns/catalog/categories/patterns-gap-fills-zh#pattern-96-risk-ordered-batch-migration-with-build-verify-loops) | 批量迁移 + 相同错误签名回滚 |
| 97 | [PII-Motivated Delivery Restriction](/prompt-context-patterns/catalog/categories/patterns-gap-fills-zh#pattern-97-pii-motivated-delivery-restriction) | 绝对的交付渠道限制，不可覆盖 |
| 98 | [Audience-Register Translation Review](/prompt-context-patterns/catalog/categories/patterns-gap-fills-zh#pattern-98-audience-register-translation-review-with-matched-frameworks) | 工程师到高管的评审 + 匹配框架 |
| 99 | [Automated Accessibility Post-Processing](/prompt-context-patterns/catalog/categories/patterns-gap-fills-zh#pattern-99-automated-accessibility-post-processing-pipeline) | 无障碍管道 + 25 项断言评估 |

### 第 14 类：开源技能模式 (/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh)

| # | 模式 | 核心价值 |
|---|------|----------|
| 100 | [Progressive Disclosure Architecture](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh#pattern-100-progressive-disclosure-architecture) | 3 级上下文加载，最小化 token 浪费 |
| 101 | [Creative Philosophy Scaffolding](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh#pattern-101-creative-philosophy-scaffolding) | 强制先有概念深度，再执行视觉 |
| 102 | [Mandatory Refinement Pass](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh#pattern-102-mandatory-refinement-pass) | 自我施加的质量门控 + 情感锚定 |
| 103 | [Reconnaissance-Then-Action](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh#pattern-103-reconnaissance-then-action) | 先观察状态再行动，防止盲目交互 |
| 104 | [Helper Script as Black Box](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh#pattern-104-helper-script-as-black-box) | 脚本封装复杂性；模型先用 --help |
| 105 | [Anti-Slop Design Guidelines](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh#pattern-105-anti-slop-design-guidelines) | 命名 AI 反模式 + 具体替代方案 |
| 106 | [Section-by-Section Collaborative Drafting](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh#pattern-106-section-by-section-collaborative-drafting) | 迭代式逐段构建 + 用户审批 |
| 107 | [Reader Testing with Sub-Agent](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh#pattern-107-reader-testing-with-sub-agent) | 派生天真读者子 Agent 做新鲜视角评审 |
| 108 | [Blind A/B Comparison](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh#pattern-108-blind-ab-comparison) | 双盲技能评估消除偏见 |
| 109 | [Composio 3-Step SaaS Integration](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh#pattern-109-composio-3-step-saas-integration) | 通用 Search-Connect-Execute 适配任何 SaaS API |
| 110 | [Algorithm-as-Domain Knowledge](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh#pattern-110-algorithm-as-domain-knowledge) | 将实际系统内部机制嵌入提示词知识 |
| 111 | [Clarifying Questions Before Action](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh#pattern-111-clarifying-questions-before-action) | 行动前的定向参数收集提问 |
| 112 | [Output Format with Populated Example](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh#pattern-112-output-format-with-populated-example) | 完整真实输出，而非抽象 Schema |
| 113 | [Multi-Workflow Routing by Input Type](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh#pattern-113-multi-workflow-routing-by-input-type) | 同一技能按输入路由创建/读取/编辑 |
| 114 | [Font/Asset Bundling with Directory Reference](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh#pattern-114-fontasset-bundling-with-directory-reference) | 相对路径捆绑资源，无需下载 |
| 115 | [QA Sub-Agent with Visual Verification](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh#pattern-115-qa-sub-agent-with-visual-verification) | 派生子 Agent 截图并检查输出 |
| 116 | [Never-Hardcode Financial Rules](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh#pattern-116-never-hardcode-financial-rules) | 所有计算值必须使用公式 |
| 117 | [Multi-Language SDK Routing](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh#pattern-117-multi-language-sdk-routing) | 检测语言，仅加载对应语言的文档 |
| 118 | [Surface Selection by Architecture](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh#pattern-118-surface-selection-by-architecture) | 按需求路由到单次调用/工作流/Agent |
| 119 | [Eval-Driven Skill Improvement Loop](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh#pattern-119-eval-driven-skill-improvement-loop) | 提示词的 TDD：写测试 → 评分 → 改进 |
| 120 | [Non-Anthropic Provider Guard](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh#pattern-120-non-anthropic-provider-guard) | 导入非 Anthropic 生态时提前退出 |

### 第 15-16 类：Claude Code 平台模式 (patterns-claude-code-platform*.md)

| # | 模式 | 核心价值 |
|---|------|----------|
| 121 | [Typed Memory Taxonomy](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-zh#pattern-121-typed-memory-taxonomy) | 四种记忆类型 + 不同写入触发器和过期规则 |
| 122 | [Bidirectional Feedback Capture](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-zh#pattern-122-bidirectional-feedback-capture) | 同时记录纠正和确认，防止行为漂移 |
| 123 | [Reversibility x Blast-Radius](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-zh#pattern-123-reversibility--blast-radius-permission-model) | 2x2 权限矩阵 + 非粘性审批 |
| 124 | [Tool Preference with Hard Routing](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-zh#pattern-124-tool-preference-hierarchy-with-hard-routing) | 有专用工具时禁用 shell 等效命令 |
| 125 | [Cache-Aware Scheduling](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-zh#pattern-125-cache-aware-scheduling) | 围绕 prompt cache TTL 死区调度延迟 |
| 126 | [Agent Briefing Protocol](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-zh#pattern-126-agent-briefing-protocol) | "像同事一样简报" + 永不委托理解 |
| 127 | [Parallel-Safe Step Identification](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-zh#pattern-127-parallel-safe-step-identification) | 为多步工作流标注并行性标记 |
| 128 | [Context Compaction Survival](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-zh#pattern-128-context-compaction-survival-protocol) | 上下文压缩时需保留的命名字段 |
| 129 | [Non-Sticky Authorization](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-zh#pattern-129-non-sticky-authorization-scope) | 审批限定在特定请求，而非操作类别 |
| 130 | [Investigate Before Destroying](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-zh#pattern-130-investigate-before-destroying) | 破坏性捷径前先调查根因 |
| 131 | [Output Visibility Awareness](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-zh#pattern-131-output-visibility-awareness) | 工具调用对用户不可见，用文本沟通 |
| 132 | [Hook-Driven Automation](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-zh#pattern-132-hook-driven-automation-awareness) | Hook 反馈视为用户输入；适应，不重试 |
| 133 | [Compositional Prompt Assembly](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-extended-zh#pattern-133-compositional-prompt-assembly) | 小型版本化片段条件组装 |
| 134 | [Tool-Constraint Boundaries](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-extended-zh#pattern-134-tool-constraint-agent-boundaries) | 从 Agent 移除工具，而非仅指令禁止 |
| 135 | [Fork vs Fresh Spawning](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-extended-zh#pattern-135-fork-vs-fresh-spawning-strategy) | 缓存共享 fork vs 独立 fresh Agent |
| 136 | [Security Monitor Agent](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-extended-zh#pattern-136-security-monitor-agent-dedicated-threat-classifier) | 独立 Agent 评估每个动作的威胁模型 |
| 137 | [Analysis-First Compaction](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-extended-zh#pattern-137-analysis-first-compaction) | 在分析标签中思考后再生成摘要 |
| 138 | [Team Task Board](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-extended-zh#pattern-138-team-task-board-coordination) | 共享任务列表 + Agent 间异步消息 |
| 139 | [Background Job Narration](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-extended-zh#pattern-139-background-job-narration-protocol) | 机器可解析的完成信号供分类器使用 |
| 140 | [Autonomous Trust Calibration](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-extended-zh#pattern-140-autonomous-trust-calibration) | "管家而非发起者" — 按影响半径调整信任 |
| 141 | [REPL as Tool Composition](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-extended-zh#pattern-141-repl-as-tool-composition-layer) | JavaScript 层实现工具调用的循环/分支 |
| 142 | [Immutable Memory + Dream](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-extended-zh#pattern-142-immutable-memory-with-dream-consolidation) | 不可编辑的记忆文件 + 定期整合 Agent |

---

## 分类文件

<a id="cat-1"></a>
### [第 1 类：结构脚手架](/prompt-context-patterns/catalog/categories/patterns-structural-scaffolding-zh)
技能提示词的组织方式 — 承载一切的骨架。

**模式：** YAML Frontmatter (1), Phased Execution (2), Workflow Mode Branching (3), $ARGUMENTS Variable (4)

<a id="cat-2"></a>
### [第 2 类：执行控制](/prompt-context-patterns/catalog/categories/patterns-execution-control-zh)
如何引导 Agent 行为 — 人设、约束、交互模式和检查点。

**模式：** Persona/Role Assignment (5), Negative Constraints (6), Interactive Flow Control (7), Confirmation Gates (8), Progress Feedback (9)

<a id="cat-3"></a>
### [第 3 类：安全与信任](/prompt-context-patterns/catalog/categories/patterns-safety-and-trust-zh)
防止 Agent 造成伤害的防护栏 — 注入防御、数据脱敏、边界和范围。

**模式：** Prompt Injection Defense (10), Sensitive Data Redaction (11), Read-Only Boundary (12), Activation Scope (13)

<a id="cat-4"></a>
### [第 4 类：输入/输出契约](/prompt-context-patterns/catalog/categories/patterns-input-output-contracts-zh)
数据如何流入流出 — 输出模板、错误处理、配置和平台适配。

**模式：** Structured Output Templates (14), Error Handling (15), Configuration Persistence (16), Cross-Platform (17)

<a id="cat-5"></a>
### [第 5 类：Agent 编排](/prompt-context-patterns/catalog/categories/patterns-agent-orchestration-zh)
多个 Agent 如何协调 — 拓扑、技能组合、路由、工具映射和共识。

**模式：** Multi-Agent Orchestration (18), Skill Composition (19), Intent Classification (20), Tool Routing Tables (21), Dedup/Consensus (22)

<a id="cat-6"></a>
### [第 6 类：知识与上下文](/prompt-context-patterns/catalog/categories/patterns-knowledge-and-context-zh)
信息如何管理 — 参考文件、领域知识、示例和证据要求。

**模式：** Reference File Injection (23), Domain Knowledge Embedding (24), Few-Shot Examples (25), Evidence Chain (26)

<a id="cat-7"></a>
### [第 7 类：质量与反馈](/prompt-context-patterns/catalog/categories/patterns-quality-and-feedback-zh)
如何确保输出质量 — 评分标准、自我批评、反馈循环和版本管理。

**模式：** Scoring Rubrics (27), Self-Critique (28), Feedback Solicitation (29), Version Check (30)

<a id="cat-8"></a>
### [第 8 类：高级 Agent 编排](/prompt-context-patterns/catalog/categories/patterns-advanced-orchestration-zh)
生产级多 Agent 架构 — 状态机、共识网格、对抗性规划、成本优化路由、记忆隔离。

**模式：** Adversarial Persona (31), Hub-and-Spoke State Machine (32), Cross-Model Consensus (33), Adversarial Planning (34), Model Routing (35), Handoff Context (36), Context Efficiency (37), Complexity Tiers (38), Message Board (39), Cloud Delegation (40), Loop Prevention (41), Memory Isolation (42), Sparse Worktree (43), Severity Promotion (44)

<a id="cat-9"></a>
### [第 9 类：高级质量与评估](/prompt-context-patterns/catalog/categories/patterns-advanced-quality-zh)
深度评审架构 — 指令式评审、证据优先分析、对抗性三人组、LLM-as-judge、测试脚手架。

**模式：** Directive Review (45), Repo Discovery (46), Evidence-First (47), Rule Catalog (48), Impact Formulas (49), Adversarial Triad (50), Schema Gate (51), LLM-as-Judge (52), Retro Rubric (53), Test Scaffolding (54), Triage Skip (55)

<a id="cat-10"></a>
### [第 10 类：高级安全与合规](/prompt-context-patterns/catalog/categories/patterns-advanced-safety-zh)
生产级安全 — MCP 数据防护栏、XPIA 防御、控诉-辩护-裁判、数据分类、策略即数据。

**模式：** MCP-Data Guardrail (56), Injection-as-Finding (57), Prosecutor-Defender-Judge (58), Rescue Tags (59), Tiered Permissions (60), Data Classification (61), XPIA Defense (62), Litmus Tests (63), Posture Delta (64), Confidence Gates (65), Non-Disclosure (66), Skill Security Checklist (67), Orchestrator-Only (68), Policy-as-Data (69)

<a id="cat-11"></a>
### [第 11 类：高级工作流与自主性](/prompt-context-patterns/catalog/categories/patterns-advanced-workflow-zh)
规模化执行控制 — 状态文件、零提问分诊、看板编排、自主开发、事件响应。

**模式：** State File Continuity (70), Zero-Questions (71), Kanban Pull (72), Deployment State Machine (73), PR Feedback Resolution (74), Autonomous Dev Flow (75), Burst Query (76), Time-Boxed Investigation (77), Override Knowledge (78), Escalation Matrix (79), Scope Checkpoints (80)

<a id="cat-12"></a>
### [第 12 类：高级输入/输出与领域特化](/prompt-context-patterns/catalog/categories/patterns-advanced-io-domain-zh)
输入/输出转换、领域推理脚手架、可视化指令、交互式推理、风格转换和受众适配。

**模式：** Schema Decomposition (81), Chart Decision Tree (82), Audience Calibration (83), Socratic Loop (84), KB Index Routing (85), Heuristic Scoring (86), Eager Materialization (87), Data Shape Detection (88), Writability Rules (89), Compatibility Matrix (90), Overlap Resolution Router (91)

<a id="cat-13"></a>
### [第 13 类：补充 — 入职、生产力、迁移与创意](/prompt-context-patterns/catalog/categories/patterns-gap-fills-zh)
来自覆盖不足领域的模式：基于 DAG 的入职旅程、个人生产力、自学习迁移和创意输出无障碍。

**模式：** DAG Journey (92), Evidence Harvest (93), Promise Detection (94), Self-Learning (95), Batch Migration (96), Delivery Restriction (97), Register Translation Review (98), A11y Post-Processing (99)

<a id="cat-14"></a>
### [第 14 类：开源技能模式](/prompt-context-patterns/catalog/categories/patterns-open-source-skills-zh)
提取自 Anthropic 官方 Agent Skills 仓库（17 个技能）和 ComposioHQ 社区精选 awesome-claude-skills 仓库（32 个独立 + 832 个 Composio 模板技能）。涵盖渐进式披露、创意脚手架、视觉 QA、评估驱动改进、SaaS 集成模板和多语言 SDK 路由。

**模式：** Progressive Disclosure (100), Creative Philosophy (101), Refinement Pass (102), Reconnaissance-Then-Action (103), Helper Script Black Box (104), Anti-Slop (105), Collaborative Drafting (106), Reader Testing (107), Blind A/B (108), SaaS Integration (109), Algorithm-as-Knowledge (110), Clarifying Questions (111), Populated Examples (112), Input-Type Routing (113), Asset Bundling (114), Visual QA (115), Never-Hardcode (116), Language Routing (117), Architecture Selection (118), Eval-Driven Loop (119), Provider Guard (120)

**架构配套文件：** [skill-architecture-patterns.md](/prompt-context-patterns/catalog/techniques/skill-architecture-zh) — 技能打包、市场分组、参考文件组织、子 Agent 设计、脚本集成和跨仓库对比。

<a id="cat-15"></a>
### [第 15 类：Claude Code 平台模式](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-zh)
提取自 Claude Code 系统提示词的模式 — 平台级关注点：记忆分类、权限模型、调度、工具路由、Agent 调度和上下文存活。

**模式：** Typed Memory Taxonomy (121), Bidirectional Feedback Capture (122), Reversibility x Blast-Radius (123), Tool Preference with Hard Routing (124), Cache-Aware Scheduling (125), Agent Briefing Protocol (126), Parallel-Safe Step Identification (127), Context Compaction Survival (128), Non-Sticky Authorization (129), Investigate Before Destroying (130), Output Visibility Awareness (131), Hook-Driven Automation (132)

<a id="cat-16"></a>
### [第 16 类：Claude Code 平台模式 — 扩展](/prompt-context-patterns/catalog/categories/patterns-claude-code-platform-extended-zh)
来自 Claude Code 可组合提示词系统的更深层架构模式：Agent 派生、安全分类、团队协调和记忆整合。

**模式：** Compositional Prompt Assembly (133), Tool-Constraint Agent Boundaries (134), Fork vs Fresh Spawning (135), Security Monitor Agent (136), Analysis-First Compaction (137), Team Task Board Coordination (138), Background Job Narration (139), Autonomous Trust Calibration (140), REPL as Tool Composition Layer (141), Immutable Memory with Dream Consolidation (142)

---

## 与基础技术的映射关系

30 个模式如何对应 [prompt-engineering-for-skills.md](/prompt-context-patterns/catalog/techniques/token-level-techniques-zh) 中的 9 个基础技术：

| 基础技术 | 应用该技术的模式 |
|----------|-----------------|
| **决策树** | Workflow Mode Branching (3), Intent Classification (20), Error Handling (15), Input-Type Routing (113), Language Routing (117), Architecture Selection (118) |
| **锚定** | Domain Knowledge Embedding (24), Few-Shot Examples (25), Structured Output Templates (14), Populated Examples (112), Algorithm-as-Knowledge (110), Reconnaissance-Then-Action (103) |
| **认知卸载** | Phased Execution (2), Evidence Chain (26), Scoring Rubrics (27), Helper Script Black Box (104), Collaborative Drafting (106), Eval-Driven Loop (119) |
| **注意力局部性** | Negative Constraints (6), Reference File Injection (23), Tool Routing Tables (21), Progressive Disclosure (100) |
| **指令-动作绑定** | Confirmation Gates (8), Interactive Flow Control (7), Progress Feedback (9), Clarifying Questions (111) |
| **Schema 预设** | YAML Frontmatter (1), Structured Output Templates (14), Scoring Rubrics (27), Populated Examples (112) |
| **负空间** | Negative Constraints (6), Activation Scope (13), Read-Only Boundary (12), Anti-Slop (105), Provider Guard (120), Never-Hardcode (116) |
| **XML 语义边界** | Structured Output Templates (14), Few-Shot Examples (25), Domain Knowledge (24), Creative Philosophy (101) |
| **带推理的示例** | Few-Shot Examples (25), Evidence Chain (26), Self-Critique (28), Blind A/B (108), Refinement Pass (102) |

---

## 数据来源

提取自对 500+ 生产级 AI Agent 插件的分析，覆盖 DevOps、安全、迁移和事件响应领域，以及 Anthropic 官方 Agent Skills 仓库（17 个技能）和 ComposioHQ 社区精选 awesome-claude-skills 仓库（32 个独立 + 832 个 Composio 模板技能）。
