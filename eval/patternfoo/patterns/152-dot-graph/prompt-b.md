Triage this incoming issue using this state machine. Start at `start`,
follow the edge whose label matches the input, end at a terminal node.

~~~dot
digraph triage {
  start -> classify [label="incoming issue"];
  classify -> bug [label="repro steps + error"];
  classify -> feature [label="behaviour change request"];
  classify -> question [label="usage / how-to"];
  classify -> clarify [label="ambiguous"];
  bug -> severity;
  severity -> p0 [label="data loss / outage"];
  severity -> p1 [label="user-blocking"];
  severity -> p2 [label="degraded"];
  question -> close [label="answer + link docs"];
}
~~~

Output JSON: { "route": "p0|p1|p2|feature|close|clarify", "reason": "..." }

Issue: {{ issue }}
