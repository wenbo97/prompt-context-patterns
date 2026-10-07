---
layout: default
title: 写出有用的对照示例
permalink: /guides/teaching-examples-zh/
alternate_url: /guides/teaching-examples/
lang: zh
description: "围绕同一任务和输入设计正反例，解释具体缺陷、改进动作与可检查结果。"
last_modified_at: 2026-10-06
---
# 写出有用的对照示例

固定任务和已知事实。先展示会引发失败的指令，再修改导致失败的部分。说明应检查什么，以及方法不再适用的边界。

## 示例

任务：为只接受四种分类的下游系统分类支持消息。

反例：`分类这条消息并解释。`

改进：`返回包含 category 和简短 reason 的 JSON。category 仅为 billing|technical|feedback|other；信息不足时用 other，并指出缺少的事实。`

可检查结果：解析 JSON 并验证 category 枚举。它检查输出格式与规则，不证明语义分类正确。分类准确性应另用有标注的代表性请求评估。

[输出格式与规则]({{ '/catalog/patterns/14-zh/' | relative_url }}) · [编辑标准]({{ '/methodology-zh/' | relative_url }})
{: .guide-references}
