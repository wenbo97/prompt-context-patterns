# 项目整理问题记录

记录日期：2026-10-03。原始问题清单来自第一轮只读探索；现已进入实施，下面保留当时的基线事实。

实施位置：`D:/Projects/prompt-context-patterns-refresh`，分支 `rebuild/skills-catalog`。双语正文、生命周期兼容页、搜索状态、案例编号映射和历史文章修订已实现。十库源码分析与最终整合仍在进行；完成状态和验证证据以 [实施记录](audit/implementation-ledger.md) 为准。

本文记录最初的问题、已验证的事实和建议执行顺序。实施采用已确认的 [重构规格](specs/2026-10-03-blog-rebuild.md)。下面各问题的“待处理”描述为探索时的状态，最终处置将在交付审核中统一核对。

## 项目现状

| 部分 | 当前状态 |
| --- | --- |
| 双语知识库 `catalog/` | 共 206 个编号模式；前 155 个有详细正文，新增 51 个主要是名称与问题摘要 |
| Jekyll 网站 | 博客、静态目录和搜索浏览器，通过 GitHub Actions 发布 |
| 评测工具 `eval/` | Patternfoo 有 10 套标为 ready 的案例；旧 decision-tree-ab 已注明由 Patternfoo 接替 |

## 待整理问题

### 模式编号在目录与评测中含义冲突

优先级建议：P0。状态：待处理。

| 编号 | 知识库模式 | Patternfoo 评测案例 |
| --- | --- | --- |
| 8 | Confirmation Gates | Decision Tree vs Prose |
| 17 | Cross-Platform Handling | Schema Lock JSON output contract |

证据：[目录索引](../catalog/catalog-index.md)、[评测目录代码](../eval/patternfoo/src/catalog.ts)、[案例 008 元数据](../eval/patternfoo/patterns/008-decision-tree/meta.yaml)、[案例 017 元数据](../eval/patternfoo/patterns/017-schema-lock/meta.yaml)。

影响：直接通过编号关联目录与评测，会把测试结果对应到不同的模式。

建议：明确目录模式与评测案例各自的身份，建立显式映射。确认案例实际测试的概念后再处理冲突，避免仅修改显示名称或盲目重编号。

### 模式元数据的维护入口分散

优先级建议：P1。状态：待处理。

目前 1–155 的元数据来自中英文索引和中文名称表，156–206 来自 harvest JSON；生成结果分别写入 `_data/patterns.json` 和 `assets/patterns.json`。修改 harvest 标题时，还需先构建网站、提取实际锚点、重新生成 JSON，再构建一次。

证据：[生成脚本](../eval/tools/build-patterns.mjs)、[锚点提取脚本](../eval/tools/wire-harvest-detail.mjs)、[当前维护说明](../CLAUDE.md)。

来源字段也需校准：生成脚本按编号区间推断旧模式来源，将 121–155 全部标为 `claude-code`；例如 #145 的正文明确引用 superpowers，生成数据却显示为 `claude-code`。

建议：确定一个权威的结构化元数据源，保存稳定编号、双语名称、分类、来源和详情链接；派生文件通过统一命令生成。评估使用稳定锚点，减少标题变化带来的维护步骤。

### 文档与当前实现不同步

优先级建议：P1。状态：待处理。

- Catalog 中英文 README 仍介绍 155 个模式，网站已收录 206 个。
- 根 README 和 CLAUDE.md 的评测说明主要指向旧脚本，未清楚说明 Patternfoo 是后续工具。
- 浏览器设计文档仍标为 DRAFT，描述的是 YAML 数据源、Liquid 生成 JSON 和 CDN Fuse.js；实际实现使用预生成 JSON 和仓库内的 Fuse.js 文件。

证据：[根 README](../README.md)、[Catalog README](../catalog/README.md)、[Catalog 中文 README](../catalog/README-zh.md)、[旧评测说明](../eval/decision-tree-ab/README.md)、[浏览器设计文档](specs/2026-07-08-catalog-browser-design.md)。

建议：统一当前功能、维护入口、历史实验和待补内容的说明；注明设计文档的实施状态与实际方案差异。历史文章中的 155 个模式属于发布时的事实，应保留其历史语境。

### Patternfoo 目录仍固定为 155 个模式

优先级建议：P1。状态：待处理，依赖编号映射和元数据方案。

Patternfoo 使用固定长度 155 初始化目录，仅 10 个编号填写实际名称，其他条目使用 `Pattern N`。对应测试也固定断言 155。当前 10 套案例均包含元数据、A/B 提示词、场景和评分标准，但新收录的 156–206 不会出现在目录中。

