---
layout: default
title: Construct a useful bad/good pair
permalink: /guides/teaching-examples/
alternate_url: /guides/teaching-examples-zh/
lang: en
---
# Construct a useful bad/good pair

Use one task and the same known facts. Show a failure-producing instruction, then change the instruction that addresses that failure. Explain what to inspect and where the method stops applying.

## Example

Task: classify a support message for a downstream consumer that accepts four categories.

Bad: `Classify the message and explain your answer.`

Good: `Return JSON with category in billing|technical|feedback|other and a short reason. If the message lacks enough information, use other and identify the missing fact.`

Expected: parse the JSON and validate category membership. This checks the output contract; it does not establish semantic classification accuracy. Evaluate accuracy with representative labelled requests separately.

[Output contracts]({{ '/catalog/patterns/14/' | relative_url }}) · [Editorial criteria]({{ '/methodology/' | relative_url }})
