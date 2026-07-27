import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
print(f"PROJECT_ROOT: {PROJECT_ROOT}")


def main() -> int:
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
        cwd=PROJECT_ROOT,
        check=False,
    )

    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
