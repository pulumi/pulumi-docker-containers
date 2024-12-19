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

    sarif["runs"] = runs

    with open("out.sarif", "w") as out:
        json.dump(sarif, out, indent=2)
