# 引用跳过问题：操作手册

当 Claude Code skill 通过 `@path/to/file.md` 引用外部文件时，运行时 agent 有时会**跳过读取并即兴发挥**。本文描述该问题，将其分解为三种不同的故障模式，并提供十一种解决模式，附适用场景和好坏示例。

---

## 1. 问题陈述

### 1.1 渐进式披露的承诺

Claude Code skill 使用三层渐进式披露模型：

1. **第一层（始终加载）** — 每个已安装 skill 的 YAML frontmatter `name` + `description`（各约100 token）。
2. **第二层（触发时加载）** — 模型决定 skill 适用时加载完整 `SKILL.md` 正文。
3. **第三层（按需加载）** — 捆绑文件如 `references/foo.md`、`examples/bar.md`、`scripts/baz.py`。模型**选择**读取这些文件。

第三层的承诺：保持 `SKILL.md` 精简，将示例和边界情况推入卫星文件，节省上下文预算。

### 1.2 出了什么问题

第三层是自愿的。**没有强制机制。** 模型可以忽略 `@reference` 并照样产出输出。当它这样做时，输出通常形状合理但事实有误——错误的格式、错误的场景分类、错误的边界情况处理。

跳过不是模型"试图节省 token"。它是下一 token 预测与 prompt 结构交互的下游效应。当模型到达 `@reference` 时，它可能已经有了一个答案，而引用只会与之矛盾——与其矛盾自己，不如跳过一个脚注。

### 1.3 为什么危险

引用跳过是**静默故障**：

- 模型产出看起来合理的输出。
- 它不会宣布"我跳过了引用"。
- 错误仅在下游工具拒绝时、人类注意到格式错误时，或最坏的情况——错误输出被提交并部署时才浮现。

这与工具错误或拒绝根本不同：那些是可见的。跳过故障伪装成成功。

---

## 2. 根因：三种不同的故障模式

朴素框架——"模型在偷懒"——不可操作。分解为三种经常共现但需要不同修复的故障模式：

### 模式 A — 裸跳转

`@reference` 出现时没有说明跳转理由的上下文脚手架。周围文字未建立*为什么*读取文件是必要的。引用读起来像脚注，不像指令。

> _症状：引用出现在段落末尾的柔和散文中（"for details, see..."）。模型将其视为可选并继续。_

### 模式 B — 预满足

当模型遇到 `@reference` 时，它已采样了看似合理的续写。引用会迫使它修改，但现有草稿满足了局部目标。跳过比重新推导便宜。

> _症状：即使有强"you must read X"框架，模型仍跳过。引用在流程中出现太晚。_

### 模式 C — 可选框架

引用的语言风格使其听起来可以忽略。如 *see*、*refer*、*for details*、*FYI*、*if interested* 等词对模型的信号与对人类读者相同："脚注"。

> _症状：引用位置正确且出现够早，但措辞没有传达"这是必需的"。_

### 为什么分解很重要

三种模式有**不可互换的修复**：

| 模式 | 什么坏了 | 什么能修复 |
|------|---------|-----------|
| A | 周围上下文未证明跳转合理 | 内联锚点 + 因果措辞 + 编号步骤 |
| B | 模型在读取前已经做出决定 | 提前放置引用；子 agent 隔离；输出 schema 要求引用内容 |
| C | 语言风格读起来可以跳过 | 祈使框架（"STOP — read X"） |

遭受模式 B 的 skill 不会被更强的模式 C 祈使句拯救。先正确诊断再应用修复。

---

## 3. 解决模式

十一种模式，按**作用机制**而非字母顺序组织。每个条目：做什么、针对哪种故障模式、适用场景、不适用场景，以及好坏示例。

### Pattern 1 — 祈使 + STOP 框架

**机制:** 将柔和的"see also"语言替换为祈使"STOP — read this before continuing"。

**针对:** 模式 C（可选框架）。

**使用时机:** 引用位置合理且确实必需——你只需要语言风格匹配。

**不单独使用时:** 模型已有空间做出决定（模式 B）——更大声的措辞不会撤销已起草的计划。

#### 差

```markdown
After analyzing the conflicts, generate a unified diff for the user.
For details on edge cases, see @examples/overlap.md.
```

