"""
Add command implementation
"""

import sys
from rich.console import Console
from src.storage.manager import TaskManager
from src.ui.editor import InteractiveEditor
from src.ui.display import TaskDisplay

console = Console()


def handle_add(args: list):
    """Handle git task add command"""

    # Если нет аргументов — открываем специальный интерактивный режим
    if not args:
        content, status = InteractiveEditor.select_status_and_edit("")
        task = TaskManager.add_task(status, content)
        TaskDisplay.show_task_created(task)

        # Показываем предупреждения если нужно
        if status == "DONE":
            show_done_warning()
        elif status == "UNLABELED":
            show_unlabeled_warning()
        return

    # Если первый аргумент --help
    if args[0] in ["-h", "--help"]:
        show_help()
        return

    subcommand = args[0]

    if subcommand == "todo":
        handle_add_todo(args[1:])
    elif subcommand == "done":
        handle_add_done(args[1:])
    elif subcommand == "unlabeled":
        handle_add_unlabeled(args[1:])
    elif subcommand in ["-m", "--message"]:
        # Прямое указание сообщения — создаём UNLABELED
        if len(args) < 2:
            console.print("[red]error:[/red] message expected", style="bold")
            sys.exit(1)
        content = args[1]
        task = TaskManager.add_task("UNLABELED", content)
        TaskDisplay.show_task_created(task)
        show_unlabeled_warning()
    else:
        console.print(
            f"[red]error:[/red] unknown subcommand: `{subcommand}'", style="bold"
        )
        show_help()
        sys.exit(1)


def handle_add_todo(args: list):
    """Handle git task add todo"""

    if args and args[0] in ["-h", "--help"]:
        show_todo_help()
        return

    if args and args[0] in ["-m", "--message"]:
        if len(args) < 2:
            console.print("[red]error:[/red] message expected", style="bold")
            sys.exit(1)
        content = args[1]
    else:
        # Интерактивное редактирование
        content, _ = InteractiveEditor.edit_task("", "TODO", allow_status_change=False)

    task = TaskManager.add_task("TODO", content)
    TaskDisplay.show_task_created(task)


def handle_add_done(args: list):
    """Handle git task add done"""

    if args and args[0] in ["-h", "--help"]:
        show_done_help()
        return

    show_done_warning()

    if args and args[0] in ["-m", "--message"]:
        if len(args) < 2:
            console.print("[red]error:[/red] message expected", style="bold")
            sys.exit(1)
        content = args[1]
    else:
        # Интерактивное редактирование
        content, _ = InteractiveEditor.edit_task("", "DONE", allow_status_change=False)

    task = TaskManager.add_task("DONE", content)
    TaskDisplay.show_task_created(task)


def handle_add_unlabeled(args: list):
    """Handle git task add unlabeled"""

    if args and args[0] in ["-h", "--help"]:
        show_unlabeled_help()
        return

    show_unlabeled_warning()

    if args and args[0] in ["-m", "--message"]:
        if len(args) < 2:
            console.print("[red]error:[/red] message expected", style="bold")
            sys.exit(1)
        content = args[1]
    else:
        # Интерактивное редактирование
        content, _ = InteractiveEditor.edit_task(
            "", "UNLABELED", allow_status_change=False
        )

    task = TaskManager.add_task("UNLABELED", content)
    TaskDisplay.show_task_created(task)


def show_done_warning():
    """Show warning for DONE tasks"""
    console.print("""
[yellow]Warning![/yellow] It's recommended to create TODO tasks and change them to DONE when completed,
rather than creating DONE tasks directly. This maintains a better workflow and history.
""")


def show_unlabeled_warning():
    """Show warning for UNLABELED tasks"""
    console.print("""
[yellow]Warning![/yellow] It's recommended to use TODO or DONE status instead of UNLABELED.
Properly labeled tasks help with organization and tracking.
""")


def show_help():
    """Show add command help"""
    help_text = """
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
"""
    console.print(help_text)


def show_todo_help():
    """Show todo subcommand help"""
    help_text = """
usage: git task add todo [-h] [-m MESSAGE]

Create a TODO task

optional arguments:
  -m, --message TEXT    Task message
  -h, --help            Show this help message and exit
"""
    console.print(help_text)


def show_done_help():
    """Show done subcommand help"""
    help_text = """
usage: git task add done [-h] [-m MESSAGE]

Create a DONE task

optional arguments:
  -m, --message TEXT    Task message
  -h, --help            Show this help message and exit
"""
    console.print(help_text)


def show_unlabeled_help():
    """Show unlabeled subcommand help"""
    help_text = """
usage: git task add unlabeled [-h] [-m MESSAGE]

Create an UNLABELED task

optional arguments:
  -m, --message TEXT    Task message
  -h, --help            Show this help message and exit
"""
    console.print(help_text)
