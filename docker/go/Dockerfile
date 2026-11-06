# syntax = docker/dockerfile:experimental@sha256:600e5c62eedff338b3f7a0850beb7c05866e0ef27b2d2e8c02aa468e78496ff5
# Interim container so we can copy pulumi binaries
# Must be defined first

# Build container
FROM ubuntu:noble@sha256:c35e29c9450151419d9448b0fd75374fec4fff364a27f176fb458d472dfc9e54 AS builder

ARG PULUMI_VERSION
# Set from .github/scripts/matrix/versions.py by the build workflows.
ARG LANGUAGE_VERSION
ARG GO_AMD64_SHA256
ARG GO_ARM64_SHA256

WORKDIR /golang
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
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
    GO_SHA256="${GO_ARM64_SHA256}" \
    ;; \
    x86_64) \
    ARCH="amd64" \
    GO_SHA256="${GO_AMD64_SHA256}" \
    ;; \
    esac && \
    curl -fsSLo /tmp/go.tgz https://golang.org/dl/go${LANGUAGE_VERSION:?}.linux-${ARCH}.tar.gz && \
    echo "${GO_SHA256:?} /tmp/go.tgz" | sha256sum -c - && \
    mkdir -p bin && \
    tar -C /golang -xzf /tmp/go.tgz && \
    rm /tmp/go.tgz && \
    export PATH="/golang/go/bin:${PATH}" && \
    go version

# The runtime container
FROM debian:trixie-slim
LABEL org.opencontainers.image.description="Pulumi CLI container for go"
WORKDIR /pulumi/projects

# Install needed tools, like git
RUN --mount=target=/var/lib/apt/lists,type=cache \
    --mount=target=/var/cache/apt,type=cache \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    curl \
    git \
    ca-certificates

RUN mkdir -p /go

# Uses the workdir
COPY --from=builder /golang/go /usr/local
# Uses the workdir, copies from pulumi interim container
COPY --from=builder /root/.pulumi/bin/pulumi /pulumi/bin/pulumi
COPY --from=builder /root/.pulumi/bin/pulumi-language-go /pulumi/bin/pulumi-language-go
ENV GOPATH=/go
ENV CGO_ENABLED=0
ENV PATH "/pulumi/bin:${GOPATH}/bin:${PATH}"

CMD ["pulumi"]
