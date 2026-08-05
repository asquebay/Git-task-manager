"""
Remove command implementation
"""

import sys
from rich.console import Console
from src.storage.manager import TaskManager
from src.utils.validators import validate_task_id

console = Console()


def handle_remove(args: list):
    """Handle git task remove command"""

    if not args or args[0] in ["-h", "--help"]:
        show_help()
        return

    force = False
    task_id = None

    # Парсим аргументы
    for arg in args:
        if arg in ["-f", "--force"]:
            force = True
        elif arg in ["-h", "--help"]:
            show_help()
            return
        elif not arg.startswith("-"):
            task_id = arg

    if not task_id:
        console.print("[red]error:[/red] task ID required", style="bold")
        show_help()
        sys.exit(1)

    if not validate_task_id(task_id):
        console.print("[red]error:[/red] invalid task ID format", style="bold")
        sys.exit(1)

    task = TaskManager.get_task(task_id)
    if not task:
        console.print(f"[red]error:[/red] task not found: {task_id}", style="bold")
        sys.exit(1)

    # Запрашиваем подтверждение если не --force
    if not force:
        console.print(
            "[yellow]Warning:[/yellow] This will permanently delete the task."
        )
        response = console.input("Do you want to continue? \\[y/N]: ").lower()
        if response not in ["y", "yes"]:
            console.print("[yellow]Cancelled[/yellow]")
            return

    # Удаляем таску
    if TaskManager.delete_task(task_id):
        console.print(f"[green]✓[/green] Deleted task [cyan]{task_id}[/cyan]")
    else:
        console.print(f"[red]error:[/red] failed to delete task", style="bold")
        sys.exit(1)


def show_help():
    """Show remove command help"""
    help_text = """
usage: git task remove [-h] [-f] TASK_ID

Remove a task

positional arguments:
  TASK_ID               Task ID (30 characters)

optional arguments:
  -f, --force           Remove without confirmation
  -h, --help            Show this help message and exit
"""
    console.print(help_text)
