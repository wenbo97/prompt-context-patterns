# 第七类：质量与反馈

确保输出质量的方法 — 评分标准、自我审查、反馈循环和版本管理。

**相关基础技术：** Schema Priming, Negative Space, Cognitive Offloading（见 [prompt-engineering-for-skills.md](../techniques/token-level-techniques)）

---

## Pattern 27: Scoring Rubrics / Quantitative Assessment

**出现频率：** 约 4% 的 skills（80-100 个文件）
**相关模式：** [Structured Output Templates](#pattern-14), [Few-Shot Examples](#pattern-25), [Self-Critique](#pattern-28)

**定义：** 提供带有明确标准、分数范围、每档描述词和阈值映射的数字化评分框架，将总分转化为分类结果。

**适用场景：**
- 主观评估需要跨运行可比性时
- 输出需要量化评分（演示评审、代码质量、就绪审计）
- 多个维度需要独立评分时
- 不同阈值触发不同后续操作时

### 正面示例
```markdown
## Scoring Criteria

| # | Criterion | Description | Score Range |
|---|-----------|-------------|-------------|
| 1 | **Hook** | Does the opening grab attention in the first 15 seconds? | 1–5 |
| 2 | **Problem / Solution** | Is the problem clear and the solution compelling? | 1–5 |
| 3 | **Demo Flow** | Is the demo logical, smooth, and shows the product working? | 1–5 |
| 4 | **Technical Clarity** | Are technical choices explained clearly for the audience? | 1–5 |
| 5 | **Call to Action** | Does the pitch end with a clear ask or next step? | 1–5 |

**Total:** 25 points. Scores map to: 20–25 Strong, 13–19 Adequate, <=12 Needs Work.
```
```markdown
**Scoring rubric for Instruction Clarity:**
- **5/5**: All checks pass. Clear phases, strong directives, output format specified.
- **4/5**: Frontmatter complete, workflow exists, minor language weakness.
- **3/5**: Basic structure exists but missing output format or has weak language.
- **2/5**: Missing frontmatter fields or no clear workflow.
- **1/5**: No frontmatter or unstructured prose.
```

**为什么有效：** 每个标准都有名称、描述和分数范围 — 模型明确知道评什么、怎么评。总分到类别的映射（20-25 Strong、13-19 Adequate、<=12 Needs Work）使最终判定确定化。skillqa 标准提供了每档描述，模型可以用具体标准区分 3 分和 4 分。五个维度覆盖不同方面 — "Hook"和"Call to Action"之间没有重叠。

### 反面示例

```markdown
Rate the pitch on a scale of 1-10. Consider things like how engaging it is,
whether the demo works, and if the technical approach makes sense.
Give an overall assessment.
```

**为什么失败：** 单一 1-10 分制无标准意味着每次运行的校准不同。"Consider things like"是建议而非必需维度。没有阈值映射意味着"7/10"在不同运行中可能代表不同含义。没有每档描述意味着模型无法区分相邻分数。对同一输入多次运行会产生不同分数。

---

## Pattern 28: Self-Critique / Quality Self-Check

**出现频率：** 约 2% 的 skills（30-50 个文件）
**相关模式：** [Evidence Chain](#pattern-26), [Negative Constraints](#pattern-6), [Scoring Rubrics](#pattern-27)

**定义：** 要求 agent 在交付前审查自己的输出 — 识别弱点、标记低置信度区域、验证是否符合规则。

**适用场景：**
- 规格/文档生成中隐含假设危险时
- 根因分析中过早下结论浪费排查时间时
- 模型置信度变化且用户需要了解时
- 产出可执行建议时（错误建议代价高昂）

### 正面示例
```markdown
### Adversarial Self-Critique

The spec author's honest assessment of where this spec is weakest. Not generic failure
modes — specific weaknesses in THIS spec.

**Rules:**
- Minimum 3 weaknesses per spec.
- Each weakness must be specific to THIS spec — "specs can be misinterpreted" is not valid.
- Watch indicators must be observable during execution, not after.

### Weakness 1: [Title]
- **Assumption being made:** [the specific assumption]
- **What happens if wrong:** [what the executor would build incorrectly]
- **Watch indicator:** [observable signal during execution]

### Weakness 2: [Title]
...
```

**为什么有效：** "至少 3 个弱点"防止敷衍了事。明确拒绝通用弱点（"specs can be misinterpreted"）迫使模型找到当前输出的实际问题。三字段结构（假设、后果、观察指标）使每个弱点可操作 — 用户知道执行期间该监控什么。"Adversarial"框架鼓励模型寻找问题而非维护自己的工作。

### 反面示例

```markdown
Review your output and make sure it's good. Fix any issues you find.
```

**为什么失败：** "Make sure it's good"与模型生成输出时遵循的指令相同 — 用同样标准自审产出同样结果。没有最少弱点数意味着模型发现零弱点（作者看自己的作品一切良好）。没有弱点结构意味着只有笼统空话。"Fix any issues"意味着用户永远看不到弱点 — 模型默默"修复"它们，实际可能是掩盖问题。

---

## Pattern 29: Feedback Solicitation

**出现频率：** <1% 的 skills（10-20 个文件）
**相关模式：** [Progress Feedback](#pattern-9), [Configuration Persistence](#pattern-16)

**定义：** 指示 agent 在自然停顿点呈现反馈调查或请求，带有优先级层级和会话级去重。

**适用场景：**
- 正在迭代中、需要用户反馈的 skills
- 有多种潜在失败模式、需要 bug 报告的 skills
- 希望在用户遇到差距时捕获功能请求
- 需要满意度指标的生产 skills

### 正面示例
```markdown
## Feedback

Surface the feedback survey **at most once per session** at a natural stopping point.

**Link:** [Excel AI Tools Pulse](https://aka.ms/ExcelAIToolsPulse) (anonymous, 2 min)

**When to surface** (pick the first that matches, then stop for the session):

1. **Bug** — something went wrong → offer to draft a brief bug report
2. **Feature gap** — user wants something this skill can't do → offer to draft feature request
3. **Satisfaction** — task completed smoothly → one-line mention
4. **First completion** — skill finished successfully, no other trigger → link in closing output

Never interrupt the active task. Never mention the survey again if declined or ignored.
```

**为什么有效：** "每个会话最多一次"防止反馈疲劳。优先级层确保 bug 在通用满意度问题之前呈现。"Pick the first that matches, then stop"是确定性规则。"Never interrupt the active task"确保反馈不干扰工作。不同反馈类型有不同响应方式（bug → 提议起草报告，satisfaction → 一句话提及）。

### 反面示例

```markdown
Ask the user for feedback when you're done. Include a link to our survey.
```

**为什么失败：** 没有会话级去重意味着模型在每次交互后都请求反馈。没有优先级层意味着 bug 和通用满意度得到同等处理。"When you're done"在多步工作流中模糊 — 每步之后还是仅在结束时？没有约束禁止中断活跃工作意味着模型可能在分析过程中请求反馈。

---

## Pattern 30: Version Check / Update Notification

**出现频率：** <1% 的 skills（10-20 个文件）
**相关模式：** [Configuration Persistence](#pattern-16), [Error Handling](#pattern-15)

**定义：** 检查已安装插件版本是否与最新可用版本一致并通知用户更新，检查失败时优雅降级。

**适用场景：**
- 正在积极开发和频繁更新的 skills
- 版本不匹配导致微妙行为差异的 skills
- 通过插件市场分发的 skills
- 用户因安全或兼容性原因需要保持最新版时

### 正面示例
```markdown
### Check for Updates

**Run this section on every invocation**, before any other workflow section. It is designed
to be non-blocking — if any step fails (network error, file not found, parse error),
log a brief warning and continue silently.

**Read installed version**

    $installedPluginJson = "$env:USERPROFILE\.copilot\installed-plugins\
      marketplace\my-plugin\.claude-plugin\plugin.json"
    $installedVersion = (Get-Content $installedPluginJson -Raw | ConvertFrom-Json).version

**Fetch latest version from GitHub**

Uses `gh api` (GitHub CLI) for authenticated access, with `Invoke-RestMethod` as fallback:

    # Primary: GitHub CLI
    $base64 = gh api repos/org/plugins/contents/plugins/
      my-plugin/.claude-plugin/plugin.json --jq '.content'
    $latestVersion = ([System.Text.Encoding]::UTF8.GetString(
      [Convert]::FromBase64String($base64.Trim())) | ConvertFrom-Json).version

    # Fallback: direct HTTP (works for public repos)
    $latestUrl = "https://raw.githubusercontent.com/org/plugins/
      main/plugins/my-plugin/.claude-plugin/plugin.json"
    $latestVersion = (Invoke-RestMethod -Uri $latestUrl -TimeoutSec 5).version

**Compare versions** using `[version]` type for numeric comparison.

**Report result:**
- If latest > installed: "Update available: v{installed} → v{latest}" + offer update command
- If versions match: "v{installed} (latest)" + continue
- If check fails: "Could not check for updates. Continuing with installed version."
```

**为什么有效：** 检查被设计为非阻塞 — 网络故障不会阻止 skill 运行。两种获取方式（gh api + 直接 HTTP）提供冗余。版本比较使用正确的数字解析（`[version]` 类型），而非字符串比较。三种结果（有更新、已最新、检查失败）各有明确的用户提示。更新路径会暂停并询问后再更新，而非自动更新。

### 反面示例

```markdown
Check if there's a newer version available. If so, tell the user to update.
```

**为什么失败：** 没有指定已安装或远程版本的路径。没有网络故障降级意味着 skill 可能在做任何实际工作前就崩溃。没有版本比较方法 — "1.9.0"和"1.10.0"的字符串比较会得出错误结果。没有处理"检查失败"的情况。没有更新前的用户确认。"Tell the user to update"没有给出实际命令。
