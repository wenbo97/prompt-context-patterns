# 防止 Agent 在 Skill 引用中偷懒

**主题:** 将 Claude Code skill 重构为渐进式披露（将示例提取到引用文件）时，如何防止运行时 agent 跳过引用读取并即兴发挥？

**受众:** 已了解 Claude Code `SKILL.md` 模型且正面临真实重构（如 command + skill 文件超出适宜大小）的 skill/plugin 作者。

---

## 1. 背景：Claude Code skill 如何工作

Skill 使用**三层渐进式披露**模型。理解所有三层是推理懒惰问题的前提。

### 第一层 — 元数据预加载（每个 skill 约100 token）

会话启动时，Claude Code 扫描每个 skill 目录，仅将每个 `SKILL.md` 的 YAML frontmatter（`name` + `description`）注入系统提示。这驱动 skill 发现：模型看到类似列表

```
<available_skills>
  <skill>
    <name>sync-prerequisite-prs</name>
    <description>Use when the user wants to sync...</description>
  </skill>
  ...
</available_skills>
```

并使用 description 决定 skill 是否适用。你可以安装数十个 skill 而无显著上下文开销。

### 第二层 — `SKILL.md` 完整正文（触发时加载）

当模型决定某 skill 适用时，它发出 `view`/`bash` 调用将完整 `SKILL.md` 读入上下文。Anthropic 建议将正文控制在 **500 行 / 1,500-2,000 词以内**以确保可靠的指令遵循。

### 第三层 — 捆绑文件（模型按需加载）

Skill 目录中的其他内容——`references/`、`examples/`、`scripts/`、`assets/`——**不自动加载**。模型必须明确选择读取。官方用语是 _"Claude **chooses to** read forms.md when filling out a form"_——`chooses to` 是关键词。**没有强制执行。**

第三层就是懒惰问题所在。

---

## 2. Agent 跳过引用读取的原因（根因分析）

跳过很少是模型"试图节省 token"。它是下一 token 预测与 prompt 框架交互的下游效应。

| 原因 | 机制 |
|------|------|
| **模式补全偏差** | 读完父级 `SKILL.md` 后，模型已对下一步采样出看似合理的计划。引用变成"不确定时查阅"——但模型并不觉得不确定。 |
| **可选框架** | 类似 _"For details, see @overlap.md"_ 的措辞在语义上是可选的。模型像对待散文脚注一样对待它们。 |
| **无矛盾信号** | 没有内联示例时，模型的内部分布对自己而言"够好了"。没有内联锚点说 _"显而易见的答案是错的"_。 |
| **长链注意力衰减** | 在多步工作流深处，对早期指令（"你必须读引用"）的注意力已衰减。 |
| **上下文压力启发式** | 上下文压力或接近 token 上限时，模型更可能跳过"额外"读取。 |

含义：**仅靠散文无法可靠地阻止跳过**。引用的框架、在工作流中的位置以及周围的结构冗余都比告诉模型"你必须读"更重要。

---

## 3. 策略——附好坏示例

策略按**保证强度**大致排列，最弱但最便宜的在前。

### 策略 1 — 祈使框架，而非"另见"

不要像脚注那样写引用。像承重指令那样写。

#### 差

```markdown
### Step 3: Resolve overlap

Identify which PRs touch the file and produce a unified diff for the user.
For more details on edge cases, see @overlap.md.
```

#### 好

```markdown
### Step 3: Resolve overlap

> ⚠️ STOP — before producing any output for this step, you MUST read
> @examples/overlap.md. Do not improvise. The example contains the only
> correct format for the diff.

Identify which PRs touch the file...
```

**强度:** 低。模型仍可跳过祈使措辞。但低成本地提高了跳过代价。

---

### 策略 2 — 将读取变成编号步骤

跳过编号步骤与跳过"另见"在模型感受上不同。

#### 差

```markdown
### Step 3: Resolve overlap
After analyzing the conflicts, generate the diff.
(Reference: @examples/overlap.md)
```

#### 好

```markdown
### Step 3a: Read @examples/overlap.md in full
### Step 3b: Identify which scenario in the example matches the current case
### Step 3c: Apply the pattern from that scenario to produce the diff
```

