---
layout: "default"
lang: "en"
title: "Content migration entry"
permalink: "/catalog/techniques/anti-laziness/"
sitemap: false
robots: "noindex,follow"
canonical_url: "/catalog/"
---

<div data-compat><h1>Content has moved</h1><p>Old addresses and sections still resolve. Follow a link to the reviewed content.</p><ul class="compat-list">
<li id="preventing-agent-laziness-in-skill-references" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">preventing-agent-laziness-in-skill-references → Current catalog</a></li>
<li id="1-background-how-claude-code-skills-work" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">1-background-how-claude-code-skills-work → Current catalog</a></li>
<li id="tier-1--metadata-pre-load-100-tokens-per-skill" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">tier-1--metadata-pre-load-100-tokens-per-skill → Current catalog</a></li>
<li id="tier-2--skillmd-full-body-loaded-on-trigger" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">tier-2--skillmd-full-body-loaded-on-trigger → Current catalog</a></li>
<li id="tier-3--bundled-files-loaded-on-demand-by-the-model" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">tier-3--bundled-files-loaded-on-demand-by-the-model → Current catalog</a></li>
<li id="2-why-agents-skip-reference-reads-root-cause-analysis" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">2-why-agents-skip-reference-reads-root-cause-analysis → Current catalog</a></li>
<li id="3-strategies--with-good-and-bad-examples" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">3-strategies--with-good-and-bad-examples → Current catalog</a></li>
<li id="strategy-1--imperative-framing-not-see-also" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">strategy-1--imperative-framing-not-see-also → Current catalog</a></li>
<li id="-bad" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">-bad → Current catalog</a></li>
<li id="-good" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">-good → Current catalog</a></li>
<li id="strategy-2--make-the-read-itself-a-numbered-step" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">strategy-2--make-the-read-itself-a-numbered-step → Current catalog</a></li>
<li id="-bad-1" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">-bad-1 → Current catalog</a></li>
<li id="-good-1" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">-good-1 → Current catalog</a></li>
<li id="strategy-3--inline-anchor--reference-for-depth" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">strategy-3--inline-anchor--reference-for-depth → Current catalog</a></li>
<li id="-bad--pure-reference-no-anchor" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">-bad--pure-reference-no-anchor → Current catalog</a></li>
<li id="-bad--full-inline-defeats-the-refactor" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">-bad--full-inline-defeats-the-refactor → Current catalog</a></li>
<li id="-good--anchor--reference" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">-good--anchor--reference → Current catalog</a></li>
<li id="strategy-4--tier-inline-vs-reference-by-risk-the-most-important-principle" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">strategy-4--tier-inline-vs-reference-by-risk-the-most-important-principle → Current catalog</a></li>
<li id="strategy-5--replace-prompt-with-deterministic-code" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">strategy-5--replace-prompt-with-deterministic-code → Current catalog</a></li>
<li id="-bad-2" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">-bad-2 → Current catalog</a></li>
<li id="-good-2" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">-good-2 → Current catalog</a></li>
<li id="strategy-6--validation-loop--self-check" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">strategy-6--validation-loop--self-check → Current catalog</a></li>
<li id="-good-3" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">-good-3 → Current catalog</a></li>
<li id="strategy-7--sub-agent-isolation-strongest" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">strategy-7--sub-agent-isolation-strongest → Current catalog</a></li>
<li id="-bad-3" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">-bad-3 → Current catalog</a></li>
<li id="-good-4" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">-good-4 → Current catalog</a></li>
<li id="strategy-8--empirically-test-dont-reason-about-it" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">strategy-8--empirically-test-dont-reason-about-it → Current catalog</a></li>
<li id="-bad-4" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">-bad-4 → Current catalog</a></li>
<li id="-good-5" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">-good-5 → Current catalog</a></li>
<li id="4-decision-framework" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">4-decision-framework → Current catalog</a></li>
<li id="5-conclusions" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">5-conclusions → Current catalog</a></li>
<li id="appendix-quick-reference-checklist-for-each-refactor-pr" data-target="{{ '/guides/reference-reading/' | relative_url }}"><a href="{{ '/guides/reference-reading/' | relative_url }}">appendix-quick-reference-checklist-for-each-refactor-pr → Current catalog</a></li>
</ul></div>
<script src="{{ '/assets/compat.js' | relative_url }}"></script>
