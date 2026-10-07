---
layout: default
title: Make reference reading observable
permalink: /guides/reference-reading/
alternate_url: /guides/reference-reading-zh/
lang: en
description: "Make task-specific reference reading observable through explicit triggers, file locations, evidence and missing-input handling."
last_modified_at: 2026-10-06
---
# Make reference reading observable

Use this when an agent acts without reading the task-specific rules. Diagnose the missing read from the actual trace; do not assume a motive such as laziness.

## Same-task teaching comparison

Bad: `Follow our deployment guidance.`

Good: `Before proposing a production deployment, read deployment-rules.md. Report the approval requirement and rollback condition, with their section locations. If the file is absent, stop and report the missing input.`

The improved instruction states the trigger, the file, required evidence and missing-input behavior. It creates an inspectable read obligation; it does not guarantee that a model will comply.

## Keep only the necessary context

Keep rules needed by every branch near the action. Route branch-specific material through explicit read conditions. Use a script for deterministic checks when its interface and failure behavior are known, and verify actual results rather than treating the script's existence as proof.

[Conditional reference pointers]({{ '/catalog/patterns/23/' | relative_url }}) · [Progressive disclosure]({{ '/catalog/patterns/100/' | relative_url }}) · [Artifact evidence]({{ '/catalog/patterns/26/' | relative_url }})
{: .guide-references}
