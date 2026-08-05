"""
Input validators
"""

import subprocess


def validate_git_repo() -> bool:
    """Check if we're in a git repository"""
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"], capture_output=True, check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def validate_task_id(task_id: str) -> bool:
    """Validate task ID format"""
    return len(task_id) == 30 and all(c.isalnum() or c in "-_" for c in task_id)
