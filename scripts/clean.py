from pathlib import Path
import shutil

PROJECT_ROOT = Path(__file__).resolve().parent.parent
print(f"PROJECT_ROOT: {PROJECT_ROOT}")

DIRECTORIES_TO_REMOVE = [
    PROJECT_ROOT / "dist",
    PROJECT_ROOT / "build",
    PROJECT_ROOT / "__pycache__",
]


def main() -> int:
    for directory in DIRECTORIES_TO_REMOVE:
        if directory.exists():
            shutil.rmtree(directory)
            print(f"Removed {directory.relative_to(PROJECT_ROOT)}")
        else:
            print(f"Skipped {directory.relative_to(PROJECT_ROOT)}: not found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