引用读起来像脚注。

#### 好

```markdown
After analyzing the conflicts, generate a unified diff for the user.

> ⚠️ STOP — before producing any diff, you MUST read @examples/overlap.md.
> Do not improvise the format. The example contains the only correct
> structure; deviating will fail downstream validation.
```

利害被点名，动作是祈使，跳过的后果是明确的。

---

### Pattern 2 — 将读取作为编号步骤

**机制:** 将"读引用"从附注提升为工作流中自己的编号步骤。

**针对:** 模式 A（裸跳转）。

**使用时机:** 多步工作流中某步骤在继续前需要外部知识。

**不使用时:** 单步任务；或引用很短（<10行），内联比仪式化更便宜。

#### 差

```markdown
### Step 3: Resolve overlap

When two PRs touch the same file, fetch each version, diff them,
and let the user pick. (Reference: @examples/overlap.md)
```

引用是注释，不是动作。

#### 好

```markdown
### Step 3a: Read @examples/overlap.md in full

### Step 3b: Identify which scenario in the example matches the
current overlap (multi-PR same-line, multi-PR different-line, etc.)

### Step 3c: Apply the matched scenario's resolution pattern.
```

读取文件现在是可检查的步骤。跳过在结构上是可见的。

---

### Pattern 3 — 内联锚点 + 引用深度

**机制:** 内联嵌入模式的一行骨架；完整推理示例放在引用中。锚点引导注意力；引用增加深度。

**针对:** 主要模式 A；部分模式 B（锚点在模型漂移前播种正确的 token 分布）。

**使用时机:** 多数引用——这是主力模式。除非有特定理由选择其他模式，否则默认使用此形状。

**不使用时:** 步骤风险太高，即使锚点也不够，完整示例必须保留内联（使用 Pattern 7）。

#### 差 — 纯引用，无锚点

```markdown
### Step 3: Multi-PR overlap resolution

For how to handle overlap, see @examples/overlap-resolution.md.
```

如果模型跳过，没有任何可回退的。

#### 差 — 完全内联（违背渐进式披露目标）

```markdown
### Step 3: Multi-PR overlap resolution

When two or more PRs touch the same file, you must fetch each
version using `gh pr view <PR>:<file>`, then construct a unified
diff with the LOCAL version on top, each PR version below...
[80 more lines of example]
```

行为有效，但将 `SKILL.md` 膨胀超过可用长度。

#### 好 — 锚点 + 引用

```markdown
### Step 3: Multi-PR overlap resolution

> **Pattern (1-line):** Overlap file → fetch ALL PR versions →
> present LOCAL vs each PR diffs → user picks ONE.
> Full worked example with <thinking> trace: @examples/overlap.md

3a. Identify all PRs that touch this file...
```

即使模型跳过引用，锚点也将其引向正确形状。引用捕获边界情况的长尾。

---

### Pattern 4 — 前置引用

**机制:** 将关键 `@reference` 读取移到 `SKILL.md` 顶部，在任何可执行步骤之前。在模型有机会起草计划前读取文件。

**针对:** 模式 B（预满足）。

**使用时机:** 引用描述工作流级不变量——命名约定、格式规则、分类体系——贯穿整个工作流，而非某一步。

**不使用时:** 引用高度局限于某一特定步骤；前置它会在到达相关步骤时稀释注意力。

#### 差 — 引用太晚

```markdown
### Step 1: Parse input
### Step 2: Determine PRs
### Step 3: Fetch versions
### Step 4: Build diff
   Format follows the rules in @rules/diff-format.md.
### Step 5: Present to user
```

到 Step 4 时，模型已吸收周围上下文，可能在读取规则前就勾勒了 diff。

#### 好 — 前置

```markdown
## Required context (read before proceeding)

@rules/diff-format.md — diff structure used throughout this skill

---

### Step 1: Parse input
### Step 2: Determine PRs
...
```

格式规则在任何起草前已被吸收。

---

### Pattern 5 — 强制清单读取

**机制:** Skill 第一步是"按顺序读取这些文件"并显式确认。跳过变成门控，不是流程中途的决策。

**针对:** 模式 A + 模式 B 同时（读取是第一个动作，不是旁支任务）。

