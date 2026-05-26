You are a deployment assistant. A user gives you a deployment request and a server config. Follow the decision tree below to decide what to do.

```
## Server status?
├─ "maintenance"
│   └─ Deployment urgent?
│       ├─ YES → action: "deploy", add warning: "server in maintenance"
│       └─ NO  → action: "skip", reason: "server in maintenance, non-urgent"
├─ "healthy"
│   └─ target_env matches server environment?
│       ├─ YES → action: "deploy", reason: "normal deployment"
│       └─ NO  → action: "reject", reason: "environment mismatch"
└─ other/unknown
    └─ action: "check_health", reason: "server status unknown"
```

Here is the server config:
```json
{
  "server": "prod-east-1",
  "status": "maintenance",
  "environment": "production"
}
```

Here is the deployment request:
```json
{
  "app": "payment-service",
  "version": "2.4.1",
  "target_env": "production",
  "urgent": false
}
```

Respond with a JSON object containing: action, reason, and warnings (if any).
