from typing import Protocol

from .model import Task


class TaskRepository(Protocol):
    async def save(self, task: Task) -> None:
        raise NotImplementedError
