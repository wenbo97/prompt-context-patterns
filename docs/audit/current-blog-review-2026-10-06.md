# 当前博客审查与搜索索引更新方案

日期：2026-10-06（Asia/Shanghai）。审查工作区：`D:\A_Projects\prompt-context-patterns-refresh`，分支 `rebuild/skills-catalog`。HEAD：`313ac65413ea7cbf4d82a8a583d8eb5c4b235ac7`。

## 范围与结论

已读交接文档 `prompt-context-patterns-handoff-20261006-212634.md`，以仓库指定的清理基线 `9456091c44d796918745eaecad9d1ee9e726b244` 对照当前工作树，包含四个已提交检查点、当前未提交改动及未跟踪交付源码。开始时 681 个 Git 状态条目；1,469 个现有工作文件保存 SHA-256 供结束时核对。refresh 没有 `.codegraph/`，未使用或建立索引。

审查覆盖规范、规格、共享模板、浏览器状态、生成与校验管线、CI、Patternfoo、全站构建路由/链接/SEO 结构和六篇双语样稿。全部 612 个有效双语详情通过结构、身份、元信息和来源定位检查；本次没有重新逐句语义评阅其余 300 篇，也没有重新人工审查十个冻结仓库的 9,806 个文件。来源检查复核现有证据记录和冻结文件身份，不把机器校验当作新一轮语义审查。

当前构建与既有测试通过，但额外组合测试发现一项双语状态缺陷，搜索专项检查发现一项 lastmod 缺陷。robots 的主机根路径问题属于部署/发现流程限制；统一摘要属于可改进项。尚未进入全站内容深化完成后的最终交付验收。

## Standards

独立规范审查未发现高置信、可行动的规范违反。检查了 AGENTS、CLAUDE、DESIGN、UX-CONTRACT、CONTEXT、工作流、配置、目录脚本、模板/CSS、README 和测试约定；扫描 780 个 pattern Markdown 文件的 bad/good 示例标记未发现缺失。

此结论没有逐行审计大型生成 JSON/harvest 证据，也不代表全文机制与每一处翻译均无问题。复核当前技术结果见下文。

## Spec

### R1 · P2 · 加载与错误状态切换语言后保留旧语言

位置：[`assets/catalog.js:24`](../../assets/catalog.js)、[`assets/catalog.js:70`](../../assets/catalog.js)、[`assets/catalog.js:91`](../../assets/catalog.js)、[`assets/catalog.js:100`](../../assets/catalog.js)、[`assets/catalog.js:112`](../../assets/catalog.js)。

规格第 7 行要求覆盖双语的 “site labels, themes, search states”；UX-CONTRACT 的目录状态和本地化反馈也应随语言变化。语言按钮更新 state 后调用 render，localize 更新页面语言与按钮；available 为 false 时 render 立即返回。加载文案只在 load 开始时写入，错误文案只在 catch 写入，因此两者没有跟随语言变化。

Chrome 154.0.8037.98 的复现：

1. 拦截 `assets/patterns.json` 请求为失败，打开 `/catalog/browse/?lang=en`。
2. 等错误出现后点击中文：html 已是 zh-CN，按钮显示“重新加载”，错误仍是 `Pattern data could not be loaded.`。
3. 延迟数据响应时点击中文：状态仍是 `Loading patterns…`，预期为“正在加载…”。

英语和中文消息均已定义；应显式记录 loading/error/ready 状态，在 localize/render 中依据当前状态更新消息。补一个真实浏览器语言切换与请求失败/延迟的组合回归。现有 26 项 E2E 全通过，未覆盖这个组合。

主审查与 Spec 审查者独立复现。证据：`.tools/review-20261006/browser-probe.json`、`browser_probe.mjs`、`failure-language-zh.png`。

独立 Spec 审查未发现其他已交付范围内可确认的高置信缺陷。其余 300 篇是规格第 9 行明确等待合并检查点接受的 Phase 3，不作为意外缺陷；当前报告明确标为尚未改写。

## 搜索与上线专项

