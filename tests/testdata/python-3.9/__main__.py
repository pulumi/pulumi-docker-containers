import os
import sys

print(f"PATH={os.getenv('PATH')}")

assert sys.version_info.major == 3 and sys.version_info.minor == 9, (
    f"version should be 3.9, got {sys.version_info.major}.{sys.version_info.minor}"
)
