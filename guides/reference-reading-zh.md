---
layout: default
title: 确认 Agent 实际读取了参考文件
permalink: /guides/reference-reading-zh/
alternate_url: /guides/reference-reading/
lang: zh
---
# 确认 Agent 实际读取了参考文件

当 agent 未读任务规则就行动时使用。依据实际记录定位缺失的读取，不假定其动机是“偷懒”。

## 同一任务的两种写法

反例：`遵守我们的部署指导。`

改进：`提出生产部署方案前读取 deployment-rules.md，报告审批要求、回滚条件及所在小节。文件不存在时停止，说明缺失输入。`

改进版本明确触发条件、文件、所需证据及缺失输入的处理，使读取义务可以检查；这不保证模型必然遵守。

## 只提供需要的上下文

每个分支都需要的规则放在行动附近。特定分支的材料通过明确读取条件加载。确定性检查可以使用接口和失败行为已知的脚本；仍须验证实际结果，不能把脚本存在本身当作完成证据。

[按需读取参考文件]({{ '/catalog/patterns/23-zh/' | relative_url }}) · [按需展开详细内容]({{ '/catalog/patterns/100-zh/' | relative_url }}) · [用证据支撑结论]({{ '/catalog/patterns/26-zh/' | relative_url }})
