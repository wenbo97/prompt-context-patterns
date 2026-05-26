# Skill 架构模式——来自开源仓库的经验

Skill 如何**组织、打包和组合**的结构模式——提取自 Anthropic 官方 `skills` 仓库和 ComposioHQ 的 `awesome-claude-skills`。

**数据来源:**
- Anthropic 官方 skill：17 个官方 skill，`marketplace.json`，`template/SKILL.md`
- 社区精选 skill：32 个独立 + 832 个 Composio skill，`CONTRIBUTING.md`
- **提取日期:** 2026-04-15

---

## 1. 规范的 Skill 结构

两个仓库趋同于此最小结构：

```
skill-name/
├── SKILL.md          # 必需：YAML frontmatter + 指令
├── LICENSE.txt        # 可选：每 skill 许可证
├── scripts/           # 可选：辅助脚本（Python、Bash、JS）
├── reference/         # 可选：领域知识文件
├── templates/         # 可选：输出模板
├── examples/          # 可选：示例输入/输出
├── agents/            # 可选：子 agent 定义
├── assets/            # 可选：字体、图片、schema
└── themes/            # 可选：预构建配置
```

### SKILL.md 结构

```yaml
---
name: lowercase-hyphenated-name
description: One line explaining WHEN to activate and WHAT it does
license: "Complete terms in LICENSE.txt" | "Proprietary" | omitted
---

# Skill Title (optional — some skills skip this)

[Body: instructions, workflows, constraints, examples]
```

### 关键设计决策

| 决策 | Anthropic 官方 | 社区 |
|------|---------------|------|
| `name` 格式 | `lowercase-hyphenated` | `lowercase-hyphenated`（CONTRIBUTING.md 强制） |
| `description` 用途 | Claude 的触发条件 | 触发条件（同一意图） |
| `license` 字段 | 15/17 个 skill 包含 | 约10% 包含 |
| 正文大小 | 30-590 行 | 30-500 行 |
| 部分 | 按复杂度变化 | 推荐 5 部分模板 |

---

## 2. Description 编写——触发机制

`description` 字段是任何 skill 中**最重要的一行**。它决定 Claude 何时激活 skill。分析 50+ 个 description 发现不同模式：

### Pattern A: 动作 + 领域 + 触发关键词

```yaml
description: >-
  Guide for creating high-quality MCP servers that enable LLMs to
  interact with external services. Use when building MCP servers to
  integrate external APIs.
```

结构：`{做什么}. {何时使用}.`

### Pattern B: 能力列表

```yaml
description: >-
  Toolkit for interacting with and testing local web applications
  using Playwright. Supports verifying frontend functionality,
  debugging UI behavior, capturing browser screenshots, and viewing
  browser logs.
```

结构：`{主要能力}. Supports {能力}, {能力}, {能力}.`

### Pattern C: 负面边界

```yaml
description: >-
  Suite of tools for creating elaborate HTML artifacts using React,
  Tailwind CSS, shadcn/ui. Use for complex artifacts requiring state
  management — not for simple single-file HTML artifacts.
```

结构：`{做什么}. Use for {范围} — not for {反范围}.`

### Pattern D: 情感钩子（社区）

```yaml
description: >-
  Automatically creates user-facing changelogs from git commits.
  Turns hours of manual changelog writing into minutes of automated
  generation.
```

结构：`{做什么}. {价值主张——节省时间}.`

### 最佳实践

组合 A + C：陈述动作、领域、触发条件和负面边界。

```yaml
description: >-
  Migrate .NET Framework projects to .NET Core multi-targeting.
  Use when the user says "start migration" or provides a .csproj path.
  NOT for greenfield .NET projects or projects already on .NET Core.
```

---

## 3. 社区五部分模板

来自 `awesome-claude-skills/CONTRIBUTING.md`——任何 skill 的推荐部分：

```markdown
# {Skill Name}

## When to Use
- [触发条件——子弹列表]
- Keywords: [逗号分隔触发词]

## What This Skill Does
- [能力——子弹列表]
- [限制——明确边界]

## How to Use
### Basic Usage
[最简调用]

### Advanced Usage
[带选项/标志]

## Example
[完整、真实的输入 → 输出]

## Tips
- [高级用户建议]
- [常见陷阱]
- [相关工作流]
```

