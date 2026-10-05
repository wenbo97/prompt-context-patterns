---
layout: "default"
lang: "zh"
title: "内容迁移入口"
permalink: "/catalog/techniques/anti-laziness-zh/"
sitemap: false
robots: "noindex,follow"
canonical_url: "/catalog/index-zh/"
---

<div data-compat><h1>内容已迁移</h1><p>原有地址和小节仍可定位；使用下列链接访问审核后的内容。</p><ul class="compat-list">
<li id="防止-agent-在-skill-引用中偷懒" data-target="{{ '/guides/reference-reading-zh/' | relative_url }}"><a href="{{ '/guides/reference-reading-zh/' | relative_url }}">防止-agent-在-skill-引用中偷懒 → 当前目录</a></li>
<li id="1-背景claude-code-skill-如何工作" data-target="{{ '/catalog/patterns/1-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/1-zh/' | relative_url }}">1-背景claude-code-skill-如何工作 → Skill 元信息（YAML frontmatter）</a></li>
<li id="第一层--元数据预加载每个-skill-约100-token" data-target="{{ '/catalog/patterns/1-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/1-zh/' | relative_url }}">第一层--元数据预加载每个-skill-约100-token → Skill 元信息（YAML frontmatter）</a></li>
<li id="第二层--skillmd-完整正文触发时加载" data-target="{{ '/catalog/patterns/1-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/1-zh/' | relative_url }}">第二层--skillmd-完整正文触发时加载 → Skill 元信息（YAML frontmatter）</a></li>
<li id="第三层--捆绑文件模型按需加载" data-target="{{ '/catalog/patterns/1-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/1-zh/' | relative_url }}">第三层--捆绑文件模型按需加载 → Skill 元信息（YAML frontmatter）</a></li>
<li id="2-agent-跳过引用读取的原因根因分析" data-target="{{ '/catalog/patterns/2-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/2-zh/' | relative_url }}">2-agent-跳过引用读取的原因根因分析 → 按阶段推进任务</a></li>
<li id="3-策略附好坏示例" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">3-策略附好坏示例 → 先选择工作模式</a></li>
<li id="策略-1--祈使框架而非另见" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">策略-1--祈使框架而非另见 → 先选择工作模式</a></li>
<li id="差" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">差 → 先选择工作模式</a></li>
<li id="好" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">好 → 先选择工作模式</a></li>
<li id="策略-2--将读取变成编号步骤" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">策略-2--将读取变成编号步骤 → 先选择工作模式</a></li>
<li id="差-1" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">差-1 → 先选择工作模式</a></li>
<li id="好-1" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">好-1 → 先选择工作模式</a></li>
<li id="策略-3--内联锚点--引用深度" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">策略-3--内联锚点--引用深度 → 先选择工作模式</a></li>
<li id="差--纯引用无锚点" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">差--纯引用无锚点 → 先选择工作模式</a></li>
<li id="差--完全内联违背重构目的" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">差--完全内联违背重构目的 → 先选择工作模式</a></li>
<li id="好--锚点--引用" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">好--锚点--引用 → 先选择工作模式</a></li>
<li id="策略-4--按风险分层内联-vs-引用最重要的原则" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">策略-4--按风险分层内联-vs-引用最重要的原则 → 先选择工作模式</a></li>
<li id="策略-5--用确定性代码替代-prompt" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">策略-5--用确定性代码替代-prompt → 先选择工作模式</a></li>
<li id="差-2" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">差-2 → 先选择工作模式</a></li>
<li id="好-2" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">好-2 → 先选择工作模式</a></li>
<li id="策略-6--验证循环--自检" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">策略-6--验证循环--自检 → 先选择工作模式</a></li>
<li id="好-3" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">好-3 → 先选择工作模式</a></li>
<li id="策略-7--子-agent-隔离最强" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">策略-7--子-agent-隔离最强 → 先选择工作模式</a></li>
<li id="差-3" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">差-3 → 先选择工作模式</a></li>
<li id="好-4" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">好-4 → 先选择工作模式</a></li>
<li id="策略-8--经验测试不要靠猜" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">策略-8--经验测试不要靠猜 → 先选择工作模式</a></li>
<li id="差-4" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">差-4 → 先选择工作模式</a></li>
<li id="好-5" data-target="{{ '/catalog/patterns/3-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/3-zh/' | relative_url }}">好-5 → 先选择工作模式</a></li>
<li id="4-决策框架" data-target="{{ '/catalog/patterns/4-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/4-zh/' | relative_url }}">4-决策框架 → $ARGUMENTS 调用参数</a></li>
<li id="5-结论" data-target="{{ '/catalog/patterns/5-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/5-zh/' | relative_url }}">5-结论 → 为 Agent 指定角色和职责</a></li>
<li id="附录每个重构-pr-的快速检查清单" data-target="{{ '/catalog/patterns/5-zh/' | relative_url }}"><a href="{{ '/catalog/patterns/5-zh/' | relative_url }}">附录每个重构-pr-的快速检查清单 → 为 Agent 指定角色和职责</a></li>
</ul></div>
<script src="{{ '/assets/compat.js' | relative_url }}"></script>
