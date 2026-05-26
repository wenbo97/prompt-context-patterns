PASS if response is JSON with `route` from the allowed enum and
`reason` cites the transition rule used.

Expected mappings:
  Checkout 500 outage -> p0
  Add dark mode       -> feature
  Rotate API key      -> close
  "It's slow"         -> clarify

FAIL if route is outside enum, missing keys, or routes the issue to a
wrong terminal.
