# syntax = docker/dockerfile:experimental
# Interim container so we can copy pulumi binaries
# Must be defined first

# Build container
FROM ubuntu:bionic AS builder

ARG PULUMI_VERSION
ARG GO_RUNTIME_VERSION=1.17.3

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
    ;; \
    x86_64) \
    ARCH="amd64" \
    ;; \
    *) \
    ARCH=$(uname -m) \
    ;; \
    esac && \
    curl -fsSLo /tmp/go.tgz https://golang.org/dl/go${GO_RUNTIME_VERSION}.linux-${ARCH}.tar.gz; \
    mkdir -p bin; \
    tar -C /golang -xzf /tmp/go.tgz; \
    rm /tmp/go.tgz; \
    export PATH="/golang/go/bin:${PATH}"; \
    go version

# The runtime container
FROM debian:11-slim
LABEL org.opencontainers.image.description="Pulumi CLI container for go"
WORKDIR /pulumi/projects

# Install needed tools, like git
RUN --mount=target=/var/lib/apt/lists,type=cache \
    --mount=target=/var/cache/apt,type=cache \
    apt-get update -y && \
    apt-get install -y \
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
ENV PATH "/pulumi/bin:${PATH}"

CMD ["pulumi"]
