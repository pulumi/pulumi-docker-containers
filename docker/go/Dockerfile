# syntax = docker/dockerfile:experimental
# Interim container so we can copy pulumi binaries
# Must be defined first

# Build container
FROM ubuntu:bionic AS builder
SHELL ["/bin/bash", "-o", "errexit", "-o", "nounset", "-o", "pipefail", "-c"]

ARG PULUMI_VERSION
ARG GO_RUNTIME_VERSION=1.23.3
ENV GO_RUNTIME_386_SHA256 3d7b00191a43c50d28e0903a0c576104bc7e171a8670de419d41111c08dfa299
ENV GO_RUNTIME_AMD64_SHA256 a0afb9744c00648bafb1b90b4aba5bdb86f424f02f9275399ce0c20b93a2c3a8
ENV GO_RUNTIME_ARM64_SHA256 1f7cbd7f668ea32a107ecd41b6488aaee1f5d77a66efd885b175494439d4e1ce
ENV GO_RUNTIME_ARMV6L_SHA256 5f0332754beffc65af65a7b2da76e9dd997567d0d81b6f4f71d3588dc7b4cb00

WORKDIR /golang
RUN apt-get update -y && \
    apt-get install -y \
    curl \
    git \
    build-essential \
    tar \
    git

# Install the Pulumi SDK, including the CLI and language runtimes.
RUN curl -fsSL https://get.pulumi.com/ | bash -s -- --version $PULUMI_VERSION

RUN case $(uname -m) in \
    aarch64) \
    ARCH="arm64" \
    GO_RUNTIME_SHA256="${GO_RUNTIME_ARM64_SHA256}" \
    ;; \
    x86_64) \
    ARCH="amd64" \
    GO_RUNTIME_SHA256="${GO_RUNTIME_AMD64_SHA256}" \
    ;; \
    386) \
    ARCH="386" \
    GO_RUNTIME_SHA256="${GO_RUNTIME_386_SHA256}" \
    ;; \
    armv6l) \
    ARCH="armv6l" \
    GO_RUNTIME_SHA256="${GO_RUNTIME_ARMV6L_SHA256}" \
    ;; \
    esac && \
    curl -fsSLo /tmp/go.tgz https://golang.org/dl/go${GO_RUNTIME_VERSION}.linux-${ARCH}.tar.gz && \
    echo "${GO_RUNTIME_SHA256} /tmp/go.tgz" | sha256sum -c -; \
    mkdir -p bin; \
    tar -C /golang -xzf /tmp/go.tgz; \
    rm /tmp/go.tgz; \
    export PATH="/golang/go/bin:${PATH}"; \
    go version

# The runtime container
FROM debian:11-slim
SHELL ["/bin/bash", "-o", "errexit", "-o", "nounset", "-o", "pipefail", "-c"]
LABEL org.opencontainers.image.description="Pulumi CLI container for go"
WORKDIR /pulumi/projects

# Install needed tools, like git
RUN --mount=target=/var/lib/apt/lists,type=cache \
    --mount=target=/var/cache/apt,type=cache \
    apt-get update -y && \
    apt-get install -y \
    curl \
    git \
    ca-certificates; \
    mkdir -p /go

# Uses the workdir
COPY --from=builder /golang/go /usr/local
# Uses the workdir, copies from pulumi interim container
COPY --from=builder /root/.pulumi/bin/pulumi /pulumi/bin/pulumi
COPY --from=builder /root/.pulumi/bin/pulumi-language-go /pulumi/bin/pulumi-language-go
COPY --from=builder /root/.pulumi/bin/pulumi-analyzer-policy /pulumi/bin/pulumi-analyzer-policy
ENV GOPATH=/go
ENV CGO_ENABLED=0
ENV PATH "/pulumi/bin:${GOPATH}/bin:${PATH}"

CMD ["pulumi"]
