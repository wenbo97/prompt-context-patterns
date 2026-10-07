# GitHub Pages + Cloudflare DNS 与 Cloudflare 静态托管选型

查阅日期：2026-10-07。范围：公开 GitHub 仓库 `wenbo97/prompt-context-patterns`、Jekyll 根域迁移、GitHub Pages 与 Cloudflare 免费静态托管。仅依据 GitHub/Cloudflare 官方文档；域名 DNS 观察另列。未据官方全球网络描述推断中国大陆访问性能。

## 已核对的项目与域名状态

本地配置当前为 `url: https://wenbo97.github.io`、`baseurl: /prompt-context-patterns`；GitHub Actions 用 Ruby 3.3 构建并部署。现有 `_site` 目录统计为 889 个文件、8,415,699 字节（约 8.03 MiB），最大单文件为 `assets/patterns.json`（341,640 字节）。这是现有本地产物统计，未在本次重建，也不代表线上下载量。

本轮 Pages API 核查记录为已构建、部署来源为 workflow、`cname=null`、HTTPS enforced。公开 DNS 查询（Google Public DNS DoH，2026-10-07）显示 `patternnotes.dev` 委派到 `elly.ns.cloudflare.com` 与 `kayden.ns.cloudflare.com`；apex 的 A/AAAA 无 Answer，`www.patternnotes.dev` 为 NXDOMAIN。这只能证明公开委派状态与当时没有网站解析，不能证明已查看 Cloudflare 账号中的 Zone 状态。[NS 查询](https://dns.google/resolve?name=patternnotes.dev&type=NS)、[apex A 查询](https://dns.google/resolve?name=patternnotes.dev&type=A)、[apex AAAA 查询](https://dns.google/resolve?name=patternnotes.dev&type=AAAA)、[www CNAME 查询](https://dns.google/resolve?name=www.patternnotes.dev&type=CNAME)。

旧站线上英/中首页和 sitemap 当前可访问；`wenbo97.github.io/robots.txt` 返回 404。这只是迁移前的基线。Workers 自定义域名要求 Cloudflare Zone 已激活；绑定后 Cloudflare 自动创建 DNS 记录与证书。根域与 `www` 是不同主机名，若两者都开放，须分别绑定或给 `www` 配置代理记录和重定向。[Workers Custom Domains](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/)。

## 两条部署路线

| 路线 | 官方能力与免费边界 | 对本项目的影响 |
|---|---|---|
| GitHub Pages + Cloudflare DNS | GitHub Free 的公开仓库可用 Pages；支持自定义域名与 HTTPS。发布站点不得大于 1 GB；每月 100 GB 是软带宽限制。自定义 Actions 发布不受每小时 10 次构建软限制影响。[GitHub Pages 限制](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)、[HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https) | 最少改动：继续现有 workflow，Cloudflare 只管理 DNS。若记录设为 DNS-only，访问直接到 GitHub Pages；若设 Proxied，才经过 Cloudflare 代理。GitHub 文档要求 apex 指向 GitHub Pages 的地址、子域 CNAME 指向 `wenbo97.github.io`。Cloudflare 仅代理提供 HTTP/HTTPS 的 A/AAAA/CNAME 记录；代理会改变公开 DNS 应答。官方文档没有确认 Cloudflare 代理与 GitHub Pages 自定义域名验证、证书续期组合的保证，因此优先 DNS-only，任何橙云方案都应先实测域名验证及源站 HTTPS。[GitHub DNS 配置](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)、[Cloudflare 代理资格与状态](https://developers.cloudflare.com/dns/proxy-status/limitations/)、[代理状态](https://developers.cloudflare.com/dns/proxy-status/) |
| Cloudflare 托管 | Cloudflare 目前建议新静态站使用 Workers Static Assets。静态资产请求免费且不限量；Free 限每 Worker 版本 20,000 个文件、单文件 25 MiB。每天 100,000 次额度针对实际执行 Worker 代码的请求，不是静态资源总请求数。Workers Builds 免费额度为每月 3,000 build-minutes、同时一个 build、单次最长 20 分钟。[Workers 建议](https://developers.cloudflare.com/workers/best-practices/workers-best-practices/)、[静态资产计费](https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/)、[限制](https://developers.cloudflare.com/workers/platform/limits/)、[Builds 额度](https://developers.cloudflare.com/workers/ci-cd/builds/limits-and-pricing/) | 本地产物明显低于文件数与最大文件限制。用 GitHub Actions 跑现有 Ruby 3.3 验证/构建，再以 Wrangler 发布 `_site` 为静态资产，可复用已验证的构建环境；需要在 GitHub Actions 配置 Cloudflare Account ID（可用普通变量）和 API Token（secret）。Workers 也有 GitHub Builds 集成和 PR 预览，但复用现有 Actions 更容易保持当前验证门禁。[Cloudflare GitHub Actions](https://developers.cloudflare.com/workers/ci-cd/external-cicd/github-actions/)、[Workers Builds GitHub 集成](https://developers.cloudflare.com/workers/ci-cd/builds/git-integration/github-integration/) |

Cloudflare Pages 仍可用，且 Jekyll 官方指南给出 `jekyll build` 与 `_site`，Git 集成支持 push 自动构建以及分支/PR 预览。当前 Pages Free 是每月 500 builds、每站 20,000 个文件、单文件 25 MiB、每项目 100 个自定义域名；当前 build image v3 默认 Ruby 3.4.4，但可用 `RUBY_VERSION` 或 `.ruby-version` 指定项目版本，因此本仓库可设为 3.3。Pages 的静态请求同样免费且不限量。[Jekyll](https://developers.cloudflare.com/pages/framework-guides/deploy-a-jekyll-site/)、[build image](https://developers.cloudflare.com/pages/configuration/build-image/)、[Pages 限制](https://developers.cloudflare.com/pages/platform/limits/)、[Git 集成](https://developers.cloudflare.com/pages/configuration/git-integration/)、[静态请求计费](https://developers.cloudflare.com/pages/functions/pricing/)。

另一个可行折衷是 Cloudflare Pages Git 集成：它直接支持 Jekyll 和 PR 预览，配置比 Workers Static Assets 少；只是 Cloudflare 当前将 Workers 作为新静态站推荐路线。选 Pages 时务必显式指定 `RUBY_VERSION=3.3`，避免依赖 build image 默认值。该选项的免费静态流量边界与 Workers 静态资产相同。

## 旧 URL 与建议

GitHub 文档明确说明的自动重定向是自定义域名 apex 与 `www` 之间的跳转；文档没有承诺从 `wenbo97.github.io/prompt-context-patterns/...` 到 `https://patternnotes.dev/...` 的旧项目路径迁移会保留深链接、查询参数和片段。Cloudflare 对新域名配置的规则无法接收发往 `github.io` 主机名的请求。即使新域名用 Workers Static Assets，`_redirects` 也不支持按查询参数匹配；片段不会发送到服务器。项目已有约 412 条双语旧方法映射；即使每条各用一条静态规则，也低于 `_redirects` 的 2,000 条静态规则上限，但仍不能拦截旧 `github.io` 主机名。上线前必须逐类实测旧深链接、query、anchor，并决定 GitHub Pages 旧入口如何保留。[GitHub 自定义域名说明](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages)、[Workers redirects](https://developers.cloudflare.com/workers/static-assets/redirects/)。

**建议：**若目标是让 `https://patternnotes.dev/` 真正由 Cloudflare 托管并使用其代理，选 Workers Static Assets + 现有 GitHub Actions Ruby 3.3 构建/验证，再用 Wrangler 发布。若优先最少改动，继续 GitHub Pages、Cloudflare 只管 DNS，并先用 DNS-only；这条路线不会让站点流量经过 Cloudflare 代理。两条路线都不能只改 DNS：根域意味着 `baseurl` 需为空，并要同步调整 URL 测试、旧路由和大量固定域名的 E2E 检查；目标正式地址定为 `https://patternnotes.dev/` 时，可另将 `www` 301 到根域。以上是根据现有仓库工作流、域名状态和官方边界作出的选型推断，不代表已实施或验证上线。
