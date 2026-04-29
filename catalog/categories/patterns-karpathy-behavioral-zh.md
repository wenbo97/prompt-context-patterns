# Karpathy 行为模式

> **来源:** [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) (68k+ stars, MIT)
> **衍生自:** [Andrej Karpathy 的观察](https://x.com/karpathy/status/2015883857489522876)，关于 LLM 编程常见陷阱
> **提取日期:** 2026-04-21
> **适用范围:** 任何编程 Skill 或 Agent 的通用行为层 -- 与领域特定规则互补

---

## 概述

四个行为模式，用于减少最常见的 LLM 编程错误。与领域模式（告诉 LLM *做什么*）不同，这些模式纠正 LLM *如何思考* -- 解决导致错误行动的推理失误，与领域专业知识无关。

**核心洞察:** 这些模式有效，因为它们瞄准了 LLM 的实际失败模式（静默假设、过度设计、风格漂移、模糊规划），而不仅仅是禁止结果。

**权衡:** 四个模式都偏向谨慎而非速度。建议包含一个安全阀："For trivial tasks, use judgment."

---

## Pattern K1: Surface Assumptions Before Acting

**分类:** Execution Control（扩展 Pattern 7: Interactive Flow Control）

**解决的问题:** LLM 静默选择一种解读并执行。用户在 200 行代码之后才发现错误假设。

**技术:** 强制 LLM 在写任何代码前显式列出假设。如果存在多种解读，呈现出来 -- 不要静默选择。

**模板:**
```markdown
Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.
```

<examples>

### 反面示例：静默假设

```
User: "Add a feature to export user data"

Agent immediately writes:
def export_users(format='json'):
    users = User.query.all()  # Assumed ALL users
    with open('users.json', 'w') as f:  # Assumed file location
        json.dump([u.to_dict() for u in users], f)  # Assumed all fields
```

**问题:**
- 假设了范围（所有用户 vs 过滤子集 -- 隐私影响）
- 假设了输出目标（文件 vs API 端点 vs 邮件）
- 假设了包含哪些字段（某些可能敏感）
- 假设了格式而未询问

### 正面示例：先暴露假设

```
Before implementing, I need to clarify:

1. **Scope**: Export all users or filtered subset? (privacy implications)
2. **Format**: Download file in browser? Background job? API endpoint?
3. **Fields**: Which user fields? (some might be sensitive)
4. **Volume**: How many users typically? (affects approach)

Simplest approach: Add an API endpoint that returns paginated JSON.
What's your preference?
```

</examples>

**在我们插件中的应用:** 交互式命令（`/dev-prompt`, `/compare-output`, `/review`）。不适用于自主迁移阶段 -- 那些有预定义的契约。

**与现有模式的关系:** 加强了 Pattern 7 (Interactive Flow Control)，将假设暴露变成*默认*行为，而不仅仅是对话管理技巧。

---

## Pattern K2: Minimum Viable Code (Anti-Over-Engineering)

**分类:** Execution Control（扩展 Pattern 6: Negative Constraints）

**解决的问题:** LLM 为单次使用的代码产出 Strategy 模式、抽象基类和可配置系统。生成的代码正确但过于复杂。

**技术:** 在写代码前应用一句话试金石。将解决方案限制在解决所述问题的最小范围。

**模板:**
```markdown
- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.
```

<examples>

### 反面示例：过度设计的折扣函数

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float: pass

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage
    def calculate(self, amount: float) -> float:
        return amount * (self.percentage / 100)

class FixedDiscount(DiscountStrategy):
    # ... 30 more lines
```

**问题:**
- 单个折扣类型使用 Strategy 模式
- 抽象基类、dataclass、enum -- 均非需求
- 使用需 30+ 行设置代码来完成一个简单计算

### 正面示例：最小可行代码

```python
def calculate_discount(amount: float, percent: float) -> float:
    """Calculate discount amount. percent should be 0-100."""
    return amount * (percent / 100)
```

**何时增加复杂度:** 只在你确实需要多种折扣类型时。如果该需求后来出现了，到时再重构。

</examples>

**在我们插件中的应用:** build-repair-agent 的修复 -- Agent 应该修复具体错误，而非重新设计周围代码。也适用于 `.NetCore.cs` 存根：最小签名 + `throw NotImplementedException`，仅此而已。

**与现有模式的关系:** 用自检门控加强 Pattern 6 (Negative Constraints)。我们的 guardrails rules 使用重量级版本（8 项 guardrail 检查）。此模式提供轻量级前置过滤："Does this fix trace directly to an error code in the build output?"

---

## Pattern K3: Surgical Changes (Anti-Style-Drift)

**分类:** Safety（扩展 Pattern 12: Read-Only Boundary）

**解决的问题:** LLM 在修 bug 时"顺手改进"相邻代码 -- 添加 type hint、改引号风格、重新格式化空白、重构布尔逻辑。差异中有 40 行变更但实际 fix 只有 2 行。

**技术:** 每行变更必须直接溯源到用户的请求。只清理你的变更造成的孤立代码。

**模板:**
```markdown
When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.
```

<examples>

### 反面示例：修 bug 时顺手重构

```
User: "Fix the bug where empty emails crash the validator"

Agent's diff:
- def validate_user(user_data):
-     # Check email format
-     if not user_data.get('email'):
+ def validate_user(user_data: dict) -> bool:     ← added type hints
+     """Validate user data."""                     ← added docstring
+     email = user_data.get('email', '').strip()
+     if not email:
          raise ValueError("Email required")
-     if '@' not in user_data['email']:
+     if '@' not in email or '.' not in email.split('@')[1]:  ← "improved" validation
          raise ValueError("Invalid email")
-     # Check username
-     if not user_data.get('username'):
+     # Validate username                           ← renamed comment
+     username = user_data.get('username', '').strip()
+     if not username:
          raise ValueError("Username required")
+     if len(username) < 3:                         ← added validation nobody asked for
+         raise ValueError("Username too short")
```

**问题:**
- 添加了无人要求的 type hint
- 添加了 docstring
- 在 bug fix 之外"改进"了邮箱验证
- 添加了用户名验证
- 修改了注释
- 2 行 fix 产出 15 行变更

### 正面示例：只做 bug fix

```diff
  def validate_user(user_data):
      # Check email format
-     if not user_data.get('email'):
+     email = user_data.get('email', '')
+     if not email or not email.strip():
          raise ValueError("Email required")
      
      # Basic email validation
-     if '@' not in user_data['email']:
+     if '@' not in email:
          raise ValueError("Invalid email")
```

**匹配原则:** 没有 type hint，没有 docstring，保留了原有注释风格和布尔模式。只改了修复空邮箱处理的行。

</examples>

**在我们插件中的应用:** build-repair-agent 的核心原则（我们的"do no harm" guardrails）。对 Tier 3 `#if NETFRAMEWORK` 包装同样关键 -- 只包装特定方法，不要重组周围的类。

**与现有模式的关系:** 将 Pattern 12 (Read-Only Boundary) 从"不碰某些文件"扩展到"不碰某些*行*"。我们的 critical rules Tier 2 编码了这点（"SHOULD NOT 'improve' adjacent code"），但缺少负面示例展示推理路径。

---

## Pattern K4: Goal-Driven Execution (Verify-per-Step)

**分类:** Structural（扩展 Pattern 2: Phased/Stepped Execution）

**解决的问题:** LLM 描述模糊计划（"review the code, identify issues, make improvements"）然后不验证就执行变更。步骤没有成功标准。

**技术:** 将每个任务转化为计划，每步有显式的 `-> verify:` 检查。将命令式任务转化为可测试的目标。

**模板:**
```markdown
Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]

Strong success criteria let you loop independently.
Weak criteria ("make it work") require constant clarification.
```

<examples>

### 反面示例：模糊计划

```
I'll fix the authentication system by:
1. Reviewing the code
2. Identifying issues
3. Making improvements
4. Testing the changes
```

**问题:**
- 无成功标准 -- "reviewing"和"identifying"不产生可验证的输出
- 步骤间无检查点 -- 怎么知道 step 2 完成了？
- "Testing the changes"很模糊 -- 什么通过什么失败？

### 正面示例：可验证的目标计划

```
Plan:
1. Write test: Change password → verify old session invalidated
   → verify: test fails (reproduces bug)

2. Implement: Invalidate sessions on password change
   → verify: test passes

3. Check edge cases: multiple sessions, concurrent changes
   → verify: additional tests pass

4. Regression check: existing auth tests still pass
   → verify: full test suite green
```

### 应用于我们的 Tier 4 文件分离:

```
1. Restore original: git checkout master -- File.cs
   → verify: git diff master -- File.cs returns empty

2. Condition Compile to net472
   → verify: grep csproj — exactly 1 entry for File.cs, has Condition

3. Create File.NetCore.cs with stub signatures
   → verify: every public method body is throw new NotImplementedException(...)

4. Add Compile for .NetCore.cs conditioned to .NET Core
   → verify: grep csproj — exactly 1 entry for File.NetCore.cs, has Condition

5. Confirm pair completeness
   → verify: csproj has BOTH Compile entries — if only one, STOP
```

</examples>

**在我们插件中的应用:** 任何多步操作：Tier 4 文件分离、Phase 1.5 迁移快照、Phase 4 推送和 PR。`-> verify:` 后缀将隐式假设转化为显式检查。

**与现有模式的关系:** 通过添加逐步验证加强 Pattern 2 (Phased/Stepped Execution)。我们的 guardrails rules 已定义了 Tier 4 步骤 -- 添加 `-> verify:` 使每步自检。

---

## Meta-Pattern K5: Narrate the LLM's Mistake Path

**分类:** Knowledge（扩展 Pattern 25: Few-Shot Examples）

**解决的问题:** 标准负面示例展示"错误输出"但不展示*为什么 LLM 产出了它*。LLM 看到错误答案但认不出导致错误的自身推理路径 -- 所以换个表面细节就会犯同样的错误。

**技术:** 在负面示例中，叙述 LLM 导向错误行动的内部推理链。展示思考过程，不仅仅是结果。

**这是使 Karpathy 指导方针有效的核心技术。** 以上四个模式都使用了它。

**模板:**
```markdown
**What the agent actually does:**

{Describe the agent's reasoning step by step — what it sees, what it concludes, 
what action it takes, and why each step seemed reasonable at the time.}

```code
{The wrong output}
```

**Why this fails:** {Consequence — what breaks, not just "this is wrong"}

**What should happen:**

```code
{The correct output}
```
```

<examples>

### 标准负面示例（效果较弱）:

```markdown
**Wrong:**
<NoWarn>$(NoWarn);NU1701</NoWarn> in PropertyGroup

**Right:**
NoWarn="NU1701" on PackageReference in .NET Core group
```

### Karpathy 风格负面示例（效果更强）:

```markdown
**What the agent actually does:**

Build produces NU1701 for LegacyOrchestrationSDK. Agent thinks: "NU1701 is a warning, 
I'll suppress it." Searches for "NoWarn NU1701" in the csproj — finds no existing 
NoWarn. Adds `<NoWarn>$(NoWarn);NU1701</NoWarn>` to PropertyGroup because that's 
where other NoWarn entries live.

```xml
<PropertyGroup>
  <NoWarn>$(NoWarn);NU1701</NoWarn>
</PropertyGroup>
```

**Why this fails:** Blanket-suppresses NU1701 for ALL packages on ALL targets. 
Hides real incompatibility warnings on net472, where NU1701 should never fire. 
Violates "do no harm" — net472 behavior changed.

**What should happen:**

Place NU1701 suppression on the specific PackageReference, only in the .NET Core group:

```xml
<ItemGroup Condition="'$(TargetFramework)' != 'net472'">
  <PackageReference Include="LegacyOrchestrationSDK" NoWarn="NU1701" PrivateAssets="all" />
</ItemGroup>
```
```

</examples>

**关键区别:** Karpathy 风格示例展示"Agent thinks: '...'" -- LLM 识别出自己的推理模式并避免它。标准示例只展示错误的 XML，LLM 可能通过不同的推理路径产出相同错误。

**在我们插件中的应用:** 每条 guardrail 规则、每条 NEVER 规则、每个反模式条目。对 Agent 反复违反的规则尤其有效（NU1701 放置、bare Compile conditioning、REPLACE_LOCKED 回滚）。

**与现有模式的关系:** 将 Pattern 25 (Few-Shot Examples) 从"展示输入 -> 输出对"扩展到"展示推理 -> 输出 -> 后果链"。我们的 `build-repair-examples.md` 部分做到了这点 -- Karpathy 技术使其系统化。

---

## 采纳检查清单

编写新规则、guardrail 或错误处理条目时：

| 检查项 | 模式 |
|--------|------|
| 规则是否说明了权衡以及何时可以覆盖？ | K1（安全阀） |
| 规则是否有一句话试金石？ | K2（"Does this fix trace to an error code?"） |
| 负面示例是否叙述了 Agent 的推理路径？ | K5（叙述错误路径） |
| 负面示例是否说明了后果，而非仅仅"wrong"？ | K5（why this fails） |
| 多步指令的每步是否都有 `-> verify:`？ | K4（verify-per-step） |
| 规则是否区分了"你的清理残余"和"已有的遗留问题"？ | K3（只清理自己造成的孤立代码） |

---

## 汇总表

| 模式 | 预防的问题 | 一句话总结 |
|------|-----------|-----------|
| K1: Surface Assumptions | 静默错误解读 | "If uncertain, ask -- don't pick silently" |
| K2: Minimum Viable Code | 过度设计 | "Would a senior engineer say this is overcomplicated?" |
| K3: Surgical Changes | 风格漂移、顺手重构 | "Every changed line traces to the user's request" |
| K4: Goal-Driven Execution | 无验证的模糊计划 | "Each step has -> verify: [check]" |
| K5: Narrate Mistake Path | 换个表面细节犯同样的错 | "Show the agent's reasoning that led to the wrong action" |
