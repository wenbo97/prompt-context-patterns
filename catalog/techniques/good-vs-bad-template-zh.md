# Prompt 编写对比：好 vs 坏

> 同一任务：验证 .csproj 是否完成了 .NET 多目标框架迁移
> 用于 Claude Code SKILL.md

---

# 坏的示例

```markdown
# Verify Migration

Check if a csproj file has been properly migrated to support multiple target frameworks.

You need to look at the csproj file and make sure it has the right target frameworks.
Check that it has both the old framework and the new one. Also check that the packages
are correct and there aren't any issues. If there are problems, report them. If everything
is fine, say it's good.

Make sure to check:
- The target framework is correct
- Packages are properly conditioned
- No duplicate references
- Build should work
- The file isn't broken

Output the results in a structured way. Include the status and any issues found.
If there are warnings, include those too. Make it clear and easy to understand.

Don't modify any files. This is a read-only check. Be thorough but don't
take too long. If you're not sure about something, flag it as a warning
rather than an error.

Example: if you check a project and it has net472 and net8.0, that's good.
If it only has net472, that's bad because the migration hasn't happened.
```

---

## 坏的示例：逐行分析

```
"Check if a csproj file has been properly migrated"
  → "properly"是主观词——模型不知道你对"properly"的标准是什么
  → 每次执行模型会自行定义"properly"，导致行为不一致

"make sure it has the right target frameworks"
  → "right"是什么？net8.0？net9.0？net10.0？未指定
  → 模型会猜测，或每次猜测不同

"Also check that the packages are correct and there aren't any issues"
  → "correct"未定义
  → "issues"未定义
  → 这句话的信息量实际为零

"Output the results in a structured way"
  → "structured way"可以是JSON、YAML、Markdown表格、纯文本列表……
  → 十次执行可能产生五种不同格式

"Be thorough but don't take too long"
  → 自相矛盾的指令——模型无法同时优化两个冲突目标
  → 每次会在"thorough"和"quick"之间随机取不同平衡

"Example: if you check a project and it has net472 and net8.0, that's good"
  → 示例只给了结论（"that's good"），没给输出格式
  → 模型知道什么是正确的，但不知道如何报告

总体问题：
  → 无输入/输出契约——调用者不知道会收到什么
  → 无枚举值——"status"可以是"good"/"bad"/"ok"/"pass"/"fail"/任何词
  → 指令和约束混在一起——模型的注意力在段落间均匀稀释
  → 无具体检查项——"packages are correct"不是可执行的检查
  → 示例太模糊——没有展示预期的输出 token 序列
```

---
---

# 好的示例

```markdown

# Verify Migration

<!-- version: 1.4.0 -->
<!-- depends_on: upgrade-package-ref@1.x -->
<!-- last_tested: 2026-03-25 -->

## Purpose
Verify whether a single .csproj file has completed multi-target framework migration. Read-only check — does not modify any files.

<input_contract>
- `projectPath`: string — absolute or relative path to the .csproj file
- `netCoreTargets`: string — expected new TFM(s) (e.g., "net8.0" or "net8.0;net10.0")
- `previousTFM`: string — original TFM before migration (e.g., "net472" or "netstandard2.0")
</input_contract>

<output_contract>
| Field        | Type   | Values                                        |
|--------------|--------|-----------------------------------------------|
| `status`     | string | `"PASS"`, `"FAIL"`, `"WARN"`                  |
| `checks`     | array  | Result of each check (see check schema below) |
| `summary`    | string | One-sentence conclusion                       |

Check schema:
| Field      | Type   | Values                                         |
|------------|--------|------------------------------------------------|
| `check`    | string | Check item name (see the check list in Step 2) |
| `result`   | string | `"PASS"`, `"FAIL"`, `"WARN"`, `"SKIP"`         |
| `expected` | string | Expected value                                 |
| `found`    | string | Actual value                                   |
| `detail`   | string | Empty string for PASS; explanation for FAIL/WARN/SKIP |
</output_contract>

<constraints>
1. Do not modify any files — this is a read-only skill
2. Do not run dotnet build — static analysis only
3. If the file at projectPath does not exist, return status: "FAIL" immediately without running any checks
4. Each check is independent — one FAIL does not affect execution of other checks
5. Final status determination rule: any check FAIL → "FAIL"; no FAIL but has WARN → "WARN"; all PASS or SKIP → "PASS"
</constraints>

```

