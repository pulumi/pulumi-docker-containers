# syntax = docker/dockerfile:experimental@sha256:600e5c62eedff338b3f7a0850beb7c05866e0ef27b2d2e8c02aa468e78496ff5
FROM debian:bookworm-slim@sha256:e899040a73d36e2b36fa33216943539d9957cba8172b858097c2cabcdb20a3e2 AS builder
ARG PULUMI_VERSION
RUN apt-get update -y && \
  apt-get upgrade -y && \
  apt-get install -y \
  curl \
  build-essential \
  git

# Install the Pulumi SDK, including the CLI and language runtimes.
RUN curl -fsSL https://get.pulumi.com/ | bash -s -- --version $PULUMI_VERSION

# The runtime container
# This is our base container, so let's copy all the runtimes to .pulumi/bin
FROM debian:bookworm-slim@sha256:e899040a73d36e2b36fa33216943539d9957cba8172b858097c2cabcdb20a3e2
LABEL org.opencontainers.image.description="Pulumi CLI container, bring your own SDK"
WORKDIR /pulumi
COPY --from=builder /root/.pulumi/bin bin

RUN --mount=target=/var/lib/apt/lists,type=cache \
  --mount=target=/var/cache/apt,type=cache \
  apt-get update -y && \
  apt-get upgrade -y && \
  apt-get install -y \
  curl \
  git \
  ca-certificates

ENV PATH "/pulumi/bin:${PATH}"
CMD ["pulumi"]
