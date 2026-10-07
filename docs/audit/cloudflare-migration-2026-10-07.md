# Cloudflare migration preparation

Date: 2026-10-07. Target: `https://patternnotes.dev/`. Baseline: `ff0125d3698c4e86a4ec320011a4b3a345cd387b` on the accepted remote master. Current branch: `migration/cloudflare-patternnotes`.

## Agreed scope and current delivery

The user chose the Cloudflare free static-hosting route and requested a beginner-friendly, one-step-at-a-time migration for mainland and overseas readers. The repository and Ruby 3.3 GitHub Actions build remain on GitHub. The user has configured the temporary publication credentials in GitHub; the agent prepares and verifies the code before asking to publish it. This document covers preparation, not a completed domain cutover.

Required behavior for this preparation:

- A separate Cloudflare override builds the existing bilingual site at the new domain root. The original GitHub Pages origin, project prefix and deployment workflow remain usable.
- Keep the catalog, search/filter/history state, no-JavaScript entry points, bilingual metadata and historical routes/anchors working at both deployment prefixes. Frozen old URL evidence is preserved rather than rewritten.
- Reuse the existing complete verification workflow and publish its exact checked artifact. Initial Cloudflare publication is explicitly dispatched; do not enable automatic production publication before acceptance.
- Use Workers Static Assets without authored Worker code or an API backend. Include Cloudflare's static redirect/header policies. Old project prefixes on the new host redirect to root paths while preserving query parameters; the real old `github.io` hostname still needs its own migration.
- The Cloudflare variant omits Google Fonts requests and uses the existing system-font fallbacks. Do not redesign the UI. Prevent the temporary workers.dev host from becoming a second indexed site.
- Keep tokens in GitHub Secrets and never put values in source, logs or documents. After initial creation, replace the seven-day bootstrap token with a token scoped to updating this Worker.
- Public access quality from mainland and overseas networks is verified only after a real deployment; local success and free global caching do not establish mainland network performance.

## Prepared implementation

`_config.cloudflare.yml` overrides the origin and empty prefix, writes the Cloudflare artifact to `.tools/cloudflare-site`, and writes new inspection reports to `.tools/cloudflare-audit`. It includes `_headers` and `_redirects`; normal GitHub Pages builds do not publish these files. `wrangler.jsonc` defines the static project `patternnotes-blog`, trailing-slash HTML routes and 404 handling. The custom domain is intentionally not bound by this first deployment configuration.

The shared site-config reader parses YAML and supports the same ordered override files as the build. Rendered-link/site checks, sitemap-date verification and Playwright use these deployment settings rather than fixed old URLs. Original archived URL/anchor records remain unchanged. Cloudflare preview tests use a dedicated local port and cannot silently reuse an unrelated existing server.

`Deploy blog to Cloudflare` is a manual GitHub Actions workflow. Its reusable verification job runs Node/Ruby/catalog/source/Patternfoo/browser checks against the Cloudflare build and uploads that verified artifact. The publication job downloads it and uses the official Cloudflare action with Wrangler 4.148.0. It reads `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` from GitHub Secrets. Secret-name existence was verified; the secret values are neither accessible to the local agent nor authenticated by a local test.

## Local verification

