#!/usr/bin/env python
#
# This script is used to create the matrix of images to sync to GCR and ECR.
#
# matrix = {
#     "image": [
#         "pulumi-base",
#         "pulumi-nodejs",
#         "pulumi-go",
#         "pulumi-dotnet",
#         "pulumi-java",
#         "pulumi-python",
#         "pulumi-python-3.9",
#         "pulumi-python-3.10"
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
for sdk in versions.sdks:
    matrix["image"].append(f"pulumi-{sdk}")

# Python without suffix
matrix["image"].append("pulumi-python")

# Python with version suffixes
for version in [versions.python_default_version, *versions.python_additional_versions]:
    matrix["image"].append(f"pulumi-python-{version}")

print(json.dumps(matrix))
