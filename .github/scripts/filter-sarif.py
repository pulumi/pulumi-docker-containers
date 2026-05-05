#!/usr/bin/python
# GitHub Code Scanning does not allow more than 20 runs per SARIF file.
# We split runs into chunks of at most 20 and write each to a separate
# file (out_0.sarif, out_1.sarif, ...). Each file should be uploaded
# separately with a distinct category to stay within GitHub's limit.
#
# The workflow supports at most 2 chunks (40 runs). If Snyk produces
# more, this script will error so we know to add more upload steps.

import glob
import json
import os
import sys

MAX_RUNS = 20
MAX_CHUNKS = 2

with open("snyk.sarif") as f:
    sarif = json.load(f)

# Remove runs with no results to stay well within the chunk limit.
runs = [run for run in sarif["runs"] if len(run["results"]) > 0]
if len(runs) == 0:
    # Keep at least one run so the upload is valid.
    runs = [sarif["runs"][0]]

num_chunks = (len(runs) + MAX_RUNS - 1) // MAX_RUNS
if num_chunks > MAX_CHUNKS:
    print(
        f"error: {len(runs)} runs would require {num_chunks} chunks, "
        f"but the workflow only supports {MAX_CHUNKS} "
        f"(max {MAX_CHUNKS * MAX_RUNS} runs)",
        file=sys.stderr,
    )
    sys.exit(1)

# GitHub expects each tool to only create 1 run, but Snyk splits the results
# across multiple runs. As a workaround, we rename the tools for each run to
# ensure they are unique within the file.
# https://github.blog/changelog/2025-07-21-code-scanning-will-stop-combining-multiple-sarif-runs-uploaded-in-the-same-sarif-file/
for i, run in enumerate(runs):
    run["tool"]["driver"]["name"] += f"_{i}"

# Clean any prior output so sequential runs in the same job don't mix results.
for old in glob.glob("out_*.sarif"):
    os.remove(old)

# Split runs into chunks of at most MAX_RUNS and write each to a separate file.
for chunk_idx in range(0, len(runs), MAX_RUNS):
    chunk = runs[chunk_idx:chunk_idx + MAX_RUNS]
    chunk_sarif = {**sarif, "runs": chunk}
    with open(f"out_{chunk_idx // MAX_RUNS}.sarif", "w") as out:
        json.dump(chunk_sarif, out, indent=2)
