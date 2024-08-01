import sys

assert sys.version_info.major == 3 and sys.version_info.minor == 10 and sys.version_info.micro == 2 , \
    f"version should be 3.10.2, got {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
