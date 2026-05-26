The response is a JSON object describing an incident response plan.

PASS if ALL of:
1. The JSON parses and contains keys: severity, mitigation_plan (with primary_action.action), responders (array with role).
2. severity is one of: P0, P1, P2, P3 (no other values).
3. primary_action.action is concrete (an imperative verb + object), not a hedge like "investigate further".
4. No prose appears outside the JSON block.

FAIL otherwise. Note specifically which check failed.
