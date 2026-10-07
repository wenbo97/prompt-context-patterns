# 提示词与上下文工程参考

从公开技能中提炼可复用的方法。每篇说明使用场景、操作步骤、同任务正反例、检查方法、适用边界与原文状态。

当前目录：**306** 个有效方法；**272** 个可查看原文实例；**34** 个带来源未确认标签。合并和撤下条目保留兼容入口，不计入有效数量。

[English](README.md)

## 本地预览

需要 Node20+、Ruby3.3 与 Bundler。

```bash
npm ci
bundle install
npm run generate
bundle exec jekyll serve --host 127.0.0.1 --port 4000
```

本机隔离版本可运行 `scripts/preview.ps1`，它会使用本地安装的 Ruby。预览地址：http://127.0.0.1:4000/prompt-context-patterns/ 。

## 内容与证据

- [_data/patterns.json](_data/patterns.json)：权威目录与编辑结论。
- [_patterns/](_patterns/)：独立双语正文。
- [审核标准](methodology/index-zh.md)：质量与追溯分别评估。
- [旧内容审核](docs/audit/legacy-review.md)：保留、合并与撤下理由。
- [来源研究](docs/research/open-source-skills-top10.md)：仓库及固定版本入口。

固定 commit 链接证明公开实例，不证明最早发明者。本站教学例独立构造，不冒充实际模型输出。历史文章保留日期与样例，缺少原始输出的数字已校正。

## 验证与维护

来源默认位于项目旁的 `open-skills/<owner>/<repo>`；可通过 `SKILLS_ROOT` 指定其他目录。恢复命令仅下载清单中的固定提交；已有目录必须通过校验，不会被重置。

```bash
npm run sources:restore
npm test
npm run check
npm run check:sources
npm run check:generated
bundle exec ruby tests/liquid-literals.rb
bundle exec jekyll build
npm run check:links
npm run check:site
npm run check:dates
npm run test:e2e
npm --prefix eval/patternfoo ci --legacy-peer-deps --omit=peer
npm --prefix eval/patternfoo test
npm --prefix eval/patternfoo run build
```

构建检查不调用模型。真实 A/B 评测通过 [Patternfoo](eval/patternfoo/README.md) 显式运行。旧评测脚本留作历史样例；原始输出缺失时不宣称实验已复核。所有文本采用 CRLF。

正文的 last_modified_at 使用实际内容修改日期（Asia/Shanghai，YYYY-MM-DD）。修改对应语言的标题、摘要或正文时同步维护；正常生成和构建不自动刷新日期。普通页面的摘要写在正文元信息或对应生成输入中。

## 许可证

本站采用 MIT。来源仓库的具体文件各自保留授权范围；引用不把整个来源仓库自动视为同一种许可证。
