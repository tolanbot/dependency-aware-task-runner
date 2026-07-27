import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BUILD_DIRECTORY = PROJECT_ROOT / "build"

FILES_TO_COPY = ["taskrunner.py", "tasks.json", "README.md"]


def main() -> int:
    if BUILD_DIRECTORY.exists():
        shutil.rmtree(BUILD_DIRECTORY)

    BUILD_DIRECTORY.mkdir()

    for filename in FILES_TO_COPY:
        source = PROJECT_ROOT / filename

        if not source.exists():
            print(f"Required file not found: {filename}")

        destination = BUILD_DIRECTORY / filename
        shutil.copy2(source, destination)
        print(f"Copied {filename}")

    print(f"Build created at {BUILD_DIRECTORY}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
