FROM golang:1.24-bookworm as builder

RUN go install sigs.k8s.io/aws-iam-authenticator/cmd/aws-iam-authenticator@v0.7.4

FROM debian:12 AS base

# These values are passed in by the build system automatically. The options are: arm64, amd64
# See: https://docs.docker.com/build/building/variables/#pre-defined-build-arguments
ARG TARGETARCH

LABEL "repository"="https://github.com/pulumi/pulumi"
LABEL "homepage"="https://pulumi.com"
LABEL "maintainer"="Pulumi Team <team@pulumi.com>"
LABEL org.opencontainers.image.description="The Pulumi CLI, in a Docker container."

ENV GOLANG_VERSION 1.24.5
ENV GOLANG_AMD64_SHA256 10ad9e86233e74c0f6590fe5426895de6bf388964210eac34a6d83f38918ecdc
ENV GOLANG_ARM64_SHA256 0df02e6aeb3d3c06c95ff201d575907c736d6c62cfa4b6934c11203f1d600ffa

# Install base dependencies
RUN apt-get update -y && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y \
  apt-transport-https \
  build-essential \
  ca-certificates \
  curl \
  git \
  jq \
  gnupg \
  libbz2-dev \
  libffi-dev \
  liblzma-dev \
  libncurses5-dev \
  libreadline-dev \
  libsqlite3-dev \
  libssl-dev \
  libxml2-dev \
  libxmlsec1-dev \
  lsb-release \
  software-properties-common \
  unzip  \
  wget \
  xz-utils \
  zlib1g-dev && \
  rm -rf /var/lib/apt/lists/*

# Install cloud tools
COPY --from=builder /go/bin/aws-iam-authenticator /usr/bin/aws-iam-authenticator
RUN \
  # Setup environment variables for architecture-specific packages
  if [ "$TARGETARCH" = "arm64" ]; then \
    AWSCLI_ARCH=aarch64; \
  else \
    AWSCLI_ARCH=x86_64; \
  fi && \
  # AWS v2 cli
  curl "https://awscli.amazonaws.com/awscli-exe-linux-${AWSCLI_ARCH}.zip" -o "awscliv2.zip" && \
  unzip awscliv2.zip && \
  ./aws/install && \
  rm -rf aws && \
  rm awscliv2.zip && \
  # Add additional apt repos
  curl -fsSL https://download.docker.com/linux/debian/gpg          | apt-key add - && \
  curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
  curl -fsSL https://packages.microsoft.com/keys/microsoft.asc     | apt-key add - && \
  echo "deb [arch=${TARGETARCH}] https://download.docker.com/linux/debian $(lsb_release -cs) stable"      | tee /etc/apt/sources.list.d/docker.list && \
  echo "deb http://packages.cloud.google.com/apt cloud-sdk-$(lsb_release -cs) main"               | tee /etc/apt/sources.list.d/google-cloud-sdk.list && \
  KUBE_LATEST=$(curl -L -s https://dl.k8s.io/release/stable.txt | awk 'BEGIN { FS="." } { printf "%s.%s", $1, $2 }') && \
  mkdir -p /etc/apt/keyrings && \
  curl -fsSL https://pkgs.k8s.io/core:/stable:/${KUBE_LATEST}/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg && \
  echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/${KUBE_LATEST}/deb/ /" | tee /etc/apt/sources.list.d/kubernetes.list && \
  echo "deb [arch=${TARGETARCH}] https://packages.microsoft.com/repos/azure-cli/ $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/azure.list && \
  # Install azure-cli, docker, gcloud, kubectl
  apt-get update -y && \
  apt-get install -y \
  azure-cli \
  docker-ce \
  google-cloud-sdk \
  google-cloud-sdk-gke-gcloud-auth-plugin \
  kubectl && \
  rm -rf /var/lib/apt/lists/*

# Install Go
RUN \
  # Setup environment variables for architecture-specific packages
  if [ "$TARGETARCH" = "arm64" ]; then \
    GOLANG_SHA256=$GOLANG_ARM64_SHA256; \
  else \
    GOLANG_SHA256=$GOLANG_AMD64_SHA256; \
  fi && \
  curl -fsSLo /tmp/go.tgz https://golang.org/dl/go${GOLANG_VERSION}.linux-${TARGETARCH}.tar.gz && \
  echo "${GOLANG_SHA256} /tmp/go.tgz" | sha256sum -c - && \
  tar -C /usr/local -xzf /tmp/go.tgz && \
  rm /tmp/go.tgz && \
  export PATH="/usr/local/go/bin:$PATH" && \
  go version
ENV GOPATH /go
ENV PATH $GOPATH/bin:/usr/local/go/bin:$PATH

# Install Java
# https://learn.microsoft.com/en-gb/java/openjdk/install
 RUN curl https://packages.microsoft.com/config/debian/$(lsb_release -rs)/packages-microsoft-prod.deb -o packages-microsoft-prod.deb && \
  dpkg -i packages-microsoft-prod.deb && \
  rm packages-microsoft-prod.deb

RUN apt-get update -y && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y \
  msopenjdk-21 \
  gradle \
  maven && \
  rm -rf /var/lib/apt/lists/*

# Install dotnet 8.0 and 9.0 using instructions from:
# https://docs.microsoft.com/en-us/dotnet/core/tools/dotnet-install-script
RUN curl -fsSL https://dot.net/v1/dotnet-install.sh | bash -s -- --channel 8.0 --install-dir /usr/local/share/dotnet
RUN curl -fsSL https://dot.net/v1/dotnet-install.sh | bash -s -- --channel 9.0 --install-dir /usr/local/share/dotnet
ENV PATH "/usr/local/share/dotnet:${PATH}"
ENV DOTNET_ROOT /usr/local/share/dotnet
ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT 1
# Allow newer dotnet version (e.g. 6) to build projects targeting older frameworks (v3.1)
ENV DOTNET_ROLL_FORWARD Major

# Install Helm
# Explicitly set env variables that helm reads to their defaults, so that subsequent calls to
# helm will find the stable repo even if $HOME points to something other than /root
# (e.g. in GitHub actions where $HOME points to /github/home).
ENV XDG_CONFIG_HOME=/root/.config
ENV XDG_CACHE_HOME=/root/.cache
RUN curl -L https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash && \
  helm repo add stable https://charts.helm.sh/stable && \
  helm repo update

# Python
# Install Pyenv and preinstall supported Python versions
RUN git clone --depth=1 https://github.com/pyenv/pyenv.git /usr/local/share/pyenv
ENV PYENV_ROOT /usr/local/share/pyenv
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"
RUN pyenv install 3.13
RUN pyenv install 3.12
RUN pyenv install 3.11
RUN pyenv install 3.10
RUN pyenv install 3.9
RUN pyenv global 3.12 # Default version
# Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local/share/pypoetry python3 -
RUN ln -s /usr/local/share/pypoetry/bin/poetry /usr/local/bin/
# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | XDG_BIN_HOME=/usr/local/share/uv bash -s -- --no-modify-path
RUN ln -s /usr/local/share/uv/uv /usr/local/bin/
RUN ln -s /usr/local/share/uv/uvx /usr/local/bin/

# Install default nodejs versions and associated tools
RUN curl -fsSL https://fnm.vercel.app/install | bash -s -- --install-dir "/usr/local/share/fnm" --skip-shell && \
  ln -s /usr/local/share/fnm/fnm /usr/local/bin/fnm
ENV FNM_COREPACK_ENABLED="true"
ENV FNM_VERSION_FILE_STRATEGY="recursive"
ENV FNM_DIR=/usr/local/share/fnm
RUN fnm install 20 && \
  fnm install 22 && \
  fnm install 23 && \
  fnm install 24 && \
  fnm alias 24 default
ENV PATH=/usr/local/share/fnm/aliases/default/bin:$PATH
RUN npm install -g corepack bun && \
    corepack install -g pnpm yarn@1

# Passing --build-arg PULUMI_VERSION=vX.Y.Z will use that version
# of the SDK. Otherwise, we use whatever get.pulumi.com thinks is
# the latest
ARG PULUMI_VERSION

# Install the Pulumi SDK, including the CLI and language runtimes.
RUN curl -fsSL https://get.pulumi.com/ | bash -s -- --version $PULUMI_VERSION && \
  mv ~/.pulumi/bin/* /usr/bin
ENV PATH="/pulumi/bin:${PATH}"

# I think it's safe to say if we're using this mega image, we want pulumi
ENTRYPOINT ["pulumi"]

# Nonroot variant of the image
#
# This sets up a non-root user and uses that user for the image.
########################################################################

FROM base AS nonroot

LABEL "repository"="https://github.com/pulumi/pulumi"
LABEL "homepage"="https://pulumi.com"
LABEL "maintainer"="Pulumi Team <team@pulumi.com>"
LABEL org.opencontainers.image.description="The Pulumi CLI, in a Docker container."

ARG UID=1000
ARG GID=1000
RUN addgroup --gid $GID pulumi && \
  adduser --uid $UID --gid $GID --disabled-password --gecos "" pulumi
USER pulumi:pulumi
# Update env vars for the non-root user
ENV GOPATH=/home/pulumi/go
ENV XDG_CONFIG_HOME=/home/pulumi/.config
ENV XDG_CACHE_HOME=/home/pulumi/.cache
# Re-run the helm setup for the non-root user
RUN helm repo add stable https://charts.helm.sh/stable && \
  helm repo update

# Pulumi Bridged Terraform Provider Build Environment
#
# Bundles together everything needed to build a Terraform-based
# provider.
#
# See https://github.com/pulumi/pulumi-docker-containers/issues/111
# for more background.
########################################################################

FROM base AS build-environment

ARG TARGETARCH

# https://github.com/pulumi/pulumictl/releases
ENV PULUMICTL_VERSION 0.0.50
# https://github.com/golangci/golangci-lint/releases
ENV GOLANGCI_LINT_VERSION 2.3.0
# https://github.com/goreleaser/goreleaser/releases
ENV GORELEASER_VERSION 2.11.1

SHELL ["/bin/bash", "-o", "errexit", "-o", "nounset", "-o", "pipefail", "-c"]

RUN \
  # Setup environment variables for architecture-specific packages
  if [ "$TARGETARCH" = "arm64" ]; then \
    GORELEASER_ARCH=arm64; \
  else \
    GORELEASER_ARCH=x86_64; \
  fi && \
  curl \
    --proto "=https" \
    --tlsv1.2 \
    --location \
    --fail \
    --verbose \
    --output "pulumictl.tar.gz" \
    "https://github.com/pulumi/pulumictl/releases/download/v${PULUMICTL_VERSION}/pulumictl-v${PULUMICTL_VERSION}-linux-${TARGETARCH}.tar.gz" && \
    mkdir pulumictl_extraction && \
    tar --extract --gunzip --verbose --directory pulumictl_extraction --file pulumictl.tar.gz && \
    mv pulumictl_extraction/pulumictl /usr/local/bin/pulumictl && \
    chmod a+x /usr/local/bin/pulumictl && \
    rm -Rf pulumictl_extraction && \
    rm pulumictl.tar.gz && \
    # Install golangci-lint
    curl --proto "=https" \
    --tlsv1.2 \
    --silent \
    --show-error \
    --fail \
    --location \
    https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh \
    | sh -s -- -b "$(go env GOPATH)/bin" "v${GOLANGCI_LINT_VERSION}" && \
    # Install goreleaser
    curl \
    --proto "=https" \
    --tlsv1.2 \
    --location \
    --fail \
    --verbose \
    --output "goreleaser.tar.gz" \
    "https://github.com/goreleaser/goreleaser/releases/download/v${GORELEASER_VERSION}/goreleaser_Linux_${GORELEASER_ARCH}.tar.gz" && \
    mkdir goreleaser_extraction && \
    tar --extract --gunzip --verbose --directory goreleaser_extraction --file goreleaser.tar.gz && \
    mv goreleaser_extraction/goreleaser /usr/local/bin/goreleaser && \
    chmod a+x /usr/local/bin/goreleaser && \
    rm -Rf goreleaser_extraction && \
    rm goreleaser.tar.gz

# The entrypoint of the base image is `pulumi`; we don't
# want that for this usecase, since we'll be performing different
# build-related tasks.
ENTRYPOINT []
CMD ["bash"]
