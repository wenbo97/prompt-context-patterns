# Skill 中的稳定分支：建议

**核心原则:** 如果分支可以由代码决定，就不要交给 LLM。分支越依赖自然语言条件，漂移概率越高。

从最稳定到最不稳定排序——这些技术可以组合使用。

## 1. 将决策推入 hook 或 bash 预处理（最稳定）

如果"问题 XX"和"白名单命中"都可通过编程检测，在 skill 运行之前解决分支：

- `UserPromptSubmit` hook 检测问题 XX → 检查白名单 → 将结果注入上下文（如 `<branch>condition_1</branch>`）。Skill 正文只执行；不决策。
- 或在 `SKILL.md` 顶部用 bash 预处理：

  ```bash
  if grep -qF "$TARGET" "${CLAUDE_PLUGIN_ROOT}/whitelist.txt"; then
    export BRANCH=1
  else
    export BRANCH=2
  fi
  ```

  Prompt 然后无歧义地按 `$BRANCH` 分发。

这一层能解决的都不应留给 prompt 层。

## 2. 通过外化 CoT 强制"先决策，后执行"

如果 LLM 确实必须判断，不要让它在同一呼吸中推理和行动。要求它**先将判断物化为结构化输出**，然后执行：

```xml
<assessment>
  <problem_detected>yes|no</problem_detected>
  <whitelist_hit>yes|no|n/a</whitelist_hit>
  <chosen_branch>1|2|none</chosen_branch>
  <rationale>one-line justification</rationale>
</assessment>
```

后续动作变成"执行 `assessment` 的结论"而非"同时思考和行动"。这比单独 few-shot 更能提升分支稳定性——可在快速评估中测量。

## 3. 使用决策表而非自然语言 if-else

避免散文如"if…, otherwise…"。编写前置条件为布尔表达式（而非句子）的显式 XML 分支：

```xml
<branch when="problem_xx AND whitelist_hit">…</branch>
<branch when="problem_xx AND NOT whitelist_hit">…</branch>
<branch when="NOT problem_xx">no-op, exit</branch>
```

## 4. Few-shot 必须覆盖所有分支加负面示例

至少三个：白名单命中、白名单未命中，以及**一个完全不触发问题 XX 的负面示例**。负面示例最容易遗忘，对防止过度触发最重要。再加一两个边界情况（空白名单、模糊问题信号）。

## 5. 分支动作差异大时拆分为独立 skill

如果 `condition_1` 和 `condition_2` 在工具调用面或输出格式上差异较大，将它们放在一个 skill 中意味着 few-shot 示例互相争夺信号。在更高层级路由——通过 command 或 hook——让每个 skill 服务单一分支。整体稳定性通常更好。

## 推荐的推出顺序

1. 用 hook 解决能解决的（#1）。
2. 对其余部分，组合外化 CoT（#2）和决策表（#3）作为骨干。
3. 用 few-shot 覆盖边界（#4）。
4. 仅在前四个仍无法稳定分支时拆分 skill（#5）。

**量化验证:** 使用 `skill-creator` 的评估框架，每个分支运行 5-10 个用例，查看命中率。比直觉更可靠。

---

## 附录：决策树 A/B 测试示例

### 场景

一个部署助手必须根据服务器配置和部署请求决定做什么。逻辑有 5 个分支。

### 散文版本（不稳定）

```
Rules:
- If the server is in maintenance mode and the deployment is not marked as urgent, skip.
- If the server is in maintenance mode but the deployment is urgent, proceed with warning.
- If the server is healthy and the target matches, deploy normally.
- If the server is healthy but the target doesn't match, reject.
- If the server status is unknown, check health first.
```

### 决策树版本（稳定）

```
## Server status?
├─ "maintenance"
│   └─ Deployment urgent?
│       ├─ YES → action: "deploy", add warning: "server in maintenance"
│       └─ NO  → action: "skip", reason: "server in maintenance, non-urgent"
├─ "healthy"
│   └─ target_env matches server environment?
│       ├─ YES → action: "deploy", reason: "normal deployment"
│       └─ NO  → action: "reject", reason: "environment mismatch"
└─ other/unknown
    └─ action: "check_health", reason: "server status unknown"
```

### 结果（各 5 次运行，歧义输入：status="degraded"）

- **散文:** 正确决策 5/5，但 action 名称、reason 文本和 warnings 数组在不同运行间变化。一次运行在 JSON 外添加了额外评论。
- **树:** 正确决策 5/5，5 次运行输出完全相同。Action 和 reason 精确匹配树的叶节点。

完整测试: [prompt-context-patterns/eval/decision-tree-ab](https://github.com/wenbo97/prompt-context-patterns/tree/master/eval/decision-tree-ab)
