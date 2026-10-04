---
layout: post
title: "Prompt engineering: observable instructions and useful contrasts"
date: 2026-04-19
categories: [prompt-engineering, patterns]
lang: en
last_modified_at: 2026-10-03
---

<span id="core-principle-reduce-conditional-entropy"></span>
<span id="what-conditional-entropy-actually-means"></span>
<span id="concrete-example"></span>
<span id="feel-it-in-numbers"></span>
<span id="why-indentation-is-information"></span>
<span id="one-line-summary"></span>
<span id="1-visual-decision-trees-over-prose"></span>
<span id="why-it-works"></span>
<span id="bad-prose"></span>
<span id="good-decision-tree"></span>
<span id="why-indentation-matters"></span>
<span id="2-grounding-anchoring"></span>
<span id="bad-unanchored"></span>
<span id="good-anchored-with-template"></span>
<span id="3-cognitive-offloading"></span>
<span id="bad-implicit-reasoning-required"></span>
<span id="good-explicit-steps-provided"></span>
<span id="4-attention-locality"></span>
<span id="bad-rule-far-from-its-target"></span>
<span id="good-rule-adjacent-to-its-target"></span>
<span id="5-token-action-binding"></span>
<span id="bad-multiple-implicit-actions-in-one-sentence"></span>
<span id="good-one-instruction--one-action"></span>
<span id="6-schema-priming"></span>
<span id="bad-open-ended"></span>
<span id="good-schema-constrained"></span>
<span id="7-negative-space-explicit-alternatives"></span>
<span id="bad-negation-only"></span>
<span id="good-negation--alternative-path"></span>
<span id="8-xml-tags-for-semantic-boundaries"></span>
<span id="recommended-structure-for-skill-prompts"></span>
<span id="9-few-shot-with-embedded-reasoning"></span>
<span id="bad-inputoutput-pairs-only"></span>
<span id="good-input--thinking--output"></span>
<span id="putting-it-all-together-skill-prompt-template"></span>
<span id="summary-of-relationships"></span>
<span id="references"></span>

## Historical revision

The original 2026-04-19 article explained prompt structure through conditional entropy and attention. This repository does not contain measurements linking its suggested wording to those internal model quantities. The revision keeps practical methods and removes unsupported causal guarantees.

## Start with the task and known facts

Specify the input, required outcome and what is not known. For a configuration diagnosis, identify the loader, config path and observed symptom before asking for a change.

## Make the contract inspectable

Replace “report clearly” with required fields and allowed values. Include a missing-input or unknown branch. A format validator checks the contract, not the truth of the answer.

## Use a same-task contrast

Keep task and facts constant. Change the instruction responsible for one concrete failure, explain the expected difference, and state the boundary. Examples here are teaching constructions, not measured model outputs.

## Route context by need

Put always-needed constraints near the action. Attach an explicit reading condition to task-specific references. Preserve a source location instead of treating a memory or summary as current proof.

[Teaching-example guide]({{ '/guides/teaching-examples/' | relative_url }}) · [Reference-reading guide]({{ '/guides/reference-reading/' | relative_url }}) · [Editorial criteria]({{ '/methodology/' | relative_url }})
