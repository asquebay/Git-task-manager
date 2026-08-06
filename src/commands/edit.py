"""
Edit command implementation
"""

import sys
from rich.console import Console
from src.storage.manager import TaskManager
from src.ui.editor import InteractiveEditor
from src.utils.validators import validate_task_id

console = Console()


def handle_edit(args: list):
    """Handle git task edit command"""

    if not args or args[0] in ["-h", "--help"]:
        show_help()
        return

    task_id = args[0]

    if not validate_task_id(task_id):
        console.print(f"[red]error:[/red] invalid task ID format", style="bold")
        sys.exit(1)

    task = TaskManager.get_task(task_id)
    if not task:
        console.print(f"[red]error:[/red] task not found: {task_id}", style="bold")
        sys.exit(1)

    # Открываем двухэтапный редактор с текущим содержимым и статусом
    content, status = InteractiveEditor.select_status_and_edit(
        initial_content=task.content, initial_status=task.status
    )

    # Обновляем таску
    TaskManager.update_task(task_id, content, status)
    console.print(f"[green]✓[/green] Updated task [cyan]{task_id}[/cyan]")


def show_help():
    """Show edit command help"""
    help_text = """
usage: git task edit [-h] TASK_ID

Edit an existing task

positional arguments:
  TASK_ID               Task ID (30 characters)

optional arguments:
  -h, --help            Show this help message and exit
"""
    console.print(help_text)
