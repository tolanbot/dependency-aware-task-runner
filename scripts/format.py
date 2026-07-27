import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
print(f"PROJECT_ROOT: {PROJECT_ROOT}")


def main() -> int:
    final_returncode = 0
    for file_path in PROJECT_ROOT.rglob("*.py"):
        print("Formatting file: {file_path}")
        result = subprocess.run(["black", file_path])
        if result.returncode != 0:
            final_returncode = result.returncode
    return final_returncode


if __name__ == "__main__":
    raise SystemExit(main())
