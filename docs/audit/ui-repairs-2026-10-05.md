# 阶段一：界面与交互修复

计划：`docs/specs/2026-10-05-blog-polish.md`。基线：`313ac65413ea7cbf4d82a8a583d8eb5c4b235ac7`，工作分支：`rebuild/skills-catalog`。

状态：阶段一已实现，等待用户界面验收；阶段二双语样稿尚未开始。没有提交、push、merge 或部署。

## 修复结果

| 项目 | 行为 |
| --- | --- |
| UI-001 | 普通页面不再无条件查询方法；标题、description、Open Graph 使用页面自己的元信息。独立方法仍使用方法记录，搜索初始 HTML 与加载后的标题分别检查。 |
| UI-002 | 完整目录的方法标题、来源页仓库标题、指南参考链接及详情中的独立来源链接有连续点击框，换行间隙包含在链接内。 |
| 分类标签 | 当前主题卡片显示不可点击 tag，且点击 tag 不会触发整卡片详情链接；首页、搜索、详情和目录仍保留分类入口。 |
| 参考外链 | 全站生成的跨域 HTTP/HTTPS anchor 输出 `_blank` 和 `noopener noreferrer`，不依赖 JavaScript。当前阅读页保留。 |
| 正反例 | 反例红色边框、改进写法绿色边框；612 份正文各加两个 Markdown 区块属性，不改其余内容。原有标题和代码语法保留。 |
| UI-003 | 来源标签不再露出 Markdown 星号；`<HARD-GATE>` 字面值仍可见。检查 P14/P25 双语详情；P112 保留合并到 P25 的双语入口。 |

已同步 `DESIGN.md`、`UX-CONTRACT.md`。中文翻译、篇幅和教学深度在此阶段没有改写。

## 验证

- 修改前：原有 19 项 Node 测试通过；新增浏览器检查复现首页 P1 标题、多行目录命中 TD、来源星号，以及尚无 tag／示例角色标记的原状。
- 修改后：19 项 Node 测试通过；完整 Playwright 套件 20 项通过，包含 8 项新增回归检查和 Axe 检查。
- 英文完整目录 768px：检查全部 306 个标题中心实际命中链接，并实际点击 P60。中文指南 375px：中心点击与键盘 Enter 均到 P26。
- 长仓库标题与来源证据链接通过真实浏览器鼠标／键盘激活创建新标签，核对精确目标 URL，确认原页面保留。测试拦截 GitHub 响应，不把上游加载速度或可访问性作为回归判据。
- 全部 876 个生成 HTML 页面检查跨域 anchor 属性；全部 612 个有效双语详情保留正反例标记。
- 源码逐份与 HEAD 比较：移除新加入的两条区块属性后，612 份正文与原文完全相同。
- Jekyll 构建、确定性生成检查、5 项 Liquid 字面值检查、目录校验通过。
- 来源身份／文件／定位检查通过：10 个冻结仓库、9,806 个文件，334 个证据文件，目录校验零错误。
- 渲染链接检查通过：876 个 HTML 页面、17,653 项内部链接／资源及旧入口检查，零错误。
- 前端静态严格审计：零错误、零警告；报告 `.tools/ui-repairs-premium-audit.json`。
- 375/768/1280px 共 15 张截图，检查过的页面无整页横向溢出；截图与元信息清单 `.tools/ui-repairs-visual-check.json`。
- 200% 检查使用 640 CSS-pixel 的等效布局视口，不声称操作了浏览器实际缩放 UI。

## 用户验收入口

- 当前主题 tag：`http://127.0.0.1:4000/prompt-context-patterns/topics/prompt-zh/`
- 正反例颜色：`http://127.0.0.1:4000/prompt-context-patterns/catalog/patterns/8-zh/`
- 新标签来源链接：`http://127.0.0.1:4000/prompt-context-patterns/catalog/patterns/1-zh/`
- 来源标签：`http://127.0.0.1:4000/prompt-context-patterns/catalog/patterns/25-zh/`
- 长标题点击：`http://127.0.0.1:4000/prompt-context-patterns/catalog/catalog-index/`

截图目录：`.tools/screens/ui-repairs-2026-10-05/`，包含 topic、examples、source-label、sources、guide 的三个宽度。

## 边界与后续

本轮没有重新逐项访问所有 GitHub 上游链接，也没有声称全部网页链接均被实际点击。自动检查外链属性与弹出目标，来源正确性以冻结文件／commit／行号校验补充。

用户验收界面后，按已批准计划进入 P1、P8、P23、P224、P323、P387 六篇双语样稿。样稿验收前不开始剩余 300 篇扩写。
