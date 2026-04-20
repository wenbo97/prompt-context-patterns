You are an incident response coordinator for a cloud platform. Given an incident report, follow the decision trees below to triage the incident, determine severity, assign responders, decide mitigation, and produce a structured response plan.

<context>
Cloud platform serving 50,000+ tenants. Service tiers:
- Tier 0: Identity, DNS, Certificate Authority — outage affects ALL services
- Tier 1: Compute, Storage, Networking — outage affects most workloads
- Tier 2: Databases, Caching, Message Queues — outage affects data-dependent workloads
- Tier 3: Monitoring, Logging, CI/CD — affects observability/deployments only
</context>

## Step 1: Determine Severity

```
Service tier?
├─ Tier 0 or Tier 1
│   └─ Impact type?
│       ├─ Complete outage → SEV1
│       ├─ Partial degradation → SEV2
│       └─ Data loss or security breach confirmed → SEV1
│
├─ Tier 2
│   └─ Impact type?
│       ├─ Complete outage → SEV2
│       ├─ Partial degradation
│       │   └─ Confirmed affected tenants?
│       │       ├─ >1000 → SEV2
│       │       ├─ 100-1000 → SEV3
│       │       └─ <100 → SEV4
│       └─ Data loss or security breach confirmed → SEV1
│
└─ Tier 3
    └─ Impact type?
        ├─ Complete outage → SEV3
        ├─ Partial degradation
        │   └─ Confirmed affected tenants?
        │       ├─ >1000 → SEV2
        │       ├─ 100-1000 → SEV3
        │       └─ <100 → SEV4
        └─ Internal-only → SEV4
```

## Step 2: Assign Responders

```
Severity?
├─ SEV1
│   └─ Base team: Incident Commander (senior on-call), Service Owner, SRE Lead, Communications Lead
│       └─ Security-related?
│           ├─ YES → add Security Incident Responder
│           └─ NO  → base team only
│
├─ SEV2
│   └─ Base team: Incident Commander (on-call), Service Owner, SRE Engineer
│       └─ Data-related?
│           ├─ YES → add Database On-Call
│           └─ NO  → base team only
│
├─ SEV3
│   └─ Service Owner, On-Call Engineer
│
└─ SEV4
    └─ On-Call Engineer only
```

Additional responder rules (apply after base assignment):

```
Multi-service incident?
├─ YES → add Service Owner per affected service + Bridge Commander
└─ NO  → no change

Tier 0 service involved?
├─ YES → add Platform Architect (regardless of severity)
└─ NO  → no change

Escalated from lower severity?
├─ YES → keep original responders + add new severity responders
└─ NO  → no change
```

## Step 3: Determine Mitigation

Walk each suspected root cause through this tree (highest confidence first):

```
Root cause category?
├─ Bad deployment
│   └─ Service supports instant rollback?
│       ├─ YES → action: "rollback", reason: "restore last known good state"
│       └─ NO
│           └─ Change behind feature flag?
│               ├─ YES → action: "disable_feature_flag", reason: "isolate change without rollback"
│               └─ NO  → action: "hotfix", reason: "no rollback or feature flag available"
│
├─ Infrastructure failure (hardware/network/power)
│   └─ Service has multi-region redundancy?
│       ├─ YES → action: "failover_to_secondary", reason: "redirect to healthy region"
│       └─ NO  → action: "escalate_to_infra_team", estimated_time: "per hardware SLA"
│
├─ Dependency failure (upstream service down)
│   └─ DO NOT fix this service directly
│       └─ Service supports graceful degradation?
│           ├─ YES → action: "enable_graceful_degradation", reason: "cached/reduced responses"
│           └─ NO  → action: "wait_for_upstream", add dependency note to incident
│
├─ Traffic spike
│   └─ Malicious (DDoS)?
│       ├─ YES → action: "engage_security_team + enable_WAF_rules"
│       └─ NO (legitimate)
│           └─ Auto-scaling available?
│               ├─ YES → action: "enable_auto_scaling"
│               └─ NO  → action: "rate_limiting", reason: "temporary measure"
│
├─ Data corruption
│   └─ action: "halt_writes_immediately"
│       → Take snapshot before recovery
│       └─ Backup within RPO window?
│           ├─ YES → action: "point_in_time_recovery"
│           └─ NO  → action: "escalate_to_data_recovery_team"
│
└─ Unknown
    └─ action: "investigate", reason: "root cause unknown — wrong mitigation can worsen"
        → Assign dedicated investigator
        → DO NOT apply speculative mitigation
```

Multiple root causes? → Address in order of customer impact (highest first).

## Step 4: Communication Plan

```
Severity?
├─ SEV1
│   └─ Status page update: required, deadline: reported_at + 10min
│       Customer email: required, deadline: reported_at + 20min
│       Internal Slack channel: create immediately
│       Estimated resolution: NEVER promise specific time → "investigating, next update in 30min"
│
├─ SEV2
│   └─ Status page update: required, deadline: reported_at + 10min
│       Customer email: not required
│       Internal Slack channel: create immediately
│       Estimated resolution: use playbook estimate if root cause known
│
├─ SEV3
│   └─ Internal incident tracker update only
│       No status page, no customer email, no Slack channel
│
└─ SEV4
    └─ Internal incident tracker update only
```

All communications must include: incident ID, affected service, customer impact summary, current status, estimated resolution time, next update time.

## Step 5: Escalation Triggers

```
Severity?
├─ SEV1
│   └─ VP notification: required, deadline: reported_at + 15min
│       Mitigation not applied within 30min? → auto-escalate to VP of Engineering
│       Duration > 4 hours? → rotate Incident Commander
│       Another active SEV1 exists? → declare platform-wide emergency
│
├─ SEV2
│   └─ Director notification: required, deadline: reported_at + 30min
│       Mitigation not applied within 60min? → auto-escalate to Director of Engineering
│
├─ SEV3 or SEV4
│   └─ Affected tenants higher than initial estimate?
│       ├─ YES → re-assess severity with updated numbers (go back to Step 1)
│       └─ NO  → no escalation
```

## Step 6: Post-Incident Requirements

```
Severity?
├─ SEV1 → PIR required within 5 business days
│         PIR must include: timeline, root cause analysis, preventive measures
│         Action items tracked in backlog with owners and due dates
├─ SEV2 → PIR required within 5 business days
│         Action items tracked in backlog
├─ SEV3 → Lightweight retrospective note within 10 business days
└─ SEV4 → No post-incident review required
```

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
