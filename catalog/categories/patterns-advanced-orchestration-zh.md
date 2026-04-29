# 高级 Agent 编排模式

多 agent 协调、路由、共识和委托的深度模式 — 在 560+ 插件中发现的生产级架构，扩展了基础编排模式（18-22）。

**来源研究：** agent-orchestrator, multiagent-planning, review-swarm, consensus-code-review, review-verdict, zen-agents, dev-team, triage-team, delegate-agency, mtp-e2e-orchestrator, model-router, component-router, synthetics-agents

---

## Pattern 31: Adversarial Persona Framing

**出现频率：** 约 3% 的编排插件
**相关模式：** [Persona/Role Assignment](#pattern-5), [Multi-Agent Orchestration](#pattern-18), [Self-Critique](#pattern-28)

**定义：** 显式赋予 agent 对抗性思维和攻防立场，而非中立分析角色。告诉 agent 假设问题存在并主动尝试破坏。

**适用场景：**
- 代码审查中发现真实 bug 比礼貌更重要时
- 安全分析中渗透测试者思维提高覆盖率时
- 设计评审中挑战假设防止群体思维时
- 任何受益于智力对抗的多 agent 系统

### 正面示例

```markdown
You are the **attacker** in an adversarial panel.
BREAK things. Find flaws, edge cases, and failure modes.
Assume there's at least one issue - find it.
```

```markdown
**The Breaker** (Correctness):
Think like a chaos monkey. Your sole focus is finding ways this code
**produces wrong results, crashes, or behaves unexpectedly**.
Your mindset:
- "What if I send garbage?"
- "What if I click rapidly?"
- "What if the network dies mid-call?"

**The Exploiter** (Security):
Think like a penetration tester. Your sole focus is finding ways this code
can be **exploited, abused, or leak sensitive data**.
```

**为什么有效：** 具体攻击问题（"What if I send garbage?"）比"look for bugs"更可操作。chaos-monkey/pentester 隐喻编码了经过验证的方法论。赋予对抗性意图克服了模型默认倾向于认同和验证的偏好。

### 反面示例

```markdown
Review the code carefully and look for any issues. Be thorough.
```

**为什么失败：** 没有对抗性框架意味着模型默认进行确认性分析。"Be thorough"没有指定攻击策略。

---

## Pattern 32: Hub-and-Spoke SDLC State Machine

**出现频率：** 约 1% 的插件（但影响力大）
**相关模式：** [Phased Execution](#pattern-2), [Multi-Agent Orchestration](#pattern-18)

**定义：** 一个中央编排 agent 拥有代表软件开发生命周期的状态机。专家 agent 是无状态工作者，完成一个状态转换后通过结构化 Completion Report 将控制权返回给 hub。

**适用场景：**
- 跨越需求→设计→评审→部署的端到端开发流程
- 多个专家 agent 需要按顺序工作并传递上下文时
- 编排器需要跨多步骤跟踪总体进度时

### 正面示例

```markdown
## SDLC State Machine

INTENT_RECEIVED → PRD_CREATED → DESIGN_CREATED → DESIGN_REVIEWED_R1 →
DESIGN_R1_ADDRESSED → DESIGN_REVIEWED_R2 → IMPLEMENTATION_PLANNED →
IMPLEMENTED → PEER_REVIEWED → PR_COMMENTS_ADDRESSED → MERGED → DEPLOYED

## Completion Report (required from every specialist agent)

| Field | Value |
| **Agent** | peer-reviewer |
| **State Completed** | PEER_REVIEWED |
| **Artifacts** | {PR ID, review comments posted} |
| **Summary** | Reviewed PR #NNN, posted M comments |
| **Findings** | Blocker: N, High: N, Medium: N, Low: N |
```

**为什么有效：** 状态机让编排器确定性地知道"我们在哪里"。Completion Report 是结构化的 — 编排器读取它们来决定下一个转换而无需解析自由文本。每个 agent 返回相同的 schema，使交接统一。

### 反面示例

```markdown
## Workflow
1. First, create a PRD
2. Then design the system
3. Get it reviewed
4. Implement it
5. Create a PR

Each agent should report back what they did when finished.
```

**为什么失败：** 没有显式状态名意味着编排器无法确定性地跟踪转换。"Report back what they did"是自由文本 — 编排器必须解析自然语言而非读取结构化字段。没有交接制品的 schema，每个 agent 发明自己的格式。

---

## Pattern 33: M x N Cross-Model Consensus Grid

**出现频率：** 约 1% 的插件
**相关模式：** [Deduplication/Consensus](#pattern-22), [Scoring Rubrics](#pattern-27)

**定义：** 对每个审查维度（M 个镜头），并行启动 N 个不同 AI 模型。然后按镜头合并（N→1），再跨镜头元合并（M→1）。创建三层管线，利用跨模型多样性捕获幻觉并提高置信度。

**适用场景：**
- 高风险代码审查中单模型幻觉风险不可接受时
- 不同模型有不同优势（安全 vs 性能 vs 风格）时
- 组织策略要求多模型验证时

### 正面示例

```markdown
Step 3: Launch M x N sub-agents (all parallel)
Step 3b: Per-lens consolidation (N→1 per lens, all parallel)
  - Validate each finding against actual code (catch hallucinations)
  - Note which models flagged each finding
  - Single-model-only findings = low confidence
Step 3c: Meta-consolidation (M→1 final)
  - De-duplicate across lenses
  - Cross-reference against existing PR threads
  - Suppress findings matching Closed/Fixed/WontFix threads
```

```markdown
### Consensus Scoring

| Agreement | Action |
|-----------|--------|
| 3/3 models | `[high]` confidence — almost certainly real |
| 2/3 models | Accept — verify specifics, `[medium]`+ confidence |
| 1/3 models | Adversarially challenge — keep only if it survives scrutiny |
```

**为什么有效：** 跨模型多样性捕获特定模型的幻觉。3/3 → 2/3 → 1/3 评分表是确定性的。每镜头合并器在传递给元合并前验证实际代码。

### 反面示例

```markdown
Run the review with multiple models and combine the results.
If models disagree, use your best judgment to pick the right answer.
```

**为什么失败：** "Combine the results"没有合并结构 — 没有按镜头分组，没有对实际代码的幻觉验证。"Use your best judgment"用主观推理替代了确定性评分表，违背了多模型共识的目的。

---

## Pattern 34: Dual-Model Adversarial Planning

**出现频率：** <1% 的插件
**相关模式：** [Self-Critique](#pattern-28), [Confirmation Gates](#pattern-8)

**定义：** 两个 AI 模型独立为同一任务创建计划，自我加固各自的计划，然后交叉评审对方的计划。人类选择获胜者，失败计划的改进被合并进来。

**适用场景：**
- 单一视角不足的高风险架构决策
- 希望减少单一模型训练分布偏差时
- 错误计划的代价超过并行运行两个会话的成本时

### 正面示例

```markdown
Phase 5: Independent plans created by two agents (in separate sessions)
Phase 6: Each agent hardens their own plan (self-review)
Phase 7: Cross-review and gap analysis performed
Phase 8: Base plan selected by user
Phase 9: Final plan created with merged improvements from both
```

通过共享配置文件实现跨会话阻塞：
```json
{
  "planAPhase": 4,
  "planBPhase": 3,
  "planASelectedIdea": null,
  "planBSelectedIdea": null,
  "alignedIdea": null
}
```

**为什么有效：** 独立性防止确认偏差 — 每个模型在不看到对方方法的情况下工作。交叉评审创造对抗性张力。人类选择保留决策权。配置文件提供跨会话协调而不耦合。

### 反面示例

```markdown
Have two agents collaborate on a plan together. They should
discuss ideas back and forth until they converge on the best approach.
```

**为什么失败：** 协作允许第一个 agent 的框架锚定第二个，破坏了独立性。通过讨论收敛产生群体思维 — 正是双模型对抗规划要消除的偏差。没有人类选择点，两个 agent 的弱点都不会被检查。

---

## Pattern 35: Cost-Optimized Model Routing

**出现频率：** <1% 的插件
**相关模式：** [Intent Classification](#pattern-20), [Tool Routing Tables](#pattern-21)

**定义：** 将任务分解为子任务，按多维度分类每个子任务，并路由到满足质量要求的最便宜模型。包含成本报告和节省对比。

**适用场景：**
- 运行多个 sub-agent 且成本重要时
- 任务复杂度差异大（有些需要 Opus，有些 Haiku 即可）时
- 希望展示相对于"所有任务用最好模型"的成本节省时

### 正面示例

```markdown
## Classification Dimensions (per subtask)
- Reasoning depth (shallow/moderate/deep)
- Output criticality (low/medium/high)
- Precision required (approximate/exact)
- Context load (light/moderate/heavy)
- Novelty (pattern/novel)
- Estimated tokens
- Domain

## Routing Priorities
Priority 1 — Output criticality: high → Force premium model
Priority 2 — Reasoning depth: deep → Force sonnet or opus
Priority 5 — Novelty: pattern → Prefer cheaper model

## Cost Report
| Model | Subtasks | Cost |
| haiku-4.5 | 2 | $0.03 |
| sonnet-4.5 | 1 | $0.25 |
| TOTAL | 3 | $0.28 |
Baseline (all Sonnet): $0.75 | Savings: 63%
```

### 反面示例

```markdown
Use the most capable model for all subtasks to ensure quality.
We can optimize costs later if needed.
```

**为什么失败：** 所有子任务路由到高端模型在浅层任务（模式匹配、格式化）上浪费预算，而便宜模型处理这些同样好。"Optimize later"永远不会发生 — 没有分类框架来识别哪些任务可以降级，成本基线就变成了永久成本。

---

## Pattern 36: Handoff Context Protocol

**出现频率：** 约 2% 的编排插件
**相关模式：** [Phased Execution](#pattern-2), [Reference File Injection](#pattern-23)

**定义：** 编排器在每次 agent 交接前准备的标准化上下文块，确保接收 agent 拥有所有必要上下文而不读取不必要数据。

### 正面示例

```markdown
**Handoff Context Summary**
**Task:** {specific task the user requested}
**Target Agent:** {which agent will handle this}
**SDLC State:** {current state in the SDLC chain}
**Inputs:** [requirements doc path, work item ID, PR ID]
**Constraints & Decisions:** [list of prior decisions that constrain this agent]
**Expected Output:** [what the orchestrator needs back]
```

**为什么有效：** 接收 agent 获得所需的一切 — 任务、状态、输入、约束和预期输出 — 格式统一。不猜测上下文。编排器综合上下文而非转发原始对话历史。

### 反面示例

```markdown
Pass the full conversation history to the next agent so it has
all the context it needs to continue the work.
```

**为什么失败：** 原始对话历史包含不相关的回合、死胡同和撤回的想法，污染接收 agent 的上下文窗口。agent 必须解析非结构化对话来提取实际任务、约束和输入 — 浪费 token 并有将放弃的想法误解为活跃需求的风险。

---

## Pattern 37: Context Efficiency Rule (Orchestrator Reads Nothing)

**出现频率：** 约 1% 的插件
**相关模式：** [Multi-Agent Orchestration](#pattern-18), [Handoff Context Protocol](#pattern-36)

**定义：** 编排器将文件路径传给 sub-agent 和合并器，但从不读取文件内容本身。仅读取最终合并报告。这保留了编排器的上下文窗口用于协调逻辑。

### 正面示例

```markdown
The orchestrator must NOT read changed file contents, full diffs, or
sub-agent output into its own context. Pass **paths** to sub-agents
and consolidators. Only read the final meta-consolidator report.
```

**为什么有效：** 编排器的上下文窗口保持干净用于协调决策。sub-agent 负责读取和分析代码的重活。编排器只需读取最终摘要即可呈现给用户。

### 反面示例

```markdown
The orchestrator reads each changed file, analyzes it, then
delegates specific findings to sub-agents for deeper investigation.
```

**为什么失败：** 编排器将所有文件内容读入自己的上下文，用代码细节消耗窗口而非协调逻辑。到委托给 sub-agent 时，它已没有足够容量来跟踪状态、管理交接和综合最终报告。

---

## Pattern 38: Complexity-Tiered Dispatch

**出现频率：** 约 2% 的编排插件
**相关模式：** [Intent Classification](#pattern-20), [Workflow Mode Branching](#pattern-3)

**定义：** 按复杂度层级分类传入任务，然后根据层级调整模型选择、规划阶段和 agent 管线。

### 正面示例

```markdown
| Tier | Signals | Model | Planning Phase |
| Simple | Single file, clear fix | haiku | None — route directly |
| Standard | Feature, 2-3 files | Default | Optional |
| Complex | Architecture, 4+ files, security | sonnet+ | Recommended |
```

复杂任务触发顺序阶段：researcher → architect → coder。
简单任务直接路由到 coder。

### 反面示例

```markdown
Analyze the task complexity and choose an appropriate approach.
For harder tasks, think more carefully before coding.
```

**为什么失败：** 没有具体层级定义意味着模型每次都要发明自己的复杂度分类，产出不一致的路由。"Think more carefully"不可操作 — 没有指定额外阶段（researcher, architect）或模型升级。没有信号到层级的映射，4 文件的架构变更可能和错别字修复得到同等处理。

---

## Pattern 39: Persistent Team with Message Board

**出现频率：** 约 1% 的插件
**相关模式：** [Multi-Agent Orchestration](#pattern-18)

**定义：** Agent 被创建为持久团队，通过共享留言板和独立状态文件通信。编排器促进跨 agent 讨论而非命令 agent。

### 正面示例

```markdown
## Communication Protocol
- After forming or updating your perspective, write your FULL current
  position to your state file
- Your state file is the source of truth - keep it current

## State Files
{tmp}/brainstorm-${SESSION_ID}-advocate-state.md
{tmp}/brainstorm-${SESSION_ID}-skeptic-state.md
{tmp}/brainstorm-${SESSION_ID}-architect-state.md
```

**为什么有效：** 状态文件是唯一真相来源 — agent 不需要解析对话历史。编排器读取状态文件来综合观点。每个 agent 独立管理自己的状态。

### 反面示例

```markdown
The agents should communicate by sending messages to each other
through the orchestrator, which relays them back and forth.
```

**为什么失败：** 基于中继的通信意味着每个 agent 的状态分散在对话回合中，而非持久存储。如果编排器的上下文压缩或 agent 会话重启，先前的立场丢失。没有单一文件让 agent 读取来恢复其完整当前立场。

---

## Pattern 40: Delegation to Cloud Agent via Work Item

**出现频率：** <1% 的插件
**相关模式：** [Skill Composition](#pattern-19)

**定义：** 通过创建分配给 agent 的工作项（如 ADO），将任务委托给云托管的编码 agent，标记目标仓库。

### 正面示例

```markdown
System.Tags: copilot:repo=<orgName>/<projectName>/<repoName>@<branchName>
System.AssignedTo: GitHub Copilot
```

使用先尝试 REST API 再回退到工作项的策略。

**为什么有效：** Agent 像任何其他团队成员一样被发现和分配。标签提供仓库上下文。工作项成为审计跟踪。

### 反面示例

```markdown
Call the cloud agent's API directly with the code changes
and wait for it to return the result.
```

**为什么失败：** 直接 API 调用创建紧耦合 — 调用方阻塞等待响应，没有审计跟踪记录请求了什么，且调用失败时没有回退。基于工作项的委托是异步的、可审计的，使用与人类开发者相同的分配机制。

---

## Pattern 41: Loop Prevention with Max Iterations

**出现频率：** 约 3% 的插件
**相关模式：** [Error Handling](#pattern-15), [Confirmation Gates](#pattern-8)

**定义：** agent 之间重试/反馈循环的硬限制。不同循环类型不同阈值，达到限制时结构化报告。

### 正面示例

```markdown
Loop max 3 iterations. If tests still fail after 3 rounds:
- Report structured failure with remaining issues
- Ask whether to proceed with known failures or stop
```

```markdown
12 round warning, 20 round hard stop
```

**为什么有效：** 硬停止防止消耗时间和 token 的无限循环。结构化失败报告保留部分进展。询问用户决定（继续 vs 停止）保持人在回路中。

### 反面示例

```markdown
Keep retrying until the tests pass. If they don't pass,
try a different approach and retry again.
```

**为什么失败：** 没有迭代上限意味着循环可以无限运行，在相同失败测试上烧 token。"Try a different approach"没有结构导致随机探索。当循环最终从外部超时，没有结构化报告记录尝试了什么或取得了什么部分进展。

---

## Pattern 42: Agent Memory Isolation

**出现频率：** 约 1% 的插件
**相关模式：** [Prompt Injection Defense](#pattern-10), [Read-Only Boundary](#pattern-12)

**定义：** 团队中每个 agent 有隔离的内存/状态目录。跨 agent 通信仅通过指定的制品目录，绝不读取另一个 agent 的内部状态。

### 正面示例

```markdown
MEMORY_ROOT/memory/{role}/     — per-agent memory files
MEMORY_ROOT/decisions/{role}/  — per-agent decisions
MEMORY_ROOT/artifacts/         — inter-agent work products (shared)
MEMORY_ROOT/messages/          — team message board (shared)

Rules:
- Agents may only read their own memory + their own decisions files
- Agents may NOT read other agents' memory, charters, or history
- The coordinator does NOT inject one agent's output into another's memory
- Inter-agent handoffs use artifacts in MEMORY_ROOT/artifacts/
```

**为什么有效：** 隔离防止一个 agent 被另一个的内部推理影响。共享制品是受控接口。协调器调解所有跨 agent 通信，保持监督。

### 反面示例

```markdown
Agents can read each other's memory files to understand what
other team members are thinking and coordinate accordingly.
```

**为什么失败：** 交叉读取内存允许一个 agent 的推理错误或偏差传播给其他人。在完成自己分析前读取审查者的草稿批评的 agent 会锚定在那些发现上而非独立发现问题。缺乏受控接口使得无法审计什么影响了每个 agent 的结论。

---

## Pattern 43: Sparse Git Worktree for Isolated Review

**出现频率：** 约 2% 的审查相关插件
**相关模式：** [Read-Only Boundary](#pattern-12)

**定义：** 创建仅包含 PR 变更文件的 sparse git worktree 进行审查，避免在大型 monorepo 中物化完整仓库。

### 正面示例

```markdown
git worktree add --no-checkout --detach $worktreePath {commit}
git -C $worktreePath sparse-checkout set $changedFiles
```

**为什么有效：** 在 40k+ 文件的 monorepo 中，物化所有内容浪费时间和磁盘。Sparse checkout 意味着 agent 只看到相关文件。worktree 是隔离的 — 不会修改主工作树。

### 反面示例

```markdown
Clone the repository and check out the PR branch to review
the changed files.
```

**为什么失败：** 完全 clone 40k+ 文件的 monorepo 在 PR 只改了 5 个文件时浪费数分钟和 GB 级存储。在主工作树检出 PR 分支有污染未提交更改的风险。审查工作区和开发者活跃工作之间没有隔离。

---

## Pattern 44: Severity Promotion/Demotion by Area

**出现频率：** 约 2% 的审查插件
**相关模式：** [Scoring Rubrics](#pattern-27), [Deduplication/Consensus](#pattern-22)

**定义：** 根据审查领域自动调整发现的严重性级别，将组织风险偏好直接编码到 prompt 中。

### 正面示例

```markdown
Security and Correctness findings: promoted +1 severity level
Performance and Architecture findings: capped at HIGH
A11y and Rollout findings: capped at MEDIUM

Verdict rules:
- Approve: 0 CRITICAL, 0 HIGH
- Approve with suggestions: 0 CRITICAL in Security/Correctness
- Request changes: 1+ CRITICAL or 1+ HIGH in Security/Correctness or 3+ HIGH elsewhere
```

**为什么有效：** 安全 bug 本质上比风格问题更危险 — 提升编码了这一点。上限防止低风险领域阻塞合并。判定规则是确定性的，而非主观的。

### 反面示例

```markdown
Flag all issues found during review. The reviewer should use
their judgment to decide which ones are important enough to block the PR.
```

**为什么失败：** 没有按领域调整严重性，CSS 中的风格细节和认证中的 SQL 注入都从相同级别开始。"Use their judgment"跨审查产出不一致的判定 — 一个审查者因性能警告阻塞，另一个在同样发现下通过。没有确定性判定规则，通过/拒绝决策不可预测。
