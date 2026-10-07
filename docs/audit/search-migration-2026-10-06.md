# 上线前 URL、sitemap 与验证文件检查

日期：2026-10-06。状态：本地检查完成，尚未发布，控制台与线上复验待明确授权的上线阶段执行。

## 本地结果

- 构建 876 个 HTML 页面，655 个可索引页面全部在 sitemap，221 个合并、撤下或兼容页面不在 sitemap。无重复、错误域名、本地地址或查询状态 URL。
- 612 个有效双语详情的标题、摘要、canonical 与权威目录对应；双语 hreflang 存在且互指。其他已声明语言配对同样核验。搜索页保留单一 canonical，lang 查询状态不作为独立语言页面。
- robots 指向现有生产 sitemap。检查保留自动 Jekyll sitemap 生成，不手写新的 URL 列表。
- 57 个旧页面、8 个历史文章路由和 412 条旧方法双语映射检查通过；13 个旧中文详情锚点别名已补足。
- 标题层级迁移校验 1410 项：数字步骤标题继承其方法归属，独立汇总小节不借用最后一个方法。旧锚点保留原生链接，JavaScript 仅补充 location.replace；不是服务器 HTTP 301。
- 本机审计报告已从发布产物排除。详细结果：[站点输出](site-output-2026-10-06.json)、[渲染链接](rendered-links.json)、[标题层级证据](legacy-heading-targets.json)。

## Bing 文件与凭据检查

两个 checkout 的 BingSiteAuth.xml 都是单个 users/user 验证值，与对应 msvalidate.01 标签一致。XML 文件和验证标签属于公开网站所有权验证方式，保留它们。[Bing 官方验证说明](https://blogs.bing.com/webmaster/2025/6/Start-Using-Bing-Webmaster-Tools-to-Improve-Your-Site-Visibility/)

本轮离线签名检查各扫描 2,126 个可达历史 blob（每个 checkout 111,831,010 字节），并检查 refresh 的 1,454 个工作文件、master 的 180 个工作文件，以及 889 个发布产物。未检出规则命中的候选凭据。报告不显示验证值或凭据原文：[检查范围与结果](credential-check-2026-10-06.json)。

这是有限签名与赋值规则检查，不是对所有可能秘密类型的不存在证明。没有因为公开验证文件而撤销、轮换或删除它；若以后找到真正的 API 凭据，需按其凭据类型处理。[Bing API 凭据与泄露处理](https://learn.microsoft.com/en-us/bingwebmaster/getting-access)

## 授权上线后的顺序

1. 完成样稿认可、其余 300 篇、最终全站验证及既定独立审阅后，准备范围明确的 Git 与发布操作。
2. 部署后验证线上版本、新旧入口、robots、sitemap 和验证文件；本地通过不替代线上结果。
3. 在现有 Google Search Console 与 Bing Webmaster Tools 属性中读取当前 sitemap 提交，必要时更新同一生产 sitemap URL；记录接收状态和检查日期。
4. 记录抓取、索引、canonical 选择及错误报告，列出后续复查项目；不自动建立定时任务，不把提交成功写成已收录。

域名与站点前缀保持不变，采用路径迁移流程，不使用 Change of Address。[Google 地址变更适用范围](https://support.google.com/webmasters/answer/9370220)、[Google URL 迁移指南](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes)。

当前没有新的控制台结果、提交记录或线上重构版本验收；本报告不代表发布授权。