**强度:** 中等。编号结构使读取成为工作流主干的一部分。仍可被跳过，但更难。

---

### 策略 3 — 内联锚点 + 引用深度

最有用的单一技术：在内联保留模式的**一行骨架**，完整推理示例放在引用中。锚点引导注意力；引用增加深度。

#### 差 — 纯引用，无锚点

```markdown
### Step 3: Multi-PR overlap resolution

For how to handle overlap, see @examples/overlap-resolution.md.
```

如果模型跳过，它什么都没有。

#### 差 — 完全内联（违背重构目的）

```markdown
### Step 3: Multi-PR overlap resolution

When two or more PRs touch the same file, you must:
1. Fetch the version from each PR using `gh pr view`...
[80 more lines of example with thinking trace]
```

行为有效但膨胀上下文。

#### 好 — 锚点 + 引用

```markdown
### Step 3: Multi-PR overlap resolution

> **Pattern anchor (1-line):** Overlap file → fetch ALL PR versions →
> present LOCAL vs each PR diffs → user picks ONE.
> Full worked example with <thinking> trace: @examples/overlap.md

3a. Identify all PRs that touch this file...
```

**强度:** 好。即使模型跳过引用，锚点也将其引向正确的 token 分布。引用覆盖边界情况的长尾。

---

### 策略 4 — 按风险分层内联 vs 引用（最重要的原则）

渐进式披露**不是统一税**。它只应在"跳过后即兴发挥"的代价可接受时应用。

**决策矩阵:**

| 内容类型 | 放置位置 | 原因 |
|---------|---------|------|
| 高风险步骤示例（overlap 解析、diff 机制、csproj 解析） | **内联在 `SKILL.md`** | 没有这些模型一定会即兴发挥出错。内联代价 >> 失败代价。 |
| 快乐路径示例（单 PR 合并、简单流程） | 提取到 `@examples/...md` 附1行锚点 | 低风险。模型可从步骤指令推断正确行为。 |
| command 和 skill 间的重复逻辑（PR 状态门、标记检测、进度格式） | 保留在 skill SSOT，从 command 删除 | 重复导致漂移；选一个归属地。 |
| 确定性操作（XML 解析、格式验证、标记检测） | **捆绑脚本**，不是 prompt | 100% 确定性，零即兴发挥面。 |

重构的目标不是"最少行数"，而是**在高风险路径上与稳定行为一致的最少行数**。

---

### 策略 5 — 用确定性代码替代 prompt

Anthropic 官方指导：_"确定性操作优先用脚本：写 `validate_form.py` 而非让 Claude 生成验证代码。"_

任何能写成脚本的步骤都应该是脚本。脚本不会即兴发挥。

#### 差

```markdown
### Step 2: Parse the .csproj file

Read the .csproj XML and extract all `<PackageReference>` elements
along with their `Version` attribute. Handle conditional references
(`<PackageReference Condition="...">`) carefully...
```

#### 好

```markdown
### Step 2: Parse the .csproj file

Run `scripts/parse_csproj.py <path>`. The script returns JSON with all
`PackageReference` entries normalized. Use the JSON directly; do not
re-parse XML in prompt.
```

**强度:** 非常高（确定性部分完美）。在操作明确定义时使用。

---

### 策略 6 — 验证循环 / 自检

在高风险步骤末尾添加明确检查清单。不完美，但可作兜底网。

#### 好

```markdown
### Self-check before proceeding:
- [ ] Did you read @examples/overlap.md? (If no, STOP and read now.)
- [ ] Does the diff include both LOCAL and each PR's version?
- [ ] Did you ask the user to pick ONE version?

If any answer is "no", re-read the reference and retry this step.
```

**强度:** 中等。捕获部分跳过。添加成本低。

---

### 策略 7 — 子 agent 隔离（最强）

对真正高风险路径，通过 `Task` 工具生成子 agent，使用隔离、专注的上下文。子 agent 只获得相关 skill 子集，没有其他事可做——无捷径可走。

#### 差

