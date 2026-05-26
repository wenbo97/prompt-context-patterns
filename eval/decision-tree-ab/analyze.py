#!/usr/bin/env python3
"""Analyze A/B test results: extract key fields from JSON outputs and compare consistency."""
import json, re, os, sys
from collections import Counter

def extract_json(text):
    m = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
    if m:
        return json.loads(m.group(1))
    m = re.search(r'(\{[\s\S]*\})', text)
    if m:
        try:
            return json.loads(m.group(1))
        except:
            pass
    return None

def analyze_group(results_dir, label):
    files = sorted([f for f in os.listdir(results_dir) if f.endswith('.txt')])
    data = []
    for f in files:
        text = open(os.path.join(results_dir, f)).read()
        j = extract_json(text)
        if j:
            data.append(j)

    print(f"\n{'='*60}")
    print(f"  {label} ({len(data)}/{len(files)} parsed)")
    print(f"{'='*60}")

    # Severity
    sevs = [d.get('severity','?') for d in data]
    print(f"\nSeverity: {dict(Counter(sevs))}")

    # Primary action
    actions = []
    for d in data:
        pa = d.get('mitigation_plan',{}).get('primary_action',{})
        actions.append(pa.get('action','?'))
    unique_actions = set(actions)
    print(f"\nPrimary action: {len(unique_actions)} unique values out of {len(actions)} runs")
    for a, c in Counter(actions).most_common(5):
        print(f"  [{c:2d}x] {a[:100]}")
    if len(unique_actions) > 5:
        print(f"  ... and {len(unique_actions)-5} more variants")

    # Secondary action
    sec_actions = []
    for d in data:
        sa = d.get('mitigation_plan',{}).get('secondary_action',{})
        sec_actions.append(sa.get('action','?'))
    unique_sec = set(sec_actions)
    print(f"\nSecondary action: {len(unique_sec)} unique values out of {len(sec_actions)} runs")
    for a, c in Counter(sec_actions).most_common(5):
        print(f"  [{c:2d}x] {a[:100]}")

    # Responder roles
    role_sets = []
    for d in data:
        roles = tuple(sorted(r.get('role','?') for r in d.get('responders',[])))
        role_sets.append(roles)
    print(f"\nResponder role sets: {len(set(role_sets))} unique combinations")
    for rs, c in Counter(role_sets).most_common(3):
        print(f"  [{c:2d}x] {rs}")

    # Actions to avoid
    avoid_counts = []
    for d in data:
        avoids = d.get('mitigation_plan',{}).get('actions_to_avoid',[])
        avoid_counts.append(len(avoids))
    print(f"\nActions to avoid count: {dict(Counter(avoid_counts))}")

    # Escalation trigger count
    esc_counts = [len(d.get('escalation_triggers',[])) for d in data]
    print(f"Escalation triggers count: {dict(Counter(esc_counts))}")

    # Extra text outside JSON?
    extras = 0
    for f in files:
        text = open(os.path.join(results_dir, f)).read().strip()
        json_match = re.search(r'```json\s*\{.*?\}\s*```', text, re.DOTALL)
        if json_match:
            before = text[:json_match.start()].strip()
            after = text[json_match.end():].strip()
            if before or after:
                extras += 1
    print(f"Runs with extra text outside JSON: {extras}/{len(files)}")

    return data

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

for model_suffix, model_label in [("", "Opus"), ("-haiku", "Haiku")]:
    prose_dir = f"{base}/prose-complex{model_suffix}"
    tree_dir = f"{base}/tree-complex{model_suffix}"
    if os.path.isdir(prose_dir) and os.path.isdir(tree_dir):
        print(f"\n{'#'*60}")
        print(f"  MODEL: {model_label}")
        print(f"{'#'*60}")
        analyze_group(prose_dir, f"PROSE ({model_label})")
        analyze_group(tree_dir, f"TREE ({model_label})")
