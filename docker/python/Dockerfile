# syntax = docker/dockerfile:experimental
# Interim container so we can copy pulumi binaries
# Must be defined first
ARG LANGUAGE_VERSION

FROM debian:bookworm-slim AS builder
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
FROM python:${LANGUAGE_VERSION}-slim-bookworm
LABEL org.opencontainers.image.description="Pulumi CLI container for python"
WORKDIR /pulumi/projects

# Install needed tools, like git
RUN apt-get update -y && \
    apt-get install -y \
    curl \
    git \
    ca-certificates

# Install poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local/share/pypoetry python3 -
RUN ln -s /usr/local/share/pypoetry/bin/poetry /usr/local/bin/

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | XDG_BIN_HOME=/usr/local/share/uv bash -s -- --no-modify-path
RUN ln -s /usr/local/share/uv/uv /usr/local/bin/
RUN ln -s /usr/local/share/uv/uvx /usr/local/bin/

# Uses the workdir, copies from pulumi interim container
COPY --from=builder /root/.pulumi/bin/pulumi /pulumi/bin/pulumi
COPY --from=builder /root/.pulumi/bin/*-python* /pulumi/bin/
ENV PATH "/pulumi/bin:${PATH}"

CMD ["pulumi"]
