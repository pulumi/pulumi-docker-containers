# syntax = docker/dockerfile:experimental@sha256:600e5c62eedff338b3f7a0850beb7c05866e0ef27b2d2e8c02aa468e78496ff5
# Interim container so we can copy pulumi binaries
# Must be defined first

# Build container
FROM ubuntu:noble@sha256:c35e29c9450151419d9448b0fd75374fec4fff364a27f176fb458d472dfc9e54 AS builder

ARG PULUMI_VERSION
ARG GO_RUNTIME_VERSION=1.26.10
ENV GO_RUNTIME_386_SHA256 fa05f9c9d71d08da81ae34f1b6baf8aacb05374b9a6fb223e92f7b29afc81148
ENV GO_RUNTIME_AMD64_SHA256 ccfe7ae822d2c2f41f4fe7c956199967a4dac22d0ee0d2b2bfdb440aab3b20c5
ENV GO_RUNTIME_ARM64_SHA256 3f4227ce7b206a513e794f1393adb473a07b46e94d18bd15d1c684bbb7319797
ENV GO_RUNTIME_ARMV6L_SHA256 7d89fd32259eb0ff647381e8c3465dc32ccfc7f71cb7b9bcd95604c3481f5109

WORKDIR /golang
RUN apt-get update -y && \
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
    echo "${GO_RUNTIME_SHA256} /tmp/go.tgz" | sha256sum -c - && \
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
