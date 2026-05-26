You are an incident response coordinator for a cloud platform. Given an incident report, you must triage the incident, determine severity, assign responders, decide on mitigation actions, and produce a structured response plan.

## Context

You work for a cloud platform serving 50,000+ tenants. Services are organized in tiers:
- Tier 0: Identity, DNS, Certificate Authority — outage affects ALL other services
- Tier 1: Compute, Storage, Networking — outage affects most workloads
- Tier 2: Databases, Caching, Message Queues — outage affects data-dependent workloads
- Tier 3: Monitoring, Logging, CI/CD — outage affects observability and deployments but not production traffic

Incident severity levels:
- SEV1: Complete outage of a Tier 0 or Tier 1 service, OR data loss confirmed, OR security breach confirmed. Requires VP notification within 15 minutes.
- SEV2: Partial degradation of Tier 0/1, OR complete outage of Tier 2, OR confirmed customer impact >1000 tenants. Requires director notification within 30 minutes.
- SEV3: Partial degradation of Tier 2, OR complete outage of Tier 3, OR confirmed customer impact 100-1000 tenants. On-call team handles, manager notified.
- SEV4: Partial degradation of Tier 3, OR confirmed customer impact <100 tenants, OR internal-only impact. On-call engineer handles.

## Mitigation Decision Rules

When choosing a mitigation action, consider these factors:
- If the root cause is a bad deployment and the service supports instant rollback, always prefer rollback over other mitigations because it restores the last known good state with minimal risk.
- If the root cause is a bad deployment but rollback is not available (e.g., database schema migration was applied), then consider feature flag disablement if the change is behind a feature flag. If no feature flag exists, proceed with hotfix.
- If the root cause is infrastructure failure (hardware, network, power), initiate failover to the secondary region if the service has multi-region redundancy. If single-region only, escalate to the infrastructure team and set expected resolution time to the hardware SLA.
- If the root cause is a dependency failure (an upstream service is down), do NOT attempt to fix the affected service directly. Instead, enable graceful degradation if the service supports it (cached responses, reduced functionality), and add a dependency note to the incident linking to the upstream incident.
- If the root cause is a traffic spike (legitimate or DDoS), first determine if it's malicious. If DDoS, engage the security team and enable WAF rules. If legitimate traffic spike, enable auto-scaling if available, or implement rate limiting as a temporary measure.
- If the root cause is a data corruption issue, immediately halt all write operations to prevent further damage. Take a snapshot of the current state before any recovery. If backups exist within the RPO window, plan a point-in-time recovery. If no viable backup exists, escalate to the data recovery specialist team.
- If multiple root causes are identified, address them in order of customer impact (highest impact first).
- If root cause is unknown after initial assessment, declare it as "investigating" and assign a dedicated investigator. Do not guess at mitigations — wrong mitigation on unknown root cause can make things worse.

## Communication Rules

- External communication (status page update) is required for SEV1 and SEV2 within 10 minutes of declaration.
- Customer notification via email is required for SEV1 within 20 minutes.
- Internal Slack channel must be created for SEV1 and SEV2 incidents.
- For SEV3 and SEV4, update the internal incident tracker only.
- All communications must include: incident ID, affected service, customer impact summary, current status, estimated resolution time, and next update time.
- Never promise a specific resolution time for SEV1 — use "investigating, next update in 30 minutes" instead.
- For known root causes with established playbooks, include the estimated resolution time from the playbook.

## Responder Assignment Rules

- SEV1: Incident Commander (senior on-call), Service Owner, SRE Lead, Communications Lead. If security-related, add Security Incident Responder.
- SEV2: Incident Commander (on-call), Service Owner, SRE Engineer. If data-related, add Database On-Call.
- SEV3: Service Owner, On-Call Engineer.
- SEV4: On-Call Engineer only.
- If the incident crosses multiple services, each service must have its own Service Owner assigned, and a Bridge Commander is added to coordinate.
- If the incident involves a Tier 0 service, the Platform Architect is always added regardless of severity.
- If the incident was escalated from a lower severity, the original responder remains on the incident plus the new responders are added.

## Escalation Rules

- If a SEV3 or SEV4 incident affects more tenants than initially estimated, re-assess severity using the updated impact numbers.
- If mitigation has not been applied within 30 minutes of SEV1 declaration, auto-escalate to VP of Engineering.
- If mitigation has not been applied within 60 minutes of SEV2, auto-escalate to Director of Engineering.
- If two or more active SEV1 incidents exist simultaneously, declare a platform-wide emergency and activate the full incident response team.
- If a SEV1 incident lasts longer than 4 hours, rotate the Incident Commander to prevent fatigue.

## Post-Incident Rules

- SEV1 and SEV2 require a post-incident review (PIR) within 5 business days.
- SEV1 PIR must include a timeline with all actions taken, root cause analysis, and preventive measures.
- SEV3 requires a lightweight retrospective note within 10 business days.
- SEV4 does not require post-incident review.
- All action items from PIR must be tracked in the engineering backlog with assigned owners and due dates.

---

Here is the incident report:

```json
{
  "incident_id": "INC-2026-04192",
  "reported_at": "2026-04-19T14:32:00Z",
  "reporter": "monitoring-bot",
  "alert_source": "PagerDuty",
  "affected_service": {
    "name": "Azure Cosmos DB",
    "tier": 2,
    "region": "East US 2",
    "has_multi_region": true,
    "supports_rollback": false,
    "supports_feature_flags": false,
    "supports_graceful_degradation": true
  },
  "symptoms": [
    "Latency p99 increased from 15ms to 4500ms over 10 minutes",
    "Error rate increased from 0.1% to 12% (HTTP 503)",
    "Throughput dropped from 50,000 RU/s to 8,000 RU/s"
  ],
  "customer_impact": {
    "estimated_affected_tenants": 3200,
    "confirmed_affected_tenants": 1850,
    "impact_type": "degraded_performance",
    "customer_complaints": 23,
    "revenue_impact_per_hour": "$45,000"
  },
  "preliminary_assessment": {
    "suspected_root_causes": [
      {
        "cause": "Recent deployment of partition rebalancing feature (deployed 45 min ago)",
        "confidence": "medium",
        "evidence": "Timing correlation with latency spike"
      },
      {
        "cause": "Underlying storage node showing elevated I/O latency",
        "confidence": "low",
        "evidence": "One storage node in the cluster reporting high disk utilization"
      }
    ],
    "recent_changes": [
      "Partition rebalancing v2.3.1 deployed at 13:47 UTC",
      "No infrastructure changes in last 24 hours"
    ],
    "dependencies_status": {
      "Azure Storage": "healthy",
      "Azure Active Directory": "healthy",
      "Azure DNS": "healthy",
      "Azure Networking": "healthy"
    }
  }
}
```

Respond with a JSON object:
```json
{
  "severity": "SEV1 | SEV2 | SEV3 | SEV4",
  "severity_justification": "...",
  "responders": [{ "role": "...", "reason": "..." }],
  "mitigation_plan": {
    "primary_action": { "action": "...", "reason": "...", "estimated_time": "..." },
    "secondary_action": { "action": "...", "reason": "...", "trigger": "..." },
    "actions_to_avoid": [{ "action": "...", "reason": "..." }]
  },
  "communication_plan": {
    "internal": { "action": "...", "deadline": "..." },
    "external": { "action": "...", "deadline": "..." },
    "customer_notification": { "required": true/false, "deadline": "..." }
  },
  "escalation_triggers": [{ "condition": "...", "action": "...", "deadline": "..." }],
  "post_incident": { "pir_required": true/false, "deadline": "..." }
}
```
