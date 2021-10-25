# pulumi-docker-images

This repository contains the official Pulumi docker images.  Pulumi publishes and supports the following images:

- [`pulumi/pulumi`](https://hub.docker.com/r/pulumi/pulumi): A "kitchen sink" image that includes the Pulumi CLI and all supported SDKs (Golang, Python, Node, Dotnet).
- [`pulumi/pulumi-base`](https://hub.docker.com/r/pulumi/pulumi-go): A slim image that contains the Pulumi CLI, but no SDK(s).
- [`pulumi/pulumi-go`](https://hub.docker.com/r/pulumi/pulumi-go): A slim image that contains the Pulumi CLI along with the Golang Pulumi SDK.
- [`pulumi/pulumi-python`](https://hub.docker.com/r/pulumi/pulumi-python): A slim image that contains the Pulumi CLI along with the Python runtime and Pulumi SDK.
- [`pulumi/pulumi-nodejs`](https://hub.docker.com/r/pulumi/pulumi-nodejs): A slim image that contains the Pulumi CLI along with the Node runtime and Pulumi SDK and is suitable for both TypeScript and JavaScript development.
- [`pulumi/pulumi-dotnet`](https://hub.docker.com/r/pulumi/pulumi-dotnet): A slim image that contains the Pulumi CLI along with the .NET runtime and Pulumi SDK.

Tags on each image match the installed version of Pulumi.  `latest` matches the latest production version of Pulumi.

The base and SDK-specific images are considerably smaller than the combined `pulumi/pulumi` container (100 to 150 MB, compared to ~1 GB for the combined image, depending on the base OS).

## Build Matrix

In addition, each of the images above (except the full `pulumi/pulumi` image) are built on a matrix of the following OS base images:

- [redhat/ubi-minimal](https://hub.docker.com/r/redhat/ubi8-minimal), tagged with a suffix of `-ubi`.  UBI images use [`microdnf`](https://github.com/rpm-software-management/microdnf) as a package manager instead of yum to minimize the size of the image.
- [debian/debian:buster-slim](https://hub.docker.com/layers/debian/library/debian/buster-slim/images/sha256-56983a389d63d1a094980897864c44d6ac3da4a91a5594992388a87f34ffaf22?context=explore), tagged with a suffix of `-debian`.

Images with no suffix tag are identical to the corresponding `-debian` tag.

Pulumi currently only supports the `linux/amd64` platform.  `linux/arm64` support is a work currently in progress.

Images are pushed to both [Docker Hub](https://hub.docker.com/u/pulumi) and the [Amazon ECR Public Gallery](https://gallery.ecr.aws/pulumi/).

## Scanning

Images are scanned nightly for vulnerabilities.  Results are checked periodically for issues that can be remediated (best effort), however there are some issues over which we have no control, e.g. vulnerabilities in base images for which there is no known remediation.

## Usage

In order to try and keep the images flexible and try to meet as many use cases as possible, none of these images have `CMD` or entrypoint set, so you'll need to specify the commands you want to run, for example:

```bash
docker run -e PULUMI_ACCESS_TOKEN=<TOKEN> -v "$(pwd)":/pulumi/projects $IMG /bin/bash -c "npm ci && pulumi preview -s <stackname>"
```

## Considerations

The base and SDK images _do not_ include additional tools you might want to use when running a pulumi provider. For example, if you're using the [pulumi-kubernetes](https://github.com/pulumi/pulumi-kubernetes) with [Helm](https://helm.sh/), you'll need to use these images as a base image, or install the `helm` command as part of your CI setup.
