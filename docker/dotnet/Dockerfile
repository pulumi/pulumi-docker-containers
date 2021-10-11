# syntax = docker/dockerfile:experimental
# Interim container so we can copy pulumi binaries
# Must be defined first
ARG PULUMI_VERSION=latest
ARG PULUMI_IMAGE=pulumi/pulumi-base
FROM ${PULUMI_IMAGE}:${PULUMI_VERSION} as pulumi

# Build container
FROM ubuntu:bionic AS builder
WORKDIR /dotnet
RUN apt-get update -y && \
    apt-get install -y \
    curl \
    gpg
RUN curl -o - https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /tmp/microsoft.asc.gpg; \
    curl -o /tmp/microsoft-prod.list https://packages.microsoft.com/config/debian/10/prod.list

# The runtime container
FROM debian:buster-slim
WORKDIR /pulumi/projects

ARG DOTNET_RUNTIME_VERSION="3.1"

RUN apt-get update -y && \
    apt-get install -y \
    git \
    curl

# arm64 packages are not available in apt-get, per
# https://docs.microsoft.com/en-us/dotnet/core/install/linux-debian, so we need
# to install via another method:
RUN curl -fsSL https://dot.net/v1/dotnet-install.sh | bash -s -- -c ${DOTNET_RUNTIME_VERSION} && \
    echo "PATH=$PATH:$HOME/.dotnet" >> ~/.bashrc && \
    echo "export DOTNET_ROOT=$HOME/.dotnet" >> ~/.bashrc

# Uses the workdir, copies from pulumi interim container
COPY --from=pulumi /pulumi/bin/pulumi /pulumi/bin/pulumi
COPY --from=pulumi /pulumi/bin/*-dotnet* /pulumi/bin/
ENV PATH "/pulumi/bin:${PATH}"

CMD ["pulumi"]