```markdown
### Step 3: Resolve overlap

[80 lines of inline instruction competing with everything else
in the 500-line SKILL.md for the model's attention]
```

#### 好

```markdown
### Step 3: Resolve overlap

Delegate to the `overlap-resolver` sub-agent.
Pass: { files: [...], prs: [...] }
Expect: { resolution: "...", chosen_version: "..." }
```

子 agent 的 prompt 在独立文件中，只在子 agent 的干净上下文内加载。

**强度:** 最高。消除注意力稀释。故障被隔离。易于重试。

**代价:** 架构复杂性。值得用于工作流中最高风险的2-3条路径，不适用于所有路径。

---

### 策略 8 — 经验测试，不要靠猜

你无法猜测跳过率。使用 **promptfoo** 等测试框架运行工作流 N 次并测量：

- 模型是否对引用文件发出了 `view`/`bash` 调用？（检查工具使用追踪。）
- 输出是否匹配预期格式？
- 重新措辞框架是否改变跳过率？

经验迭代。Anthropic 的 `skill-creator` skill 附带专为此设计的评估框架。

#### 差
> "我觉得这个框架应该行，发布吧。"

#### 好
> "基线（916行版本）：0%跳过率，92%格式正确。新版本（450行）：12%跳过率，78%格式正确。→ 拒绝此重构；定位哪个提取导致了回退。"

**强度:** 这才能告诉你其他策略是否真的有效。

---

## 4. 决策框架

决定是否将内联内容提取到引用时：

```
For each chunk of inline content:

  1. Is the step deterministic?
     YES → Replace with a script. Remove from prompt entirely.
     NO  → continue.

  2. If the model improvised this step, would the result be
     (a) wrong-and-the-user-would-not-notice, or
     (b) catastrophically wrong / hard to roll back?
     (a) → safe to extract to @reference. Use Strategy 3 (anchor + reference).
     (b) → keep inline. The token cost is paying for behavioral stability.

  3. Is this content duplicated between command and skill?
     YES → Pick the SSOT (usually the skill), delete from the other.

  4. Could this be a sub-agent boundary?
     YES → Strategy 7. Especially if the step is complex AND
           high-risk AND has a clear input/output contract.
```

---

## 5. 结论

1. **引用读取没有强制执行。** `references/` 中的任何内容都是可选的。将每个 `@reference` 视为模型_可能_跳过的内容。

2. **仅靠散文无法可靠阻止跳过。** 祈使措辞略有帮助；结构变化（编号步骤、锚点、子 agent、脚本）帮助更多。

3. **不要统一提取。** 按风险分层。高风险 few-shot 示例（即兴发挥有危险的）**保持内联**，即使有 token 开销。低风险示例可干净提取。

4. **锚点 + 引用优于纯引用。** 模式的一行骨架内联，即使完整引用被跳过也能引导模型注意力。这是主力模式。

5. **确定性 > prompt。** 任何能写成脚本的都应该是脚本。零即兴发挥面。

6. **子 agent 被低估。** 对于有明确输入/输出契约的高风险多步路径，子 agent 隔离比内联或引用可靠得多。

7. **目标不是"最少行数"。** 目标是**在高风险路径上与稳定行为一致的最少行数**。一个 450 行的重构如果格式正确率下降14个百分点，无论看起来多干净都是失败的重构。

8. **测量，别猜。** 用现有版本建立基线，在每个重构变体上运行固定评估集，只接受保持或提升指标的变更。promptfoo + skill-creator 的评估框架正是为此设计。

---

## 附录：每个重构 PR 的快速检查清单

合并将内容提取到引用的 skill 重构前：

- [ ] 每个提取的引用都有1行内联锚点
- [ ] 高风险步骤（即兴发挥 = 错误输出）仍有内联示例
- [ ] "read @reference"使用编号步骤框架（不是"另见"）
- [ ] 确定性操作是脚本，不是 prompt
- [ ] command 和 skill 间的重复逻辑已合并到一个 SSOT
- [ ] 在基线和新版本上运行评估套件；比较跳过率 + 格式正确率
- [ ] 任何高风险路径的指标回退不超过 2-3%
