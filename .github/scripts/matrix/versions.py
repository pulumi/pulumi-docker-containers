# SDKs without version suffixes.
# For these SDKs we only have unsuffixed images, for example `pulumi-java` and `pulumi-go`.
unversioned = ["go", "java"]

# For the versioned SDKS we have a default version and additional versions with suffixes.
# The default version is used for the unsuffixed image `pulumi-python` and for the suffixed version `pulumi-python-3.9`.
# The additional versions are used for the suffixed images `pulumi-python-3.10`, `pulumi-python-3.11`, ...
versioned = {
    "nodejs": {
        "default": "18",
        "additional": ["20", "22"]
    },
    "python": {
        "default": "3.9",
        "additional": ["3.10", "3.11", "3.12"]
    },
    "dotnet": {
        "default": "6.0",
        "additional": ["8.0"]
    }
}
