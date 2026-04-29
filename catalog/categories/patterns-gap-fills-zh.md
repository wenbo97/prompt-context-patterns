# 补充模式: 入职、生产力、迁移与创意

初始研究未覆盖的八个模式 -- 涵盖基于 DAG 的入职流程、自学习迁移、个人生产力、高管沟通审查和无障碍后处理。

**数据来源:** 从 500+ 生产级 AI Agent 插件中提取，覆盖 DevOps、安全、迁移和事件响应领域。

---

## Pattern 92: DAG Journey with Typed Gates

**出现频率:** <1% 的插件
**相关模式:** [Phased Execution](#pattern-2), [Deployment State Machine](#pattern-73), [State File Continuity](#pattern-70)

**定义:** 基于 DAG（而非线性）的入职/迁移流程。每个步骤有前置依赖、自动化级别标注（auto/approval/manual/decision），Agent 可在数天后从持久化状态恢复。与线性阶段执行或状态机不同，这是一个完整的依赖图，支持并行路径、可选步骤和回填逻辑。

### 正面示例

```markdown
## Step Dependency Graph (topological ordering)
Step A → Step B → Step D
Step A → Step C → Step D
Step E (optional, activates on user opt-in)

## Automation Levels per Step
- `auto` — agent can complete without user input
- `approval` — agent prepares, user confirms
- `manual` — user must do this externally (e.g., order hardware)
- `saw` — user must complete a secure workstation (privileged access) step
- `decision` — user must make a choice between alternatives
- `tbd` — automation not yet determined

## Journey State File (JSON)
Each step tracks: not-started / in-progress / pending / completed / failed

## Auto-Detection with Backfill
At initialization, scan existing repo artifacts to detect which steps are
already done. Backfill implied prerequisites. But distinguish:
- "repo-level" artifacts (can infer from files) vs.
- "machine-state" steps (must always be runtime-verified)

## Manual Gate Resumption
User returns days later: "my secure workstation device is ready"
→ Agent reads journey state, marks secure workstation step completed, unlocks dependents

## Critical Path Visualization
Show the longest dependency chain to production readiness.
```

**生效原因:** DAG 能处理线性执行无法覆盖的并行路径。自动化级别标注阻止 Agent 尝试手动步骤。回填逻辑避免用户重复已完成的工作。手动门恢复机制支持跨天流程。

### 反面示例

```markdown
## Onboarding Steps (linear)
1. Order hardware
2. Set up dev environment
3. Configure SAW device
4. Clone repo
5. Run first build
Complete steps in order. If a step fails, retry until it succeeds.
```

**失败原因:** 线性排序强制独立步骤串行执行（硬件采购和仓库克隆可以并行）。无自动化级别标注导致 Agent 会尝试仅限手动的步骤。无状态持久化意味着多天流程在会话结束后从头开始。

---

## Pattern 93: Multi-Source Evidence Harvest with Goal-Aligned Synthesis

**出现频率:** <1% 的插件
**相关模式:** [Audience-Purpose Calibration](#pattern-83), [Reference File Injection](#pattern-23)

**定义:** 从 6+ 异构数据源并行采集证据（GitHub PR、ADO 工作项、Claude 会话、邮件、Teams、日历），将每个证据项映射到用户定义的目标/OKR，然后从同一证据生成面向不同受众的报告。

### 正面示例

```markdown
## Evidence Sources (parallel harvest)
1. GitHub PRs — merged, reviewed, authored
2. ADO work items — state changes, comments
3. Claude sessions — conversation summaries
4. M365 emails — sent threads with action items
5. Teams — meeting actions, chat commitments
6. Calendar — meeting attendance and patterns

## Goal Alignment
Map each evidence item to goals from user's goals.md file.
Unaligned evidence gets flagged for user attention.

## Audience-Stratified Reports (same evidence, different framing)
- Manager report: tactical, what was delivered, blockers
- Skip-level report: strategic, themes and trajectory
- Executive report: business outcomes, metrics impact
- Team report: recognition, shared context
```

**生效原因:** 同一证据以不同抽象层级服务四类受众。目标对齐防止出现"我很忙但没有产出"的报告。多源并行采集提供完整画面。

### 反面示例

```markdown
## Weekly Report
Collect all PRs merged this week and list them.
Format as bullet points for the manager.
If the manager wants more detail, they can ask.
```

**失败原因:** 单数据源（仅 PR）遗漏会议、承诺和跨职能工作。无目标对齐使报告变成活动日志而非生产力叙事。单受众格式迫使用户为 skip-level 或高管受众手动重写。

---

## Pattern 94: Promise Detection and Knowledge Base Sync

**出现频率:** <1% 的插件
**相关模式:** [Configuration Persistence](#pattern-16), [Intent Classification](#pattern-20)

**定义:** 扫描自然语言对话（Teams 聊天、邮件）中的隐含承诺（"I'll follow up"、"let me check"、"will do"），提取为结构化承诺，与现有个人知识库去重，并提议写回新承诺。

### 正面示例

```markdown
## Commitment Extraction
Scan Teams chats and WorkIQ for commitment phrases:
- "I'll follow up on..."
- "Let me check..."
- "Will do"
- "I'll send you..."
- "I can take that"

## Deduplication
Compare extracted commitments against existing personal KB file.
Skip duplicates. Flag commitments that are overdue.

## Write-Back
Propose adding new commitments to the KB file.
User approves before write.
```

**生效原因:** LLM 的语言理解能捕获关键词匹配遗漏的隐含承诺。与现有 KB 去重防止重复跟踪。写回前需用户审批，构建持久的责任追踪系统。

### 反面示例

```markdown
## Track Commitments
Search messages for "I will" and "I'll" keywords.
Add all matches to a TODO list.
```

**失败原因:** 关键词匹配遗漏"let me check"等隐含承诺，同时误捕"I'll be in the meeting"（非承诺）。无去重导致同一承诺每次扫描都被重复添加。写回前无审批门控使知识库积累噪音。

---

## Pattern 95: Mandatory Self-Learning After Failure Resolution

**出现频率:** <1% 的插件
**相关模式:** [Rule-Catalog Review](#pattern-48), [Error Handling](#pattern-15)

**定义:** 诊断并修复构建失败后，Agent 必须用新的错误模式、根因和修复方案更新知识库文件 -- 使知识库随每次执行增长。未来运行会查阅扩展后的 KB。

### 正面示例

```markdown
After each build failure resolution:
1. Diagnose error:
   - Tier 1: Match against known patterns in known-errors.md
   - Tier 2: Novel investigation if no pattern matches
2. Apply fix
3. MANDATORY: Update known-errors.md with:
   - Error signature (regex pattern)
   - Root cause explanation
   - Fix applied
   - Files affected
4. Update shared rules files so future sub-skill runs handle it automatically

New Boost types encountered in the wild → categorize and record for
incorporation into the skill.
```

**生效原因:** 知识库是随每次失败变得更智能的活文档。Tier 1/Tier 2 区分确保已知模式即时处理而新错误仍被调查。强制更新防止"修了但没记录"的失败模式。

### 反面示例

```markdown
After a build failure:
1. Diagnose the error
2. Apply a fix
3. If the fix works, move on to the next task
```

**失败原因:** 修复已应用但从未记录。下次遇到相同错误的会话将从头重新调查，浪费相同的诊断时间。没有强制写回步骤，Agent 的知识永远无法跨运行复合增长。

---

## Pattern 96: Risk-Ordered Batch Migration with Build-Verify Loops

**出现频率:** <1% 的插件
**相关模式:** [Deployment State Machine](#pattern-73), [Loop Prevention](#pattern-41)

**定义:** 将大型迁移拆分为按风险排序的批次，每批经历：迁移 -> 提交 -> 远程构建 -> 自动监控 -> 自动诊断 -> 自动修复 -> 重新提交。仅在构建通过后进入下一批。相同错误签名检测触发回滚。

### 正面示例

```markdown
## Batch Ordering
Order by risk: lowest-dependency files first, highest-risk last.

## Per-Batch Loop
1. Migrate code in batch
2. Commit changes
3. Submit remote build
4. Auto-monitor via CronCreate polling
5. On failure: auto-diagnose → auto-fix → resubmit
6. If same error signature repeats → STOP, revert batch
7. On green build → proceed to next batch

## No-Progress Detection
If the same error signature appears 2x after fix attempts:
→ Revert entire batch
→ Report failure with error details
→ Move to next batch (skip problematic files)
```

**生效原因:** 按风险排序最小化早期失败的影响范围。相同错误签名检测防止无限重试。批次级回滚保留先前成功的迁移。

### 反面示例

```markdown
## Migration
1. Migrate all files at once
2. Submit build
3. If build fails, fix errors and resubmit
4. Repeat until green
```

**失败原因:** 一次迁移所有文件意味着单个失败污染整个变更集，无法隔离是哪些文件导致的。无相同错误检测使 Agent 可能无限重试同一无法修复的错误。没有批次级回滚，一个有问题的文件会阻塞所有其他文件。

---

## Pattern 97: PII-Motivated Delivery Restriction

**出现频率:** <1% 的插件
**相关模式:** [Sensitive Data Redaction](#pattern-11), [Read-Only Boundary](#pattern-12)

**定义:** 输出包含从多个来源聚合的个人数据。投递仅限用户自己的账户（Outlook/Teams）。即使用户明确要求发送给他人，Agent 也拒绝。PII 保护优先于用户同意。

### 正面示例

```markdown
## Delivery Restriction (ABSOLUTE)
Briefing delivery: ONLY to the user's own Outlook inbox or Teams chat.

Even if user explicitly asks to send to someone else → REFUSE.
"This briefing contains your personal activity data from multiple sources.
I can only deliver it to your own accounts."

This is not a confirmation gate — there is no override.
```

**生效原因:** 与数据脱敏（从输出中移除敏感部分）不同，此模式限制整个投递渠道而不论内容。绝对性质防止社会工程攻击（"just send it to my manager, it's fine"）。

### 反面示例

```markdown
## Delivery
Send the briefing to the user's preferred channel.
If user asks to forward it to someone, confirm before sending.
"Are you sure you want to share this with [person]?"
```

**失败原因:** 确认门控不是限制 -- 用户在认为请求合理时总会确认。来自多个来源的 PII 聚合报告永远不应离开用户自己的账户，无论是否同意。社会工程路径（"my manager asked for it"）轻松绕过确认提示。

---

## Pattern 98: Audience-Register Translation Review with Matched Frameworks

**出现频率:** <1% 的插件
**相关模式:** [Scoring Rubrics](#pattern-27), [Audience-Purpose Calibration](#pattern-83)

**定义:** 围绕"翻译问题"构建的审查方法论 -- 技术作者为高管受众写作。包含文档类型分类、每种类型的匹配内容框架，以及工程师-to-高管沟通的反模式目录。

### 正面示例

```markdown
## Six Executive Fundamentals (scoring rubric)
1. Unambiguous Ask — what exactly do you want the executive to DO?
2. Quantified Business Impact — numbers, not adjectives
3. Strategic Framing — connect to company priorities
4. Executive Tone — confident, concise, no hedging
5. Decision-Enabling Structure — reader can decide from this alone
6. Self-Contained — no required pre-reading

## Document Type → Content Framework
| Type | Recommended Framework |
| Strategy Brief | SCR (Situation, Complication, Resolution) |
| Investment Ask | What / So What / Now What |
| Post-Mortem | Finding / Implication / Recommendation |
| Decision Record | Evidence-First Decision |

## Engineer-to-Executive Anti-Patterns (14 named)
- "The Architecture Astronaut" — leading with system design, not business value
- "The Hedge Fund" — "we might potentially consider possibly..."
- "The Kitchen Sink" — every detail included, no hierarchy of importance

## Verdict: SEND-READY / NEEDS REVISION / DO NOT SEND
```

**生效原因:** 审查针对特定失败模式（技术专家 -> 高管受众），而非泛泛的文档质量。每种文档类型的匹配框架给作者一个结构起点。命名的反模式具有记忆性且可操作。

### 反面示例

```markdown
## Document Review Checklist
- Is the writing clear?
- Is the grammar correct?
- Is the document well-structured?
- Are there any typos?
Rate overall quality: 1-5
```

**失败原因:** 通用质量标准遗漏了核心翻译问题 -- 一个技术上准确的文档在清晰度和语法上可以得 5/5，但完全无法向高管传达商业价值。无文档类型匹配意味着 post-mortem 和 strategy brief 使用相同的审查框架。无命名反模式使反馈模糊（"could be more concise"）而非可操作（"you're leading with architecture, not business impact"）。

---

## Pattern 99: Automated Accessibility Post-Processing Pipeline

**出现频率:** <1% 的插件
**相关模式:** [Schema Validation Gate](#pattern-51), [Test Scaffolding](#pattern-54)

**定义:** 生成输出（如 PPTX 演示文稿）后，专门的无障碍后处理器自动运行以符合无障碍标准。独立的评估脚本运行断言检查。

### 正面示例

```markdown
## A11y Post-Processing (automatic, after PPTX generation)
1. Mark decorative shapes as decorative
2. Inject slide titles (for screen reader navigation)
3. Fix reading order (logical, not visual)
4. Group elements for screen readers
5. Set alt text on images

## A11y Evaluation (25 assertions)
Run accessibility eval script that checks:
- Every slide has a title
- Every image has alt text
- Reading order matches visual order
- No decorative elements are in the tab sequence
- Color contrast meets WCAG AA
```

**生效原因:** 无障碍作为后处理管道而非内嵌在生成逻辑中。关注点分离意味着创意生成可专注内容，而专门管道确保合规。25 项断言评估提供可量化的质量。

### 反面示例

```markdown
## Presentation Generation
When creating slides, make sure to:
- Add alt text to images
- Use readable fonts
- Keep good contrast
Generate the PPTX with these guidelines in mind.
```

**失败原因:** 将无障碍作为指导方针嵌入生成提示意味着合规依赖 LLM 在创作时记住每条规则。没有验证步骤，违规被静默发布。没有具体断言的独立评估，"make sure to add alt text"产生不一致的、无法衡量或强制执行的结果。
