# Karpathy Behavioral Patterns

> **Source:** [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) (68k+ stars, MIT)
> **Derived from:** [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls
> **Extraction date:** 2026-04-21
> **Applicability:** General behavioral layer for any coding skill or agent — complements domain-specific rules

---

## Overview

Four behavioral patterns that reduce the most common LLM coding mistakes. Unlike domain patterns (which tell the LLM *what* to do), these patterns correct *how* the LLM thinks — addressing reasoning failures that cause wrong actions regardless of domain expertise.

**Key insight:** These patterns work because they target the LLM's actual failure modes (silent assumption, over-engineering, style drift, vague planning) rather than just prohibiting outcomes.

**Tradeoff:** All four patterns bias toward caution over speed. Include an escape valve: "For trivial tasks, use judgment."

---

## Pattern K1: Surface Assumptions Before Acting

**Category:** Execution Control (extends Pattern 7: Interactive Flow Control)

**Problem it solves:** LLMs silently pick one interpretation and run with it. The user only discovers the wrong assumption after 200 lines of code.

**Technique:** Force the LLM to list assumptions explicitly before writing any code. If multiple interpretations exist, present them — don't pick silently.

**Template:**
```markdown
Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.
```

<examples>

### ❌ Bad: Silent assumption

```
User: "Add a feature to export user data"

Agent immediately writes:
def export_users(format='json'):
    users = User.query.all()  # Assumed ALL users
    with open('users.json', 'w') as f:  # Assumed file location
        json.dump([u.to_dict() for u in users], f)  # Assumed all fields
```

**Problems:**
- Assumed scope (all users vs filtered subset — privacy implications)
- Assumed output destination (file vs API endpoint vs email)
- Assumed which fields to include (some might be sensitive)
- Assumed format without asking

### ✅ Good: Surface assumptions first

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

**When to use in our plugin:** Interactive commands (`/dev-prompt`, `/compare-output`, `/review`). NOT for autonomous migration phases — those have pre-defined contracts.

**Relationship to existing patterns:** Strengthens Pattern 7 (Interactive Flow Control) by making assumption-surfacing the *default* behavior, not just a conversation management technique.

---

## Pattern K2: Minimum Viable Code (Anti-Over-Engineering)

**Category:** Execution Control (extends Pattern 6: Negative Constraints)

**Problem it solves:** LLMs produce Strategy patterns, abstract base classes, and configurable systems for single-use code. The generated code is correct but overcomplicated.

**Technique:** Apply a one-sentence litmus test before writing code. Cap the solution at the minimum that solves the stated problem.

**Template:**
```markdown
- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.
```

<examples>

### ❌ Bad: Over-engineered discount function

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

**Problems:**
- Strategy pattern for a single discount type
- Abstract base class, dataclass, enum — none requested
- Usage requires 30+ lines of setup for a simple calculation

### ✅ Good: Minimum viable code

```python
def calculate_discount(amount: float, percent: float) -> float:
    """Calculate discount amount. percent should be 0-100."""
    return amount * (percent / 100)
```

**When to add complexity:** Only when you actually need multiple discount types. If that requirement comes later, refactor then.

</examples>

**When to use in our plugin:** Build-repair-agent fixes — the agent should fix the specific error, not redesign the surrounding code. Also applies to `.NetCore.cs` stubs: minimum signatures + `throw NotImplementedException`, nothing more.

**Relationship to existing patterns:** Reinforces Pattern 6 (Negative Constraints) with a self-check gate. Our guardrails rules uses the heavy version (8 guardrail checks). This pattern provides the lightweight pre-filter: "Does this fix trace directly to an error code in the build output?"

---

## Pattern K3: Surgical Changes (Anti-Style-Drift)

**Category:** Safety (extends Pattern 12: Read-Only Boundary)

**Problem it solves:** LLMs "improve" adjacent code while fixing a bug — adding type hints, changing quote styles, reformatting whitespace, refactoring boolean logic. The diff contains 40 changed lines for a 2-line fix.

**Technique:** Every changed line must trace directly to the user's request. Clean up only orphans YOUR changes created.

**Template:**
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

### ❌ Bad: Drive-by refactoring while fixing a bug

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

**Problems:**
- Added type hints nobody asked for
- Added docstring
- "Improved" email validation beyond the bug fix
- Added username validation
- Changed comments
- 15 changed lines for a 2-line fix

### ✅ Good: Only the bug fix

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

**Matched:** No type hints, no docstring, existing comment style, existing boolean pattern. Only changed the lines that fix empty email handling.

</examples>

**When to use in our plugin:** Core principle for build-repair-agent (our "do no harm" guardrails). Also critical for Tier 3 `#if NETFRAMEWORK` wraps — wrap only the specific method, don't reorganize the surrounding class.

**Relationship to existing patterns:** Extends Pattern 12 (Read-Only Boundary) from "don't touch certain files" to "don't touch certain *lines*." Our critical rules Tier 2 encodes this ("SHOULD NOT 'improve' adjacent code"), but without the negative example showing the reasoning path.

---

## Pattern K4: Goal-Driven Execution (Verify-per-Step)

**Category:** Structural (extends Pattern 2: Phased/Stepped Execution)

**Problem it solves:** LLMs describe vague plans ("review the code, identify issues, make improvements") then make changes without verification. Steps have no success criteria.

**Technique:** Transform every task into a plan where each step has an explicit `→ verify:` check. Convert imperative tasks into testable goals.

**Template:**
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

### ❌ Bad: Vague plan

```
I'll fix the authentication system by:
1. Reviewing the code
2. Identifying issues
3. Making improvements
4. Testing the changes
```

**Problems:**
- No success criteria — "reviewing" and "identifying" produce no verifiable output
- No checkpoint between steps — how do you know step 2 is complete?
- "Testing the changes" is vague — what passes, what fails?

### ✅ Good: Verifiable goal plan

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

### ✅ Applied to our Tier 4 file separation:

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

**When to use in our plugin:** Any multi-step operation: Tier 4 file separation, Phase 1.5 migration snapshot, Phase 4 push-and-PR. The `→ verify:` suffix converts implicit assumptions into explicit checks.

**Relationship to existing patterns:** Strengthens Pattern 2 (Phased/Stepped Execution) by adding per-step verification. Our guardrails rules already define the Tier 4 steps — adding `→ verify:` makes each step self-checking.

---

## Meta-Pattern K5: Narrate the LLM's Mistake Path

**Category:** Knowledge (extends Pattern 25: Few-Shot Examples)

**Problem it solves:** Standard negative examples show "wrong output" but not *why the LLM produced it*. The LLM sees the wrong answer but doesn't recognize its own reasoning that led there — so it makes the same mistake with different surface details.

**Technique:** In negative examples, narrate the LLM's internal reasoning chain that leads to the wrong action. Show the thought process, not just the result.

**This is the core technique that makes the Karpathy guidelines effective.** All four patterns above use it.

**Template:**
```markdown
**❌ What the agent actually does:**

{Describe the agent's reasoning step by step — what it sees, what it concludes, 
what action it takes, and why each step seemed reasonable at the time.}

```code
{The wrong output}
```

**Why this fails:** {Consequence — what breaks, not just "this is wrong"}

**✅ What should happen:**

```code
{The correct output}
```
```

<examples>

### Standard negative example (less effective):

```markdown
**Wrong:**
<NoWarn>$(NoWarn);NU1701</NoWarn> in PropertyGroup

**Right:**
NoWarn="NU1701" on PackageReference in .NET Core group
```

### Karpathy-style negative example (more effective):

```markdown
**❌ What the agent actually does:**

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

**✅ What should happen:**

Place NU1701 suppression on the specific PackageReference, only in the .NET Core group:

```xml
<ItemGroup Condition="'$(TargetFramework)' != 'net472'">
  <PackageReference Include="LegacyOrchestrationSDK" NoWarn="NU1701" PrivateAssets="all" />
</ItemGroup>
```
```

</examples>

**Key difference:** The Karpathy-style example shows "Agent thinks: '...'" — the LLM recognizes its own reasoning pattern and avoids it. The standard example only shows the wrong XML, which the LLM may produce via a different reasoning path.

**When to use in our plugin:** Every guardrail rule, every NEVER rule, every anti-pattern entry. Especially effective for rules the agent repeatedly violates (NU1701 placement, bare Compile conditioning, REPLACE_LOCKED revert).

**Relationship to existing patterns:** Extends Pattern 25 (Few-Shot Examples) from "show input → output pairs" to "show reasoning → output → consequence chains." Our `build-repair-examples.md` partially does this — the Karpathy technique makes it systematic.

---

## Adoption Checklist

When writing new rules, guardrails, or error-handling entries for this plugin:

| Check | Pattern |
|-------|---------|
| Does the rule state its tradeoff and when to override? | K1 (escape valve) |
| Does the rule have a one-sentence litmus test? | K2 ("Does this fix trace to an error code?") |
| Do negative examples narrate the agent's reasoning path? | K5 (narrate mistake path) |
| Do negative examples state the consequence, not just "wrong"? | K5 (why this fails) |
| Do multi-step instructions have `→ verify:` on each step? | K4 (verify-per-step) |
| Does the rule distinguish "your mess" from "pre-existing mess"? | K3 (clean up only your orphans) |

---

## Summary Table

| Pattern | What It Prevents | One-Liner |
|---------|-----------------|-----------|
| K1: Surface Assumptions | Silent wrong interpretation | "If uncertain, ask — don't pick silently" |
| K2: Minimum Viable Code | Over-engineering | "Would a senior engineer say this is overcomplicated?" |
| K3: Surgical Changes | Style drift, drive-by refactoring | "Every changed line traces to the user's request" |
| K4: Goal-Driven Execution | Vague plans without verification | "Each step has → verify: [check]" |
| K5: Narrate Mistake Path | Repeating mistakes with different surface details | "Show the agent's reasoning that led to the wrong action" |