### 分析：哪些部分最重要？

| 部分 | 对质量的影响 | 使用率 |
|------|------------|--------|
| **How to Use**（步骤） | 关键——提供执行路径 | 约90% 的 skill |
| **Example**（已填充） | 高——锚定输出格式 | 约65% 的 skill |
| **When to Use**（范围） | 中——防止误激活 | 约40% 的 skill |
| **Tips**（陷阱） | 中——防止常见错误 | 约50% 的 skill |
| **What This Skill Does** | 低——与 description 冗余 | 约30% 的 skill |

---

## 4. Marketplace 打包

Anthropic 的 `marketplace.json` 将 17 个 skill 分为 3 个可安装包：

```json
{
  "plugins": [
    {
      "name": "document-skills",
      "skills": ["xlsx", "docx", "pptx", "pdf"]
    },
    {
      "name": "example-skills",
      "skills": ["algorithmic-art", "brand-guidelines", "canvas-design", ...]
    },
    {
      "name": "claude-api",
      "skills": ["claude-api"]
    }
  ]
}
```

### 分组策略

| 策略 | 何时使用 | 示例 |
|------|---------|------|
| **按领域** | Skill 共享资源（schema、helper） | document-skills: xlsx + docx + pptx + pdf |
| **按受众** | Skill 面向相同用户类型 | example-skills: creative + testing + building |
| **独立** | Skill 自包含且专门化 | claude-api |

### 包内资源共享

document-skills 包共享：
- 39 个 XSD schema（OOXML 验证）
- Python 辅助脚本（文件操作）
- Office 辅助工具（样式管理、XML 编辑）

比 4 个独立 skill 减少了总包大小。

---

## 5. 脚本集成模式

### Pattern A: 自文档化脚本 (--help)

```markdown
Always run `python scripts/with_server.py --help` before first use.
Use the script as a black box — do not modify it.
```

使用者: webapp-testing, skill-creator

### Pattern B: Init + Build 管线

```markdown
1. Run `bash scripts/init-artifact.sh` (creates project structure)
2. [User develops in the created structure]
3. Run `bash scripts/bundle-artifact.sh` (produces single output file)
```

使用者: web-artifacts-builder, artifacts-builder

### Pattern C: 验证脚本

```markdown
Before packaging, run validation:
`python scripts/package_skill.py --validate`
Checks: frontmatter present, description non-empty, no broken references
```

使用者: skill-creator

### Pattern D: 数据处理脚本

```markdown
Use bundled scripts for file processing:
- `scripts/read_pdf.py` — extract text from PDF
- `scripts/create_pdf.py` — generate PDF with reportlab
- `scripts/merge_pdfs.py` — combine multiple PDFs
```

使用者: pdf, docx, pptx, xlsx

---

## 6. 引用文件组织

### 扁平引用（简单 skill）

```
mcp-builder/
├── SKILL.md
└── reference/
    ├── mcp_best_practices.md
    ├── node_mcp_server.md
    ├── python_mcp_server.md
    └── evaluation.md
```

### 层级引用（复杂 skill）

```
claude-api/
├── SKILL.md
├── shared/           # 跨语言
│   ├── models.md
│   ├── prompt-caching.md
│   └── tool-use-concepts.md
├── python/
│   └── claude-api/
│       ├── README.md
│       ├── streaming.md
│       └── tool-use.md
├── typescript/
│   └── claude-api/
│       ├── README.md
│       └── ...
└── [5 more languages]
```

### Theme/Variant 引用

```
theme-factory/
├── SKILL.md
└── themes/
    ├── arctic-frost.md
    ├── ocean-depths.md
    ├── sunset-boulevard.md
    └── [7 more themes]
```

### 关键洞察：引用文件作为渐进式披露第三层

所有引用文件遵循 Progressive Disclosure 模式（Pattern 100）：
- SKILL.md 告诉模型读取哪个文件
- 模型仅在进入相关阶段/工作流时读取
- 如果工作流不需要该文件，则永不加载

---

## 7. 子 Agent 架构

