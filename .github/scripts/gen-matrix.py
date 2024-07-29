#!/usr/bin/env python
# Create a matrix wihout any variables. Each desired combination is explicitly listed as an include.
# https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs#example-adding-configurations
#
# matrix = {
#     "include": [
#         # Unversion SDKs
#         {"sdk": "go", "arch": "amd64"},
#         {"sdk": "go", "arch": "ard64"},
#         # An unversioned variant for Python
#         {"sdk": "python", "arch": "amd64"},
#         {"sdk": "python", "arch": "arm64"},
#         # Versioned variants for Python, include a suffix to add the container name
#         {"sdk": "python", "arch": "amd64", "version": "3.9", "suffix": "-3.9"},
#         {"sdk": "python", "arch": "arm64", "version": "3.9", "suffix": "-3.9"},
#         {"sdk": "python", "arch": "amd64", "version": "3.10", "suffix": "-3.10"},
#         {"sdk": "python", "arch": "arm64", "version": "3.10", "suffix": "-3.10"},
#         ...
#     ]
# }
#
import json

matrix = {
    "include": []
}

sdks = ["nodejs", "python", "dotnet", "go", "java"]
archs = ["amd64", "arm64"]
python_versions = ["3.9", "3.10", "3.11", "3.12"]
node_versions = ["18", "20", "22"]

# Unversioned SDKs, this includes an unversioned variant for Python and Nodejs
for sdk in sdks:
    for arch in archs:
        matrix["include"].append({
            "sdk": sdk,
            "arch": arch,
        })

# Add versioned variants for Python
for version in python_versions:
    for arch in archs:
        matrix["include"].append({
            "sdk": "python",
            "arch": arch,
            "version": version,
            "suffix": f"-{version}",
        })

# Add versioned variants for Nodejs
for version in node_versions:
    for arch in archs:
        matrix["include"].append({
            "sdk": "nodejs",
            "arch": arch,
            "version": version,
            "suffix": f"-{version}",
        })

print(f"matrix={json.dumps(matrix)}")
