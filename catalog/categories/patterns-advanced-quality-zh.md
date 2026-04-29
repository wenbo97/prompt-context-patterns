# 高级质量、审查与评估模式

代码审查、bug 分析、测试生成和 LLM-as-Judge 评估的深度模式 — 在 560+ 插件中发现的生产级架构，扩展了基础质量模式（27-30）。

**来源研究：** code-review, code-reviewer, peer-reviewer, deep-review, pr-review-critic, aspen-pr-review, review-swarm, review-verdict, consensus-code-review, bug-assessor, bug-hunter, test-sentinel, llm-as-judge-eval, plugin-eval, hackathon-evaluator, retro-bar-raiser

---

## Pattern 45: Directive-Based Review with on_fail Classification

**出现频率：** 约 2% 的审查插件
**相关模式：** [Scoring Rubrics](#pattern-27), [Negative Constraints](#pattern-6)

**定义：** 通过 YAML "directives" 参数化审查，每个标准带有 `on_fail` 字段（`fail` 或 `review`），决定"Not Met"判定是阻塞性还是建议性的。

### 正面示例

```yaml
criteria:
  - text: All codeflows from the PR-linked issues are fixed
    on_fail: review
  - text: At least one codeflow shows progress (non-zero fix count)
    on_fail: fail
  - text: No high-severity risks introduced
    on_fail: fail
```

决策规则（三路）：
- **Fail**：任何 `on_fail: fail` 标准为 `Not Met`，`build_error_likelihood` 为 `High`，`runtime_error_likelihood` 为 `High`
- **Pass**：所有标准均为 `Met`，两种 likelihood 均为 `Low`，无 priority <= 2 的 uncertainty，无 Medium+ risk
- **Review**：其他情况（证据不足时倾向 Review 而非 Pass）

**为什么有效：** `on_fail` 字段让每个标准的阻塞性 vs 建议性明确。三路决策（Pass/Review/Fail）避免了二元陷阱，不是"通过"就是"拒绝"。倾向 Review 而非 Pass 防止虚假自信。

### 反面示例

```yaml
criteria:
  - text: All codeflows from the PR-linked issues are fixed
  - text: At least one codeflow shows progress (non-zero fix count)
  - text: No high-severity risks introduced

Decision: If any criterion is Not Met → Fail. Otherwise → Pass.
```

**为什么失败：** 没有 `on_fail` 分类，每个未满足的标准都同样具有阻塞性。一个轻微的不完整 codeflow 修复与高严重性风险引入产生相同判定。二元 Pass/Fail 决策迫使审查者要么对不完整工作盖章要么因建议性问题阻塞 PR。

---

## Pattern 46: Multi-Stage Repo Discovery Before Review

**出现频率：** 约 2% 的审查插件
**相关模式：** [Reference File Injection](#pattern-23), [Domain Knowledge Embedding](#pattern-24)

**定义：** 在审查任何代码之前，agent 执行多个发现阶段以学习仓库的约定、架构和模式 — 然后应用校准到所学内容的审查标准。

### 正面示例

```markdown
## Discovery (before any review)
- Stage 0: Tech stack detection (Backend/Frontend/Library/Infra/Full-stack)
- Stage 1a: Architecture & wiring
- Stage 1b: Conventions & patterns
- Stage 1c: Functional flows
- Stage 1d: Test patterns
- Stage 1e: Data access patterns
- Stage 1f: Best-practice inventory
- Stage 2: Business context and intent (trace call chains, identify scale/frequency)

## 6-Dimension Review (after discovery)
1. Convention Enforcement
2. Completeness (Round-the-Circle)
3. Security (OWASP-aligned)
4. Performance
5. Data Access
6. Test Coverage
```

包含一个 29 点的 **Coding Conventions Checklist**（A1-A29），带有语言特定示例。

**为什么有效：** 发现阶段防止模型对有特定约定的仓库应用通用审查标准。理解仓库模式的审查者能捕获有意义的违规，而非误报。

### 反面示例

```markdown
## Review Checklist
1. Check for code style violations
2. Check for security issues
3. Check for performance problems
4. Check for test coverage
5. Verify PR description is complete
```

**为什么失败：** 检查清单在没有任何仓库发现的情况下应用通用标准。它会标记实际上是仓库约定的风格违规，遗漏项目特定模式（如必需的中间件注册），产出侵蚀开发者对审查者信任的误报。

---

## Pattern 47: Evidence-First Review ("Demonstrate, Don't Cite Rules")

**出现频率：** 约 2% 的审查插件
**相关模式：** [Evidence Chain](#pattern-26), [Adversarial Persona Framing](#pattern-31)

**定义：** 审查者不引用抽象规则（"missing null check"），而必须用具体代码引用展示实际失败路径。

### 正面示例

```markdown
**Demonstrate, don't cite rules.** Instead of "missing null check," show:
`getUser()` returns null on cache miss (CacheManager.ts:89), so `user.email`
at line 45 throws TypeError.

Eight attack patterns:
1. null/empty/boundary  2. stale data  3. error paths  4. sequence breaking
5. resource exhaustion  6. concurrency  7. performance  8. security

Trust boundary analysis:
- Entry points (validation appropriate) vs internal code (should trust callers)
- Over-protective checks are a SMELL correlating with real bugs

Call stack analysis:
- Look UP: Who calls this? Could a caller violate assumptions?
- Look DOWN: What do callees assume? Could this code pass invalid state?
```

**为什么有效：** 带有 file:line 引用的已证明 bug 可立即操作。抽象规则引用（"OWASP A1"）要求开发者自己弄清实际问题。八种攻击模式提供系统化覆盖。

### 反面示例

```markdown
**Review finding:** Missing null check on user input.
This violates OWASP A1 (Injection) and CWE-476 (NULL Pointer Dereference).
Recommendation: Add input validation per secure coding guidelines.
```

**为什么失败：** 审查者引用规则 ID 但从未展示哪个函数、哪一行或哪条输入路径导致失败。开发者必须自己重新发现实际 bug。"Add input validation"在不知道具体入口点和数据流的情况下太模糊而无法操作。

---

## Pattern 48: Rule-Catalog Review (Hierarchical YAML)

**出现频率：** 约 1% 的审查插件
**相关模式：** [Tool Routing Tables](#pattern-21), [Domain Knowledge Embedding](#pattern-24)

**定义：** 由分层 YAML 规则文件目录驱动的审查，每个规则带有评估类型（regex, metric, semantic）和规则 ID。包含从历史 PR 评论分析中生成的"trained rules"。

### 正面示例

```markdown
Rule catalogs:
- base-rules-test-quality.yaml (TEST-*)
- base-rules-security.yaml (SEC-*)
- base-rules-code-quality.yaml (CODE-*)
- base-rules-workflow.yaml (WF-*)
- base-rules-pr-metadata.yaml (PR-*)
- trained-rules.yaml (TRAINED-*) — rules from historical PR comment analysis

Evaluation types per rule:
- `regex` — pattern matching against code
- `metric` — computed thresholds (e.g., method length > 50 lines)
- `semantic` — LLM-guided via `hint` field
```

**为什么有效：** 规则有版本、可审计、可独立更新。Trained rules 捕获通用检查清单遗漏的团队特定约定。三种评估类型将正确技术匹配到每条规则的性质。

### 反面示例

```markdown
Review rules (embedded in prompt):
- Methods should not be too long
- Avoid security vulnerabilities
- Tests should cover edge cases
- Code should follow team conventions
- Use meaningful variable names
```

**为什么失败：** 规则作为散文嵌入 prompt，无版本无审计。"Too long"和"meaningful"是主观的，没有指定评估类型。无法在不重写整个 prompt 的情况下更新单条规则，也没有从历史数据中学习团队特定约定的机制。

---

## Pattern 49: Blast Radius & On-Call Impact Formulas

**出现频率：** <1% 的插件
**相关模式：** [Scoring Rubrics](#pattern-27)

**定义：** 用于评估代码变更运营影响的量化公式，产出映射到风险级别的数值分数。

### 正面示例

```markdown
## Blast Radius
Blast Radius = (Direct Consumers) + (Transitive Consumers x 0.5) + (Cross-Repo Refs x 2)
Risk: 0-5 Low, 6-15 Medium, 16-50 High, 50+ Critical

## On-Call Impact Score
OIS = (Blast Radius x 0.3) + (User Impact x 0.3) + (Data Risk x 0.2) + (Recovery Difficulty x 0.2)
Risk: 0-25 Low, 26-50 Medium, 51-75 High, 76-100 Critical

## Weighted Merge Readiness Score (0-100)
CI passing (20%) + Regression risks (20%) + Breaking changes (15%) +
Review completeness (15%) + Sanity checks (10%) + Work items (5%) +
PR description (5%) + Threads (5%) + Test coverage (5%)

Verdict: 90-100 Ready, 70-89 Caution, 50-69 Needs work, <50 Do not merge
```

**为什么有效：** 数字公式跨审查产出一致的分数。权重编码组织优先级（CI passing 比 PR description 重要）。跨仓库引用获得 2x 权重因为它们影响最多人。

### 反面示例

```markdown
## Risk Assessment
Evaluate the blast radius of this change.
Consider: How many consumers? Is it cross-repo? Could it page on-call?
Rate as: Low / Medium / High / Critical
```

**为什么失败：** 没有公式，一个审查者的"Medium"是另一个的"High"。无法区分 5 个直接消费者和 50 个的变更。主观评级产出无法跨审查比较或随时间跟踪的不一致分数。

---

## Pattern 50: Adversarial Triad with Counterargument Phase

**出现频率：** 约 1% 的插件
**相关模式：** [Adversarial Persona Framing](#pattern-31), [Multi-Agent Orchestration](#pattern-18)

**定义：** 三个持有对立思维的 agent（Advocate/Skeptic/Architect）并行运行，然后第二轮三个反驳 agent 挑战每个原始视角。有争议的点升级到对等协商。

### 正面示例

```markdown
Round 1 (parallel): Advocate, Skeptic, Architect — independent reviews
Round 2 (parallel): 3 counterargument agents read the OTHER two reviews
Round 3: Disputed agents message each other directly (peer consultation)

Conflict resolution:
- If Skeptic shows reproducible path, it's a bug regardless of Advocate's defense
- If Architect says blocking, Architect wins on architectural concerns
- file:line evidence beats "probably"
- Peer consultation resolution = highest confidence
```

**为什么有效：** 两轮防止群体思维 — 反驳挑战初始立场。基于证据的冲突解决是确定性的。对等协商解决规则无法处理的争议。

### 反面示例

```markdown
Three reviewers analyze the PR independently.
Combine findings into a single list.
If reviewers disagree, include both opinions in the output.
```

**为什么失败：** 没有反驳阶段的独立审查产出意见并集而非解决后的判定。"Include both opinions"将冲突推迟给开发者而非解决它。没有基于证据的冲突解决规则，开发者无法判断哪个审查者是正确的。

---

## Pattern 51: Schema Validation Gate

**出现频率：** 约 2% 的审查插件
**相关模式：** [Structured Output Templates](#pattern-14), [Error Handling](#pattern-15)

**定义：** 每个 agent 对其输出 JSON 运行 schema 验证器。验证失败时 agent 必须修复违规并重新运行直到通过。编排器在接受输出前检查验证成功。

### 正面示例

```markdown
Every agent runs `validate_review.py` on its output JSON.
If validation fails: fix violations and re-run until PASSED.
Orchestrator checks for "Schema validation: PASSED" in agent output.
Agents that skip validation are re-launched.
```

**为什么有效：** Schema 验证在格式错误的输出传播前捕获它。重新启动机制防止 agent 静默产出垃圾。

### 反面示例

```markdown
Output your review as JSON with fields: severity, description, file, line.
Make sure the JSON is valid.
```

**为什么失败：** "Make sure the JSON is valid"是指令不是验证机制。没有生成后运行的验证器，没有失败时的重试循环，没有编排器门控。agent 可以产出畸形 JSON（缺字段、类型错误），下游消费者发现错误时已太迟无法恢复。

---

## Pattern 52: LLM-as-Judge Evaluation Scenarios (8 Types)

**出现频率：** <1% 的插件
**相关模式：** [Scoring Rubrics](#pattern-27), [Self-Critique](#pattern-28)

**定义：** 八种不同评估场景的综合工具箱，用于使用 LLM 评判 AI 输出，每种都有特定的输入/输出合约。

### 正面示例

```markdown
1. **Live API Testing**: Call endpoint, judge response (verdict/reasoning/confidence)
2. **Offline Batch**: Evaluate pre-collected pairs against assertions
3. **Meta-Judge (Judge the Judge)**: Validate another LLM's judgment — AGREE/DISAGREE
4. **Pairwise Comparison (A/B)**: Compare two outputs, pick winner with criteria
5. **Multi-Aspect**: Grade 6 dimensions 1-10 (accuracy, helpfulness, safety, tone, relevance, clarity)
6. **Regression Testing**: Compare baseline vs candidate — BETTER/SAME/WORSE with severity
7. **Safety & Compliance**: Screen for PII, harmful content, policy violations, bias
8. **Claim-Based Grounding (Claimbreak)**: Extract factual claims, convert to verifiable
   questions, assess grounding (SUPPORTED/UNSUPPORTED/PARTIAL) with grounding_score
```

**为什么有效：** 八种场景覆盖完整评估空间。每种都有具体合约而非模糊的"evaluate quality"。Meta-judging 支持评审评审者。Claimbreak 通过验证单个声明捕获虚构。

### 反面示例

```markdown
Evaluate the AI's response for quality.
Rate on a scale of 1-10.
Provide reasoning for your score.
```

**为什么失败：** 单一"quality"维度将准确性、安全性、有用性和语调折叠成一个数字。没有场景区分 — 无论评估聊天机器人响应、测试用例批次还是模型版本间的回归都用同一 prompt。没有声明级 grounding，90% 正确但包含一个虚构事实的响应整体得高分。

---

## Pattern 53: Retrospective Quality Rubric (Incident Postmortem)

**出现频率：** <1% 的插件
**相关模式：** [Evidence Chain](#pattern-26), [Scoring Rubrics](#pattern-27)

**定义：** 评估事件复盘质量的综合检查清单，带有捕获模糊或归咎性文字的反模式。

### 正面示例

```markdown
Customer Impact:
- Anti-pattern: "customers experienced slower performance"
- Pattern: "450K read requests (12% of traffic) received 5xx errors for 117 minutes"

Five Whys: structure, depth, branching, detection/prevention analysis

Repair Items must have:
- Actionable scope
- Verifiable completion criterion
- Individual owner + target date
```

**为什么有效：** 反模式/正模式对精确教会模型"量化"对客户影响意味着什么。修复项要求个人负责 — "the team will fix it"被拒绝。

### 反面示例

```markdown
Review the postmortem for completeness:
- Does it describe what happened?
- Does it identify root cause?
- Does it list action items?
- Is the tone blameless?
```

**为什么失败：** 检查清单接受模糊答案为完整。"Customers experienced degraded performance"通过"describe what happened"而不量化影响。"The team will improve monitoring"通过"list action items"而没有负责人、日期或可验证的完成标准。没有反模式示例来校准"完整"实际意味着什么。

---

## Pattern 54: Test Scaffolding with Convention Enforcement

**出现频率：** 约 1% 的插件
**相关模式：** [Domain Knowledge Embedding](#pattern-24), [Phased Execution](#pattern-2)

**定义：** 带有强制约定、反模式表、确定性测试规则和并行生成 fleet mode 的综合测试生成。

### 正面示例

```markdown
Enforced Conventions:
- AAA pattern (Arrange/Act/Assert) in every test
- Naming: {Method}_{Scenario}_{Expected}
- [Description("...")] on every test method
- Folder mirroring (test project mirrors source structure)

Anti-Pattern Table (10 entries):
| Anti-Pattern | Problem | Correct Approach |
| Testing internal state | Brittle to refactoring | Test observable behavior |
| Shared mutable state | Order-dependent tests | Fresh setup per test |

Deterministic Test Rules:
| Non-deterministic Source | Replacement |
| DateTime.Now | Inject IClock |
| Random | Seed-based or inject |
| File I/O | In-memory abstraction |

Edge Case Checklist:
null, empty, single, boundary, duplicate, whitespace, case sensitivity,
concurrent, default/zero, large input

Fleet Mode: Parallel generation with sub-agents, hard stop after 3 consecutive build failures
```

**为什么有效：** 约定执行防止"通过但错误的测试"。反模式表针对特定的反复出现的错误。确定性测试规则在生成时就消除 flaky 测试。Fleet mode 扩展到大型代码库。

### 反面示例

```markdown
Generate unit tests for the changed files.
Ensure good coverage of edge cases.
Use mocking where appropriate.
Follow the existing test style.
```

**为什么失败：** "Good coverage"和"where appropriate"是主观的 — 模型自己决定什么算边缘情况。没有显式边缘情况检查清单，null 输入和边界值经常被遗漏。"Follow the existing test style"要求模型推断可能在代码库中不一致的约定，且没有反模式表来防止测试内部状态或共享可变 fixture 等常见错误。

---

## Pattern 55: Smart Triage-Skip with Model Tracking

**出现频率：** <1% 的插件
**相关模式：** [Deduplication/Consensus](#pattern-22), [Configuration Persistence](#pattern-16)

**定义：** 在分诊 bug 前检查是否已被分诊过，查找元数据签名。如果由同一模型分诊则跳过，如果由不同模型分诊则重新分诊（允许模型升级增加价值）。

### 正面示例

```markdown
Check for existing triage:
- If triaged by same model → skip
- If triaged by different model → re-triage
- This prevents duplicate assessments while allowing model upgrades
```

**为什么有效：** 防止在已分诊 bug 上浪费计算。模型跟踪使更好模型可用时可以渐进改善。

### 反面示例

```markdown
Before triaging, check if the bug already has a triage comment.
If it does, skip it.
```

**为什么失败：** 检查"a triage comment"而不跟踪哪个模型产出它意味着旧的、能力较弱模型的分诊被视为最终结果。模型升级永远没有机会改善分诊质量。跳过也很脆弱 — 任何评论（甚至人类注释）都可能被误认为先前分诊，导致 bug 被永久跳过。
