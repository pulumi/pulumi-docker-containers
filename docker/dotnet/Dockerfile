# syntax = docker/dockerfile:experimental

FROM debian:bookworm-slim AS builder
SHELL ["/bin/bash", "-o", "errexit", "-o", "nounset", "-o", "pipefail", "-c"]
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
FROM debian:bookworm-slim
SHELL ["/bin/bash", "-o", "errexit", "-o", "nounset", "-o", "pipefail", "-c"]
LABEL org.opencontainers.image.description="Pulumi CLI container for dotnet"
WORKDIR /pulumi/projects

ARG LANGUAGE_VERSION

RUN apt-get update -y && \
    apt-get install -y \
    git \
    curl

# Install dotnet 6.0 using instructions from:
# https://docs.microsoft.com/en-us/dotnet/core/tools/dotnet-install-script
RUN curl -fsSL https://dot.net/v1/dotnet-install.sh | bash -s -- -channel ${LANGUAGE_VERSION}

# Uses the workdir, copies from pulumi interim container
COPY --from=builder /root/.pulumi/bin/pulumi /pulumi/bin/pulumi
COPY --from=builder /root/.pulumi/bin/*-dotnet* /pulumi/bin/

ENV PATH "/root/.dotnet:/pulumi/bin:${PATH}"
ENV DOTNET_ROOT /root/.dotnet
ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT 1
# Allow newer dotnet version (e.g. 6) to build projects targeting older frameworks (v3.1)
ENV DOTNET_ROLL_FORWARD Major

CMD ["pulumi"]
