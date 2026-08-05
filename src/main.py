#!/usr/bin/env python3
"""
Git task manager - Main entry point
"""

import sys
from pathlib import Path
from rich.console import Console

# Добавляем текущую директорию в path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.commands.add import handle_add
from src.commands.list import handle_list
from src.commands.edit import handle_edit
from src.commands.remove import handle_remove
from src.utils.validators import validate_git_repo
from src.storage.manager import TaskManager

console = Console()

HELP_TEXT = """
usage: git task [-h] {add,list,edit,remove,rm} ...

Git task management system

positional arguments:
  {add,list,edit,remove,rm}
    add                 Add a new task
    list                List all tasks
    edit                Edit an existing task
    remove, rm          Remove a task

optional arguments:
  -h                    Show this help message and exit
"""

SUBCOMMAND_HELP = {
    "add": """
usage: git task add [-h] {todo,done,unlabeled} ...

Add a new task

positional arguments:
  {todo,done,unlabeled}
    todo                Create a TODO task (default)
    done                Create a DONE task
    unlabeled           Create an UNLABELED task

optional arguments:
  -m, --message TEXT    Task message
  -h, --help            Show this help message and exit
""",
    "list": """
usage: git task list [-h] [--todo] [--done] [--unlabeled]

List all tasks

optional arguments:
  --todo                Show only TODO tasks
  --done                Show only DONE tasks
  --unlabeled           Show only UNLABELED tasks
  -h, --help            Show this help message and exit
""",
    "edit": """
usage: git task edit [-h] TASK_ID

Edit an existing task

positional arguments:
  TASK_ID               Task ID (30 characters)

optional arguments:
  -h, --help            Show this help message and exit
""",
    "remove, rm": """
usage: git task remove [-h] [-f] TASK_ID

Remove a task

positional arguments:
  TASK_ID               Task ID (30 characters)

optional arguments:
  -f, --force           Remove without confirmation
  -h, --help            Show this help message and exit
""",
}


def main():
    """Main entry point"""
    # Проверяем, находимся ли в Git репозитории
    if not validate_git_repo():
        console.print("[red]error:[/red] not a git repository", style="bold")
        sys.exit(128)

    # Инициализируем хранилище тасок (это часть исполняемого файла)
    TaskManager.initialize()

    # Парсим аргументы
    if len(sys.argv) < 2:
        console.print(HELP_TEXT)
        sys.exit(1)

    command = sys.argv[1]

    # Обработка help флагов
    if command in ["-h"]:
        console.print(HELP_TEXT)
        sys.exit(0)

    # Обработка команд
    try:
        if command == "add":
            handle_add(sys.argv[2:])
        elif command == "list":
            handle_list(sys.argv[2:])
        elif command == "edit":
            handle_edit(sys.argv[2:])
        elif command in ["remove", "rm"]:
            handle_remove(sys.argv[2:])
        else:
            console.print(
                f"[red]error:[/red] unknown subcommand: `{command}'", style="bold"
            )
            console.print(HELP_TEXT)
            sys.exit(1)
    except Exception as e:
        console.print(f"[red]error:[/red] {str(e)}", style="bold")
        sys.exit(1)


if __name__ == "__main__":
    main()
