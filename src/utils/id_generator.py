"""
Task ID generation
"""

import secrets
import string


def generate_task_id() -> str:
    """Generate a unique 30-character task ID"""
    # Используем буквы, цифры и некоторые символы
    alphabet = string.ascii_letters + string.digits + "-_"
    return "".join(secrets.choice(alphabet) for _ in range(30))
