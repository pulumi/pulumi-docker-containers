# SDKs without version suffixes.
# For these SDKs we only have unsuffixed images, for example `pulumi-dotnet` and `pulumi-go`.
sdks = {
    "go": "1.21.1",
    "dotnet": "6.0",
    "java": "not-used-yet",
}

# For Python and Nodejs we have a default version and additional versions with suffixes.
# The default version is used for the unsuffixed image `pulumi-python` and for the suffixed version `pulumi-python-3.9`.
# The additional versions are used for the suffixed images `pulumi-python-3.10`, `pulumi-python-3.11`, ...
python_default_version = "3.9"
python_additional_versions = ["3.10", "3.11", "3.12"]
nodejs_default_version = "18"
nodejs_additional_versions = ["20", "22"]