**使用时机:** 多个引用都是必需的，你无法信任选择性读取。

**不使用时:** 大多数用户不需要大多数引用；或清单本身成为 token 预算负担。

#### 差 — 引用分散

```markdown
### Step 1: ... (uses @rules/A.md)
### Step 2: ... (uses @rules/B.md)
### Step 3: ... (uses @rules/C.md)
```

三次独立的跳过机会。

#### 好 — 单一清单门控

```markdown
## Step 0: Required context

Before doing anything else, read these files top to bottom:

1. @rules/diff-format.md
2. @examples/overlap-cases.md
3. @rules/csproj-conventions.md

State "context loaded" when complete. Do not proceed otherwise.
```

一个门控，一个决策点，低跳过面。

---

### Pattern 6 — 输出 schema 要求引用内容

**机制:** 设计输出格式使正确答案**不可能**不读取引用。强制模型输出仅存在于引用文件中的值。

**针对:** 模式 B（预满足）。即使模型有草稿答案，schema 也强制重新推导。

**使用时机:** 引用包含离散可枚举的类别、场景名或封闭分类体系，你可以在输出中要求。

**不使用时:** 引用是连续散文，没有可命名的离散元素；输出格式受外部约束，你无法添加字段。

#### 差 — schema 与引用无关

```markdown
Output a JSON object with:
- `summary`: brief description
- `recommendation`: what to do
```

模型可以从任何地方产生这些。

#### 好 — schema 要求引用内容

```markdown
Output a JSON object with:
- `applied_scenario`: one of [
    "multi_pr_same_line",
    "multi_pr_different_line",
    "version_conflict",
    "namespace_collision"
  ] — defined in @examples/overlap.md
- `decision_trace`: which paragraph in @examples/overlap.md
  the resolution was based on
- `recommendation`: ...
```

场景名不在 `SKILL.md` 中。要产生它们，模型必须读取引用。可 grep 审计随之而来：如果 `applied_scenario` 是发明的或不认识的，跳过可以被检测到。

---

### Pattern 7 — 按风险分层内联

**机制:** 拒绝为最高风险步骤提取示例。即使有 token 成本也保留内联。只为低风险路径提取。

**针对:** 所有三种模式——通过完全移除跳转。

**使用时机:** 特定步骤在被提取后反复失败；或失败后果严重（错误代码被提交、生产配置损坏、PR 错误合并）。

**不使用时:** 大面积使用——将所有内容内联违背了渐进式披露，且在 500 行 `SKILL.md` 之后遇到注意力衰减问题。

#### 差 — 为"整洁"提取所有内容

```markdown
### Step 3: Overlap resolution → @examples/overlap.md
### Step 4: csproj merge       → @examples/csproj.md
### Step 5: Branch sync        → @examples/branch.md
```

三个高风险步骤，三个跳过机会。

#### 好 — 按风险分层

```markdown
### Step 3: Overlap resolution

[80 lines of inline example with <thinking> trace — too risky to extract]

### Step 4: csproj merge

[80 lines of inline example — same reasoning]

### Step 5: Branch sync (low-risk happy path)

> **Pattern:** fetch → rebase → push. See @examples/branch.md for the
> rare conflict case.
```

高风险步骤支付内联税。低风险步骤使用锚点 + 引用。

---

### Pattern 8 — 确定性脚本

**机制:** 用脚本调用替代 prompt 步骤。模型调用脚本；脚本完成工作。没有 prompt 路径意味着没有即兴发挥面。

**针对:** 所有三种模式——消除 prompt 即消除伴随它的故障模式。

**使用时机:** 步骤定义明确，输入输出可枚举——XML 解析、格式验证、标记检测、文件 diff、版本比较、正则提取。

**不使用时:** 步骤需要语义判断（代码意图、用户意图、代码评审）；I/O 边界模糊。

#### 差 — prompt 当解析器

```markdown
### Step 2: Parse the .csproj file

Read the .csproj XML and extract all `<PackageReference>` elements
along with their `Version` attribute. Handle conditional references
(`<PackageReference Condition="...">`) carefully...
```

模型被要求在 prompt 中做 XML 解析，带有所有随之而来的脆弱性。

