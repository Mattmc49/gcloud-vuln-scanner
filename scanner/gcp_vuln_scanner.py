#!/usr/bin/env python3
import argparse
import json
import sys

from google.cloud import compute_v1, storage, iam_v1
from tabulate import tabulate

def list_firewalls(project):
    client = compute_v1.FirewallsClient()
    misconfigs = []
    for fw in client.list(project=project):
        if fw.source_ranges and '0.0.0.0/0' in fw.source_ranges:
            misconfigs.append({
                'name': fw.name,
                'direction': fw.direction,
                'allows': ','.join(f"{rule.IPProtocol}:{','.join(rule.ports or [])}"
                                   for rule in (fw.allowed or []))
            })
    return misconfigs

def list_public_buckets(project):
    client = storage.Client(project=project)
    misconfigs = []
    for bucket in client.list_buckets():
        for entry in bucket.acl:
            if entry['entity'] in ("allUsers", "allAuthenticatedUsers"):
                misconfigs.append({
                    'name': bucket.name,
                    'role': entry['role']
                })
                break
    return misconfigs

def list_disabled_service_accounts(project):
    client = iam_v1.IAMClient()
    parent = f"projects/{project}"
    misconfigs = []
    for sa in client.list_service_accounts(request={'name': parent}).accounts:
        if sa.disabled:
            misconfigs.append({
                'name': sa.name.split('/')[-1],
                'email': sa.email
            })
    return misconfigs

def main():
    parser = argparse.ArgumentParser("GCP Vulnerability Scanner")
    parser.add_argument('--project', required=True, help="GCP project ID")
    parser.add_argument('--output', default='report.json',
                        help="Path to JSON report")
    args = parser.parse_args()

    results = {
        'firewalls': list_firewalls(args.project),
        'public_buckets': list_public_buckets(args.project),
        'disabled_service_accounts': list_disabled_service_accounts(args.project),
    }

    for section, items in results.items():
        print(f"\n=== {section} ({len(items)}) ===")
        if items:
            print(tabulate(items, headers="keys"))
        else:
            print("None found.")

    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nReport written to {args.output}")

if __name__ == '__main__':
    main()
