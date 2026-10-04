---
layout: post
title: "提示词工程：可观察的指令与有效对照"
date: 2026-04-19
categories: [prompt-engineering, patterns]
lang: zh
last_modified_at: 2026-10-03
---

<span id="核心原则降低不确定性"></span>
<span id="简单例子"></span>
<span id="一句话总结"></span>
<span id="模式-1决策树替代自然语言"></span>
<span id="不好自然语言"></span>
<span id="好决策树"></span>
<span id="模式-2锚定给起点"></span>
<span id="不好无锚定"></span>
<span id="好用模板锚定"></span>
<span id="模式-3认知卸载把思考步骤写出来"></span>
<span id="不好隐式推理"></span>
<span id="好显式步骤"></span>
<span id="模式-4注意力局部性把相关的放在一起"></span>
<span id="不好规则离目标太远"></span>
<span id="好规则紧挨目标"></span>
<span id="模式-5指令-动作绑定一条指令一个动作"></span>
<span id="不好一句话多个动作"></span>
<span id="好一条指令--一个动作"></span>
<span id="模式-6输出格式预设给输出一个形状"></span>
<span id="不好开放式"></span>
<span id="好结构约束"></span>
<span id="模式-7负空间说不要的同时说要"></span>
<span id="不好只说不要"></span>
<span id="好不要--替代方案"></span>
<span id="模式-8xml-标签做语义分区"></span>
<span id="推荐的提示词结构"></span>
<span id="模式-9带推理过程的示例"></span>
<span id="不好只有输入输出"></span>
<span id="好输入--思考过程--输出"></span>
<span id="各模式之间的关系"></span>
<span id="参考资料"></span>

## 历史修订说明

原2026-04-19文章用条件熵和注意力解释提示词结构，但仓库没有将具体措辞与这些模型内部量关联的测量。修订版保留实用方法，移除未经支持的因果保证。

## 从任务和已知事实开始

明确输入、所需结果及未知信息。例如诊断配置问题时，先定位加载器、配置路径和已观察到的症状，再讨论修改。

## 让契约可检查

把“清楚报告”改成必需字段和允许值，并提供缺失输入或未知分支。格式校验能检查契约，不能证明答案为真。

## 使用同任务对照

固定任务与事实，只修改导致一个具体失败的指令，解释可检查的差异并说明边界。本站示例是教学构造，不是模型效果测量。

## 按需要加载上下文

每个分支都需要的约束放在行动附近。任务专属参考材料附明确的读取条件。保留来源位置，不把记忆或摘要当作当前事实的证明。

[教学示例指南]({{ '/guides/teaching-examples-zh/' | relative_url }}) · [参考读取指南]({{ '/guides/reference-reading-zh/' | relative_url }}) · [编辑标准]({{ '/methodology-zh/' | relative_url }})
