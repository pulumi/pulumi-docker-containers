#!/usr/bin/python
# Merge all runs in Snyk's snyk.sarif into a single run and write it to
# out.sarif.
#
# Snyk emits one SARIF run per target it detects in the image (OS packages,
# npm projects, go binaries, ...). GitHub code scanning treats every run as a
# separate analysis whose category is derived from the run's
# `automationDetails.id`, ignoring the `category` input of the upload-sarif
# action:
# https://github.blog/changelog/2025-07-21-code-scanning-will-stop-combining-multiple-sarif-runs-uploaded-in-the-same-sarif-file/
#
# Uploading a single run without `automationDetails` makes GitHub use the
# per-image category the workflow passes to upload-sarif. A stable category
# per image lets GitHub track alerts across scans and automatically close
# alerts that no longer appear in the image's latest scan.
#
# snyk.sarif is deleted after a successful merge so that sequential scans
# within the same job can never accidentally re-upload a previous scan's
# results. If snyk.sarif is missing the script fails, failing the job without
# uploading anything, so a broken scan leaves existing alerts untouched.

import json
import os
import sys

if not os.path.exists("snyk.sarif"):
    print(
        "error: snyk.sarif not found — the Snyk scan failed to produce output.",
        file=sys.stderr,
    )
    sys.exit(1)

with open("snyk.sarif") as f:
    sarif = json.load(f)

runs = sarif.get("runs", [])
if len(runs) == 0:
    print("error: snyk.sarif contains no runs", file=sys.stderr)
    sys.exit(1)

# Merge the rules of all runs, deduplicating by rule id, and remember each
# rule's index in the merged rules array so results can be re-pointed at it.
merged_rules = []
rule_index_by_id = {}
for run in runs:
    for rule in run["tool"]["driver"].get("rules", []):
        if rule["id"] not in rule_index_by_id:
            rule_index_by_id[rule["id"]] = len(merged_rules)
            merged_rules.append(rule)

# Merge the results of all runs, dropping exact duplicates (the same vuln
# reported at the same location for multiple targets collapses into a single
# alert in GitHub anyway).
merged_results = []
seen_results = set()
for run in runs:
    for result in run.get("results", []):
        if "ruleId" in result:
            result["ruleIndex"] = rule_index_by_id[result["ruleId"]]
        key = json.dumps(result, sort_keys=True)
        if key not in seen_results:
            seen_results.add(key)
            merged_results.append(result)

merged_driver = {**runs[0]["tool"]["driver"], "name": "Snyk Container", "rules": merged_rules}
merged_run = {**runs[0], "tool": {"driver": merged_driver}, "results": merged_results}
merged_run.pop("automationDetails", None)

with open("out.sarif", "w") as out:
    json.dump({**sarif, "runs": [merged_run]}, out, indent=2)

os.remove("snyk.sarif")
print(f"Merged {len(runs)} runs into one: {len(merged_results)} results, {len(merged_rules)} rules.")