<steps>

## Step 1: 读取并解析 .csproj

```bash
cat "$projectPath"
```

如果文件不存在 → 返回 `{ status: "FAIL", checks: [], summary: "File not found: $projectPath" }`

从文件内容中提取以下元素：
- `<TargetFramework>` 或 `<TargetFrameworks>` 的值
- 所有 `<PackageReference>` 元素及其 Condition 属性
- 所有 `<ProjectReference>` 路径

如果某元素缺失，按具体检查项的定义处理（如缺少 `<TargetFramework>` 对于 Check 2 是 PASS，不是 SKIP）。

## Step 2: 执行检查项

按顺序执行以下检查。每个检查独立——一个失败不跳过后续检查。

### Check 1: TargetFrameworks 包含新旧 TFM

- expected: `<TargetFrameworks>` 同时包含 `{previousTFM}` 和 `{netCoreTargets}` 中的每个 TFM
- PASS: `<TargetFrameworks>net472;net8.0</TargetFrameworks>` 当 previousTFM=net472, netCoreTargets=net8.0
- FAIL: 仍是 `<TargetFramework>net472</TargetFramework>`（单数形式，未迁移）
- FAIL: `<TargetFrameworks>` 存在但缺少 previousTFM 或 netCoreTargets

### Check 2: 不存在单数 TargetFramework

- expected: 文件中没有 `<TargetFramework>` 标签（应已替换为复数形式）
- PASS: 无 `<TargetFramework>` 标签
- FAIL: `<TargetFramework>` 仍然存在

### Check 3: PackageReference 条件化

- expected: 平台特定的 PackageReference 有 Condition 属性
- WARN: 已知的 .NET Framework 专用包（如 System.Runtime.Caching）无 Condition
- PASS: 所有平台特定包已条件化，或不存在平台特定包
- 已知 .NET Framework 专用包列表: System.Runtime.Caching, System.ServiceModel.*, Microsoft.AspNet.*

### Check 4: 无重复 PackageReference

- expected: 同一包名不出现两次（忽略 Condition 差异）
- PASS: 无重复
- WARN: 同一包在不同 Condition 下出现（合法但需人工审查）
- FAIL: 同一包在相同 Condition 下出现两次

### Check 5: ProjectReference 路径有效

- expected: 每个 `<ProjectReference Include="...">` 路径指向存在的文件
- PASS: 所有引用路径存在
- WARN: 路径不存在（可能是相对路径解析问题）

## Step 3: 组装输出

按 output_contract 格式组装结果。状态判定规则按 constraints 第5条。

</steps>

<examples>

### 示例 1: 正常通过

<example>

<input>
projectPath: src/Services/Auth/Auth.csproj
netCoreTargets: net8.0
previousTFM: net472
</input>

<expected_output>
{
  "status": "PASS",
  "checks": [
    { "check": "TargetFrameworks contains old+new TFM", "result": "PASS", "expected": "net472;net8.0", "found": "net472;net8.0", "detail": "" },
    { "check": "No singular TargetFramework", "result": "PASS", "expected": "absent", "found": "absent", "detail": "" },
    { "check": "PackageReference conditioned", "result": "PASS", "expected": "all conditioned", "found": "all conditioned", "detail": "" },
    { "check": "No duplicate PackageReference", "result": "PASS", "expected": "no duplicates", "found": "0 duplicates", "detail": "" },
    { "check": "ProjectReference paths valid", "result": "PASS", "expected": "all exist", "found": "3/3 exist", "detail": "" }
  ],
  "summary": "All 5 checks passed. Migration verified."
}
</expected_output>
</example>

### 示例 2: 未迁移 + 问题包

<example>
<input>
projectPath: src/Legacy/Reporting.csproj
netCoreTargets: net8.0;net10.0
previousTFM: net472
</input>

