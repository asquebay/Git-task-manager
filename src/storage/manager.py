"""
Task storage management
"""

import json
from pathlib import Path
from typing import Optional, List, Dict
from dataclasses import dataclass, asdict
from enum import Enum


class TaskStatus(Enum):
    """Task status enum"""

    TODO = "TODO"
    DONE = "DONE"
    UNLABELED = "UNLABELED"


@dataclass
class Task:
    """Task data class"""

    id: str
    status: str
    content: str

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "Task":
        return cls(**data)


class TaskManager:
    """Manage task storage"""

    TASKS_DIR = ".git/tasks"
    TASKS_FILE = ".git/tasks/tasks.json"

    @classmethod
    def initialize(cls):
        """Initialize task storage"""
        Path(cls.TASKS_DIR).mkdir(parents=True, exist_ok=True)

        # Создаем файл если его нет
        if not Path(cls.TASKS_FILE).exists():
            cls._save_tasks([])

    @classmethod
    def _load_tasks(cls) -> List[Task]:
        """Load tasks from storage"""
        try:
            with open(cls.TASKS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Task.from_dict(t) for t in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @classmethod
    def _save_tasks(cls, tasks: List[Task]):
        """Save tasks to storage"""
        Path(cls.TASKS_DIR).mkdir(parents=True, exist_ok=True)
        with open(cls.TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tasks], f, indent=2, ensure_ascii=False)

    @classmethod
    def add_task(cls, status: str, content: str) -> Task:
        """Add a new task"""
        from src.utils.id_generator import generate_task_id

        tasks = cls._load_tasks()
        task_id = generate_task_id()

        # Проверяем уникальность
        while any(t.id == task_id for t in tasks):
            task_id = generate_task_id()

        task = Task(id=task_id, status=status, content=content)
        tasks.append(task)
        cls._save_tasks(tasks)
        return task

    @classmethod
    def get_task(cls, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        tasks = cls._load_tasks()
        return next((t for t in tasks if t.id == task_id), None)

    @classmethod
    def update_task(
        cls, task_id: str, content: str, status: Optional[str] = None
    ) -> Optional[Task]:
        """Update task"""
        tasks = cls._load_tasks()
        for task in tasks:
            if task.id == task_id:
                task.content = content
                if status:
                    task.status = status
                cls._save_tasks(tasks)
                return task
        return None

    @classmethod
    def delete_task(cls, task_id: str) -> bool:
        """Delete task"""
        tasks = cls._load_tasks()
        original_count = len(tasks)
        tasks = [t for t in tasks if t.id != task_id]

        if len(tasks) < original_count:
            cls._save_tasks(tasks)
            return True
        return False

    @classmethod
    def get_all_tasks(cls) -> List[Task]:
        """Get all tasks"""
        return cls._load_tasks()

    @classmethod
    def get_tasks_by_status(cls, status: str) -> List[Task]:
        """Get tasks by status"""
        return [t for t in cls._load_tasks() if t.status == status]
