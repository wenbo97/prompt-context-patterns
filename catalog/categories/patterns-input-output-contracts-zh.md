# 类别 4：输入/输出契约

数据的流入和流出方式 — 输出模板、错误处理、配置和平台适配。

**相关基础技术：** Schema Priming, Grounding/Anchoring, Cognitive Offloading（见 [prompt-engineering-for-skills.md](/prompt-context-patterns/catalog/techniques/token-level-techniques)）

---

## Pattern 14: Structured Output Templates

**出现频率：** ~26% 的技能（590 文件）
**相关模式：** [Few-Shot Examples](#pattern-25), [Scoring Rubrics](#pattern-27), [Progress Feedback](#pattern-9)

**定义：** 规定 agent 输出必须遵循的确切格式、结构或模板 — 从表格 schema 和报告章节到带占位变量的完整 markdown 文档。

**适用场景：**
- 下游消费者（人或自动化）需要解析输出时
- 跨运行一致性很重要时（对比不同时期的报告）
- 输出足够复杂，格式漂移会降低可用性时
- 技能的价值在于结构而非仅仅内容时

### 正面示例
```markdown
### Output
# Pitch Review — CodePilot

**Format:** 5 slides, ~3 minutes | **Overall:** 16/25 (Adequate)

## Scorecard

| Criterion | Score | Feedback |
|-----------|-------|----------|
| Hook | 2/5 | Title slide alone is not a hook. Start with a pain point: "Your PR has been waiting 3 days. Sound familiar?" |
| Problem / Solution | 4/5 | Problem is clear and quantified. Solution is specific. Add one metric: "reduces review time by 60%." |
| Demo Flow | 4/5 | Live demo in VS Code is strong. Add a before/after comparison to make impact visible. |
| Technical Clarity | 4/5 | Architecture diagram is clear. Mention latency and cost briefly for judge credibility. |
| Call to Action | 2/5 | "Thank you" is not a CTA. End with: "Try it today — install from VS Code marketplace." |

## Suggested Improved Outline

| Slide | Content | Time |
|-------|---------|------|
| 1 | **Hook:** "Your PR has been waiting 3 days." + problem stat | 0:00–0:30 |
| 2 | **Solution:** CodePilot overview + key metric (60% faster reviews) | 0:30–1:00 |
| 3 | **Demo:** Live VS Code refactor suggestion → PR comment | 1:00–2:00 |
| 4 | **How It Works:** Architecture + cost/latency | 2:00–2:30 |
| 5 | **CTA:** "Install now" or "Join our beta" + team slide | 2:30–3:00 |

Complete — pitch scored 16/25, 5 actionable improvements provided.
```

**为何有效：** 模板展示了完成输出的确切结构 — 标题格式、评分表列、改进大纲表列和结束状态行。模型无法发明不同结构，因为形状已完全指定。示例包含填充内容而非仅列头，模型可以看到真实条目的样子（例如反馈是具体建议而非评级）。

### 反面示例

```markdown
Output the results in a structured way. Include the scores and feedback.
Make it clear and easy to understand. Use a table if appropriate.
```

**为何失败：** "Structured way" 可以是 JSON、YAML、markdown 表格、列表或纯文本 — 模型每次选择不同。"If appropriate" 让表格使用变成可选。没有列定义意味着模型可能一次创建 3 列表格，下次创建 7 列。没有示例内容意味着模型可能在反馈列中放评级而非具体建议。

---

## Pattern 15: Error Handling / Graceful Degradation

**出现频率：** ~10% 的技能（222 文件）
**相关模式：** [Phased Execution](#pattern-2), [Tool Routing Tables](#pattern-21), [Configuration Persistence](#pattern-16)

**定义：** 规定 agent 在出错时的行为 — 工具失败、数据缺失、超时、输入格式错误 — 带有按阶段区分的降级策略。

**适用场景：**
- 多阶段工作流中部分结果仍有价值时
- 技能依赖可能失败的外部工具/API 时
- 技能有多个数据源且部分可能不可用时
- 长时间运行的工作流中单次失败不应浪费所有先前工作时

### 正面示例
```markdown
### Timeout & Error Handling
Every Bash command specifies a timeout. On timeout:
1. Retry ONCE with the same timeout
2. If retry fails, apply graceful degradation:
   - **Phase 1 (metadata) timeout/failure:** STOP — no manifest, cannot proceed
   - **Phase 2 (collect) timeout/failure:** Check if manifest was partially written.
     If `changed_files` present → re-run Phase 3 with `--api-only`. If missing → STOP
   - **Phase 3 (finalize) timeout/failure:** Check if partial diffs exist.
     If some → proceed with available diffs. If none → STOP
   - **Agent timeout/failure:** Log "Agent {name} did not complete" and continue with
     remaining agents' results. If ALL 5 agents fail → STOP
   - **Posting (Step 8.1) timeout:** Report partial results and offer retry

Common error patterns:
- `az CLI not found` → tell user to run `az login`
- HTTP 401/403 (ADO) → token expired, re-run `az login`
- HTTP 404 → PR not found, verify URL
- `No manifest found` → Phase 1 did not complete, re-run from Phase 1

### Partial Result Handling
- Missing diff for a file → skip that file, note in output
- Missing local context → proceed without (review still works, just shallower)
- Agent returns no findings → treat as "no issues found" (not an error)
- Agent returns malformed output → attempt salvage (infer severity from keywords)
```

**为何有效：** 每种失败模式都有具体响应 — 而非笼统的 "handle errors gracefully"。降级按阶段区分：Phase 1 失败是致命的（无数据），但 Phase 3 失败允许部分结果。重试策略明确（一次，相同超时）。常见错误模式映射到具体的用户提示和可操作修复。部分结果处理为每种数据类型定义了 "skip" 的含义。

### 反面示例

```markdown
If something goes wrong, try to recover gracefully. Report any errors to the user.
If a tool fails, try an alternative approach.
```

**为何失败：** "Try to recover gracefully" 没有恢复策略。"Try an alternative approach" 没有指定每个工具的替代方案。每次运行处理失败的方式不同 — 有时重试，有时跳过，有时停止。没有区分致命失败（Phase 1 — 无法继续）和非致命失败（一个 agent — 可以继续其他的）。

---

## Pattern 16: Configuration Persistence / First-Time Setup

**出现频率：** ~4% 的技能（80-100 文件）
**相关模式：** [Interactive Flow Control](#pattern-7), [Cross-Platform Handling](#pattern-17), [$ARGUMENTS Pattern](#pattern-4)

**定义：** "检查配置、缺失则创建" 模式，用于需要跨会话保持用户特定设置的技能。配置保存到已知路径并在后续调用时加载。

**适用场景：**
- 技能需要不随运行变化的组织/项目/团队上下文时
- 技能依赖外部工具认证（az login, gh auth）时
- 技能需要应持久化的用户偏好时
- 多命令插件中所有命令共享相同配置时

### 正面示例
```markdown
## First-Time Setup

On every invocation, check whether saved configuration exists before doing anything else.

### Step 1: Load Saved Configuration

Check for the config file. Use `$HOME` which works across all platforms:

    cat "$HOME/.config/ado-flow/config.json" 2>/dev/null

If the file exists and contains valid JSON with all required fields (`organization`,
`work_item_project`, `pr_project`), skip ahead to the relevant task workflow.

If the file does not exist or is missing fields, proceed with setup steps below.

### Step 2: Check Prerequisites

Verify Azure CLI and the DevOps extension are installed:

    az version 2>/dev/null && az extension show --name azure-devops 2>/dev/null

If Azure CLI is missing, display install instructions per platform.

### Step 3: Collect Configuration

Ask the user for these details one at a time:

1. **Organization name** - "What is your Azure DevOps organization name?"
2. **Project for work items** - "What project should I create work items in?"
3. **Project for pull requests** - "What project are your repositories in?"

### Step 4: Save Configuration

    mkdir -p "$HOME/.config/ado-flow"
    cat > "$HOME/.config/ado-flow/config.json" <<EOF
    {
      "organization": "{ORG}",
      "work_item_project": "{WORK_ITEM_PROJECT}",
      "pr_project": "{PR_PROJECT}"
    }
    EOF

Confirm: "All set! Your configuration has been saved."
```

**为何有效：** 检查-加载-设置-保存流程显式且确定性。必填字段已命名（`organization`、`work_item_project`、`pr_project`）— 模型确切知道什么构成"有效"配置。前置条件检查在数据收集之前（az CLI 未安装就不要收集组织名）。配置路径使用 `$HOME` 实现跨平台兼容。问题"逐一"收集（Pattern 7 组合）。

### 反面示例

```markdown
If this is the user's first time, ask them for their Azure DevOps settings.
Save the settings somewhere for next time.
```

**为何失败：** "Ask for settings" 没有枚举哪些设置。"Save somewhere" 没有指定路径 — 每次运行可能保存到不同位置。没有前置条件检查意味着技能可能收集完配置后因 az CLI 未安装而失败。没有验证步骤意味着格式错误的配置被保存并破坏后续运行。

---

## Pattern 17: Cross-Platform Handling

**出现频率：** ~3% 的技能（60-80 文件）
**相关模式：** [Configuration Persistence](#pattern-16), [Error Handling](#pattern-15)

**定义：** 为 Windows、macOS 和 Linux 环境提供不同指令 — 不同的命令、路径、工具和回退链。

**适用场景：**
- 技能使用系统特定工具（TTS 引擎、文件管理器、通知系统）时
- 技能引用文件路径（临时目录、配置目录）时
- 技能调用平台可用性不同的 CLI 工具时
- 跨开发环境使用的任何技能

### 正面示例
```markdown
## Platform Support

| Platform | TTS Engine | Focus Detection |
|----------|-----------|-----------------|
| Windows | OneCore (Mark) with SAPI fallback | Windows Terminal tab inspection (UI Automation) |
| macOS | `say` command (system voices) | `osascript` frontmost app + window title |
| Linux | espeak-ng / spd-say / festival / notify-send | `xdotool` (X11), Wayland stub |

## Cache Location

- **Windows:** `$env:TEMP\claude_voice\{session-id}.txt`
- **macOS/Linux:** `${TMPDIR:-/tmp}/claude_voice/{session-id}.txt`
```

**为何有效：** 表格将每个平台映射到其主工具和回退方案。回退链明确（Linux: espeak-ng → spd-say → festival → notify-send）。缓存路径使用正确的平台特定环境变量。Wayland "stub" 的声明意味着模型知道 Wayland 支持有限，不会尝试必定静默失败的 X11 命令。

### 反面示例

```markdown
Play a notification sound when done. Use whatever audio tool is available on the system.
```

**为何失败：** "Whatever is available" 要求模型在运行时探测已安装工具 — 不同系统上工具不同。没有回退链意味着模型可能在 Linux 上尝试 `say` 并静默失败。没有平台特定路径意味着临时文件在 Windows 上写到 `/tmp`（映射到不存在的 `C:\tmp\`）。同一平台上每次运行可能使用不同工具。
