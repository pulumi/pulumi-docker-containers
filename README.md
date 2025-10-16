# pulumi-docker-containers

This repository contains the source for Pulumi's official Docker images.  Pulumi publishes and supports the following images:

- [`pulumi/pulumi`](https://hub.docker.com/r/pulumi/pulumi): A "kitchen sink" image that includes the Pulumi CLI and all supported SDKs (Golang, Python, Node, Dotnet, Java).
- [`pulumi/pulumi-base`](https://hub.docker.com/r/pulumi/pulumi-base): A slim image that contains the Pulumi CLI, but no SDK(s).
- [`pulumi/pulumi-go`](https://hub.docker.com/r/pulumi/pulumi-go): A slim image that contains the Pulumi CLI along with the Golang Pulumi SDK.
- [`pulumi/pulumi-python`](https://hub.docker.com/r/pulumi/pulumi-python): A slim image that contains the Pulumi CLI along with the Python runtime and Pulumi SDK. This image also exists in per-language versions for different Python versions: `pulumi/pulumi-python-3.9` to `pulumi/pulumi-python-3.12`. The `pulumi/pulumi-python` image is based on the default Python version, which is currently 3.9.
- [`pulumi/pulumi-nodejs`](https://hub.docker.com/r/pulumi/pulumi-nodejs): A slim image that contains the Pulumi CLI along with the Node runtime and Pulumi SDK and is suitable for both TypeScript and JavaScript development. This image also exists in per-language versions for different Node versions: `pulumi/pulumi-nodejs-18`, `pulumi/pulumi-nodejs-20` and `pulumi/pulumi-nodejs-22`. The `pulumi/pulumi-nodejs` image is based on the default Node version, which is currently 18.
- [`pulumi/pulumi-dotnet`](https://hub.docker.com/r/pulumi/pulumi-dotnet): A slim image that contains the Pulumi CLI along with the .NET runtime and Pulumi SDK. This image also exists in per-language versions for different .NET versions: `pulumi/pulumi-dotnet-8.0` and `pulumi/pulumi-dotnet-9.0`. The `pulumi/pulumi-dotnet` image is based on the default .NET version, which is currently 8.0.
- [`pulumi/pulumi-java`](https://hub.docker.com/r/pulumi/pulumi-java): A slim image that contains the Pulumi CLI along with the Java runtime and Pulumi SDK.

Tags on each image match the installed version of Pulumi.  The `latest` tag matches the latest production version of Pulumi.

The base and SDK-specific images are considerably smaller than the combined `pulumi/pulumi` container (200 to 300 MB, compared to ~2 GB for the combined image).

## Build Matrix

`pulumi/pulumi` is built for amd64 and arm64, using Debian Bookworm (12) as the base image.

Each of the other images described above are built on a matrix of the following base images and platforms:

- [debian/debian:12-slim](https://github.com/debuerreotype/docker-debian-artifacts/blob/d99a48edaa18ad2bbb260c388b274c8c093f2d32/bullseye/slim/Dockerfile), (AKA "bookworm") tagged with the following suffixes:
  - `-debian-amd64`: Image manifest for the `linux/amd64` platform.
  - `-debian-arm64`: Image manifest for the `linux/arm64` platform.
  - `-debian`:  Manifest list of `-debian-amd64` and `-debian-arm64`.  Executing `docker pull` against this tag will grab the appropriate image for the supported platform you are currently running, and thus should be the default choice.
- [redhat/ubi9-minimal](https://hub.docker.com/r/redhat/ubi9-minimal), tagged with a suffix of `-ubi`.  UBI images use [`microdnf`](https://github.com/rpm-software-management/microdnf) as a package manager instead of yum to minimize the size of the image.  We currently only support `linux/amd64` for our UBI SDK images.

Images with no suffix tag are identical to the corresponding `-debian` tag.

Images are pushed to:

* [Docker Hub](https://hub.docker.com/u/pulumi)
* [Amazon ECR Public Gallery](https://gallery.ecr.aws/pulumi/)
* [GitHub Container Registry](https://github.com/orgs/pulumi/packages)

## Language Versions

Images without a version suffix use the following language versions by default:

 - .NET 8.0
 - Go 1.24
 - JDK 21
 - Node.js 24
 - Python 3.13

### Version Policy

Language runtimes are kept up-to-date with current LTS versions. For Python, the default version corresponds to the release prior to the latest release, for other languages the default version corresponds to the latest release. You can pin the image tag to a particular version in order to avoid unintended upgrades.

### Choosing a Language Version

For the language specific slim images, you can choose a specific version of the language runtime by using the suffixed images. For example to use Node.js 22, you would use `pulumi/pulumi-nodejs-22`, for Python 3.12, you would use `pulumi/pulumi-python-3.12`, etc.

For the kitchen sink image (`pulumi/pulumi`), choosing a specific version depends on the language.

#### .NET

The `pulumi/pulumi` image includes .NET 6.0 and 8.0. The `TargetFramework` property in your project’s `.csproj` or `.fsproj` file determines which SDK is used.

```xml
﻿<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    ...
```

#### Go

The Go version used to compile your program is determined by the `go` statement in your Pulumi project's `go.mod` file, see [Go Toolchains](https://go.dev/doc/toolchain).

#### Java

The images currently only ship a single version of the JDK, which is 17.

#### Node.js

The `pulumi/pulumi` image uses [fnm](https://github.com/Schniz/fnm) to manage Node.js versions, and comes with the latest patch releases of Node.js 18, 20 and 22 preinstalled. To select a specific version, create a `.node-version` file in your project directory with the desired version number, and run the command `pulumi install --use-language-version-tools`. This will setup the aliases for the image's default version of Node.js, npm, and other Node.js specific tools in `/usr/local/share/fnm/aliases/default/bin`.

To avoid downloading Node.js versions on each run, it is recommended to only specify the major version number, for example `22`. This ensures that the pre-installed version is used.

If you are building your own image by extending the `pulumi/pulumi` image, you can use the `fnm` command `fnm alias ${MY_NODEJS_VERSION} default` to configure the default version of Node.js to be used in your image.

#### Python

The `pulumi/pulumi` image uses [pyenv](https://github.com/pyenv/pyenv) to manage Python versions, and comes with Python 3.10 to 3.14 preinstalled. To select a specific version, create a `.python-version` file in your project directory with the desired version number.

To avoid downloading and building Python versions on each run, it is recommended to only specify the major version number, for example `3.12`. This ensures that the pre-installed version of Python 3.12 is used.

## Scanning

Images are scanned nightly for vulnerabilities.  Results are checked periodically for issues that can be remediated (best effort), however there are some issues over which we have no control, e.g. vulnerabilities in base images for which there is no known remediation.

## Considerations

The base and SDK images _do not_ include additional tools you might want to use when running a Pulumi provider. For example, if you're using the [pulumi-kubernetes](https://github.com/pulumi/pulumi-kubernetes) provider with [Helm](https://helm.sh/), you'll need to use these images as a base image, and install `helm` as part of your CI setup.

## Release Cadence

The images in this repository are released automatically as part of the release process for the `pulumi` CLI. You can expect **new minor releases** roughly every week, with patch releases more frequently as necessary.

The image tags for each image in this repository mirror the git tags on the `pulumi` CLI. Thus, when [`pulumi v3.35.1`](https://github.com/pulumi/pulumi/releases) is released, you will find a corresponding Docker image [`pulumi/pulumi:3.35.1`](https://hub.docker.com/r/pulumi/pulumi) in DockerHub, ECR, and GHCR.