证据：[目录实现](../eval/patternfoo/src/catalog.ts)、[目录测试](../eval/patternfoo/tests/catalog.test.ts)、[案例目录](../eval/patternfoo/patterns/)。

建议：从权威目录数据读取模式信息；将“被知识库收录”和“已有可运行评测案例”分别表示，避免目录总数与可运行案例数混淆。

### 发布流程缺少自动质量检查

优先级建议：P1。状态：待处理。

当前 GitHub Actions 工作流在 master 推送或手动触发时构建并发布 Jekyll，没有 PR 检查，也没有运行语言链接扫描、生成数据一致性检查或 Patternfoo 测试。

证据：[发布工作流](../.github/workflows/jekyll.yml)、[语言链接扫描](../eval/tools/scan-lang-links.mjs)、[Patternfoo 脚本](../eval/patternfoo/package.json)。

建议：整理统一检查命令，并接入 PR CI。检查覆盖 ID 唯一性、双语映射、生成数据一致性、构建后的详情锚点和 Patternfoo 单元测试。真实模型评测另行运行，避免常规检查依赖付费模型接口。

### 内容完整度与分类口径需要后续梳理

优先级建议：P2。状态：待规划。

新增 51 个模式目前有双语名称与问题摘要，完整正文仍在待补状态。分类同时包含功能、来源和平台等维度；Karpathy 文档使用 K1–K4 编号，未纳入 206 个数字编号模式的数据集，需要明确两者的关系。

证据：[新增模式静态页](../catalog/patterns-156-206.md)、[分类入口](../catalog/index.md)、[Karpathy 文档](../catalog/categories/patterns-karpathy-behavioral.md)。

建议：先明确分类与标签的职责、K1–K4 的收录口径，再安排新增模式正文的双语补齐顺序。该项不要求首轮完成全部内容。

## 建议执行顺序

1. 校准 README、维护说明和设计文档状态，明确当前项目结构。
2. 统一模式元数据，解决编号语义冲突，建立评测案例映射。
3. 将目录维护工具从 `eval/tools/` 整理到专门的脚本目录，提供统一生成与检查命令，接入 PR CI。
4. 梳理分类、Karpathy 模式归属和新增 51 个模式的正文优先级。

首轮建议覆盖第 1、2 步。整理时保留现有文章 URL 和目录模式编号；若详情锚点需要调整，应保留旧链接的兼容性。

## 已验证的基线和验证范围

- 模式总数为 206，ID 连续且无重复，范围为 1–206。
- `_data/patterns.json` 与 `assets/patterns.json` 解析后的内容一致。
- 按当前生成规则在内存中重建的数据与提交数据一致，未改写生成文件。
- 中英文旧索引各含 155 条记录，中文名称表覆盖 155 个编号。
- 已检查的博客、分类、技巧和标准文档都有对应的中英文文件。
- 运行 `node eval/tools/scan-lang-links.mjs`，报告 0 个跨语言链接错配；这不等于全部页面和详情锚点均已验证。
- 10 套评测案例的五类必需文件均存在，未运行真实模型评测。
- 探索时本机没有 Ruby/Bundler，Patternfoo 的 node_modules 也未安装，因此未验证 Jekyll 构建和 Vitest 测试。
- 记录前 Git 工作区干净。

## 新增的内容重构需求

用户要求先收集全球范围内的 Top 10 开源 prompt skills 仓库，随后以真实来源重构当前 prompt 和 context engineering 的 description、examples 与 good/bad samples。

当前阶段：来源收集与一手文件核对。研究结果记录在 [开源 Skills Top 10 来源研究](research/open-source-skills-top10.md)，仓库搜索、stars 快照和版本信息记录在 [来源快照](research/open-source-skills-top10.snapshot.json)。榜单采用全球范围 GitHub 检索，并按已发现且符合 skills 内容条件的仓库 stars 排序，不将其视为全平台官方排名或质量排名。

后续内容重构应与上述整理问题合并安排：先确定权威模式编号和元数据，再把每个改写示例关联到具体仓库、文件、版本和适用条件；原作者已有的反例与本项目自行设计的 bad sample 应明确区分。双语描述与例子保持同一概念、任务和评价标准，来源仓库的热度不能代替效果验证。

当前没有开始修改 Catalog 正文或示例。完成来源收集后，再统一确定重构范围、首批模式和实施顺序。