#### 好 — 脚本调用

```markdown
### Step 2: Parse the .csproj file

Run `scripts/parse_csproj.py <path>`. The script returns JSON with
all PackageReference entries, normalized. Use the JSON directly;
do not re-parse the XML.
```

100% 确定性。没有 prompt 级即兴发挥的可能。

---

### Pattern 9 — 子 agent 隔离

**机制:** 通过 `Task` 工具将高风险子流程委派给子 agent。子 agent 只接收相关 skill 子集并以干净上下文启动。

**针对:** 主要模式 B（预满足）。子 agent 启动时没有已提交的计划。也针对模式 A——子 agent 的 prompt 是聚焦的，所以引用不是从长父流程的裸跳转。

**使用时机:** 复杂的多步子流程，高风险，有清晰的输入/输出契约。工作流中最高风险的两三条路径。

**不使用时:** 步骤极短（子 agent 开销超过收益）；I/O 契约不清楚（子 agent 不知道返回什么）。

#### 差 — 高风险步骤内联在长父流程中

```markdown
### Step 7: Resolve overlap

[80 lines of instruction competing with the surrounding 400-line
SKILL.md for the model's attention; references appear deep into
a long execution chain where attention has decayed]
```

#### 好 — 子 agent 边界

```markdown
### Step 7: Resolve overlap

Delegate to the `overlap-resolver` sub-agent via Task tool.

Input: { files: [...], prs: [...], local_branch: "..." }
Expect: { resolution: "...", chosen_version: "...", trace: "..." }

Validate the returned `chosen_version` exists in one of the input PRs.
```

子 agent 的 prompt 在独立文件中。在该 prompt 内，引用在无竞争关切的干净上下文中被读取。

---

### Pattern 10 — 自检 / 验证循环

**机制:** 在高风险步骤末尾附加明确检查清单。强制模型回答"我读了X吗？我的输出有Y吗？"然后再继续。

**针对:** 三种模式的兜底网。不是主要防御——模型也可以在检查清单上自欺——但有意义比例的跳过可以被捕获。

**使用时机:** 叠加在其他模式上。作为单一防御它很弱；作为纵深防御中的一层它物有所值。

**不单独使用时:** 用作唯一缓解——模型可以产生看似合理的所有"是"的检查清单而实际未做工作。

#### 差 — 无验证

```markdown
### Step 3: Resolve overlap

Identify which PRs touch the file and produce a diff.
```

无反思门控。模型无论是否跳过引用都继续前进。

#### 好 — 明确自检

```markdown
### Step 3: Resolve overlap

[step body]

### Self-check before proceeding to Step 4:

- [ ] Did you read @examples/overlap.md? (If not, STOP and read now.)
- [ ] Does your diff include both LOCAL and each PR's version?
- [ ] Did you ask the user to pick exactly ONE version?
- [ ] Did you record the chosen version in the migration marker?

If any answer is "no", re-read the reference and retry this step.
```

捕获部分跳过。叠加 Pattern 3 或 9 获得更强保证。

---

### Pattern 11 — Hooks（Claude Code 专有）

**机制:** 使用 Claude Code 的 hook 系统在 skill 执行前机械地强制条件——如验证必需文件已被读取、验证必需工具已被调用。

**针对:** 所有三种模式——这是唯一提供**机械保证**而非行为建议的模式。

**使用时机:** 真正关键的路径，不接受任何即兴发挥。跳过的成本足够高，值得维护 hook 的负担。

**不使用时:** 引用是锦上添花而非必须；hook 本身比偶尔跳过负担更重；hook 会阻塞合理的灵活性。

**注意:** Hook 能力取决于你的 Claude Code 版本和项目配置。在围绕它们设计之前验证你环境中可用的功能。

---

## 4. 决策矩阵

