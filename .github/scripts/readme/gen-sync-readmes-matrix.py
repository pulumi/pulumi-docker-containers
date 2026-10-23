#!/usr/bin/env python
#
# This script creates the matrix of image repositories whose descriptions the `sync-readmes` workflow updates on
# Docker Hub and AWS ECR Public Gallery.
#
# matrix = {
#     "include": [
#         {"repo": "pulumi",        "readme": "docker/pulumi/README.md", "short_description": "..."},
#         {"repo": "pulumi-python", "readme": "docker/python/README.md", "short_description": "..."},
#         {"repo": "pulumi-python-3.12", "readme": "docker/python/README.md", "short_description": "..."},
#         ...
#     ]
# }
#
import json
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "matrix"))
import versions  # noqa: E402

import images  # noqa: E402

# Docker Hub rejects longer short descriptions.
MAX_SHORT_DESCRIPTION = 100

matrix = {"include": []}


def add(repo, image, version=None):
    short_description = image["short_description"].format(version=version)
    if len(short_description) > MAX_SHORT_DESCRIPTION:
        sys.exit(f"error: short description for {repo} is longer than {MAX_SHORT_DESCRIPTION} characters")
    matrix["include"].append({"repo": repo, "readme": image["readme"], "short_description": short_description})


for name, image in images.IMAGES.items():
    sdk = image.get("sdk")
    if sdk in versions.versioned:
        info = versions.versioned[sdk]
        add(name, image, info["default"])
        for version in [info["default"]] + info["additional"]:
            add(f"{name}-{version}", image, version)
    else:
        add(name, image)

print(json.dumps(matrix))
