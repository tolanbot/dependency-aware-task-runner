import argparse
import json
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Task:
    name: str
    command: list[str]
    dependencies: list[str] = field(default_factory=list)
    description: str = ""


def load_config(path: Path) -> dict[str, Task]:
    with path.open("r", encoding="utf-8") as config_file:
        data = json.load(config_file)

    if not isinstance(data, dict):
        raise ValueError("Configuration root must be an object.")

    raw_tasks = data.get("tasks")

    if not isinstance(raw_tasks, dict):
        raise ValueError("Configuration must contain a 'tasks' object.")

    tasks: dict[str, Task] = {}

    for name, raw_task in raw_tasks.items():
        if not isinstance(raw_task, dict):
            raise ValueError(f"Task {name} must be an object.")

        command = raw_task.get("command")
        if not isinstance(command, list):
            raise ValueError(f"Task '{name}' command input must be a list.")
        dependencies = raw_task.get("depends_on", [])
        description = raw_task.get("description", "")

        tasks[name] = Task(
            name=name,
            command=command,
            dependencies=dependencies,
            description=description,
        )

    return tasks


def validate_tasks(tasks: dict[str, Task]) -> None:
    for task in tasks.values():
        if not task.command:
            raise ValueError(f"Task '{task.name}' command must not be empty.")

        if not all(isinstance(argument, str) for argument in task.command):
            raise ValueError(
                f"Task '{task.name}' command arguments must all be strings."
            )

        if not isinstance(task.description, str):
            raise ValueError(f"Task '{task.name}' description must be a string.")

        if not isinstance(task.dependencies, list):
            raise ValueError(f"Task '{task.name}' dependencies must be a list")

        if not all(isinstance(dependency, str) for dependency in task.dependencies):
            raise ValueError(
                f"Task '{task.name}' dependency list items must all be strings."
            )

        for dependency in task.dependencies:
            if dependency not in tasks:
                raise ValueError(
                    f"Task '{task.name}' depends on unknown task: " f"'{dependency}'"
                )


def resolve_execution_order(tasks: dict[str, Task], target: str) -> list[str]:
    states: dict[str, str] = {}
    order: list[str] = []
    path: list[str] = []

    def visit(name: str) -> None:
        if name not in tasks:
            raise ValueError(f"Unknown Task: {name}")

        state = states.get(name, "unvisited")

        if state == "visted":
            return

        if state == "visiting":
            cycle_start = path.index(name)
            cycle = path[:cycle_start] + [name]
            raise ValueError(f"Dependency Cycle detected: " + " -> ".join(cycle))

        states[name] = "visiting"
        path.append(name)

        for dependency in tasks[name].dependencies:
            visit(dependency)

        path.pop()
        states[name] = "visited"
        order.append(name)

    visit(target)
    return order


# def resolve_execution_order(tasks: dict[str, Task], target: str) -> list[str]:
#     states: dict[str, str] = {}
#     order: list[str] = []
#     path: list[str] = []

#     def visit(name: str) -> None:
#         if name not in tasks:
#             raise ValueError(f"Unknown task: {name}")
#         state = states.get(name, "unvisited")

#         if state == "visited":
#             return

#         if state == "visiting":
#             cycle_start = path.index(name)
#             cycle = path[cycle_start:] + [name]
#             raise ValueError("Dependency cycle detected: " + " -> ".join(cycle))

#         states[name] = "visiting"
#         path.append(name)

#         for dependency in tasks[name].dependencies:
#             visit(dependency)

#         path.pop()
#         states[name] = "visited"
#         order.append(name)

#     visit(target)
#     return order


def execute_tasks(tasks: dict[str, Task], order: list[str], dry_run: bool) -> int:
    if dry_run:
        print("Dry Execution Plan:")
        for index, name in enumerate(order, start=1):
            print(f"{index}. {name}")
        return 0

    total = len(order)
    for index, name in enumerate(order, start=1):
        print(f"{index}/{total} Running: {name}")
        exit_code = run_task(tasks[name])
        if exit_code != 0:
            return exit_code

    return 0


def run_task(task: Task) -> int:
    start = time.perf_counter()
    try:
        result = subprocess.run(task.command)
    except FileNotFoundError:
        print(
            f"Task '{task.name}' failed\ncommand not found: {task.command[0]}",
            file=sys.stderr,
        )
        return 127

    elapsed = time.perf_counter() - start

    if result.returncode == 0:
        print(f"Completed {task.name} in {elapsed:.2f}s")
    else:
        print(
            f"Task '{task.name}' failed with exit code {result.returncode}",
            file=sys.stderr,
        )

    return result.returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run tasks with dependency resolution."
    )

    parser.add_argument("target", nargs="?", help="Task to execute")

    parser.add_argument(
        "--config",
        type=Path,
        default=Path("tasks.json"),
        help="Path to the task configuration file.",
    )

    parser.add_argument("--list", action="store_true", help="List available tasks")

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print task execution plan without running.",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        tasks = load_config(args.config)
        validate_tasks(tasks)

        if args.list:
            for task in tasks.values():
                description = task.description or "No description"
                print(f"{task.name}: {description}")
            return 0

        if args.target is None:
            print("A target task is required unless --list is used", file=sys.stderr)
            return 2

        order = resolve_execution_order(tasks, args.target)
        return execute_tasks(tasks, order, args.dry_run)

    except json.JSONDecodeError as err:
        print(f"Invalid JSON: {err}", file=sys.stderr)
        return 2

    except FileNotFoundError:
        print(f"Configuration file not found: {args.config}", file=sys.stderr)
        return 2

    except ValueError as err:
        print(err, file=sys.stderr)
        return 2

    except Exception as ex:
        print(f"you done fukked up: {ex}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
