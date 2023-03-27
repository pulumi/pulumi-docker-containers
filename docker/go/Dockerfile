# syntax = docker/dockerfile:experimental
# Interim container so we can copy pulumi binaries
# Must be defined first

# Build container
FROM ubuntu:bionic AS builder

ARG PULUMI_VERSION
ARG GO_RUNTIME_VERSION=1.20.2
ENV GO_RUNTIME_386_SHA256 ee240ed33ae57504c41f04c12236aeaa17fbeb6ea9fcd096cd9dc7a89d10d4db
ENV GO_RUNTIME_AMD64_SHA256 4eaea32f59cde4dc635fbc42161031d13e1c780b87097f4b4234cfce671f1768
ENV GO_RUNTIME_ARM64_SHA256 78d632915bb75e9a6356a47a42625fd1a785c83a64a643fedd8f61e31b1b3bef
ENV GO_RUNTIME_ARMV6L_SHA256 d79d56bafd6b52b8d8cbe3f8e967caaac5383a23d7a4fa9ac0e89778cd16a076

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
ENV PATH "/pulumi/bin:${PATH}"

CMD ["pulumi"]
