import os
import subprocess

cpp_file = "binding.cpp"
output_file = "binding"

def run_tests():
    try:
        result = subprocess.run(
            [ "g++", cpp_file, "-o", output_file, "-std=c++17" ],
            check=True,
            text=True,
            capture_output=True
        )
        print(f"Compilation successful")

    except subprocess.CalledProcessError as e:
        print(f"Compilation failed: {e.stderr}")
        return None

    try:
        result = subprocess.run(
            [ f"./{output_file}" ],
            check=True,
            text=True,
            capture_output=True
        )
        os.remove(output_file)
        print(f"Execution successful")

    except subprocess.CalledProcessError as e:
        print(f"Execution failed: {e.stderr}")
        return None

    return result.stdout.strip()