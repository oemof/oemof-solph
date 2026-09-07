import subprocess
import sys

# Process build without output
result = subprocess.run(
    [sys.executable, "-m", "build", "."],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

# Create an output if process failed
if result.returncode != 0:
    print("Build failed. Starting over with active output:")
    subprocess.run([sys.executable, "-m", "build", "."])

sys.exit(result.returncode)
