"""
Interactive terminal editor with prompt_toolkit
"""

from prompt_toolkit import prompt
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.formatted_text import HTML, FormattedText
from rich.console import Console
import sys

console = Console()


class InteractiveEditor:
    """Interactive task editor in terminal"""

    @staticmethod
    def _create_task_preview(
        content: str, max_chars: int = 1000, max_lines: int = 20
    ) -> str:
        """
        Создаёт превью таски с ограничением по символам и строкам

        Args:
            content: полное содержимое таски
            max_chars: максимальное количество символов
            max_lines: максимальное количество строк

        Returns:
            превью таски (с "..." в конце если обрезано)
        """
        if not content:
            return ""

        # Проверяем базовое условие: если текст укладывается в лимиты,
        # то возвращаем его целиком без добавления "..."
        lines = content.split("\n")
        if len(content) <= max_chars and len(lines) <= max_lines:
            return content

        result_lines = []
        current_chars = 0

        for line in lines:
            # Проверяем лимит по строкам (учитывая будущую строку)
            if len(result_lines) >= max_lines:
                break

            # Длина строки + символ переноса (если это не первая строка)
            line_cost = len(line) + (1 if result_lines else 0)

            # Проверяем, не превысим ли лимит символов
            if current_chars + line_cost > max_chars:
                # Сколько символов осталось до лимита
                remaining_chars = max_chars - current_chars - (1 if result_lines else 0)
                if remaining_chars > 0:
                    result_lines.append(line[:remaining_chars])
                break

            result_lines.append(line)
            current_chars += line_cost

        # Собираем результат и добавляем "..." в конце
        return "\n".join(result_lines) + "..."

    @staticmethod
    def edit_task(
        initial_content: str, status: str, allow_status_change: bool = False
    ) -> tuple[str, str]:
        """
        Open interactive editor for task editing

        Returns: (content, status)
        """
        # Определяем цвет статуса
        status_colors = {"TODO": "yellow", "DONE": "green", "UNLABELED": "red"}
        color = status_colors.get(status, "white")

        # Очищаем экран
        console.clear()
        console.print("[bold cyan]Task Editor[/bold cyan]")
        console.print("=" * 40)
        console.print()

        if allow_status_change:
            console.print("[dim]Press Ctrl+C to cancel, Ctrl+D to finish editing[/dim]")
            console.print(
                "[dim]Status is changeable - edit the prefix if needed[/dim]\n"
            )
        else:
            console.print(
                "[dim]Press Ctrl+C to cancel, Ctrl+D or Enter to finish[/dim]\n"
            )

        # Создаём prompt с цветным префиксом
        prefix = (
            HTML(f"<ansiyellow><b>{status}:</b></ansiyellow> ")
            if status == "TODO"
            else HTML(f"<ansigreen><b>{status}:</b></ansigreen> ")
            if status == "DONE"
            else HTML(f"<ansired><b>{status}:</b></ansired> ")
        )

        try:
            if allow_status_change:
                # Режим с возможностью изменения статуса
                full_text = prompt(
                    "",
                    default=f"{status}: {initial_content}",
                    multiline=False,
                )

                # Парсим результат
                if full_text.startswith("TODO: "):
                    return full_text[6:], "TODO"
                elif full_text.startswith("DONE: "):
                    return full_text[6:], "DONE"
                elif full_text.startswith("UNLABELED: "):
                    return full_text[11:], "UNLABELED"
                else:
                    # Если префикс не найден, считаем UNLABELED
                    return full_text, "UNLABELED"
            else:
                # Режим без изменения статуса — префикс защищён
                content = prompt(
                    prefix,
                    default=initial_content,
                    multiline=False,
                )
                return content, status

        except KeyboardInterrupt:
            console.print("\n[red]Cancelled[/red]")
            sys.exit(1)
        except EOFError:
            # Ctrl+D без ввода
            if not initial_content.strip():
                console.print("\n[red]Cancelled - empty content[/red]")
                sys.exit(1)
            return initial_content, status

    @staticmethod
    def edit_with_status_change(
        initial_content: str, initial_status: str
    ) -> tuple[str, str]:
        """
        Edit task with ability to change status
        """
        return InteractiveEditor.edit_task(
            initial_content, initial_status, allow_status_change=True
        )

    @staticmethod
    def select_status_and_edit(
        initial_content: str = "", initial_status: str = "TODO"
    ) -> tuple[str, str]:
        """
        Two-stage editor: first select status with arrows, then edit content

        Args:
            initial_content: предзаполненное содержимое таски
            initial_status: статус, который будет выбран по умолчанию

        Returns: (content, status)
        """
        # Создаём превью таски для отображения на первом этапе
        task_preview = InteractiveEditor._create_task_preview(initial_content)

        # Этап 1: выбор статуса с превью таски
        console.clear()
        console.print("[bold cyan]Task Editor - Select Status[/bold cyan]")
        console.print("=" * 40)
        console.print()
        console.print("[dim]Use arrow keys (↑↓←→) to change status[/dim]")
        console.print("[dim]Press Enter to proceed to content editing[/dim]")
        console.print("[dim]Press Ctrl+C to cancel[/dim]")
        console.print()

        statuses = ["TODO", "DONE", "UNLABELED"]

        # Устанавливаем начальный статус на основе initial_status
        if initial_status in statuses:
            current_status_idx = statuses.index(initial_status)
        else:
            current_status_idx = 0

        # Key bindings для выбора статуса
        kb = KeyBindings()
        selected_status = [
            statuses[current_status_idx]
        ]  # используем список для изменяемости

        @kb.add("up")
        @kb.add("down")
        @kb.add("left")
        @kb.add("right")
        def cycle_status(event):
            """Cycle through statuses"""
            key = event.key_sequence[0].key
            if key in ["up", "right"]:
                # Вперёд по кольцу
                idx = statuses.index(selected_status[0])
                selected_status[0] = statuses[(idx + 1) % len(statuses)]
            else:  # down или left
                # Назад по кольцу
                idx = statuses.index(selected_status[0])
                selected_status[0] = statuses[(idx - 1) % len(statuses)]

        @kb.add("c-c")
        def cancel(event):
            """Cancel on Ctrl+C"""
            event.app.exit(result="cancelled")

        @kb.add("enter")
        def accept(event):
            """Accept on Enter"""
            event.app.exit(result=selected_status[0])

        # Создаём интерактивный контрол для отображения статуса + превью
        def get_status_text():
            status = selected_status[0]
            # Формируем статус с превью таски
            if status == "TODO":
                status_part = [("ansiyellow bold", "TODO: ")]
            elif status == "DONE":
                status_part = [("ansigreen bold", "DONE: ")]
            else:
                status_part = [("ansired bold", "UNLABELED: ")]

            # Добавляем превью таски обычным текстом
            if task_preview:
                status_part.append(("", task_preview))

            return FormattedText(status_part)

        status_control = FormattedTextControl(
            text=get_status_text,
            focusable=True,
        )

        layout = Layout(
            Window(
                content=status_control,
                wrap_lines=True,  # визуальный перенос длинных строк
                dont_extend_height=True,  # окно занимает ровно столько строк, сколько позволяют визуальные границы терминала
            )
        )
        app = Application(layout=layout, key_bindings=kb, full_screen=False)

        try:
            result = app.run()
            if result == "cancelled":
                console.print("\n[red]Cancelled[/red]")
                sys.exit(1)

            final_status = result

        except KeyboardInterrupt:
            console.print("\n[red]Cancelled[/red]")
            sys.exit(1)

        # Этап 2: редактирование содержимого
        console.clear()
        console.print("[bold cyan]Task Editor - Edit Content[/bold cyan]")
        console.print("=" * 40)
        console.print()
        console.print("[dim]Press Ctrl+C to cancel, Enter to finish[/dim]")
        console.print()

        # Определяем цвет для префикса
        prefix = (
            HTML(f"<ansiyellow><b>{final_status}:</b></ansiyellow> ")
            if final_status == "TODO"
            else HTML(f"<ansigreen><b>{final_status}:</b></ansigreen> ")
            if final_status == "DONE"
            else HTML(f"<ansired><b>{final_status}:</b></ansired> ")
        )

        try:
            content = prompt(
                prefix,
                default=initial_content,
                multiline=False,
            )
            return content, final_status

        except KeyboardInterrupt:
            console.print("\n[red]Cancelled[/red]")
            sys.exit(1)
        except EOFError:
            # Ctrl+D без ввода
            if not initial_content.strip():
                console.print("\n[red]Cancelled - empty content[/red]")
                sys.exit(1)
            return initial_content, final_status
