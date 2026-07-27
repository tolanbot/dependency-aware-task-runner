import json
import unittest
from pathlib import Path
from taskrunner import resolve_execution_order, load_config
from unittest.mock import patch, mock_open


class TestTaskRunner(unittest.TestCase):
    EXPECTED_TASK_COMMANDS = {
        "task1": ["one", "two", "three"],
        "task2": ["four", "five", "six"],
    }

    def test_dependency_cycle_detection(self):
        pass

    def test_command_parsing(self):

        json_payload = {
            "tasks": {
                task: {"command": cmd}
                for task, cmd in self.EXPECTED_TASK_COMMANDS.items()
            }
        }

        json_str = json.dumps(json_payload)

        with patch("pathlib.Path.open", mock_open(read_data=json_str)):
            tasks = load_config(Path("dummy_config.json"))

        print(f"tasks: {tasks}")
        for task in tasks:
            command = tasks[task].command
            self.assertEqual(command, self.EXPECTED_TASK_COMMANDS[task])
