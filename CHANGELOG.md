# CHANGELOG

Container versions follow the Pulumi CLI version. Entries describe container-specific changes.

See [legacy history](.changes/legacy.md) for the changelog before automated releases,
including the original Unreleased section whose release assignments were not recorded.

## 3.273.0

### Bug Fixes

- [all] Remove the temporary UBI CA trust workaround now that updated ca-certificates packages remove the affected eMudhra trust roots

Includes [Pulumi CLI 3.273.0](https://github.com/pulumi/pulumi/releases/tag/v3.273.0).

Container source: `8d69802ca81863d52d6c0baf4a1537165dacc638`.

## 3.272.0

Includes [Pulumi CLI 3.272.0](https://github.com/pulumi/pulumi/releases/tag/v3.272.0).

Container source: `24e07ce5be8bec15293139ae1eeace2535486432`.

## 3.271.0

### Bug Fixes

- [pulumi] Pre-install the Java language runtime, which the Pulumi CLI no longer bundles
- [pulumi-java] Pre-install the Java language runtime, which the Pulumi CLI no longer bundles

### Security

- [all] Update Go to 1.26.10, npm to 11.21.1, GoReleaser to 2.18.3, golangci-lint to 2.15.0, and aws-iam-authenticator to 0.7.23.
- [all] Update container certificate trust stores and Python packaging tools to address security findings.

Includes [Pulumi CLI 3.271.0](https://github.com/pulumi/pulumi/releases/tag/v3.271.0).

Container source: `0066e7922e7e2c6f994f9d71835e678b25968311`.

## 3.270.0

Includes [Pulumi CLI 3.270.0](https://github.com/pulumi/pulumi/releases/tag/v3.270.0).

Container source: `7871407a4b9c1bc02555b69550f96d62fcf5db95`.

## 3.269.0

Includes [Pulumi CLI 3.269.0](https://github.com/pulumi/pulumi/releases/tag/v3.269.0).

Container source: `be529e65b3ee8409ad9284f0f3b91de51325ac7d`.

## 3.268.0

Includes [Pulumi CLI 3.268.0](https://github.com/pulumi/pulumi/releases/tag/v3.268.0).

Container source: `abc2fe79833a460198810dc183158f680ef3113a`.

## 3.267.0

Includes [Pulumi CLI 3.267.0](https://github.com/pulumi/pulumi/releases/tag/v3.267.0).

Container source: `f06735b1adf012c31409de901ab5741594244b6c`.

## 3.266.0

Includes [Pulumi CLI 3.266.0](https://github.com/pulumi/pulumi/releases/tag/v3.266.0).

Container source: `6ca1d7d98c343d00c51c466bccf6e68f1ee43de5`.

## 3.265.0

Includes [Pulumi CLI 3.265.0](https://github.com/pulumi/pulumi/releases/tag/v3.265.0).

Container source: `0623906244d396d6d237e871aeb778c74a046c10`.

## 3.264.0

### Security

- [all] Run apt-get upgrade to pick up updates not baked into the base image yet

Includes [Pulumi CLI 3.264.0](https://github.com/pulumi/pulumi/releases/tag/v3.264.0).

Container source: `8f90139cac3cc6ef804b08d531e1a1f553649b5d`.
