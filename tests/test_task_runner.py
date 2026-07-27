import json
import unittest
from pathlib import Path
from taskrunner import resolve_execution_order, load_config, Task
from unittest.mock import patch, mock_open


class TestTaskRunner(unittest.TestCase):
    EXPECTED_TASKS = {
        "task1": {
            "command": ["one", "two", "three"],
            "description": "task1 description",
            "depends_on": ["dep1"],
        },
        "task2": {
            "command": ["four", "five", "six"],
            "description": "task2 description",
            "depends_on": ["dep2"],
        },
    }

    CYCLE_TASKS = {
        "build": Task(name="build", command=[], dependencies=["test"]),
        "test": Task(name="test", command=[], dependencies=["build"]),
    }

    NON_CYCLE_TASKS = {
        "clean": Task(name="clean", command=[], dependencies=[]),
        "build": Task(name="build", command=[], dependencies=["clean"]),
    }

    def test_dependency_cycle_detection(self):
        with self.assertRaises(ValueError) as context:
            resolve_execution_order(self.CYCLE_TASKS, "build")

        self.assertIn("cycle", str(context.exception).lower())

    def test_successfull_execution_order(self):
        expected_order = ["clean", "build"]
        order = resolve_execution_order(self.NON_CYCLE_TASKS, "build")
        self.assertEqual(order, expected_order)

    def test_command_parsing(self):
        json_payload = {"tasks": self.EXPECTED_TASKS}
        json_str = json.dumps(json_payload)

        with patch("pathlib.Path.open", mock_open(read_data=json_str)):
            tasks = load_config(Path("dummy_config.json"))

        for task in tasks:
            command = tasks[task].command
            self.assertEqual(command, self.EXPECTED_TASKS[task]["command"])
            desc = tasks[task].description
            self.assertEqual(desc, self.EXPECTED_TASKS[task]["description"])
            dep = tasks[task].dependencies
            self.assertEqual(dep, self.EXPECTED_TASKS[task]["depends_on"])
