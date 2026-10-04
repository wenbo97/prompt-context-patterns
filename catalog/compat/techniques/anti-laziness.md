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
<li id="1-background-how-claude-code-skills-work" data-target="{{ '/catalog/patterns/1/' | relative_url }}"><a href="{{ '/catalog/patterns/1/' | relative_url }}">1-background-how-claude-code-skills-work → YAML Frontmatter Metadata</a></li>
<li id="tier-1--metadata-pre-load-100-tokens-per-skill" data-target="{{ '/catalog/patterns/1/' | relative_url }}"><a href="{{ '/catalog/patterns/1/' | relative_url }}">tier-1--metadata-pre-load-100-tokens-per-skill → YAML Frontmatter Metadata</a></li>
<li id="tier-2--skillmd-full-body-loaded-on-trigger" data-target="{{ '/catalog/patterns/1/' | relative_url }}"><a href="{{ '/catalog/patterns/1/' | relative_url }}">tier-2--skillmd-full-body-loaded-on-trigger → YAML Frontmatter Metadata</a></li>
<li id="tier-3--bundled-files-loaded-on-demand-by-the-model" data-target="{{ '/catalog/patterns/1/' | relative_url }}"><a href="{{ '/catalog/patterns/1/' | relative_url }}">tier-3--bundled-files-loaded-on-demand-by-the-model → YAML Frontmatter Metadata</a></li>
<li id="2-why-agents-skip-reference-reads-root-cause-analysis" data-target="{{ '/catalog/patterns/2/' | relative_url }}"><a href="{{ '/catalog/patterns/2/' | relative_url }}">2-why-agents-skip-reference-reads-root-cause-analysis → Phased/Stepped Execution</a></li>
<li id="3-strategies--with-good-and-bad-examples" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">3-strategies--with-good-and-bad-examples → Workflow Mode Branching</a></li>
<li id="strategy-1--imperative-framing-not-see-also" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">strategy-1--imperative-framing-not-see-also → Workflow Mode Branching</a></li>
<li id="-bad" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">-bad → Workflow Mode Branching</a></li>
<li id="-good" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">-good → Workflow Mode Branching</a></li>
<li id="strategy-2--make-the-read-itself-a-numbered-step" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">strategy-2--make-the-read-itself-a-numbered-step → Workflow Mode Branching</a></li>
<li id="-bad-1" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">-bad-1 → Workflow Mode Branching</a></li>
<li id="-good-1" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">-good-1 → Workflow Mode Branching</a></li>
<li id="strategy-3--inline-anchor--reference-for-depth" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">strategy-3--inline-anchor--reference-for-depth → Workflow Mode Branching</a></li>
<li id="-bad--pure-reference-no-anchor" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">-bad--pure-reference-no-anchor → Workflow Mode Branching</a></li>
<li id="-bad--full-inline-defeats-the-refactor" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">-bad--full-inline-defeats-the-refactor → Workflow Mode Branching</a></li>
<li id="-good--anchor--reference" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">-good--anchor--reference → Workflow Mode Branching</a></li>
<li id="strategy-4--tier-inline-vs-reference-by-risk-the-most-important-principle" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">strategy-4--tier-inline-vs-reference-by-risk-the-most-important-principle → Workflow Mode Branching</a></li>
<li id="strategy-5--replace-prompt-with-deterministic-code" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">strategy-5--replace-prompt-with-deterministic-code → Workflow Mode Branching</a></li>
<li id="-bad-2" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">-bad-2 → Workflow Mode Branching</a></li>
<li id="-good-2" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">-good-2 → Workflow Mode Branching</a></li>
<li id="strategy-6--validation-loop--self-check" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">strategy-6--validation-loop--self-check → Workflow Mode Branching</a></li>
<li id="-good-3" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">-good-3 → Workflow Mode Branching</a></li>
<li id="strategy-7--sub-agent-isolation-strongest" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">strategy-7--sub-agent-isolation-strongest → Workflow Mode Branching</a></li>
<li id="-bad-3" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">-bad-3 → Workflow Mode Branching</a></li>
<li id="-good-4" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">-good-4 → Workflow Mode Branching</a></li>
<li id="strategy-8--empirically-test-dont-reason-about-it" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">strategy-8--empirically-test-dont-reason-about-it → Workflow Mode Branching</a></li>
<li id="-bad-4" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">-bad-4 → Workflow Mode Branching</a></li>
<li id="-good-5" data-target="{{ '/catalog/patterns/3/' | relative_url }}"><a href="{{ '/catalog/patterns/3/' | relative_url }}">-good-5 → Workflow Mode Branching</a></li>
<li id="4-decision-framework" data-target="{{ '/catalog/patterns/4/' | relative_url }}"><a href="{{ '/catalog/patterns/4/' | relative_url }}">4-decision-framework → $ARGUMENTS Variable</a></li>
<li id="5-conclusions" data-target="{{ '/catalog/patterns/5/' | relative_url }}"><a href="{{ '/catalog/patterns/5/' | relative_url }}">5-conclusions → Persona/Role Assignment</a></li>
<li id="appendix-quick-reference-checklist-for-each-refactor-pr" data-target="{{ '/catalog/patterns/5/' | relative_url }}"><a href="{{ '/catalog/patterns/5/' | relative_url }}">appendix-quick-reference-checklist-for-each-refactor-pr → Persona/Role Assignment</a></li>
</ul></div>
<script src="{{ '/assets/compat.js' | relative_url }}"></script>
