#!/usr/bin/python
# Dismiss open code scanning alerts whose analysis category is not produced by
# the current scan matrix.
#
# GitHub only auto-closes an alert when a newer analysis is uploaded to the
# *same* category. When an image is retired from the scan matrix, its
# categories stop receiving uploads and their alerts stay open forever. This
# script dismisses those orphaned alerts.
#
# The set of expected categories is derived from the same versions.py that
# generates the scan matrix, so retiring an image automatically retires its
# alerts on the next scheduled run.
#
# Pass --dry-run to only print what would be dismissed.

import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "matrix"))
import versions

DRY_RUN = "--dry-run" in sys.argv
REPO = os.environ.get("GITHUB_REPOSITORY", "pulumi/pulumi-docker-containers")
TOKEN = os.environ["GH_TOKEN"]
ARCHS = ["amd64", "arm64"]

DISMISS_COMMENT = (
    "This alert belongs to an analysis category that is not produced by the "
    "Snyk scan workflow (retired image or renamed category), so it can never "
    "be closed automatically. Current results are tracked under the per-image "
    "categories."
)


def expected_categories():
    expected = set()
    for suffix in ["", "-nonroot"]:
        for arch in ARCHS:
            expected.add(f"pulumi{suffix}-{arch}")
    for arch in ARCHS:
        expected.add(f"pulumi-provider-build-environment-{arch}")
    for base_os in ["debian", "ubi"]:
        for arch in ARCHS:
            expected.add(f"pulumi-base-{base_os}-{arch}")
    for sdk in versions.unversioned:
        for arch in ARCHS:
            expected.add(f"pulumi-{sdk}-debian-{arch}")
    for sdk, info in versions.versioned.items():
        for version in [info["default"]] + info["additional"]:
            for arch in ARCHS:
                expected.add(f"pulumi-{sdk}-{version}-debian-{arch}")
    for sdk in ["nodejs", "python", "dotnet", "go"]:
        expected.add(f"pulumi-{sdk}-ubi")
    return expected


def api(path, method="GET", body=None):
    request = urllib.request.Request(
        f"https://api.github.com{path}",
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def open_alerts():
    alerts = []
    page = 1
    while True:
        batch = api(f"/repos/{REPO}/code-scanning/alerts?state=open&per_page=100&page={page}")
        alerts.extend(batch)
        if len(batch) < 100:
            return alerts
        page += 1


expected = expected_categories()
stale = [
    alert
    for alert in open_alerts()
    if alert.get("most_recent_instance", {}).get("category") not in expected
]
print(f"Found {len(stale)} open alerts in stale categories.")

for alert in stale:
    category = alert["most_recent_instance"]["category"]
    label = f"alert #{alert['number']} ({alert['rule']['id']}) in category '{category}'"
    if DRY_RUN:
        print(f"Would dismiss {label}")
        continue
    api(
        f"/repos/{REPO}/code-scanning/alerts/{alert['number']}",
        method="PATCH",
        body={
            "state": "dismissed",
            "dismissed_reason": "won't fix",
            "dismissed_comment": DISMISS_COMMENT,
        },
    )
    print(f"Dismissed {label}")
