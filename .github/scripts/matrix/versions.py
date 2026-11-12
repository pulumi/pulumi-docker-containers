# Language versions for all images. The Dockerfiles take these as build arguments, see `build-args.py`.

# SDKs without version suffixes.
# For these SDKs we only have unsuffixed images, for example `pulumi-java` and `pulumi-go`.
unversioned = {
    "go": {
        "version": "1.26.10",
        # Checksums of the Go release archives, from https://go.dev/dl/.
        "sha256": {
            "amd64": "ccfe7ae822d2c2f41f4fe7c956199967a4dac22d0ee0d2b2bfdb440aab3b20c5",
            "arm64": "3f4227ce7b206a513e794f1393adb473a07b46e94d18bd15d1c684bbb7319797",
        },
    },
    "java": {
        "version": "21",
    },
}

# For the versioned SDKS we have a default version and additional versions with suffixes.
# The default version is used for the unsuffixed image `pulumi-python` and for the suffixed version `pulumi-python-3.12`.
# The additional versions are used for the suffixed images `pulumi-python-3.10`, `pulumi-python-3.11`, ...
# The `pulumi` image includes all of these versions.
versioned = {
    "nodejs": {
        "default": "26",
        "additional": ["22", "24"]
    },
    "python": {
        "default": "3.13",
        "additional": ["3.10", "3.11", "3.12", "3.14"]
    },
    "dotnet": {
        "default": "8.0",
        "additional": ["9.0", "10.0"]
    }
}