49 个非 Composio skill 中只有 2 个使用子 agent，均来自 Anthropic：

### skill-creator: 3 个子 Agent

| Agent | 角色 | 何时生成 | 记忆 |
|-------|------|---------|------|
| `grader` | 评估测试结果 | 每次 eval 运行后 | 隔离（无 skill 上下文） |
| `comparator` | 盲 A/B 对比 | 两个版本运行后 | 隔离（不知道版本标签） |
| `analyzer` | 提取改进 | 对比后 | 有两个转录本 + 结果 |

### doc-coauthoring: 1 个子 Agent

| Agent | 角色 | 何时生成 | 记忆 |
|-------|------|---------|------|
| naive-reader | 新鲜视角审查 | 文档草稿后 | 隔离（只有文档） |

### 关键架构规则

**子 agent 获得更少的上下文，而非更多。** 其价值来自它们不知道的：
- Grader 不知道 skill 意图 → 纯粹评判输出
- Comparator 不知道版本标签 → 消除偏差
- Naive-reader 不知道写作过程 → 发现真实困惑

---

## 8. Composio 的通用模板

832 个 skill 使用几乎相同的模板，只有 3 个变量：

| 变量 | 示例值 |
|------|--------|
| `{service_name}` | "slackbot", "atlassian", "googledrive" |
| `{toolkit_name}` | "SLACKBOT", "ATLASSIAN", "GOOGLEDRIVE" |
| `{specific_tools}` | 各异——部分 skill 列出工具，大多不列 |

### 模板质量分层

| 层 | 数量 | 特征 |
|----|------|------|
| **通用** | 约780 | 3步（Search → Connect → Execute），不列具体工具 |
| **丰富** | 约50 | 列出具体工具名、参数表、常见模式 |
| **定制** | 约2 | 超出模板的完全自定义内容 |

### 教训：模板实现规模，不实现质量

Composio 通过模板化达到 832 个 skill。但通用 skill 质量低——不提供领域特定指导。列出具体工具和陷阱的丰富变体（如 `googledocs-automation`）明显更有用。

**对我们的插件:** 模板对生成样板（PR 描述、分支名）有用，但高价值内容（错误处理规则、修复策略）必须按领域手工制作。

---

## 9. 跨仓库对比摘要

| 维度 | Anthropic 官方 | 社区 | 我们的插件（迁移插件） |
|------|---------------|------|----------------------|
| **Skill 数量** | 17 | 32 独立 + 832 模板 | 21 skill + 3 agent + 4 command |
| **平均 SKILL.md 大小** | 约200 行 | 约120 行 | 约150 行 |
| **渐进式披露** | 明确3层 | 罕见 | 明确（`<always-loaded>` / `<on-demand>`） |
| **子 agent** | 2 个 skill 使用 | 0 个 skill | 3 个 agent（build-repair、ado、dependency） |
| **脚本捆绑** | 5 个 skill（Python、Bash） | 0 个 skill | 2 个 skill（Python） |
| **评估框架** | 内置（skill-creator） | 无 | dev-prompt-review（自定义） |
| **安全边界** | Provider guards、anti-slop | 最小 | 广泛（7 护栏、4 层级、99 模式） |
| **领域知识** | SDK 文档、字体目录 | 算法内部、SaaS API | 错误处理规则、包映射、项目映射 |
| **输出验证** | 可视 QA 子 agent | 无 | 构建循环（7 次尝试） |

### 可以从各方学到什么

**从 Anthropic 官方:**
- 渐进式披露值得形式化（我们已在做）
- Anti-Slop 命名对创意/生成输出很有效
- 盲 A/B 对比用于 skill 质量评估
- 可视 QA 用于生成制品

**从社区:**
- Clarifying Questions 被普遍采用——应确保 Phase 0 做到这一点
- 已填充的示例比抽象 schema 更有效
- 五部分模板是任何新 skill 的良好最低标准
- Description 中的情感钩子提高用户参与度

**从 Composio:**
- 通用模板实现规模但不实现质量
- Search → Connect → Execute 模式是任何动态 API 的强大抽象
- Known Pitfalls 部分防止用户间的重复失败
