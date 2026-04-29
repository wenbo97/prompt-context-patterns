# 高级工作流、执行控制与自治模式

工作流编排、状态机、事件响应、部署管线、监控、规划和自治 agent 行为的深度模式 — 在 500+ 插件中发现的生产级架构，扩展了基础执行模式（5-9）。

**来源研究：** 从 DevOps、安全、迁移和事件响应领域的 500+ 生产级 AI agent 插件分析中提取。

---

## Pattern 70: State File as Sole Continuity Mechanism

**出现频率：** 约 2% 的插件
**相关模式：** [Configuration Persistence](#pattern-16), [Persistent Team with Message Board](#pattern-39)

**定义：** 多 agent 管线的每个阶段读写一个共享 markdown/JSON 状态文件，因为 agent 运行在隔离的上下文窗口中没有共享内存。状态文件是阶段之间信息流动的唯一方式。

### 正面示例

```markdown
Every phase reads the state file at start and writes updated state at end.
The state file is the SOLE continuity mechanism between phases.

State file structure:
- Phase status (pending/in-progress/completed/failed)
- Phase artifacts (file paths, PR URLs, work item IDs)
- Accumulated decisions and context
- Error state for recovery

Recovery: If a phase fails, the next invocation reads the state file
and resumes from the last completed phase, not from the beginning.
```

**为什么有效：** Agent 没有共享内存 — 状态文件桥接上下文窗口。结构化阶段状态支持从失败点恢复而无需重新运行已完成阶段。累积的决策防止上下文丢失。

### 反面示例

```markdown
Each phase passes its results to the next phase via the return value.
If a phase fails, restart the entire pipeline from the beginning.
```

**为什么失败：** 返回值仅存在于单个上下文窗口内 — 下一个 agent 在新会话中启动时那些值就消失了。从头重启浪费已完成阶段的所有工作，且在失败阶段不确定时会创建无限重试循环。

---

## Pattern 71: Zero-Questions Triage (Maximum Autonomy)

**出现频率：** <1% 的插件
**相关模式：** [Interactive Flow Control](#pattern-7), [Confirmation Gates](#pattern-8)

**定义：** 零用户交互的固定协议，带硬时间预算和尊重外部速率限制的交错突发查询。agent 必须在严格时间约束内自主完成全部分析。

### 正面示例

```markdown
Total time budget: 95 seconds
- Phase 1 (Data Gathering): 30s — staggered burst queries (max 3 concurrent)
- Phase 2 (Correlation): 25s — cross-reference all signals
- Phase 3 (Impact Assessment): 20s — quantified customer impact
- Phase 4 (Triage Decision): 20s — severity, routing, immediate actions

Zero user interaction during execution.
Respect external rate limits: stagger MCP calls, max 3 concurrent.
If a data source times out, proceed with available data — note gap.
```

**为什么有效：** 时间预算防止无边界分析。零交互意味着 agent 可以被自动触发（如事件告警）。速率限制尊重防止 agent 依赖的工具中出现级联故障。

### 反面示例

```markdown
Gather all available data before making any triage decision.
Ask the oncall engineer for clarification if any signal is ambiguous.
Query all data sources in parallel for maximum speed.
```

**为什么失败：** "All available data"没有时间边界，agent 可能在事件恶化时花数分钟追逐边际信号。需要人类澄清阻塞了自主执行。无限制并行查询会触发速率限制，导致 MCP 工具的级联故障。

---

## Pattern 72: Pull-Based Kanban Orchestration

**出现频率：** <1% 的插件
**相关模式：** [Multi-Agent Orchestration](#pattern-18), [Complexity-Tiered Dispatch](#pattern-38)

**定义：** Kanban 式工作系统，agent 基于亲和性（匹配其专长）拉取任务而非由编排器推送。包含两层 Ready Gate、动态扩展的 fork 协议和范围升级规则。

### 正面示例

```markdown
Two-Tier Ready Gate:
- Tier 1: Task has clear acceptance criteria AND no blockers
- Tier 2: Task is scoped to ≤ 2 hours of work for one agent

Pull Assignment by Affinity:
- Each agent has skill tags (frontend, backend, infra, test)
- Agents pull tasks matching their affinity from the Ready queue
- If no affinity match, any available agent can pull

Fork Protocol:
- If task exceeds 4 hours estimate, fork into sub-tasks
- Sub-tasks inherit parent's priority but get independent Ready Gate checks
- Original task moves to "Waiting for subtasks" column

Scope Escalation:
- If agent discovers task is larger than estimated, escalate to coordinator
- Coordinator decides: re-scope, fork, or reassign

8 Prompt-Enforced Invariants with Detection/Recovery:
1. No task may bypass Ready Gate
2. No agent may hold > 2 tasks simultaneously
3. Every task must have an owner before leaving Ready
...
```

**为什么有效：** 拉取式分配自然匹配任务到最适合的 agent。两层 Ready Gate 防止定义不清的任务消耗 agent 时间。Fork 协议动态处理范围蔓延。带检测/恢复的不变量防止系统状态损坏。

### 反面示例

```markdown
The orchestrator assigns tasks to agents round-robin.
If a task is too large, the agent should try its best to complete it.
Agents can pick up as many tasks as needed to stay busy.
```

**为什么失败：** 轮询忽略 agent 专长，前端任务可能落在基础设施 agent 上。没有 fork 协议，超大任务无限期阻塞 agent。不限制并发任务数意味着一个 agent 可能囤积工作而其他空闲，且同时处理太多上下文时质量下降。

---

## Pattern 73: Deployment State Machine (Stateless/Re-entrant/Idempotent)

**出现频率：** 约 1% 的插件
**相关模式：** [Hub-and-Spoke State Machine](#pattern-32), [Error Handling](#pattern-15)

**定义：** 部署工作流的详细状态机，其中处理器并发运行，系统被设计为无状态、可重入和幂等 — 任何处理器可以崩溃和重启而不损坏状态。

### 正面示例

```markdown
States: QUEUED → VALIDATING → BUILDING → TESTING → STAGING → CANARY → PRODUCTION → COMPLETED
         ↘ FAILED (from any state)
         ↘ ROLLING_BACK (from CANARY or PRODUCTION)

Design principles:
- Stateless: Handler reads current state from external store, processes, writes new state
- Re-entrant: If handler crashes mid-execution, restart reads same state and re-processes
- Idempotent: Running the same handler twice on the same state produces the same result

Concurrent handlers:
- Multiple handlers can process independent deployment units simultaneously
- Handlers claim work via optimistic locking (read version, write new version)
- Version conflict → re-read state and retry
```

**为什么有效：** 无状态 + 可重入 + 幂等意味着崩溃无需人工干预即可恢复。乐观锁实现并发而无分布式锁。状态机使每个转换显式且可审计。

### 反面示例

```markdown
Each handler keeps deployment progress in local variables.
Handlers coordinate via shared in-memory state.
If a handler fails, an operator manually restarts the deployment.
```

**为什么失败：** 本地变量在崩溃时丢失，使部署无法在没有人工干预的情况下恢复。共享内存状态在并发处理器不加锁地读-改-写时损坏。需要手动重启违背了自动化部署管线的目的。

---

## Pattern 74: Autonomous PR Feedback Resolution

**出现频率：** <1% 的插件
**相关模式：** [Self-Critique](#pattern-28), [Confirmation Gates](#pattern-8)

**定义：** Agent 自主读取 PR 审查评论并决定是实施反馈还是以理由反驳 — 每个评论无需人工干预。

### 正面示例

```markdown
For each PR review comment:
1. Classify: bug-fix, style-nit, architecture-concern, question, praise
2. Decide:
   - bug-fix → implement immediately
   - style-nit → implement if < 5 minutes
   - architecture-concern → push back with reasoning if disagree, implement if agree
   - question → respond with explanation
   - praise → acknowledge
3. After all comments resolved: re-request review

Decision log: Record every decision (implement/pushback) with reasoning
for audit trail.
```

**为什么有效：** 分类防止将所有评论同等对待。"push back with reasoning"选项意味着 agent 不会盲目实施每个建议。决策日志提供问责。

### 反面示例

```markdown
For each PR review comment:
1. Implement the requested change
2. Mark the comment as resolved
3. After all comments addressed, re-request review
```

**为什么失败：** 盲目实施每个评论意味着 agent 会同等应用矛盾的建议、风格细节争论和不正确的反馈。没有分类，琐碎的格式请求与关键 bug 修复消耗相同精力。没有决策日志意味着审查者无法理解为什么做了这些更改。

---

## Pattern 75: 11-Phase Autonomous Development Flow

**出现频率：** <1% 的插件
**相关模式：** [Phased Execution](#pattern-2), [Skill Composition](#pattern-19)

**定义：** 完整的自主开发工作流，从任务理解到部署，串联11个阶段，包括对抗性代码审查和 CI 监控。

### 正面示例

```markdown
Phase 1: Task Understanding (read work item, clarify requirements)
Phase 2: Codebase Analysis (repo structure, conventions, dependencies)
Phase 3: Design (architecture, data model, API design)
Phase 4: Implementation (write code following discovered conventions)
Phase 5: Self-Review (adversarial review of own code)
Phase 6: Testing (write and run tests, fix failures)
Phase 7: CI Integration (push, monitor CI, fix build breaks)
Phase 8: Code Review (read reviewer comments, implement/pushback)
Phase 9: Merge (after approval, merge and monitor)
Phase 10: Deployment Monitoring (watch for regression signals)
Phase 11: Work Item Update (close task, write completion notes)

Guardrails:
- Hard stop after 3 consecutive build failures
- Escalate to human after 2 review cycles without approval
- Never force-push, never merge without CI green
```

### 反面示例

```markdown
Phases:
1. Read the task
2. Write the code
3. Push to main
4. Fix any issues that come up in production
```

**为什么失败：** 跳过设计、自审和测试阶段意味着 bug 在生产环境而非开发期间被发现。直接推送到 main 而不经过 CI 或代码审查绕过了所有质量门控。"Fix issues in production"将生产环境当作测试环境。

---

## Pattern 76: Staggered Burst Query with Rate Limit Respect

**出现频率：** 约 2% 的插件
**相关模式：** [Tool Routing Tables](#pattern-21), [Error Handling](#pattern-15)

**定义：** 发起多个 MCP/API 调用时，用受控并发和明确速率限制意识交错发送，而非全部并行发射。

### 正面示例

```markdown
Staggered burst queries:
- Max 3 concurrent MCP calls
- Group queries by target service (all Kusto together, all ADO together)
- Wait for each group to complete before starting the next
- If any call returns 429 (rate limited): back off 2s, retry once, then skip

Cross-server parallelism rule:
NEVER run MCP calls to different servers in the same parallel batch —
one 403 cancels ALL parallel calls in the batch.
```

**为什么有效：** 跨服务器反并行规则防止单个认证失败取消不相关的查询。按服务分组在速率限制内最大化吞吐量。跳过重试后的策略防止无限重试循环。

### 反面示例

```markdown
Fire all MCP queries in parallel for maximum speed.
If a query fails, retry it immediately up to 10 times.
Mix Kusto, ADO, and Graph queries in the same parallel batch.
```

**为什么失败：** 在一个并行批次中混合 MCP 服务器意味着来自一个服务器的单个 403 取消对其他服务器所有进行中的查询。无限并行查询超过速率限制并全面触发 429。不加退避地重试10次放大速率限制问题，可能阻塞 agent 数分钟。

---

## Pattern 77: Time-Boxed Investigation with Partial Results

**出现频率：** 约 2% 的事件响应插件
**相关模式：** [Error Handling](#pattern-15), [Progress Feedback](#pattern-9)

**定义：** 每个调查阶段的硬时间预算，时间到期时强制报告部分结果而非无限继续。

### 正面示例

```markdown
Investigation time budget: 5 minutes per hypothesis
- If hypothesis not confirmed in 5 minutes, mark as INCONCLUSIVE
- Move to next hypothesis
- Report all investigated hypotheses (confirmed, refuted, inconclusive)
- Never spend > 15 minutes total on initial investigation

Partial result format:
| Hypothesis | Status | Evidence | Time Spent |
| DB connection pool exhaustion | CONFIRMED | Connection count = MAX | 2m 30s |
| Memory leak in service X | REFUTED | Memory stable over 24h | 3m 15s |
| Network partition | INCONCLUSIVE | Insufficient data | 5m 00s (timeout) |
```

**为什么有效：** 时间预算防止 agent 在事件中速度重要时走入死胡同。假设表展示了所有调查过的内容包括死胡同 — 对交接至关重要。

### 反面示例

```markdown
Investigate the root cause thoroughly before reporting any findings.
Do not move to the next hypothesis until the current one is fully resolved.
Only report confirmed findings — do not include inconclusive results.
```

**为什么失败：** "Thoroughly"没有时间边界，agent 可能在一个假设上花 30 分钟而事件不断升级。要求完全解决后才能继续意味着死胡同假设阻塞所有进展。隐藏非结论性结果丢失了下一个响应者交接所需的调查上下文。

---

## Pattern 78: Deployment Override Knowledge Encoding

**出现频率：** 约 1% 的插件
**相关模式：** [Domain Knowledge Embedding](#pattern-24)

**定义：** 将部署覆盖类型的完整分类、效果和常用 KQL 过滤模式直接编码到 prompt 中，支持精确的部署状态查询。

### 正面示例

```markdown
Blocking Override Types (checked by deployment gate system DeploymentBlockRule):
| Type | Effect |
| BlockAll | Blocks all deployment to matching machines |
| Halt | Halts deployment of specific version range |
| HaltAndStop | Halts and stops any in-progress deployment |
| Purge | Rolls back to previous version |

Common KQL Filters:
| Filter | KQL |
| Active only | where IsDeleted == false |
| Blocking types only | where DeploymentConfigurationItemType in ("BlockAll",...) |
| By ring | where TargetFilterExpression has "global" |
```

### 反面示例

```markdown
Query the deployment override API for current status.
Filter out any overrides that seem irrelevant.
Summarize the results for the user.
```

**为什么失败：** 不编码覆盖分类，agent 无法区分阻塞性覆盖（Halt）和信息性覆盖。"Seem irrelevant"是主观的 — agent 缺乏正确过滤的领域知识。没有 KQL 模式意味着 agent 必须对每个请求猜测查询语法，产出不一致且常常不正确的结果。

---

## Pattern 79: Incident Escalation Decision Matrix

**出现频率：** 约 2% 的事件响应插件
**相关模式：** [Confirmation Gates](#pattern-8), [Blast Radius Formula](#pattern-49)

**定义：** 基于量化影响维度确定升级路径的决策矩阵，带有明确阈值决定何时呼叫、开桥接会议或升级到管理层。

### 正面示例

```markdown
| Customer Impact | Duration | Escalation |
| < 100 users | < 30 min | Sev 3 — assign to oncall |
| 100-10K users | < 1 hour | Sev 2 — page secondary oncall |
| 10K+ users | Any | Sev 1 — bridge call, page management |
| Data loss | Any | Sev 0 — all-hands, exec notification |

Auto-escalation triggers:
- Sev 2 unacknowledged for 15 minutes → escalate to Sev 1
- Any severity with "security breach" signal → Sev 0 immediately
```

### 反面示例

```markdown
Assess the severity of the incident based on your best judgment.
Escalate if the situation seems serious.
Page the oncall team if needed.
```

**为什么失败：** "Best judgment"和"seems serious"是主观的 — 不同 agent 运行对相同事件产出不一致的严重性分配。没有量化阈值（用户数、持续时间），Sev 2 和 Sev 1 之间没有可复现的边界。缺失的自动升级规则意味着未确认的 Sev 2 可以数小时坐着不升级。

---

## Pattern 80: Scope Estimation and Re-estimation Checkpoints

**出现频率：** 约 2% 的规划插件
**相关模式：** [Complexity-Tiered Dispatch](#pattern-38), [Phased Execution](#pattern-2)

**定义：** 要求 agent 在开始前估算任务范围，然后在执行期间的定义检查点重新估算。范围显著增加时触发升级。

### 正面示例

```markdown
Before starting:
- Estimate: hours of work, number of files, risk level
- If estimate > 8 hours: recommend decomposition

Checkpoint re-estimation (at 25%, 50%, 75%):
- Compare actual progress to estimate
- If actual/estimate > 1.5x: flag scope creep
- If actual/estimate > 2x: stop and escalate to user
```

**为什么有效：** 早期估算在投入前就捕获不合理的任务。重新估算检查点在过程中捕获范围蔓延。1.5x/2x 阈值是具体的而非主观的。

### 反面示例

```markdown
Start working on the task immediately.
If it takes longer than expected, let the user know when you're done.
```

**为什么失败：** 没有前期估算，agent 承诺可能需要数天的任务 — 在有人意识到范围错误之前浪费 token 和时间。没有检查点意味着范围蔓延在完成（或失败）前是不可见的。"完成时通知"不提供用于干预的早期预警信号。
