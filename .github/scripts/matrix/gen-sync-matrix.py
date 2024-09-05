#!/usr/bin/env python
#
# This script is used to create the matrix of images to sync to GCR and ECR.
#
# matrix = {
#     "image": [
#         "pulumi-base",
#         "pulumi-go",
#         "pulumi-dotnet",
#         "pulumi-java",
#         "pulumi-python",
#         "pulumi-python-3.9",
#         "pulumi-python-3.10"
#         "pulumi-nodejs",
#         "pulumi-nodejs-18",
#         "pulumi-nodejs-20",
#         ...
#     ]
# }
#
import json

import versions

matrix = {"image": [
    "pulumi-base", # The base image without any language sdks
]}

# Images without language versions
for sdk in versions.unversioned:
    matrix["image"].append(f"pulumi-{sdk}")

for sdk, info in versions.versioned.items():
    # Without suffix
    matrix["image"].append(f"pulumi-{sdk}")
    matrix["image"].append(f"pulumi-{sdk}-{info['default']}")
    # Additional versions with suffixes
    for version in info["additional"]:
        matrix["image"].append(f"pulumi-{sdk}-{version}")

print(json.dumps(matrix))
