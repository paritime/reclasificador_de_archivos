import sys
import os

print("Hello from executable!")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
with open("test_log.txt", "w") as f:
    f.write("Hello from file!")
input("Press Enter to exit...")