<expected_output>
{
  "status": "FAIL",
  "checks": [
    { "check": "TargetFrameworks contains old+new TFM", "result": "FAIL", "expected": "net472;net8.0;net10.0", "found": "net472", "detail": "Still using singular <TargetFramework>. Migration not applied." },
    { "check": "No singular TargetFramework", "result": "FAIL", "expected": "absent", "found": "<TargetFramework>net472</TargetFramework>", "detail": "Singular form still present." },
    { "check": "PackageReference conditioned", "result": "WARN", "expected": "all conditioned", "found": "System.Runtime.Caching unconditioned", "detail": "Known .NET Framework-only package without Condition attribute." },
    { "check": "No duplicate PackageReference", "result": "PASS", "expected": "no duplicates", "found": "0 duplicates", "detail": "" },
    { "check": "ProjectReference paths valid", "result": "PASS", "expected": "all exist", "found": "5/5 exist", "detail": "" }
  ],
  "summary": "2 checks FAILED, 1 WARNING. Migration not complete."
}
</expected_output>
</example>

</examples>
```

---

## 好的示例为什么有效：逐点分析

```
1. Input Contract 精确到类型和含义
   坏:  "look at the csproj file" — 哪个文件？怎么传入？
   好:  projectPath: string — absolute or relative path to the .csproj file
   效果: 模型无需猜测输入来源——直接使用 $projectPath

2. Output Contract 锁定字段名和枚举值
   坏:  "output the results in a structured way"
   好:  status 只能是 "PASS" | "FAIL" | "WARN"，每个 check 有固定 schema
   效果: 十次执行，十次相同的输出格式。下游 agent 可以可靠解析

3. 约束放在步骤之前（高注意力位置）
   坏:  "Don't modify any files" 埋在段落中间
   好:  constraints 第1条，独立编号，用 XML 标签隔离
   效果: 模型在开始执行步骤前已"看到"约束

4. 每个检查项定义了具体的 PASS/FAIL/WARN 条件
   坏:  "make sure the target framework is correct"
   好:  "FAIL: Still <TargetFramework>net472</TargetFramework> (singular form, not migrated)"
   效果: 不是让模型判断什么是"correct"，而是提供枚举判定条件

5. 示例展示完整的输出 token 序列
   坏:  "if it has net472 and net8.0, that's good"
   好:  完整 JSON 输出包含每个字段的具体值
   效果: 模型直接模仿此 JSON 结构而非自己发明

6. 示例覆盖快乐路径和失败路径
   坏:  只有一个模糊的正面示例
   好:  示例1全部通过，示例2有混合 FAIL + WARN
   效果: 模型看到两种模式，知道失败时输出是什么样

7. 措辞消除歧义
   坏:  "Be thorough but don't take too long"（矛盾）
   好:  "Do not run dotnet build — static analysis only"（清晰边界）
   效果: 模型无需在矛盾指令间权衡

8. 错误处理不是分离的——它嵌入在对应步骤中
   坏:  完全没有提到错误情况
   好:  Step 1 以文件不存在时的返回值开始
   效果: 当模型执行到该步骤时，失败处理在其注意力范围内

9. 状态聚合规则是明确且确定性的
   坏:  "If there are problems, report them"（什么算 problem？）
   好:  "Any check FAIL → FAIL; no FAIL but has WARN → WARN; all PASS → PASS"
   效果: 这是确定性逻辑规则——模型以极高概率遵循

10. 版本和依赖信息（给人类，不是给模型）
    坏:  无法追踪运行的是哪个版本的 prompt
    好:  version: 1.4.0, depends_on, last_tested
    效果: 出问题时可以快速定位是哪次修改导致的
```

---

## 核心差异摘要

| 维度 | 坏 | 好 |
|------|-----|-----|
| 输出空间 | 无限（模型自由即兴发挥） | 高度收窄（枚举值 + schema） |
| 注意力利用 | 均匀稀释（纯文本段落） | 精确引导（XML 分区 + 位置策略） |
| 训练先验利用 | 无（通用英文描述） | 有（XML 标签激活结构化模式） |
| 可复现性 | 低（每次格式不同） | 高（output contract 锁定） |
| 可测试性 | 不可能（无预期输出定义） | 可能（示例即测试用例） |
| 调试效率 | 低（无法判断哪步出错） | 高（每个 check 独立，可精确定位） |
