from typing import Any, Protocol

from ...task.domain.model import Task, TaskTitle
from ...task.domain.repository import TaskRepository
from .commands import AddTaskCommand


class Handler(Protocol):
    def handle(self, command: Any) -> Any:
        ...


class AddTaskCommandHandler(Handler):
    def __init__(self, repository: TaskRepository) -> None:
        self.__repository = repository

    async def handle(self, command: AddTaskCommand) -> Any:
        title = command.title
        _id = command.id

        task = Task(id=_id, title=TaskTitle(title))

        await self.__repository.save(task)
