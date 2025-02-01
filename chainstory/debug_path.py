import sys
import os

print("Current working directory:", os.getcwd())
print("\nPython path:")
for path in sys.path:
    print(path) 