# Windows continuation recovery

## Restored checkpoint

Continuation starts from `9feafa7c3631859f4a08ecbd942fe9f6e6f9f9fb` on local branch `rebuild/skills-catalog`, in the isolated worktree `D:/A_Projects/prompt-context-patterns-refresh`. The original project stays on `master`; its uncommitted contributor guide is preserved. The complete rebuild review baseline remains `9456091c44d796918745eaecad9d1ee9e726b244`.

The ten evidence repositories were recovered at the immutable commits recorded in `source-inventory.json`, under `D:/A_Projects/open-skills`. Verification read Git trees and blobs: all 9,806 path/mode/object identities and normalized-content hashes matched. Existing evidence repositories are never reset by the restoration command. They remain clean; their skills, tests, installers, and model calls are not executed.

Private reading caches from the other device were unavailable. Researchers reconstruct them from frozen Git blobs, retain persisted read statuses, and record additional reads only after inspecting actual bounded output. Historical helper scripts are evidence and must not overwrite later conclusions merely because they can run.

## Dependency migration and baseline

Tools: Node 24.18.0, npm 11.12.1, Python 3.13.15, Ruby 3.3.11, Bundler 2.5.22. Ruby gems live in ignored `vendor/bundle`; research caches live in ignored `.tools`.

The root npm lockfile referenced a private corporate registry, causing HTTP 401. Its five package versions were preserved, while tarball URLs and integrity values were resolved from the public npm registry. Root `npm ci` then succeeded. Patternfoo's lockfile installed without changes; npm reported eight pre-existing dependency advisories. The offline checks do not exercise provider-backed evaluations, and no force dependency upgrade was applied.

Observed staging baseline after recovery and source-verification tests:

- Root: 16 passing Node tests; Patternfoo: 11 passing Vitest tests and TypeScript compilation.
- Jekyll build succeeded; five Liquid literal roundtrips passed.
- 508 rendered pages / 12,353 internal href checks / zero failures.
- Nine Playwright tests passed, including Axe checks at 375, 768 and 1280 CSS pixels, locale/Back restoration, retry, IME and no-JavaScript routes.
- Generated outputs were deterministic; 122 legacy-staging methods remained active. The staging source-range check read 35 source files with zero errors.
- Strict premium static audit found zero findings. Static audit is separate from browser verification.

These are local staging results, not final integrated validation or remote CI results. Final delivery must rerun strict coverage and source checks without `--allow-pending`, followed by the integrated site checks and the independent review round.
