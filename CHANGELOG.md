# CHANGELOG

## Unreleased

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

- Unpin Azure CLI tools ([#214])(https://github.com/pulumi/pulumi-docker-containers/pull/214)

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
