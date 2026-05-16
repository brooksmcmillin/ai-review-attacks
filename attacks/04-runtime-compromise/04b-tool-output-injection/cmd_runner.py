"""Task runner using cool-lib's CLI wrapper."""

import subprocess


def run_user_task(task: str) -> str:
    """Run a user-supplied task name via cool-lib's CLI wrapper."""
    return subprocess.check_output(f"cool-lib run {task}", shell=True, text=True)
