# syntax = docker/dockerfile:experimental
# Interim container so we can copy pulumi binaries
# Must be defined first

# Build container
FROM ubuntu:bionic AS builder

ARG PULUMI_VERSION
ARG GO_RUNTIME_VERSION=1.20.3
ENV GO_RUNTIME_386_SHA256 e12384311403f1389d14cc1c1295bfb4e0dd5ab919403b80da429f671a223507
ENV GO_RUNTIME_AMD64_SHA256 979694c2c25c735755bf26f4f45e19e64e4811d661dd07b8c010f7a8e18adfca
ENV GO_RUNTIME_ARM64_SHA256 eb186529f13f901e7a2c4438a05c2cd90d74706aaa0a888469b2a4a617b6ee54
ENV GO_RUNTIME_ARMV6L_SHA256 b421e90469a83671641f81b6e20df6500f033e9523e89cbe7b7223704dd1035c

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