| 场景 | 主要 | 叠加 |
|------|------|------|
| 步骤可脚本化（解析、验证、格式检查） | **Pattern 8** | — |
| 高风险步骤有清晰 I/O 契约 | **Pattern 9** | Pattern 6（output schema） |
| 高风险步骤 I/O 模糊 | **Pattern 7**（内联） | Pattern 5（清单）+ 6（schema） |
| 中风险多步，怀疑模型漂移 | **Pattern 3** + **Pattern 2** | Pattern 10（自检） |
| 多个引用全部必需 | **Pattern 5**（清单） | Pattern 4（前置） |
| 引用包含离散可枚举类别 | **Pattern 6**（output schema） | Pattern 3（锚点） |
| 引用是工作流级不变量 | **Pattern 4**（前置） | Pattern 1（祈使） |
| 引用框架只是太软 | **Pattern 1**（祈使） | — |
| 关键路径，不接受即兴发挥 | **Pattern 11**（hook） | Pattern 8 + 9 |

---

## 5. 选择的元原则

### 5.1 消除优于缓解

如果步骤可以脚本化（Pattern 8）或 hook 化（Pattern 11），先做那个。不要在不必以 prompt 形式存在的 prompt 路径上叠加缓解措施。消除即兴发挥面在结构上比用措辞与之对抗更强。

### 5.2 先诊断模式再应用修复

三种故障模式不可互换。更强的祈使措辞（Pattern 1）对预满足（模式 B）无效。前置引用（Pattern 4）对可选框架（模式 C）无效。在你的具体情况中识别哪种模式在作怪，然后再选择模式。

诊断问题：

- _模型产出的东西看起来正确但使用了错误格式？_ → 可能是模式 C（它知道去哪里看，但不觉得有义务）。试 Pattern 1。
- _模型产出的东西内部一致但与引用内容不一致？_ → 可能是模式 B（它先有了自己的答案）。试 Pattern 4 / 9 / 6。
- _模型产出的东西与引用的领域完全脱节？_ → 可能是模式 A（跳转根本没注册到）。试 Pattern 2 / 3 / 5。

### 5.3 高风险路径的纵深防御

对真正关键的步骤，叠加 2-3 个模式是合适的，不是过度工程。子 agent (9) + 内联锚点 (3) + output schema (6) 覆盖同一步骤是合理的，当步骤值得保护时。没有单个模式覆盖所有三种故障模式。

### 5.4 目标是行为稳定性，不是最少行数

一个 450 行的 `SKILL.md` 如果格式正确率下降 14 个百分点，无论看起来多干净都是回退。重构不是免费的；将内容移到引用中的结构变更必须用补偿失去的内联脚手架的模式来支付。如果模式不能完全补偿，内容就不应该被移走。

### 5.5 能测量时就测量

引用跳过行为无法通过阅读 prompt 可靠地预测。唯一诚实的测试是运行工作流 N 次并观察引用是否实际被读取（在工具使用追踪中可见）以及输出是否正确。在宣布重构成功之前，对受影响的工作流建立简单的冒烟测试通过，即使没有完整的评估框架。

---

## 6. 应避免的反模式

一个简短清单，列出持续使跳过问题恶化的做法：

- **道歉式框架。** _"You may want to look at @ref"_ — 听起来像建议，不是指令。
- **长列表中截断的引用路径。** 当一个步骤随意列出六个 `@references` 时，模型将其视为参考文献，不是阅读清单。
- **引用不存在的文件**（被重命名或移动）。模型静默失败并即兴发挥。在 CI 中验证引用。
- **在低风险步骤上叠加五个模式**因为模式"好"。模式有成本（行数、注意力稀释、维护）。在它们赚回成本的地方应用。
- **将 SKILL.md 视为唯一需要模式的地方。** 如果调用 command 复制了 skill 逻辑，应用在 skill 上的模式在 command 的 prompt 漂移时不起作用。先消除重复。

---

## 7. 总结

引用跳过问题是**渐进式披露下的静默即兴发挥**。它有三种不同的故障模式——裸跳转、预满足、可选框架——需要不可互换的修复。十一种模式覆盖该空间，从最廉价的缓解（祈使措辞）到最强的保证（hook 和脚本）。按诊断选择，消除优于缓解，在高风险路径上叠加，重构时测量结果。

最深层的原则：**渐进式披露不是统一税**。它是逐步决策，在 token 成本与即兴发挥风险之间权衡。任何单个 skill 都应该有内联的步骤、带锚点引用的步骤、脚本步骤和子 agent 步骤——根据风险和 I/O 形状逐步选择，而非作为项目级策略统一选择。
