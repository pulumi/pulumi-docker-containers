# syntax = docker/dockerfile:experimental
# Interim container so we can copy pulumi binaries
# Must be defined first
FROM debian:bullseye-slim AS builder
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
FROM eclipse-temurin:18.0.1_10-jdk
LABEL org.opencontainers.image.description="Pulumi CLI container for java"
WORKDIR /pulumi/projects

# Install needed tools, like git
RUN apt-get update -y && \
    apt-get install -y \
    git \
    ca-certificates \
    maven

# Uses the workdir, copies from pulumi interim container
COPY --from=builder /root/.pulumi/bin/pulumi /pulumi/bin/pulumi
COPY --from=builder /root/.pulumi/bin/*-java* /pulumi/bin/
COPY --from=builder /root/.pulumi/bin/pulumi-analyzer-policy /pulumi/bin/
ENV PATH "/pulumi/bin:${PATH}"

CMD ["pulumi"]
