#!/usr/bin/python
# GitHub Code Scanning does not allow more than 20 runs per file. We filter out
# empty runs to avoid this limit. Note that the file needs to include at least
# one run.

import json

with open("snyk.sarif") as f:
    sarif = json.load(f)

    # Remove runs with no results
    runs = [run for run in sarif["runs"] if len(run["results"]) > 0]

    # Keep at least one run
    runs = runs if len(runs) > 0 else [sarif["runs"][0]]

    # GitHub expects each tool to only create 1 run, but Snyk splits the results
    # across multiple runs. As a workaround, we rename the tools for each run to
    # ensure they are unique within the file.
    # https://github.blog/changelog/2025-07-21-code-scanning-will-stop-combining-multiple-sarif-runs-uploaded-in-the-same-sarif-file/
    for i, run in enumerate(runs):
        run["tool"]["driver"]["name"] += f"_{i}"

    sarif["runs"] = runs

    with open("out.sarif", "w") as out:
        json.dump(sarif, out, indent=2)
