import os
import sys

print("Current working directory:", os.getcwd())
print("Contents:")
for item in os.listdir():
    print(" ", item)


assert sys.version_info.major == 3 and sys.version_info.minor == 9, (
    f"version should be 3.9, got {sys.version_info.major}.{sys.version_info.minor}"
)
