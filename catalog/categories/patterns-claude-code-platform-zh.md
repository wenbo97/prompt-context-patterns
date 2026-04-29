# Claude Code 平台模式

从 **Claude Code system prompt**（Anthropic 官方 CLI agent）提取的模式。涵盖平台级关注点：harness 如何管理记忆、权限、调度、工具路由、Agent 分发和上下文存活。扩展目录至 Patterns 121-132。

**数据来源:** `C:\src\claude-code-system-prompts\claude-code-system-prompt.md` -- Claude Code CLI 的完整 system prompt。

**提取日期:** 2026-04-24

---

## Pattern 121: Typed Memory Taxonomy

**出现率:** Claude Code 平台独有（插件 skill 中未观察到）
**相关模式:** [Configuration Persistence (16)](#pattern-16), [State File Continuity (70)](#pattern-70), [Reference File Injection (23)](#pattern-23)

**定义:** 基于文件的持久记忆系统，具有四种离散记忆类型 -- `user`, `feedback`, `project`, `reference` -- 各有不同的写入触发条件、使用规则和过期特征。始终加载的索引文件（MEMORY.md）指向带有 frontmatter 元数据的单独记忆文件。

**适用场景:**
- 对话状态需跨重启存活的多会话 Agent 系统
- 不同类型的记忆信息有不同的生命周期和验证规则
- 需要区分"用户是谁"、"用户让我怎么做"和"项目发生了什么"

### 正面示例

```markdown
## Memory Types

| Type | When to Save | How to Use |
|------|-------------|------------|
| `user` | Learn details about user's role, preferences, knowledge | Tailor behavior to user's perspective |
| `feedback` | User corrects approach OR confirms non-obvious approach | Guide behavior so user doesn't repeat guidance |
| `project` | Learn who is doing what, why, or by when | Understand broader context behind requests |
| `reference` | Learn about resources in external systems | Remember where to look for information |

## What NOT to Save
- Code patterns, architecture, file paths — derive from current state
- Git history — `git log` / `git blame` are authoritative
- Debugging solutions — the fix is in the code
- Anything in CLAUDE.md files

## Staleness Rule
Before acting on a memory: verify it is still correct by reading current
state. If memory conflicts with what you observe now — trust what you see,
update or remove the stale memory.
```

**生效原因:** 四种类型在写入时创建了**决策过滤器** -- Agent 不会把所有东西倒进一个日志。"不该保存什么"的列表同样重要：防止记忆变成可推导信息的过时缓存。过期规则（"验证后再使用"）防止持久记忆最危险的失败模式 -- 基于过时事实行动。

### 反面示例

```markdown
## Memory
Save important things the user tells you to a memory file.
Read the memory file at the start of each conversation.
```

**失败原因:** 无类型分类意味着所有内容进入一个文件。无过期规则意味着 Agent 信任 3 周前关于已被重命名的文件路径的记忆。无"不该保存"列表意味着记忆充满可推导的事实（文件结构、git 历史），它们腐烂的速度快于更新速度。

---

## Pattern 122: Bidirectional Feedback Capture

**出现率:** Claude Code 平台独有
**相关模式:** [Feedback Solicitation (29)](#pattern-29), [Mandatory Self-Learning After Failure (95)](#pattern-95)

**定义:** 同时记录纠正（"don't do X"）和确认（"yes, exactly like that"）作为反馈记忆。纠正容易注意到；确认更安静 -- 系统显式监听它们。

**适用场景:**
- 行为漂移是风险的长期 Agent-用户关系
- 希望 Agent 保持已验证的方法，而非只避免过去的错误
- 用户的沉默或接受本身就是信号

### 正面示例

```markdown
Record from failure AND success: if you only save corrections, you will
avoid past mistakes but drift away from approaches the user has already
validated, and may grow overly cautious.

## Body Structure for Feedback Memories
Lead with the rule itself, then:
- **Why:** the reason the user gave (a past incident, a strong preference)
- **How to apply:** when/where this guidance kicks in

Knowing *why* lets you judge edge cases instead of blindly following the rule.

## Examples

user: don't mock the database — we got burned last quarter
assistant: [saves: integration tests must hit real DB. Why: mock/prod
           divergence masked a broken migration]

user: yeah the single bundled PR was the right call here
assistant: [saves: for refactors in this area, user prefers one bundled PR.
           Confirmed after I chose this approach — a validated judgment call]
```

**生效原因:** "Why + How to apply"结构将原始指令转化为**可迁移的原则** -- Agent 可以将规则应用于新的边缘情况，而非只适用于学到它的精确场景。捕获确认防止 Agent 变得过度谨慎（只记住什么不该做）。

### 反面示例

```markdown
When the user corrects you, save what they said to avoid repeating the mistake.
```

**失败原因:** 只捕获纠正。保存 50 个会话的"don't do X"后，Agent 有一长串禁令但不记得什么方法有效。它变得犹豫不决，质疑之前已被验证的方法。

---

## Pattern 123: Reversibility x Blast-Radius Permission Model

**出现率:** Claude Code 核心模式；约 4% 的插件通过 [Confirmation Gates (8)](#pattern-8) 有类似概念
**相关模式:** [Confirmation Gates (8)](#pattern-8), [Read-Only Boundary (12)](#pattern-12), [Tiered Permissions (60)](#pattern-60)

**定义:** 二维权限评估：操作可逆性有多高，影响范围有多大？本地+可逆=自由执行。远程+不可逆=始终确认。关键点：**授权是非粘性的** -- 一次批准 push 不代表授权所有未来的 push。

**适用场景:**
- 混合安全探索和危险修改的自主 Agent
- Agent 可以影响共享状态的系统（git 仓库、API、消息）
- 需要一个心智模型来判断哪些操作需要人类审批

### 正面示例

```markdown
## Action Risk Assessment

                    Local              Shared/Remote
                    ┌──────────────────┬──────────────────┐
   Reversible       │ Proceed freely   │ Confirm first    │
                    │ (edit file,      │ (comment on PR,  │
                    │  run tests)      │  create branch)  │
                    ├──────────────────┼──────────────────┤
   Hard to reverse  │ Confirm first    │ ALWAYS confirm   │
                    │ (delete file,    │ (force push,     │
                    │  reset --hard)   │  close PR,       │
                    │                  │  send message)   │
                    └──────────────────┴──────────────────┘

CRITICAL: Approval is NON-STICKY.
A user approving `git push` once does NOT mean they approve it in all contexts.
Authorization stands for the scope specified, not beyond.
```

**生效原因:** 2x2 矩阵给 Agent 提供了**决策框架**而非具体命令列表。非粘性授权防止 Agent 通过先例积累随时间升级自己的权限。

### 反面示例

```markdown
Always ask before running dangerous commands like `rm -rf` or `git push --force`.
```

**失败原因:** 枚举的危险命令总会遗漏新情况。无框架评估新操作。无范围概念 -- 用户说了"yes push"后 Agent 可能在任何地方都 push。

---

## Pattern 124: Tool Preference Hierarchy with Hard Routing

**出现率:** Claude Code 核心模式；类似于 [Tool Routing Tables (21)](#pattern-21) 但增加了**禁止层**
**相关模式:** [Tool Routing Tables (21)](#pattern-21), [Intent Classification (20)](#pattern-20)

**定义:** 将操作类别映射到首选工具，然后禁止通用替代方案（shell 命令）。这比"prefer X over Y"更强 -- 是"NEVER use Y for this task."

**适用场景:**
- 有重叠工具能力的 Agent harness（shell 什么都能做，但专用工具更好）
- 通用工具的 UX、性能或可审计性更差
- 需要确定性的工具选择而非概率性偏好

### 正面示例

```markdown
IMPORTANT: Avoid using Bash to run `find`, `grep`, `cat`, `head`, `tail`,
`sed`, `awk`, or `echo` commands. Instead use the appropriate dedicated tool:

 - File search: Use Glob (NOT find or ls)
 - Content search: Use Grep (NOT grep or rg)
 - Read files: Use Read (NOT cat/head/tail)
 - Edit files: Use Edit (NOT sed/awk)
 - Write files: Use Write (NOT echo >/cat <<EOF)

While the Bash tool can do similar things, the built-in tools provide a
better user experience and make it easier to review tool calls.
```

**生效原因:** 每个映射后的括号"NOT X"消除了歧义。Agent 无法合理化"well, grep via bash is faster" -- 禁令是明确的。UX 理由（"easier to review"）让 Agent 有理由内化规则而非视其为武断。

### 反面示例

```markdown
Use the right tool for the job. Prefer built-in tools when available.
```

**失败原因:** "Prefer"不等于"never"。Agent 在觉得方便时会合理化用 bash 做 grep。无显式映射意味着 Agent 必须自行判断哪个工具适合每个操作。

---

## Pattern 125: Cache-Aware Scheduling

**出现率:** Claude Code 平台独有（调度基础设施）
**相关模式:** [State File Continuity (70)](#pattern-70), [Time-Boxed Investigation (77)](#pattern-77)

**定义:** 基于 LLM prompt cache TTL 选择轮询/循环任务的延迟间隔。缓存有 5 分钟窗口 -- 超过它意味着下次唤醒读取完整上下文（更慢更贵）。系统明确识别了一个"死区"（恰好 300s），永远不应选择。

**适用场景:**
- 任何有轮询/sleep 间隔的自主 Agent 循环
- 长期运行 Agent 会话的成本优化
- 有缓存层的 LLM 驱动系统中的定时任务

### 正面示例

```markdown
## Picking delaySeconds

The prompt cache has a 5-minute TTL.

| Range | Cache | When to use |
|-------|-------|-------------|
| 60-270s | Warm (cache hit) | Active work: checking builds, polling state |
| 300s | DEAD ZONE | Worst-of-both: pays cache miss, doesn't amortize |
| 300-3600s | Cold (cache miss) | Genuinely idle: nothing to check for minutes |

**Don't pick 300s.** If you're tempted to "wait 5 minutes," either drop to
270s (stay in cache) or commit to 1200s+ (one miss buys a much longer wait).

Default idle: 1200-1800s (20-30 min). Don't burn cache 12x/hour for nothing.

Think about what you're WAITING FOR, not "how long should I sleep."
If you kicked off an 8-minute build, sleeping 60s burns the cache 8 times
before it finishes — sleep ~270s twice instead.
```

**生效原因:** "死区"概念令人难忘，防止最浪费的选择。"think about what you're waiting for"重新框定从任意间隔到目标导向调度。8 分钟构建示例使错误间隔的成本具体化。

### 反面示例

```markdown
Wait an appropriate amount of time between checks. Don't check too frequently.
```

**失败原因:** 无框架定义"appropriate"。不了解缓存边界。Agent 会选择整数（60s、300s、600s），要么浪费缓存要么浪费钱。

---

## Pattern 126: Agent Briefing Protocol

**出现率:** Claude Code 的 Agent 工具核心模式；[Handoff Context Protocol (36)](#pattern-36) 中有回响
**相关模式:** [Handoff Context Protocol (36)](#pattern-36), [Hub-and-Spoke (32)](#pattern-32), [Multi-Agent Orchestration (18)](#pattern-18)

**定义:** 编排器如何为子 Agent 编写提示的规则集。核心原则："brief the agent like a smart colleague who just walked into the room." 子 Agent 从父对话中获得零上下文。关键反模式："Never delegate understanding" -- 永远不要写"based on your findings, fix the bug."

**适用场景:**
- 任何向子 Agent 分发工作的系统
- 编排器必须为专业 Agent 制定提示
- Agent 结果需要由编排器综合，而非由 Agent 综合

### 正面示例

```markdown
## Writing Agent Prompts

Brief the agent like a smart colleague who just walked into the room.
- Explain what you're trying to accomplish and WHY
- Describe what you've already learned or ruled out
- Give enough context that the agent can make judgment calls

**Never delegate understanding.** Don't write:
  "based on your findings, fix the bug"
  "based on the research, implement it"
Those phrases push synthesis onto the agent instead of doing it yourself.

Write prompts that prove you understood: include file paths, line numbers,
what specifically to change.

## Good prompt:
"Review migration 0042_user_schema.sql for safety. Context: we're adding a
NOT NULL column to a 50M-row table. I've checked locking behavior but want
independent verification. Report: is this safe, and if not, what breaks?"

## Bad prompt:
"Look at the migration and tell me if it's safe."
```

**生效原因:** "Smart colleague who just walked in"是一个立即可理解的心智模型。"Never delegate understanding"规则防止编排器最懒惰的失败模式 -- 将子 Agent 当作预言机而非专业工人。正反对比使差异直观。

### 反面示例

```markdown
Send clear instructions to the agent. Include relevant context.
```

**失败原因:** "Clear"和"relevant"是没有锚点的判断调用。编排器会写"investigate the issue and fix it"并认为它很清楚。

---

## Pattern 127: Parallel-Safe Step Identification

**出现率:** Claude Code 的 git/PR 协议核心；类似 [Phased Execution (2)](#pattern-2) 但增加了并行标注
**相关模式:** [Phased Execution (2)](#pattern-2), [Multi-Agent Orchestration (18)](#pattern-18)

**定义:** 为多步工作流标注显式的并行标记 -- 哪些步骤可以同时运行，哪些必须等待前序。用于 Claude Code 的 git commit 协议、PR 创建协议和通用工具调用指导。

**适用场景:**
- 部分步骤独立的多步工作流
- Agent 必须在顺序和并行执行间做选择
- 错误排序导致数据竞争或读取过时数据

### 正面示例

```markdown
## Git Commit Protocol

1. Run these in parallel (all independent):
   - `git status` to see untracked files
   - `git diff` to see staged/unstaged changes
   - `git log` to see recent commit style

2. Analyze all changes and draft commit message (depends on step 1)

3. Run these in parallel:
   - `git add` relevant files
   - Create commit with HEREDOC message
   - Run `git status` after commit (depends on commit completing —
     run sequentially after commit, but parallel with add)

4. If pre-commit hook fails: fix and create NEW commit (never amend)
```

**生效原因:** 带有显式"run these in parallel"标头的编号步骤消除歧义。括号中的依赖说明（"depends on step 1"）解释了为什么某些步骤不能并行。Step 4 的"NEW commit (never amend)"防止了此流程中最危险的错误。

### 反面示例

```markdown
Run git status, git diff, and git log. Then analyze changes and commit.
```

**失败原因:** 无并行标注。Agent 顺序运行所有三个（慢 3 倍）。无依赖推理意味着未来的编辑者可能错误地重新排序步骤。

---

## Pattern 128: Context Compaction Survival Protocol

**出现率:** Claude Code 平台独有；扩展 [State File Continuity (70)](#pattern-70)
**相关模式:** [State File Continuity (70)](#pattern-70), [Phase Data Contract (SSG P14)](#pattern-14)

**定义:** 当系统在对话接近上下文限制时自动压缩先前消息时，关于什么状态必须存活的显式指令。Agent 被告知哪些字段必须保留（按名称），以及对话不受上下文窗口限制 -- 消息被压缩，不是丢失。

**适用场景:**
- 超过上下文窗口限制的长时间 Agent 会话
- 早期决策影响后期阶段的多阶段工作流
- 任何有自动上下文压缩/摘要的系统

### 正面示例

```markdown
## Context Compaction

The system will automatically compress prior messages as it approaches
context limits. This means your conversation is not limited by the
context window.

When compaction occurs, preserve ALL fields from the Phase Data Contract:
- projectPath, netCoreTargets, assemblyName, branchName
- LocalBuildStatus, LocalBuildAttempts, LocalBuildErrors
- Current phase number (0, 1, 1.5, 2, 3, or 4)

During Phase 3, ALSO preserve build-repair loop state:
- quickbuildUsed (boolean)
- previousRootCauses (array)
- Current attempt counter N
```

**生效原因:** 命名字段无歧义 -- Agent 确切知道要保留什么。阶段特定的补充（Phase 3 循环状态）防止"保留所有东西"的反模式。"conversation is not limited"的保证防止 Agent 因上下文丢失而恐慌。

### 反面示例

```markdown
Try to remember important information from earlier in the conversation.
```

**失败原因:** "Important"未定义。Agent 要么记住太多（在可推导事实上浪费压缩上下文），要么记住太少（丢失关键状态如当前尝试计数器）。

---

## Pattern 129: Non-Sticky Authorization Scope

**出现率:** Claude Code 独有；为 [Confirmation Gates (8)](#pattern-8) 增加时间维度
**相关模式:** [Confirmation Gates (8)](#pattern-8), [Tiered Permissions (60)](#pattern-60)

**定义:** 明确规则：用户在一个上下文中批准某操作，不会创建常设授权。每次批准的范围仅限于特定请求，而非操作类别。防止 Agent 在长会话中通过隐式批准积累的"权限蠕变"。

**适用场景:**
- 同一操作类型在不同上下文中反复出现的长时间 Agent 会话
- 操作的风险特征随上下文变化（push 到 feature 分支 vs main）
- 权限范围必须显式的安全关键系统

### 正面示例

```markdown
A user approving an action (like a git push) once does NOT mean that they
approve it in all contexts. Unless actions are authorized in advance in
durable instructions like CLAUDE.md files, always confirm first.

Authorization stands for the scope specified, not beyond.
```

**生效原因:** 两句话，清晰明了。"Scope specified, not beyond"是一个易记的原则。例外情况（CLAUDE.md 持久指令）防止规则对显式预授权的操作造成烦扰。

---

## Pattern 130: Investigate Before Destroying

**出现率:** Claude Code 独有；为 [Read-Only Boundary (12)](#pattern-12) 增加调查要求
**相关模式:** [Read-Only Boundary (12)](#pattern-12), [Confirmation Gates (8)](#pattern-8)

**定义:** 遇到意外状态（陌生文件、分支、配置、锁文件）时，Agent 必须先调查根因再采取破坏性操作。防止 Agent 用破坏作为消除障碍的捷径。

**适用场景:**
- 在共享开发环境中运行的自主 Agent
- 工作区可能包含其他人进行中的工作
- 任何有权限执行破坏性操作（delete、reset、clean）的 Agent

### 正面示例

```markdown
When you encounter an obstacle, do not use destructive actions as a shortcut.

- Try to identify root causes and fix underlying issues rather than
  bypassing safety checks (e.g. --no-verify)
- If you discover unexpected state like unfamiliar files, branches, or
  configuration, investigate before deleting or overwriting — it may
  represent the user's in-progress work
- Resolve merge conflicts rather than discarding changes
- If a lock file exists, investigate what process holds it rather than
  deleting it

In short: measure twice, cut once.
```

**生效原因:** 具体示例（锁文件、陌生分支、合并冲突）锚定了抽象原则。"May represent the user's in-progress work"给出了 WHY，使规则感觉是保护性的而非官僚化的。"Measure twice, cut once"是易记的锚点。

### 反面示例

```markdown
Be careful with destructive operations. Ask before deleting things.
```

**失败原因:** "Be careful"不可操作。无调查要求。Agent 可能问"can I delete this lock file?"而不调查什么持有它 -- 问题本身就是过早的。

---

## Pattern 131: Output Visibility Awareness

**出现率:** Claude Code 平台独有
**相关模式:** [Progress Feedback (9)](#pattern-9), [Structured Output Templates (14)](#pattern-14)

**定义:** 明确告知 Agent 用户看不到大多数工具调用或内部思考 -- 只有文本输出可见。这创建了沟通义务：在第一次工具调用前说明要做什么，在关键时刻给更新，在回合结束时总结。

**适用场景:**
- 工具执行对用户不可见的 Agent
- 用户体验 Agent 为文本流而非工具调用日志
- 长操作期间的沉默会让用户困惑

### 正面示例

```markdown
Assume users can't see most tool calls or thinking — only your text output.

Before your first tool call: state in one sentence what you're about to do.
While working: give short updates at key moments — when you find something,
change direction, or hit a blocker.
End-of-turn summary: one or two sentences. What changed and what's next.

Brief is good — silent is not. One sentence per update is almost always enough.

Don't narrate your internal deliberation. State results and decisions directly.
Write so the reader can pick up cold: complete sentences, no unexplained jargon.
```

**生效原因:** "Brief is good -- silent is not"完美捕获了张力。三点结构（before/during/after）覆盖完整的回合生命周期。"Pick up cold"防止依赖上下文的缩写让翻阅过的用户困惑。

### 反面示例

```markdown
Keep the user informed about what you're doing.
```

**失败原因:** 无结构说明何时沟通。Agent 要么叙述每个工具调用（噪音），要么到最后才说（混乱）。

---

## Pattern 132: Hook-Driven Automation Awareness

**出现率:** Claude Code 平台独有
**相关模式:** [Confirmation Gates (8)](#pattern-8), [Configuration Persistence (16)](#pattern-16)

**定义:** 系统声明用户可以配置 shell 命令（"hooks"），在工具调用或事件响应中自动执行。Agent 必须将 hook 反馈视为来自用户，如果被 hook 阻止则适配而非重试。

**适用场景:**
- 有可扩展事件系统的 Agent 平台
- 外部进程可以拦截和修改 Agent 行为
- Agent 需要区分用户发起的和系统发起的反馈

### 正面示例

```markdown
Users may configure 'hooks' — shell commands that execute in response to
events like tool calls, in settings.

Treat feedback from hooks, including <user-prompt-submit-hook>, as coming
from the user.

If you get blocked by a hook:
1. Determine if you can adjust your actions in response to the blocked message
2. If not, ask the user to check their hooks configuration
3. Do NOT re-attempt the exact same action that was blocked
```

**生效原因:** "Treat as coming from the user"是简单的归因规则。三步响应（适配 -> 升级 -> 不重试）防止无限循环。显式的"do NOT re-attempt"防止最常见的失败模式。

### 反面示例

```markdown
The system may run additional checks on your tool calls. Handle any errors that occur.
```

**失败原因:** 无归因模型。"Handle errors"可能意味着重试，而当 hook 有意阻止操作时重试恰恰是错的。
