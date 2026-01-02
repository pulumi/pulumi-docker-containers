# CHANGELOG

## Unreleased

- Update Debian-based images to Debian Trixie (13).
- Remove Node.js 23 support (EOL).

## 3.211.0

- Update default Python version to 3.13 & add Python 3.14 to the kitchen sink image
  ([#595](https://github.com/pulumi/pulumi-docker-containers/issues/595))

## 3.209.0

- Update default Python version to 3.13 & add a Python 3.14 standalone image
  ([#555](https://github.com/pulumi/pulumi-docker-containers/pull/555))

## 3.202.0

- Provider Build Environment image: Update golangci-lint to v2
 ([#515](https://github.com/pulumi/pulumi-docker-containers/pull/515))

- Add tags and labels for dependabot
 ([#510](https://github.com/pulumi/pulumi-docker-containers/pull/510))

- Add Bun to allow using it as a package manager for Node.js programs
 ([#509](https://github.com/pulumi/pulumi-docker-containers/pull/509))

- Add pnpm to Node.js images
 ([#509](https://github.com/pulumi/pulumi-docker-containers/pull/509))

- Fix pushing all image variants of pulumi/pulumi to ECR and GHCR
  ([#492](https://github.com/pulumi/pulumi-docker-containers/pull/492))

## 3.178.0

- Pin Gradle to 8.14.2 and Maven to 3.9.10 in the UBI Java image
  ([#487](https://github.com/pulumi/pulumi-docker-containers/pull/487))

## 3.175.0

- Ensure we install Yarn classic
  ([#480](https://github.com/pulumi/pulumi-docker-containers/pull/480))

## 3.171.0

- Support Node.js 24
  ([#464](https://github.com/pulumi/pulumi-docker-containers/pull/464))

## 3.167.0

- Update corepack
  ([#391](https://github.com/pulumi/pulumi-docker-containers/pull/391))
- Drop .NET 6.0 container
  ([#436](https://github.com/pulumi/pulumi-docker-containers/pull/436))
- Drop .NET 6.0 from kitchen sink
  ([#437](https://github.com/pulumi/pulumi-docker-containers/pull/437))
- Update tools in build-environment
  ([#441](https://github.com/pulumi/pulumi-docker-containers/pull/441))
- Update aws-iam-authenticator to 0.6.31
  ([#442](https://github.com/pulumi/pulumi-docker-containers/pull/442))
- Update to Go 1.24
  ([#443](https://github.com/pulumi/pulumi-docker-containers/pull/443))

## 3.147.0

- Add ARM64 version of the kitchen sink and provider build environment images
  ([#377](https://github.com/pulumi/pulumi-docker-containers/pull/377))

## 3.146.0

- Update to redhat/ubi9 for UBI based images
  ([#342](https://github.com/pulumi/pulumi-docker-containers/pull/342))

- Update Poetry config for the Poetry 2.0 release
  ([#353](https://github.com/pulumi/pulumi-docker-containers/pull/353)

## 3.144.0

- Update Go container to debian 12 (bookworm) slim as base image
  ([#347](https://github.com/pulumi/pulumi-docker-containers/pull/347))

- Update aws-iam-authenticator to version 0.6.29
  ([#345](https://github.com/pulumi/pulumi-docker-containers/pull/345))

- Include uv in images that provide Python
  -([341](https://github.com/pulumi/pulumi-docker-containers/pull/341))

- Default to Python 3.12 instead of 3.13
  ([335](https://github.com/pulumi/pulumi-docker-containers/pull/335))

- Install Python and Node.js in the UBI containers using pyenv and fnm
  ([326])https://github.com/pulumi/pulumi-docker-containers/pull/326))

- Update default language versions
  ([324](https://github.com/pulumi/pulumi-docker-containers/pull/324))

- Add .NET 9.0 to the kitchen sink and as per-language version
  ([#318](https://github.com/pulumi/pulumi-docker-containers/pull/318)

- Add Node.js 23 and Python 3.13 to the kitchen sink and as per-language versions
  ([#309](https://github.com/pulumi/pulumi-docker-containers/pull/309)

- Add nonroot variant for the kitchen sink image
([#277](https://github.com/pulumi/pulumi-docker-containers/pull/277)

- Add per language versions for ubi images
  ([#260](https://github.com/pulumi/pulumi-docker-containers/pull/260))

## 3.132.0

- Add dotnet 8.0 to the kitchen sink image
  ([#259](https://github.com/pulumi/pulumi-docker-containers/pull/259)

- Include fnm and Nodejs 18, 20 and 22 in the kitchen sink image
  ([#253](https://github.com/pulumi/pulumi-docker-containers/pull/253)

## 3.131.0

- Add per-language versions of the `pulumi/pulumi-dotnet` image
  ([#257](https://github.com/pulumi/pulumi-docker-containers/pull/257))

- Add per-language versions of the `pulumi/pulumi-nodejs` image
  ([#255](https://github.com/pulumi/pulumi-docker-containers/pull/255))

- Include jq in the kitchen sink image
  ([#258](https://github.com/pulumi/pulumi-docker-containers/pull/258))

- Include pyenv and Python 3.9 to 3.12 in the kitchen sink image
  ([#232](https://github.com/pulumi/pulumi-docker-containers/pull/232))

## 3.130.0

- Add $GOPATH/bin to $PATH for Go containers
  ([249](https://github.com/pulumi/pulumi-docker-containers/pull/249))

- Ensure corepack is installed in the `pulumi/pulumi` image
  ([#247](https://github.com/pulumi/pulumi-docker-containers/pull/247))

- Add Poetry to Python images ([#240](https://github.com/pulumi/pulumi-docker-containers/pull/240))

## 3.128.0

- Update to debian 12 (bookworm) slim as base image
  ([#236](https://github.com/pulumi/pulumi-docker-containers/pull/236))

- Add per-language versions of the `pulumi/pulumi-python` image
  ([#226](https://github.com/pulumi/pulumi-docker-containers/pull/226))

- Unpin Azure CLI tools ([#214])(https://github.com/pulumi/pulumi-docker-containers/pull/214))

- Ensure that the containers are compatible with deployments
  ([#219])(https://github.com/pulumi/pulumi-docker-containers/pull/219)

- Test AWS CLI and templates in the `pulumi/pulumi` image
  ([#213](https://github.com/pulumi/pulumi-docker-containers/pull/213))

- Fix compilation issue when running `azure-java` in `pulumi-java`
  ([#212](https://github.com/pulumi/pulumi-docker-containers/pull/212))

- Test Azure CLI and templates in the `pulumi/pulumi` image
  ([#208](https://github.com/pulumi/pulumi-docker-containers/pull/208))

## 3.117.0

- Revert adding Oracle Cloud Infrastructure CLI (oci-cli)
  ([#195](https://github.com/pulumi/pulumi-docker-containers/pull/195))

## 3.116.0

- Add Oracle Cloud Infrastructure CLI (oci-cli)
  ([#182](https://github.com/pulumi/pulumi-docker-containers/pull/182))

## 3.112.0

- Install the latest version of `npm` in the `pulumi/nodejs` image
  ([#190](https://github.com/pulumi/pulumi-docker-containers/pull/190))

## 3.87.0

- Upgrade Go to 1.21.1. ([#159](https://github.com/pulumi/pulumi-docker-containers/pull/159))

## 3.82.0

- Upgrade Node.js in the `pulumi/pulumi` image and `pulumi/nodejs` UBI image to the Active LTS version 18
  ([#150](https://github.com/pulumi/pulumi-docker-containers/pull/150))

## 3.63.0

- Upgrade Go to 1.20.3. ([#134](https://github.com/pulumi/pulumi-docker-containers/pull/134))
