export function readmeOutputs(stats) {
  const files = {};
  for (const lang of ['en', 'zh']) {
    const zh = lang === 'zh';
    const heading = zh ? '提示词与上下文工程参考' : 'Prompt and Context Engineering Reference';
    const intro = zh ? '从公开技能中提炼可复用的方法。每篇说明使用场景、操作步骤、同任务正反例、检查方法、适用边界与原文状态。' :
      'Reusable methods extracted from real agent skills. Every active pattern has a concise description, concrete use case, same-task bad/good examples, observable expectations, limits and provenance.';
    const counts = zh ? `当前目录：**${stats.active}** 个有效方法；**${stats.traced}** 个可查看原文实例；**${stats.untraced}** 个带来源未确认标签。合并和撤下条目保留兼容入口，不计入有效数量。` :
      `Current directory: **${stats.active}** active methods, **${stats.traced}** with located source instances, **${stats.untraced}** labelled Source unconfirmed. Merged and withdrawn identities remain reachable and are not counted as active.`;
    const doc = `# ${heading}\n\n${intro}\n\n${counts}\n\n` +
      (zh ? '[English](README.md)\n\n' : '[中文](README-zh.md)\n\n') +
      (zh ? '## 本地预览\n\n需要 Node20+、Ruby3.3 与 Bundler。\n\n' : '## Local preview\n\nRequires Node20+, Ruby3.3 and Bundler.\n\n') +
      '```bash\nnpm ci\nbundle install\nnpm run generate\nbundle exec jekyll serve --host 127.0.0.1 --port 4000\n```\n\n' +
      (zh ? '本机隔离版本可运行 `scripts/preview.ps1`，它会使用本地安装的 Ruby。预览地址：http://127.0.0.1:4000/prompt-context-patterns/ 。\n\n' : 'The isolated Windows copy can use `scripts/preview.ps1` with its local Ruby installation. Preview: http://127.0.0.1:4000/prompt-context-patterns/ .\n\n') +
      (zh ? '## 内容与证据\n\n' : '## Content and evidence\n\n') +
      (zh ? '- [_data/patterns.json](_data/patterns.json)：权威目录与编辑结论。\n- [_patterns/](_patterns/)：独立双语正文。\n- [审核标准](methodology/index-zh.md)：质量与追溯分别评估。\n- [旧内容审核](docs/audit/legacy-review.md)：保留、合并与撤下理由。\n- [来源研究](docs/research/open-source-skills-top10.md)：仓库及固定版本入口。\n\n' :
        '- [_data/patterns.json](_data/patterns.json): authoritative metadata and editorial dispositions.\n- [_patterns/](_patterns/): independent bilingual bodies.\n- [Editorial criteria](methodology/index.md): usefulness and provenance are separate.\n- [Legacy audit](docs/audit/legacy-review.md): retention, merge and withdrawal reasons.\n- [Source research](docs/research/open-source-skills-top10.md): repositories and frozen revisions.\n\n') +
      (zh ? '固定 commit 链接证明公开实例，不证明最早发明者。本站教学例独立构造，不冒充实际模型输出。历史文章保留日期与样例，缺少原始输出的数字已校正。\n\n' :
        'Pinned commit links establish observed instances, not earliest invention. Teaching examples are independently constructed, not measured model outputs. Historical articles retain dates and fixtures; unsupported numbers without raw outputs are corrected.\n\n') +
      (zh ? '## 验证与维护\n\n' : '## Verification and maintenance\n\n') +
      (zh ? '来源默认位于项目旁的 `open-skills/<owner>/<repo>`；可通过 `SKILLS_ROOT` 指定其他目录。恢复命令仅下载清单中的固定提交；已有目录必须通过校验，不会被重置。\n\n' :
        'Sources default to the adjacent `open-skills/<owner>/<repo>` directory; override with `SKILLS_ROOT`. Restoration fetches only frozen commits. Existing directories must pass verification and are never reset.\n\n') +
      '```bash\nnpm run sources:restore\nnpm test\nnpm run check\nnpm run check:sources\nnpm run check:generated\nbundle exec ruby tests/liquid-literals.rb\nbundle exec jekyll build\nnpm run check:links\nnpm run check:site\nnpm run check:dates\nnpm run test:e2e\nnpm --prefix eval/patternfoo ci --legacy-peer-deps --omit=peer\nnpm --prefix eval/patternfoo test\nnpm --prefix eval/patternfoo run build\n```\n\n' +
      (zh ? '构建检查不调用模型。真实 A/B 评测通过 [Patternfoo](eval/patternfoo/README.md) 显式运行。旧评测脚本留作历史样例；原始输出缺失时不宣称实验已复核。所有文本采用 CRLF。\n\n' :
        'Build checks do not call models. Real A/B evaluations run explicitly through [Patternfoo](eval/patternfoo/README.md). Legacy runners retain historical fixtures; missing raw outputs are not represented as revalidated results. Text files use CRLF.\n\n') +
      (zh ? '正文的 last_modified_at 使用实际内容修改日期（Asia/Shanghai，YYYY-MM-DD）。修改对应语言的标题、摘要或正文时同步维护；正常生成和构建不自动刷新日期。普通页面的摘要写在正文元信息或对应生成输入中。\n\n' : 'Authored last_modified_at records the actual content update date (Asia/Shanghai, YYYY-MM-DD). Update it with relevant title, summary or body changes; generation and builds never refresh it automatically. Ordinary descriptions belong to authored front matter or generator inputs.\n\n') +
      (zh ? '## 许可证\n\n本站采用 MIT。来源仓库的具体文件各自保留授权范围；引用不把整个来源仓库自动视为同一种许可证。\n' :
        '## License\n\nThis project uses MIT. Referenced files retain their own licensing scope; citations do not assign one license to an entire source corpus.\n');
    files[zh ? 'README-zh.md' : 'README.md'] = doc;
    files[`catalog/README${zh ? '-zh' : ''}.md`] = `# ${heading}\n\n${counts}\n\n` +
      (zh ? '[完整目录](catalog-index-zh.md) · [中英文独立正文](../_patterns/) · [编辑标准](../methodology/index-zh.md) · [来源记录](../docs/research/open-source-skills-top10.md)\n' :
        '[Full index](catalog-index.md) · [Bilingual bodies](../_patterns/) · [Editorial criteria](../methodology/index.md) · [Source records](../docs/research/open-source-skills-top10.md)\n');
  }
  return files;
}