- Node regression tests: 28 passed, including ordered deployment overrides, empty YAML baseurl handling, and frozen old-route mapping at a domain root.
- Cloudflare build: 876 HTML pages, 655 indexable pages and 221 noindex compatibility pages; 21,948 rendered links and 412 legacy method mappings checked with zero errors. The 1,410 legacy heading-owner mappings also pass.
- Cloudflare browser suite: 34 passed, including search/filter/history, both languages, data failure/retry, IME event behavior, keyboard/reflow, native anchors, no JavaScript and Axe accessibility at 375/768/1280 CSS pixels. This does not claim hardware IME or browser-menu zoom testing.
- The first browser attempt reached an old local review page on port 4100. The dedicated port was changed to 4173 and the complete suite then passed; the unrelated review server was preserved.
- 612 authored sitemap dates stayed stable across two artificial build times. Five Liquid literal roundtrips passed. Catalog, pinned-source and generated-output checks passed; Patternfoo passed 11 tests and TypeScript compilation.
- Wrangler 4.148.0 dry-run accepted the asset-only configuration. Local Wrangler serving verified 200 for the bilingual entry points and robots, a trailing-slash redirect, old-prefix 301 redirects with query preservation, and 404 for absent routes. A raw Host-header request verified `X-Robots-Tag: noindex` on the workers.dev pattern.
- Local Chinese homepage screenshots at 375/1280px were inspected. Homepage and catalog browsing made zero external resource requests and loaded 30 search results.
- The strict premium static audit reports zero findings. Legacy GitHub Pages build and its 21,948 rendered-link checks passed. Four legacy browser smoke tests passed: search/filter/history, data failure/retry, no-JavaScript legacy entry and localized category/source navigation.
- Independent review: Standards found no hard standards/deployment-wiring defects; Spec found no actionable missing, partial or incorrect preparation behavior. Standards noted one non-blocking maintenance heuristic: the ordered override filename list is declared in YAML, package commands and the Node launcher. Those declarations currently agree; an extra abstraction was not added solely for a hypothetical filename change.

Local machine-readable/browser/routing/static evidence and screenshots are under `.tools/cloudflare-audit`. This ignored directory is not published. Baseline acceptance reports under `docs/audit` are preserved.

## Operator steps after publication approval

1. Commit and publish the prepared change through the repository's normal Git workflow, then manually dispatch `Deploy blog to Cloudflare`. Verify the Cloudflare credential authorization in that real workflow and save its public run URL.
2. Open the returned workers.dev URL; check the homepage, Chinese content, catalog search, old-prefix redirects and the preview noindex header. The official domain is still not connected at this point.
3. In Cloudflare, open Workers & Pages > `patternnotes-blog` > Settings > Domains & Routes > Add > Custom Domain, and bind `patternnotes.dev`. Cloudflare manages the DNS record and certificate. Verify live HTTPS, root robots/sitemap, canonical/hreflang and direct deep links.
4. Configure a proxied `www` record and a www-to-apex 301 rule preserving path and query. Test mainland access without a proxy on broadband and mobile networks, plus actual overseas access.
5. Arrange and test the GitHub-side old-host migration before retiring its current publication. Cloudflare rules cannot intercept requests to `wenbo97.github.io`; do not claim an old-host HTTP 301 until observed.
6. Replace the bootstrap token with a scoped Workers Editor token (and only necessary domain-route permissions), save it under the same GitHub secret name, then revoke the bootstrap token. Enable master-triggered Cloudflare publication only after the new site is accepted.
7. Verify the new search-engine properties and sitemap status separately from deployment success. Do not report sitemap submission as indexing.

## Sources and limits

[Hosting comparison and public DNS observations](hosting-options-2026-10-07.md) contains the initial source-based decision. Current permission roles are documented in [Workers roles and permissions](https://developers.cloudflare.com/workers/authorization/workers/): creation needs product-level Admin; subsequent updates can use Editor scoped to an existing Worker. [Static asset billing](https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/), [GitHub Actions publication](https://developers.cloudflare.com/workers/ci-cd/external-cicd/github-actions/), [custom domains](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/), [redirects](https://developers.cloudflare.com/workers/static-assets/redirects/) and [preview headers](https://developers.cloudflare.com/workers/static-assets/headers/) describe the service behavior. [Cloudflare China Network](https://developers.cloudflare.com/china-network/) is a separate Enterprise subscription, not the free deployment's mainland CDN.

At this preparation stage no Cloudflare project has been created remotely, no DNS record has been changed, and no repository change has been pushed. Actual credential authorization, public-site network performance and the old-host/domain/search cutover remain to be verified during subsequent guided steps.
