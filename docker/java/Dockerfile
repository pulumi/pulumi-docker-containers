# syntax = docker/dockerfile:experimental@sha256:600e5c62eedff338b3f7a0850beb7c05866e0ef27b2d2e8c02aa468e78496ff5
# Interim container so we can copy pulumi binaries
# Must be defined first
FROM debian:trixie-slim AS builder
ARG PULUMI_VERSION
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    curl && \
    rm -rf /var/lib/apt/lists/*

# Install the Pulumi SDK, including the CLI and language runtimes.
RUN curl -fsSL https://get.pulumi.com/ | bash -s -- --version $PULUMI_VERSION

# The runtime container
FROM debian:trixie-slim
LABEL org.opencontainers.image.description="Pulumi CLI container for java"
WORKDIR /pulumi/projects

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    curl \
    git \
    openjdk-21-jdk \
    maven \
    gradle && \
    rm -rf /var/lib/apt/lists/*

# Uses the workdir, copies from pulumi interim container
COPY --from=builder /root/.pulumi/bin/pulumi /pulumi/bin/pulumi
COPY --from=builder /root/.pulumi/bin/*-java* /pulumi/bin/
ENV PATH "/pulumi/bin:${PATH}"

CMD ["pulumi"]
