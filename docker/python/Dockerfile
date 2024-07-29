# syntax = docker/dockerfile:experimental
# Interim container so we can copy pulumi binaries
# Must be defined first
ARG LANGUAGE_VERSION

FROM debian:buster-slim AS builder
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
FROM python:${LANGUAGE_VERSION}-slim
LABEL org.opencontainers.image.description="Pulumi CLI container for python"
WORKDIR /pulumi/projects

# Install needed tools, like git
RUN apt-get update -y && \
    apt-get install -y \
    curl \
    git \
    ca-certificates

# Uses the workdir, copies from pulumi interim container
COPY --from=builder /root/.pulumi/bin/pulumi /pulumi/bin/pulumi
COPY --from=builder /root/.pulumi/bin/*-python* /pulumi/bin/
ENV PATH "/pulumi/bin:${PATH}"

CMD ["pulumi"]
