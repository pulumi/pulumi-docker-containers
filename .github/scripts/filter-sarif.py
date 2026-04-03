#!/usr/bin/python
# GitHub Code Scanning does not allow more than 20 runs per SARIF file.
# We filter out empty runs, then split the remainder into chunks of at most
# 20 runs each, writing each chunk to a separate file in the "out/" directory.
# The upload-sarif action accepts a directory and uploads all *.sarif files
# within it, so no findings are dropped.

import json
import os
import shutil

MAX_RUNS = 20

with open("snyk.sarif") as f:
    sarif = json.load(f)

# Remove runs with no results.
runs = [run for run in sarif["runs"] if len(run["results"]) > 0]

# Keep at least one run.
if len(runs) == 0:
    runs = [sarif["runs"][0]]

# GitHub expects each tool to only create 1 run, but Snyk splits the results
# across multiple runs. As a workaround, we rename the tools for each run to
# ensure they are unique within the file.
# https://github.blog/changelog/2025-07-21-code-scanning-will-stop-combining-multiple-sarif-runs-uploaded-in-the-same-sarif-file/
for i, run in enumerate(runs):
    run["tool"]["driver"]["name"] += f"_{i}"

# Clean any prior output so sequential runs in the same job don't mix results.
if os.path.exists("out"):
    shutil.rmtree("out")
os.makedirs("out")

# Split runs into chunks of at most MAX_RUNS and write each to a separate file.
for chunk_idx in range(0, len(runs), MAX_RUNS):
    chunk = runs[chunk_idx:chunk_idx + MAX_RUNS]
    chunk_sarif = {**sarif, "runs": chunk}
    with open(f"out/results_{chunk_idx // MAX_RUNS}.sarif", "w") as out:
        json.dump(chunk_sarif, out, indent=2)
