# Dependency Task Runner

A Python command-line tool that executes tasks in dependency order.

Tasks are defined in a JSON configuration file. The runner:

- Resolves task dependencies using a topological sort
- Detects dependency cycles
- Executes each dependency only once
- Stops execution if a task fails

## Requirements

- Python 3.10+

## Usage

Run a task:

```bash
python taskrunner.py package
```

List available tasks:

```bash
python taskrunner.py --list
```

Preview the execution order without running commands:

```bash
python taskrunner.py package --dry-run
```

Use a different configuration file:

```bash
python taskrunner.py package --config other_tasks.json
```

## Example Configuration

```json
{
  "tasks": {
    "clean": {
      "command": ["python", "scripts/clean.py"]
    },
    "generate": {
      "command": ["python", "scripts/generate.py"],
      "depends_on": ["clean"]
    },
    "package": {
      "command": ["python", "scripts/package.py"],
      "depends_on": ["generate"]
    }
  }
}
```