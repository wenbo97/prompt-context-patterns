# 高热度开源 Agent Skills 仓库 Top 10：素材来源调查

本轮收集用于后续重写本项目的 prompt / context engineering **description、examples 和 good / bad samples**。已确定 10 个仓库并核对实际技能正文；本轮产出是来源清单与采集建议，尚未改写 catalog 内容。

统计快照：**2026-10-03 12:00（Asia/Shanghai）**，原始时间为 `2026-10-03T04:00:12.267841+00:00`。仓库数据来自 GitHub REST API；候选、检索条件、排除记录、固定 commit 和文件路径保存在 [元数据快照](open-source-skills-top10.snapshot.json)。

## 排名口径

- 范围为全球 GitHub 公开仓库，无地区限制；筛除 fork 和 archived 仓库。
- 纳入以实际 Agent Skills、单个技能或技能工作流为主要内容的仓库，并确认存在有实质正文的 `SKILL.md`。ECC 的技能是主要用户入口之一，因此纳入。
- 排除只有链接的清单、没有技能文件的通用 prompt / persona 集合，以及仅附带技能的应用、客户端和工具。
- 5 组检索发现 72 个去重候选，检查 19 个仓库的文件树后，按符合口径候选的 `stargazers_count` 降序选取 10 个。**这是本次检索范围内的热度 Top 10，不能声称是穷尽全部 GitHub 仓库的官方全球榜单，也不是质量排名。**
- 文件树中的技能文件数量包含镜像、翻译、生成文件和测试夹具，因此不把它当作独立原创技能数。

检索条件如下，具体 API 返回见快照：

```text
skills in:name stars:>10000 fork:false archived:false
"agent skills" stars:>10000 fork:false archived:false
"claude skills" stars:>10000 fork:false archived:false
skill in:name stars:>40000 fork:false archived:false
"SKILL.md" in:readme stars:>60000 fork:false archived:false
```

## Top 10 清单

以下星数为上述时间的 API 快照；素材正文引用固定 commit，避免后续仓库变化影响溯源。

