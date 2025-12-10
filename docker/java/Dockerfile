# syntax = docker/dockerfile:experimental@sha256:600e5c62eedff338b3f7a0850beb7c05866e0ef27b2d2e8c02aa468e78496ff5
# Interim container so we can copy pulumi binaries
# Must be defined first
FROM debian:bookworm-slim@sha256:e899040a73d36e2b36fa33216943539d9957cba8172b858097c2cabcdb20a3e2 AS builder
ARG PULUMI_VERSION
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    curl && \
    rm -rf /var/lib/apt/lists/*

# Install the Pulumi SDK, including the CLI and language runtimes.
RUN curl -fsSL https://get.pulumi.com/ | bash -s -- --version $PULUMI_VERSION

# The runtime container
FROM debian:bookworm-slim@sha256:e899040a73d36e2b36fa33216943539d9957cba8172b858097c2cabcdb20a3e2
LABEL org.opencontainers.image.description="Pulumi CLI container for java"
WORKDIR /pulumi/projects

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    curl \
    git \
    lsb-release && \
    rm -rf /var/lib/apt/lists/*

# https://learn.microsoft.com/en-gb/java/openjdk/install
RUN curl https://packages.microsoft.com/config/debian/$(lsb_release -rs)/packages-microsoft-prod.deb -o packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    rm packages-microsoft-prod.deb

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    msopenjdk-21 \
    maven \
    gradle && \
    rm -rf /var/lib/apt/lists/*

# Uses the workdir, copies from pulumi interim container
COPY --from=builder /root/.pulumi/bin/pulumi /pulumi/bin/pulumi
COPY --from=builder /root/.pulumi/bin/*-java* /pulumi/bin/
COPY --from=builder /root/.pulumi/bin/pulumi-analyzer-policy /pulumi/bin/
ENV PATH "/pulumi/bin:${PATH}"

CMD ["pulumi"]