### R2 · P2 · 612 个详情的 lastmod 使用构建时间

位置：[`_patterns/1.en.md:1`](../../_patterns/1.en.md) 所代表的全部有效 collection front matter，及 [`_config.yml:10`](../../_config.yml) 的 collection 配置。现有源码没有给这些文件定义 date/last_modified_at。

安装的 Jekyll 3.10.0 `Document#date` 默认返回 site.time；jekyll-sitemap 1.4.0 的 collection 模板使用 last_modified_at，缺失时使用 doc.date。因此每次构建都把所有 612 个详情声明为刚更新。

复现：首次构建的详情 lastmod 为 `2026-10-06T21:36:47+08:00`；不改源码，第二次构建到隔离输出目录后全部变为 `2026-10-06T21:39:03+08:00`。两次 sitemap 的 655 个 URL 集合相同，612 个详情时间戳发生变化；开始时记录的 1,469 个工作文件均无变化。证据：`.tools/review-20261006/lastmod-reproduction.json` 和 `lastmod-rebuild/sitemap.xml`。

应维护实际内容更新时间并提供准确的 last_modified_at；拿不到可信日期时，应调整生成方式省略该值。不能直接补丁 `_site/sitemap.xml`，也不能把编辑准入审核日期当作内容更新日期。回归判据：无内容变更的两次构建不改变这些值，实际内容修改才更新对应页面。Google 使用 consistently accurate 的 lastmod；这项修复改善变更信号，不保证抓取时间或排名。[Google sitemap 指南](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)

### R3 · 部署/发现限制 · 项目子路径的 robots.txt 不具主机级效力

位置：[`robots.txt:1`](../../robots.txt)、[`scripts/catalog/check-site.mjs:66`](../../scripts/catalog/check-site.mjs)。

