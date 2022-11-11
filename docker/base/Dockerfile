# syntax = docker/dockerfile:experimental
FROM debian:11-slim AS builder
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
FROM debian:11-slim
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
