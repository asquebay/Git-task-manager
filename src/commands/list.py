"""
List command implementation
"""

import sys
from rich.console import Console
from src.storage.manager import TaskManager
from src.ui.display import TaskDisplay

console = Console()


def handle_list(args: list):
    """Handle git task list command"""

    if args and args[0] in ["-h", "--help"]:
        show_help()
        return

    filter_status = None

    if args:
        if args[0] == "--todo":
            filter_status = "TODO"
        elif args[0] == "--done":
            filter_status = "DONE"
        elif args[0] == "--unlabeled":
            filter_status = "UNLABELED"
        else:
            console.print(
                f"[red]error:[/red] unknown option: `{args[0]}'", style="bold"
            )
            show_help()
            sys.exit(1)

    tasks = TaskManager.get_all_tasks()

    if filter_status:
        tasks = [t for t in tasks if t.status == filter_status]

    TaskDisplay.display_tasks(tasks, filter_status)


def show_help():
    """Show list command help"""
    help_text = """
usage: git task list [-h] [--todo] [--done] [--unlabeled]

List all tasks

optional arguments:
  --todo                Show only TODO tasks
  --done                Show only DONE tasks
  --unlabeled           Show only UNLABELED tasks
  -h, --help            Show this help message and exit
"""
    console.print(help_text)