本次真实 HTTP 读取：`https://wenbo97.github.io/robots.txt` 返回 404；`https://wenbo97.github.io/prompt-context-patterns/robots.txt` 返回 200 并声明 sitemap。爬虫采用主机根目录的 robots.txt，不能把子目录文件作为主机规则。当前本地 checker 只检查 `_site/robots.txt` 内容，不能验证上线后的适用范围。[Google robots 位置规则](https://developers.google.com/crawling/docs/robots-txt/create-robots-txt)

根目录没有 robots 不等于禁止抓取，但不能依赖当前子目录声明来自动发现 sitemap。可以由主机根站点维护正确的文件，或直接在现有 Google/Bing 属性提交 sitemap。本仓库不能靠把文件放在项目目录解决主机根路径问题；本轮没有修改根站点。之前“robots 检查通过”应理解为本地产物文本正确。

### R4 · P3 建议 · 41 个普通页面共用英文摘要

位置：[`_layouts/default.html:4`](../../_layouts/default.html) 的全站摘要回退，以及普通页面/生成器 front matter。

全部 655 个可索引页标题无重复；其中 41 个普通页，包括中文主题、来源、指南、方法论和八个历史文章，共用英文 site.description。有效方法详情均使用各自摘要，不受此项影响。建议给这些普通页面补与内容和语言一致的 description，必要时由主题/索引生成器统一产出。搜索摘要可能来自正文；此项不代表这些页面不能收录。[Google 页面摘要建议](https://developers.google.com/search/docs/appearance/snippet)

## 当前验证结果

以下为本次实际重跑结果，不沿用交接数字作为当前通过证据：

| 检查 | 当前结果 |
| --- | --- |
| npm test | 23 项通过 |
| npm run check / check:sources | 390 个身份、306 个有效方法；9,806 个来源文件记录、334 个证据文件、553 个范围检查，零错误 |
| npm run check:generated | 生成结果一致，无源码写入 |
| Liquid 字面值检查 | 5 项通过 |
| Patternfoo | 11 项通过，TypeScript 构建通过 |
| Jekyll | 主构建与隔离 lastmod 复现构建均通过 |
| npm run check:links | 876 HTML、21,948 项检查，零错误 |
| npm run check:site | 655 可索引、221 noindex；57 旧页面、8 历史文章路由、412 双语旧方法映射、1,410 标题归属映射，零结构错误 |
| Google Chrome E2E/Axe | 26 项通过，channel=chrome；安装版 154.0.8037.98 |
| frontend premium strict audit | 零错误、零警告 |
| 额外浏览器检查 | 上述语言状态缺陷复现；中英首页、中文 P323 和总目录在 375/1280px 八张截图无页面宽度溢出 |

已查看代表性首页、详情与目录截图。375/768/1280px 的应用回归由套件覆盖；本次没有重新执行上轮 876 页三宽度的 2,628 份截图及全部链接逐项激活，也没有重跑 355 个外部地址探测。真实浏览器菜单 200% 缩放和 Windows 系统 IME 仍未执行；套件的等效重排和合成 composition 不替代它们。没有执行模型效果 A/B 或真实教学系统操作。

原审计 JSON 和 `.tools/polish-2026-10-06/site-manifest.json` 在检查前保存，检查后恢复原字节；本次结果单独留在 `.tools/review-20261006/`。没有重写旧主报告或删除证据。`.tools` 为忽略材料，不能自动随仓库交付。

## 生产版本与索引现状

2026-10-06 21:38 左右实际 HTTP 读取：

| 地址 | 观察 |
| --- | --- |
| 正式首页 | 200，仍显示旧版 Prompt, Context & Agent Orchestration |
| 正式 sitemap.xml | 200，67 个 URL |
| 新版 /catalog/patterns/1/ | 404，尚未发布 |
| 新版 /index-zh/ | 404，尚未发布 |
| 现有 /catalog/catalog-index/ | 200，旧版目录 |
| 项目路径 BingSiteAuth.xml | 200，验证 XML；首页同时有 Google/Bing 验证 meta |
| 主机根 robots.txt / BingSiteAuth.xml | 均 404 |

本地与线上 sitemap 比较：13 个 URL 相同，新版增加 642 个可索引 URL，54 个旧 sitemap URL 不再进入新版可索引列表。它们的兼容路由/锚点仍按既有规格保留；没有授权删除旧路由。

这是公开 HTTP 与 sitemap 观察，不是 Search Console/Webmaster Tools 的账户记录，也不能推出已收录数量。本轮没有登录控制台、读取账号属性/提交历史、提交 sitemap、调用 IndexNow 或部署。

## 发布后的 Google 流程

1. 完成当前缺陷修复、界面/样稿检查点、剩余内容计划及最终交付验证，再按届时明确的发布授权发布。
2. 验证线上新版首页、双语详情、旧兼容页、canonical/hreflang、验证 meta/XML 和 sitemap；确认 sitemap 返回 200 且内容为最终发布版本。当前目标 655 URL，以最终版本实数为准。
3. 在现有 Search Console 选择覆盖 `https://wenbo97.github.io/prompt-context-patterns/` 的属性。现有验证方式继续保留；账号属性与权限需届时实际读取。URL-prefix 属性适用于本项目，不需要为了本轮改版新建域名属性。
4. 打开 Sitemaps，先读取现有提交和 Last read/Status，再提交或重新提交同一完整 URL：`https://wenbo97.github.io/prompt-context-patterns/sitemap.xml`。若输入框已固定项目 URL 前缀，只填写 `sitemap.xml`；若属性前缀为主机，则填写 `prompt-context-patterns/sitemap.xml`。不删除再换一个带随机参数的 sitemap。Google 在重大 sitemap 变更后允许重新提交；正常情况下也会定期读取。[Search Console Sitemaps](https://support.google.com/webmasters/answer/7451001?hl=en)
5. 对少量重点页做 URL Inspection → Test live URL → Request indexing，例如中英文首页、总目录和六篇样稿。大量新详情通过 sitemap 发现；重复提交同一 URL 不会加快抓取。[Google 重新抓取指南](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl)
6. 检查 Page indexing、Google-selected canonical、抓取日期、noindex 排除及 404/soft-404。成功提交、已抓取、已收录分别记录，不能互相替代。

此次域名和 baseurl 不变，不使用 Change of Address。[Google 站点迁移指南](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes)

Google Indexing API 仅用于规定的 JobPosting 和直播 BroadcastEvent/VideoObject 页面，这个方法博客通过 sitemap 与 URL Inspection 更新。[Google Indexing API 使用范围](https://developers.google.com/search/apis/indexing-api/v3/using-api)

## 发布后的 Bing 流程

1. 选择现有、已验证且覆盖项目路径的 Bing Webmaster Tools 网站，读取现有 sitemap 与最近抓取记录。
2. 在 Sitemaps 提交/更新同一完整生产 sitemap URL。先确认成功读取，再观察 URL Inspection 与索引状态；现有所有权 meta/XML 保留。Bing 支持 sitemap 与 IndexNow 配合使用。[Bing sitemap 与变更发现说明](https://blogs.bing.com/webmaster/2025/7/Keeping-Content-Discoverable-with-Sitemaps-in-AI-Powered-Search/)
3. 初次发布可先采用控制台 sitemap 加少量重点 URL 提交；持续更新时可接入 IndexNow。当前站点实现未发现 IndexNow 接入，BingSiteAuth/msvalidate 验证值不是 IndexNow key。
4. IndexNow 用独立 key，在项目根发布 UTF-8 key 文件，例如 `https://wenbo97.github.io/prompt-context-patterns/<key>.txt`。每次通知显式传 keyLocation，作用范围覆盖此项目子路径；无需为了接入项目更新占用主机根目录。[IndexNow keyLocation 规则](https://www.indexnow.org/documentation)
5. 对 `https://api.indexnow.org/indexnow` 发送 JSON，host 为 `wenbo97.github.io`，keyLocation 为上述项目 key 文件，urlList 为真实已新增/修改/删除的线上 URL。示意如下，尚未生成 key 或发送请求：

```json
{
  "host": "wenbo97.github.io",
  "key": "<actual-indexnow-key>",
  "keyLocation": "https://wenbo97.github.io/prompt-context-patterns/<actual-indexnow-key>.txt",
  "urlList": [
    "https://wenbo97.github.io/prompt-context-patterns/",
    "https://wenbo97.github.io/prompt-context-patterns/catalog/patterns/1/",
    "https://wenbo97.github.io/prompt-context-patterns/catalog/patterns/1-zh/"
  ]
}
```

协议每个 POST 最多 10,000 URL。200 表示接收，202 表示接收且 key 验证待完成；均不能写成已收录。旧页改为 noindex 也是页面变更，可通知 Bing 重新读取；不会仅靠“从 sitemap 去掉”立刻删除索引。[IndexNow 协议及状态码](https://www.indexnow.org/documentation)

Bing 的匿名 sitemap ping 已被移除；采用 Webmaster Tools 或 IndexNow。[Bing 官方公告](https://blogs.bing.com/webmaster/2022/5/Spring-cleaning-Removed-Bing-anonymous-sitemap-submission/)

## 后续顺序与审查计数

先处理 R1 和 R2；补充 R3 的上线校验/提交路径，R4 可随普通页面文案完善处理。继续既有内容检查点与剩余内容计划后，发布最终版本，再在现有属性更新 sitemap。旧兼容页采用原生迁移链接与客户端重定向，并非 HTTP 301；保持该边界，不声称已保证旧排名信号转移。[Google 重定向建议](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes)

建议发布后第 2–3 天查看接收/读取状态，第 7 天查看代表性页面抓取与 canonical，第 14–28 天看索引覆盖与迁移变化；这是人工复查建议，未创建定时任务，不是索引时限承诺。

独立审查计数：Standards 0 项；Spec 1 项（P2，语言状态）；附加 SEO 1 项 P2（lastmod）、1 项部署/发现限制（robots）、1 项 P3 建议（普通页面摘要）。未修改产品源码，未提交、推送、合并、部署或写入搜索服务。
