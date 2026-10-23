# Metadata about each image, shared by gen-readmes.py and gen-sync-readmes-matrix.py.
#
#  * `readme` is the generated README for the image. Versioned images, for example `pulumi-python-3.12`, share the
#     README of their language image.
#  * `short_description` is the one-line description shown on Docker Hub (at most 100 characters) and in the ECR
#     Public Gallery. `{version}` is replaced with the language version for versioned images.
#  * For the language images, `sdk` matches the directory under `docker/` and the keys in `versions.py`.
IMAGES = {
    "pulumi": {
        "readme": "docker/pulumi/README.md",
        "short_description": "Pulumi CLI with every supported language runtime and common cloud tools.",
    },
    "pulumi-base": {
        "readme": "docker/base/README.md",
        "short_description": "Pulumi CLI without language toolchains. Bring your own Node.js, Python, Go, .NET, or Java.",
    },
    "pulumi-nodejs": {
        "readme": "docker/nodejs/README.md",
        "sdk": "nodejs",
        "language": "Node.js",
        "short_description": "Pulumi CLI with Node.js {version}, for TypeScript and JavaScript programs.",
        "summary": "The Pulumi CLI with Node.js, for TypeScript and JavaScript programs.",
        "about": "A slim image that contains the Pulumi CLI and Node.js, for running Pulumi programs written in "
        "TypeScript or JavaScript.",
        "contents": lambda v: "- The Pulumi CLI and the Node.js and Bun language runtimes.\n"
        "- Node.js, with npm, Yarn, pnpm, Bun, and Corepack.\n"
        "- `git` and `curl`.",
    },
    "pulumi-python": {
        "readme": "docker/python/README.md",
        "sdk": "python",
        "language": "Python",
        "short_description": "Pulumi CLI with Python {version}, plus pip, Poetry, and uv.",
        "summary": "The Pulumi CLI with Python, plus pip, Poetry, and uv.",
        "about": "A slim image that contains the Pulumi CLI and Python, for running Pulumi programs written in Python.",
        "contents": lambda v: "- The Pulumi CLI and the Python language runtime.\n"
        "- Python, with pip, [Poetry](https://python-poetry.org/), and [uv](https://docs.astral.sh/uv/).\n"
        "- `git` and `curl`.",
    },
    "pulumi-go": {
        "readme": "docker/go/README.md",
        "sdk": "go",
        "language": "Go",
        "short_description": "Pulumi CLI with the Go toolchain, for Pulumi programs written in Go.",
        "summary": "The Pulumi CLI with the Go toolchain.",
        "about": "A slim image that contains the Pulumi CLI and the Go toolchain, for running Pulumi programs written "
        "in Go.",
        "contents": lambda v: "- The Pulumi CLI and the Go language runtime.\n"
        f"- Go {v['go']}, with `CGO_ENABLED=0` and `GOPATH=/go`.\n"
        "- `git` and `curl`.",
    },
    "pulumi-dotnet": {
        "readme": "docker/dotnet/README.md",
        "sdk": "dotnet",
        "language": ".NET",
        "short_description": "Pulumi CLI with the .NET {version} SDK, for C#, F#, and VB.NET programs.",
        "summary": "The Pulumi CLI with the .NET SDK, for C#, F#, and VB.NET programs.",
        "about": "A slim image that contains the Pulumi CLI and the .NET SDK, for running Pulumi programs written in "
        "C#, F#, or VB.NET.",
        "contents": lambda v: "- The Pulumi CLI and the .NET language runtime.\n"
        "- The .NET SDK.\n"
        "- `git` and `curl`.",
    },
    "pulumi-java": {
        "readme": "docker/java/README.md",
        "sdk": "java",
        "language": "Java",
        "short_description": "Pulumi CLI with OpenJDK, Maven, and Gradle, for Pulumi programs written in Java.",
        "summary": "The Pulumi CLI with OpenJDK, Maven, and Gradle.",
        "about": "A slim image that contains the Pulumi CLI and a JDK, for running Pulumi programs written in Java.",
        "contents": lambda v: "- The Pulumi CLI and the Java language runtime.\n"
        f"- OpenJDK {v['java']}, with Maven and Gradle.\n"
        "- `git` and `curl`.",
    },
    "pulumi-provider-build-environment": {
        "readme": "docker/provider-build-environment/README.md",
        "short_description": "The pulumi/pulumi image plus tools for building Pulumi providers.",
    },
}
