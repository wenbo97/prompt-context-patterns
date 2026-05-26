Classify this customer message. Output ONLY the JSON object below — no
preface, no markdown fence, no trailing prose.

```json
{
  "category": "billing|technical|feedback|other",
  "sentiment": "positive|neutral|negative",
  "next_action": "string — imperative verb + object",
  "priority": "P0|P1|P2|P3"
}
```

Message:
{{ message }}
