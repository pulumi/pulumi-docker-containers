# pulumi-docker-containers

This repository contains the source for Pulumi's official Docker images.  Pulumi publishes and supports the following images:

- [`pulumi/pulumi`](https://hub.docker.com/r/pulumi/pulumi): A "kitchen sink" image that includes the Pulumi CLI and all supported SDKs (Golang, Python, Node, Dotnet, Java).
- [`pulumi/pulumi-base`](https://hub.docker.com/r/pulumi/pulumi-base): A slim image that contains the Pulumi CLI, but no SDK(s).
- [`pulumi/pulumi-go`](https://hub.docker.com/r/pulumi/pulumi-go): A slim image that contains the Pulumi CLI along with the Golang Pulumi SDK.
- [`pulumi/pulumi-python`](https://hub.docker.com/r/pulumi/pulumi-python): A slim image that contains the Pulumi CLI along with the Python runtime and Pulumi SDK. This image also exists in per-language versions for different Python versions: `pulumi/pulumi-python-3.9` to `pulumi/pulumi-python-3.12`. The `pulumi/pulumi-python` image is based on the default Python version, which is currently 3.9.
- [`pulumi/pulumi-nodejs`](https://hub.docker.com/r/pulumi/pulumi-nodejs): A slim image that contains the Pulumi CLI along with the Node runtime and Pulumi SDK and is suitable for both TypeScript and JavaScript development. This image also exists in per-language versions for different Node versions: `pulumi/pulumi-nodejs-18`, `pulumi/pulumi-nodejs-20` and `pulumi/pulumi-nodejs-22`. The `pulumi/pulumi-nodejs` image is based on the default Node version, which is currently 18.
- [`pulumi/pulumi-dotnet`](https://hub.docker.com/r/pulumi/pulumi-dotnet): A slim image that contains the Pulumi CLI along with the .NET runtime and Pulumi SDK. This image also exists in per-language versions for different .NET versions: `pulumi/pulumi-dotnet-6.0` to `pulumi/pulumi-dotnet-8.0`. The `pulumi/pulumi-dotnet` image is based on the default .NET version, which is currently 6.0.
- [`pulumi/pulumi-java`](https://hub.docker.com/r/pulumi/pulumi-java): A slim image that contains the Pulumi CLI along with the Java runtime and Pulumi SDK.

Tags on each image match the installed version of Pulumi.  The `latest` tag matches the latest production version of Pulumi.

The base and SDK-specific images are considerably smaller than the combined `pulumi/pulumi` container (200 to 300 MB, compared to ~2 GB for the combined image).

## Build Matrix

Each of the images described above (except the full `pulumi/pulumi` image) are built on a matrix of the following base images and platforms:

- [debian/debian:12-slim](https://github.com/debuerreotype/docker-debian-artifacts/blob/d99a48edaa18ad2bbb260c388b274c8c093f2d32/bullseye/slim/Dockerfile), (AKA "bookworm") tagged with the following suffixes:
  - `-debian-amd64`: Image manifest for the `linux/amd64` platform.
  - `-debian-arm64`: Image manifest for the `linux/arm64` platform.
  - `-debian`:  Manifest list of `-debian-amd64` and `-debian-arm64`.  Executing `docker pull` against this tag will grab the appropriate image for the supported platform you are currently running, and thus should be the default choice.
- [redhat/ubi8-minimal](https://hub.docker.com/r/redhat/ubi8-minimal), tagged with a suffix of `-ubi`.  UBI images use [`microdnf`](https://github.com/rpm-software-management/microdnf) as a package manager instead of yum to minimize the size of the image.  We currently only support `linux/amd64` for our UBI SDK images.

Images with no suffix tag are identical to the corresponding `-debian` tag.

Images are pushed to:

* [Docker Hub](https://hub.docker.com/u/pulumi)
* [Amazon ECR Public Gallery](https://gallery.ecr.aws/pulumi/)
* [GitHub Container Registry](https://github.com/orgs/pulumi/packages)

## Default Language Versions

- .NET 6.0
- Go 1.21
- JDK 11
- Node.js 18
- Python 3.9

### Version Policy

Language runtimes are kept up-to-date with current LTS versions. You can pin the image tag to a particular version in order to avoid unintended upgrades.

## Scanning

Images are scanned nightly for vulnerabilities.  Results are checked periodically for issues that can be remediated (best effort), however there are some issues over which we have no control, e.g. vulnerabilities in base images for which there is no known remediation.

## Usage

In order to try and keep the images flexible and try to meet as many use cases as possible, none of these images have `CMD` or entrypoint set, so you'll need to specify the commands you want to run, for example:

```bash
docker run -e PULUMI_ACCESS_TOKEN=<TOKEN> -v "$(pwd)":/pulumi/projects $IMG /bin/bash -c "npm ci && pulumi preview -s <stackname>"
```

## Considerations

The base and SDK images _do not_ include additional tools you might want to use when running a Pulumi provider. For example, if you're using the [pulumi-kubernetes](https://github.com/pulumi/pulumi-kubernetes) provider with [Helm](https://helm.sh/), you'll need to use these images as a base image, and install `helm` as part of your CI setup.

## Release Cadence

The images in this repository are released automatically as part of the release process for the `pulumi` CLI. You can expect **new minor releases** roughly every week, with patch releases more frequently as necessary.

The image tags for each image in this repository mirror the git tags on the `pulumi` CLI. Thus, when [`pulumi v3.35.1`](https://github.com/pulumi/pulumi/releases) is released, you will find a corresponding Docker image [`pulumi/pulumi:3.35.1`](https://hub.docker.com/r/pulumi/pulumi) in DockerHub, ECR, and GHCR.
