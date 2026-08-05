"""
Display utilities with Rich
"""

from rich.console import Console
from rich.table import Table
from rich.text import Text
from typing import List
from src.storage.manager import Task

console = Console()


class TaskDisplay:
    """Display tasks in formatted way"""

    @staticmethod
    def display_tasks(tasks: List[Task], filter_status: str | None = None):
        """Display tasks grouped by status"""

        if not tasks:
            console.print("[yellow]No tasks found[/yellow]")
            return

        # Группируем по статусам
        unlabeled = [t for t in tasks if t.status == "UNLABELED"]
        todo = [t for t in tasks if t.status == "TODO"]
        done = [t for t in tasks if t.status == "DONE"]

        # Выводим в порядке: UNLABELED, TODO, DONE
        if filter_status is None or filter_status == "UNLABELED":
            TaskDisplay._display_group(unlabeled, "UNLABELED", "red")

        if filter_status is None or filter_status == "TODO":
            TaskDisplay._display_group(todo, "TODO", "yellow")

        if filter_status is None or filter_status == "DONE":
            TaskDisplay._display_group(done, "DONE", "green")

    @staticmethod
    def _display_group(tasks: List[Task], status: str, color: str):
        """Display group of tasks"""
        if not tasks:
            return

        # Заголовок печатаем отдельно от таблицы:
        # статичный отступ 24 знака + жирная цветная метка + обычное слово "Tasks"
        title = Text(" " * 24)
        title.append(status, style=f"bold {color}")
        title.append(" Tasks")
        console.print(title)

        table = Table()
        # Устанавливаем ширину 30 для ID, чтобы все символы поместились
        table.add_column("ID", style="cyan", no_wrap=True, width=30)
        table.add_column("Content", style="white")

        for task in tasks:
            # Показываем полный ID
            table.add_row(task.id, task.content)

        console.print(table)
        console.print()

    @staticmethod
    def show_task_created(task: Task):
        """Show task created message"""
        status_colors = {"TODO": "yellow", "DONE": "green", "UNLABELED": "red"}
        color = status_colors.get(task.status, "white")
        console.print(
            f"[green]✓[/green] Created {task.status} task [cyan]{task.id}[/cyan]"
        )
