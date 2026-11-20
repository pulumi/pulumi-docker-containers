#!/usr/bin/env python
#
# This script prints the `docker build` arguments that pass language versions from `versions.py` to an image's
# Dockerfile, so that the versions are only defined in one place. Pass the image's directory under `docker/`:
#
#     docker build $(python ./.github/scripts/matrix/build-args.py pulumi) ...
#
# The single language images also get their language version as `LANGUAGE_VERSION` from the build matrix, see
# `gen-matrix.py`.
#
import sys

import versions


def all_versions(sdk):
    info = versions.versioned[sdk]
    return ",".join([info["default"], *info["additional"]])


def go_args():
    go = versions.unversioned["go"]
    return {
        "GO_AMD64_SHA256": go["sha256"]["amd64"],
        "GO_ARM64_SHA256": go["sha256"]["arm64"],
    }


if len(sys.argv) != 2:
    sys.exit("usage: build-args.py <image>")
image = sys.argv[1]

if image == "pulumi":
    args = {
        "GO_VERSION": versions.unversioned["go"]["version"],
        **go_args(),
        "JAVA_VERSION": versions.unversioned["java"]["version"],
        "DOTNET_VERSIONS": all_versions("dotnet"),
        "PYTHON_VERSIONS": all_versions("python"),
        "PYTHON_DEFAULT": versions.versioned["python"]["default"],
        "NODEJS_VERSIONS": all_versions("nodejs"),
        "NODEJS_DEFAULT": versions.versioned["nodejs"]["default"],
    }
elif image == "go":
    args = go_args()
else:
    args = {}

print(" ".join(f"--build-arg {name}={value}" for name, value in args.items()))
