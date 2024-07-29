#!/usr/bin/env python
# Create a matrix wihout any variables. Each desired combination is explicitly listed as an include.
# https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs#example-adding-configurations
#
# matrix = {
#     "include": [
#         {"sdk": "go",     "arch": "amd64", "language_version": "1.21.1", "default": True},
#         {"sdk": "go",     "arch": "ard64", "language_version": "1.21.1", "default": True},
#         {"sdk": "python", "arch": "amd64", "language_version": "3.9",    "default": True, "suffix": "-3.9"},
#         {"sdk": "python", "arch": "arm64", "language_version": "3.9",    "default": True, "suffix": "-3.9"},
#         {"sdk": "python", "arch": "amd64", "language_version": "3.10",                    "suffix": "-3.10"},
#         {"sdk": "python", "arch": "arm64", "language_version": "3.10",                    "suffix": "-3.10"},
#         ...
#     ]
# }
#
# `suffix` is an optional suffix to append to the image name, for example `-3.9` to build `pulumi-python-3.9`
# `default` indicates that this is the default language_version, and we will push two tags for the image, once
# with and once without the suffix.
#
import json

matrix = {"include": []}
archs = ["amd64", "arm64"]
sdks = {
    "python": "3.9",
    "nodejs": "18",
    "go": "1.21.1",
    "dotnet": "6.0",
    "java": "not-versioned",
}
python_versions = ["3.9", "3.10"]  # , "3.11", "3.12"]
node_versions = ["18", "20", "22"]

# Unversioned SDKs, this includes an unversioned variant for Python and Nodejs
for (sdk, language_version) in sdks.items():
    for arch in archs:
        matrix["include"].append(
            {
                "sdk": sdk,
                "arch": arch,
                "language_version": language_version,
                "default": True,
            }
        )

# Add suffixed variants for Python
for version in python_versions:
    for arch in archs:
        matrix["include"].append(
            {
                "sdk": "python",
                "arch": arch,
                "language_version": version,
                "suffix": f"-{version}",
            }
        )

# Add suffixed variants for Nodejs
# for version in node_versions:
#     for arch in archs:
#         matrix["include"].append({
#             "sdk": "nodejs",
#             "arch": arch,
#             "language_version": version,
#             "suffix": f"-{version}",
#         })

print(f"matrix={json.dumps(matrix)}")
