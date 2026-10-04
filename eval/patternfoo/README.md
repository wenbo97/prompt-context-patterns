# Patternfoo

Select active catalog methods with runnable evaluation cases. The directory comes from canonical metadata rather than a fixed155-item list. Each case has a case_id and explicit pattern_ids; historic008/017 folder names are not catalog identities.

## Setup

Run npm install --legacy-peer-deps --omit=peer in this directory for the TUI and static tests. Install a compatible promptfoo CLI explicitly before a model experiment. Configure provider, judge and endpoint in the TUI; configuration stays in ~/.patternfoo/config.json.

```bash
npm test
npm run build
npm start
```

Selecting several methods runs each matched case once. Each case has its own A/B pair, scenarios, rubric and result directory; cases are not cross-multiplied. Provider calls are opt-in and are not part of static blog checks.

## Add a case

Create patterns/<case-id>/ containing meta.yaml, prompt-a.md, prompt-b.md, scenarios.yaml and rubric.md. Metadata requires case_id, nonempty pattern_ids, name, category, hypothesis and status ready|todo. Identifiers use letters, digits and hyphens. Link active canonical methods; resolve merged identities during migration.

Examples are not guaranteed winners. Preserve raw outputs and configuration before reporting measured results. Promptfoo exit100 denotes failed assertions, so results remain available; invocation failures are reported separately.

[Promptfoo CLI documentation](https://www.promptfoo.dev/docs/usage/command-line/) describes repeats, cache behavior and evaluation failure codes.
