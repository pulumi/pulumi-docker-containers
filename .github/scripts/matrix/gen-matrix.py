#!/usr/bin/env python
#
# This script is used to create the matrix for the language specific images, for example in the `debian-sdk` job. The
# created matrix has no variables, instead we list each desired combination explicitly in the `include` field.
# https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs#example-adding-configurations
#
# matrix = {
#     "include": [
#         {"sdk": "go",     "arch": "amd64", "default": True},
#         {"sdk": "go",     "arch": "arm64", "default": True},
#         {"sdk": "python", "arch": "amd64", "default": True,  "language_version": "3.9",  "suffix": "-3.9"},
#         {"sdk": "python", "arch": "arm64", "default": True,  "language_version": "3.9",  "suffix": "-3.9"},
#         {"sdk": "python", "arch": "amd64", "default": False, "language_version": "3.10", "suffix": "-3.10"},
#         {"sdk": "python", "arch": "arm64", "default": False, "language_version": "3.10", "suffix": "-3.10"},
#         ...
#     ]
# }
#
#  * `language_version` is the version of the language runtime to use, for example `3.9` for Python.
#     For Java and Go, this field is omitted as we only have one version of the runtime.
#  * `suffix` is an optional suffix to append to the image name, for example `-3.9` to generate `pulumi-python-3.9`.
#  * `default` indicates that this is the default language_version. We will push two tags for the image, once
#     with and once without the suffix in the name, for example `pulumi-python-3.9` and `pulumi-python`.
#
# When running this script, pass `--no-arch` to exclude the `arch` field from the matrix. This is used in the release
# job for creating the docker manifests. For example the manifest for `pulumi-python:3.123.0-debian` includes the
# images `pulumi-python-3.123.0-debian-amd64` and `pulumi-python-3.123.0-debian-arm64`, so we don't need to iterate
# over the architecutres in the matrix.
#
import json
import sys

import versions

INCLUDE_ARCH = False if len(sys.argv) > 1 and sys.argv[1] == "--no-arch" else True

archs = ["amd64", "arm64"] if INCLUDE_ARCH else [None]
matrix = {"include": []}

def make_entry(*, sdk, arch, default, language_version=None, suffix=None):
    entry = {
        "sdk": sdk,
        "default": default,
    }
    if language_version is not None:
        entry["language_version"] = language_version
    if arch is not None:
        entry["arch"] = arch
    if suffix is not None:
        entry["suffix"] = suffix
    return entry


for arch in archs:

    for sdk in versions.unversioned:
        # Default (and only) version for unversioned SDKs
        matrix["include"].append(
            make_entry(sdk=sdk, arch=arch, default=True)
        )

    for sdk, info in versions.versioned.items():
        # Default version
        matrix["include"].append(
            make_entry(
                sdk=sdk,
                arch=arch,
                language_version=info["default"],
                default=True,
                suffix=f"-{info['default']}",
            )
        )
        # Additional versions
        for version in info["additional"]:
            matrix["include"].append(
                make_entry(
                    sdk=sdk,
                    arch=arch,
                    language_version=version,
                    default=False,
                    suffix=f"-{version}",
                )
            )

print(json.dumps(matrix))
