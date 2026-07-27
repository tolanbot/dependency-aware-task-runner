from pathlib import Path
import shutil

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BUILD_DIRECTORY = PROJECT_ROOT / "build"
DIST_DIRECTORY = PROJECT_ROOT / "dist"
ARCHIVE_BASE = DIST_DIRECTORY / "dependency-task-runner"


def main() -> int:
    if not BUILD_DIRECTORY.exists():
        print(f"Build directory does not exist.\nRun the build task before packaging")

    DIST_DIRECTORY.mkdir(exist_ok=True)

    archive_path = shutil.make_archive(
        base_name=str(ARCHIVE_BASE), format="zip", root_dir=BUILD_DIRECTORY
    )

    print(f"Created package: {archive_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
