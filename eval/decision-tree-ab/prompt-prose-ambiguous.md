You are a deployment assistant. A user gives you a deployment request and a server config. Decide what to do.

Rules:
- If the server is in maintenance mode and the deployment is not marked as urgent, skip the deployment and notify the user.
- If the server is in maintenance mode but the deployment is urgent, proceed but add a warning.
- If the server is healthy and the deployment target matches the server's environment, deploy normally.
- If the server is healthy but the target environment doesn't match, reject the deployment with an error.
- If the server status is unknown, check health first before deciding.

Here is the server config:
```json
{
  "server": "prod-east-1",
  "status": "degraded",
  "environment": "production"
}
```

Here is the deployment request:
```json
{
  "app": "payment-service",
  "version": "2.4.1",
  "target_env": "production",
  "urgent": true
}
```

Respond with a JSON object containing: action, reason, and warnings (if any).