| 排名 | 仓库 | Stars | 主要素材价值 | 许可证范围 |
|---:|---|---:|---|---|
| 1 | [obra/superpowers](https://github.com/obra/superpowers) | 294,518 | 触发描述、好坏对照、失败场景与验证 | MIT |
| 2 | [mattpocock/skills](https://github.com/mattpocock/skills) | 274,789 | 上下文指针、按需披露、交接和完成条件 | MIT |
| 3 | [affaan-m/ECC](https://github.com/affaan-m/ECC) | 271,437 | 迭代检索、上下文压缩、持久化状态 | MIT；个别附带目录另有声明 |
| 4 | [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | 216,601 | 假设、简化、改动边界、可验证目标 | 代表技能 frontmatter 声明 MIT；未发现根 LICENSE |
| 5 | [anthropics/skills](https://github.com/anthropics/skills) | 179,423 | 技能结构、渐进加载、触发与基线评测 | 代表 skill-creator 为 Apache-2.0；全库混合授权 |
| 6 | [garrytan/gstack](https://github.com/garrytan/gstack) | 134,811 | 条件路由、工具边界、输出契约、证据表达 | MIT |
| 7 | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 132,596 | 检索契约、按需参考、全局规则与局部覆盖 | MIT；ui-styling 附带目录另有声明 |
| 8 | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 100,569 | 分层上下文、有效/浪费输入对照、重启交接 | MIT |
| 9 | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | 92,092 | 明确适用场景、配置参数、具体输出示例 | MIT |
| 10 | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 76,376 | 技能结构、资源拆分、具体任务与反馈模板 | README 声明 Apache-2.0，要求逐技能核对 |

名称已归一：`forrestchang/andrej-karpathy-skills` 当前重定向至 `multica-ai/andrej-karpathy-skills`；`affaan-m/everything-claude-code` 当前重定向至 `affaan-m/ECC`，不重复计入。

## 已读素材与可提取模式

每段的“观察”是文件中实际存在的结构；“建议”是本项目后续采集方向，并不表示这些写法已在本项目通过实验。

### 1. obra/superpowers

观察：[skills/writing-skills/SKILL.md](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/writing-skills/SKILL.md) 有 description 好坏对照、症状触发、常见误区和压力测试方法，主张先观察无技能基线的失败。建议优先采集“模糊能力描述 → 明确适用症状”和“流程要求 → 可检查完成条件”。作者关于措辞效果的经验陈述应保留为作者观点，后续自行验证。[许可证](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/LICENSE)：MIT。

### 2. mattpocock/skills

观察：[skills/productivity/writing-for-agents/SKILL.md](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/skills/productivity/writing-for-agents/SKILL.md) 把读取条件写入上下文指针，按任务分支披露参考材料，并区分步骤与参考；[handoff/SKILL.md](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/skills/productivity/handoff/SKILL.md) 通过路径引用已有工件，且限制模型自动调用。建议采集“没有读取条件的链接 → 条件化指针”和“重复整个历史 → 引用已保存状态”。[许可证](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/LICENSE)：MIT。

### 3. affaan-m/ECC

观察：[skills/iterative-retrieval/SKILL.md](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/iterative-retrieval/SKILL.md) 展示检索、相关性判断、补缺和再次检索，用鉴权和限流任务说明术语更新；[strategic-compact/SKILL.md](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/strategic-compact/SKILL.md) 有阶段切换决策表与压缩前保存计划的要求。建议采集“全量塞入/完全不提供上下文 → 发现缺口后补齐”和“压缩中途状态 → 先保存再切换”。检索代码含未定义辅助函数，应标为示意伪代码。[许可证](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/LICENSE)：MIT；本轮选用 `skills/` 下上述正文。

### 4. multica-ai/andrej-karpathy-skills

观察：[skills/karpathy-guidelines/SKILL.md](https://github.com/multica-ai/andrej-karpathy-skills/blob/2c606141936f1eeef17fa3043a72095b4765b9c2/skills/karpathy-guidelines/SKILL.md) 是精简行为约束；[EXAMPLES.md](https://github.com/multica-ai/andrej-karpathy-skills/blob/2c606141936f1eeef17fa3043a72095b4765b9c2/EXAMPLES.md) 以同一请求呈现错误实现、问题说明和改进，例如导出范围的隐藏假设、折扣计算的过度抽象。建议用作本项目 K1–K4 对照例的来源，给每个例子加可观察判据。技能声明 MIT，但根目录没有 LICENSE；`EXAMPLES.md` 的复用范围需另行确认，当前先保留链接和自主总结。

### 5. anthropics/skills

观察：[skills/skill-creator/SKILL.md](https://github.com/anthropics/skills/blob/8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4/skills/skill-creator/SKILL.md) 包含元数据、技能正文、按需资源的三层结构，以及触发正负案例、with-skill / baseline 对照与人工反馈。建议采集“触发描述如何评测”和“核心流程与按需参考如何拆开”。该技能有 [Apache-2.0 许可证](https://github.com/anthropics/skills/blob/8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4/skills/skill-creator/LICENSE.txt)；[README](https://github.com/anthropics/skills/blob/8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4/README.md) 明确 docx/pdf/pptx/xlsx 是 source-available，不能把这四类当作同样的开源素材。

### 6. garrytan/gstack

观察：[plan-eng-review/SKILL.md](https://github.com/garrytan/gstack/blob/f30b7b788a210d217ea3125bf3001b29cbc2a463/plan-eng-review/SKILL.md) 含触发词、工具范围、目标选择和条件路由；[review/SKILL.md](https://github.com/garrytan/gstack/blob/f30b7b788a210d217ea3125bf3001b29cbc2a463/review/SKILL.md) 有具体证据表达的好坏对照。文件由 `SKILL.md.tmpl` 生成，并依赖运行时 preamble。建议采集“泛泛宣称发现问题 → 文件、触发、用户影响与修复依据”；教学短例应说明环境依赖，保留真正的授权边界。[许可证](https://github.com/garrytan/gstack/blob/f30b7b788a210d217ea3125bf3001b29cbc2a463/LICENSE)：MIT。

### 7. nextlevelbuilder/ui-ux-pro-max-skill

观察：[.claude/skills/ui-ux-pro-max/SKILL.md](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/09170eec67eefd46a7ae85de61b40c194020f997/.claude/skills/ui-ux-pro-max/SKILL.md) 根据任务选择设计系统、domain 或 stack 检索，要求检查匹配结果并限制重试；完整规则按需读取，持久化区分 MASTER 与页面覆盖。建议采集“关键词堆叠 → 一个意图和必要约束”和“通用规则 → 局部覆盖”，用小任务呈现流程。它的 UX 数值和技术建议仍需各自的权威来源。[许可证](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/09170eec67eefd46a7ae85de61b40c194020f997/LICENSE)：MIT；不由此推定附带 `ui-styling` 的授权。

### 8. addyosmani/agent-skills

观察：[skills/context-engineering/SKILL.md](https://github.com/addyosmani/agent-skills/blob/9d0c60d406b454a78ccc0a175b19932047aa4dac/skills/context-engineering/SKILL.md) 分出项目规则、规格、源码、错误输出和历史五层；有有效/浪费上下文对照，以及重启前需保存的范围、状态、文件和验证结果。建议优先采集“整个规格/完整日志 → 当前任务所需片段”和“口头进度 → 可恢复交接”。文中的上下文阈值视为作者建议，不能写成跨模型定律。[许可证](https://github.com/addyosmani/agent-skills/blob/9d0c60d406b454a78ccc0a175b19932047aa4dac/LICENSE)：MIT。

### 9. Leonxlnx/taste-skill

观察：[skills/taste-skill/SKILL.md](https://github.com/Leonxlnx/taste-skill/blob/ce26fc25c0e5e8cab638f883de62d9a86ee5e45b/skills/taste-skill/SKILL.md) 先声明落地页、作品集和重设计场景，按 brief 推断方向，并用三个参数连接约束与输出，提供具体设计理解示例。建议采集“抽象形容词 → 受众、页面类型和可操作参数”。[README](https://github.com/Leonxlnx/taste-skill/blob/ce26fc25c0e5e8cab638f883de62d9a86ee5e45b/README.md) 把当前默认版本标为 v2 experimental；审美偏好与硬性质量条件应分别记录。[许可证](https://github.com/Leonxlnx/taste-skill/blob/ce26fc25c0e5e8cab638f883de62d9a86ee5e45b/LICENSE)：MIT。

### 10. ComposioHQ/awesome-claude-skills

观察：[skill-creator/SKILL.md](https://github.com/ComposioHQ/awesome-claude-skills/blob/be2a406907dbc61b73e6827ded415c96139d13a2/skill-creator/SKILL.md) 用具体任务推导可复用脚本、参考和资源；[content-research-writer/SKILL.md](https://github.com/ComposioHQ/awesome-claude-skills/blob/be2a406907dbc61b73e6827ded415c96139d13a2/content-research-writer/SKILL.md) 有输入、分节反馈和修改理由模板。建议优先采集资源拆分与反馈结构；writer 中的演示统计、人物引语不能当作已验证事实。creator 的 [局部许可证](https://github.com/ComposioHQ/awesome-claude-skills/blob/be2a406907dbc61b73e6827ded415c96139d13a2/skill-creator/LICENSE.txt) 为 Apache-2.0；[README](https://github.com/ComposioHQ/awesome-claude-skills/blob/be2a406907dbc61b73e6827ded415c96139d13a2/README.md) 提醒各技能授权可能不同，不能批量套用。

## 下一轮采集建议

下面是从已读来源推导的工作建议，暂未建立与现有模式编号的正式映射。

| 重写目标 | 优先来源 | 下一轮记录的证据 |
|---|---|---|
| description 的触发与边界 | superpowers、Anthropic、Matt Pocock | 原始触发、适用/不适用请求、正文读取条件 |
| 上下文选择与渐进加载 | Matt Pocock、Addy Osmani、ECC | 入口信息、按需材料、检索缺口、终止条件 |
| good / bad 成对例 | Karpathy、superpowers、gstack | 同一任务、相同已知条件、改变的行为、失败原因 |
| 结构化输出与反馈 | gstack、Composio | 必填字段、具体反馈、证据位置、可检查完成条件 |
| 长任务与交接 | ECC、Matt Pocock、Addy Osmani | 已接受范围、状态、下一步、验证命令与结果 |
| 参数化、规则继承与局部覆盖 | UI UX Pro Max、taste-skill | 约束来源、选择分支、参数含义、覆盖顺序 |

采集记录建议保留：仓库、固定 commit、文件/小节、许可证范围、原始任务、失败行为、改善行为、适用边界、候选模式名称和验证状态。自主改写的反例标明“教学构造”；源仓库已有反例标明“来源中的对照示例”。只有观察到实际运行或测试证据，才标记“已验证有效”。

两项差异需要在重写时保留：Anthropic 建议 description 同时表达能力和触发，superpowers 倾向只表达触发；这些是待用正负触发案例比较的设计选择。各仓库关于 token 节省、速度提升和上下文阈值的数字，也需要追溯原始评测或在本项目重测。

后续可以补充两个**榜外高相关来源**，不混入热度排名：[Vercel React Best Practices](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/SKILL.md) 的独立规则采用原因、Incorrect、Correct、参考结构，尤其 [async-parallel.md](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/async-parallel.md) 适合短对照例；[Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/main/skills/context-fundamentals/SKILL.md) 将概念解释与检索、压缩、退化诊断等操作分流。补充源目前只确认入口正文，正式采集时再固定 commit。

本轮未安装这些技能、执行外部仓库脚本、调用付费评测或更改产品代码。后续内容重写与项目结构整理一起规划，关联事项见 [项目整理问题记录](../project-cleanup-issues.md)。
