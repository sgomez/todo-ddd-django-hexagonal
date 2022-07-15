from dataclasses import dataclass
from typing import List

from tododdd.task.application.command_handlers import Handler
from tododdd.task.application.dto import TaskDto
from tododdd.task.application.queries import GetTasksQuery
from tododdd.task.domain.services import TaskFinder


class GetTasksQueryHandler(Handler):
    def __init__(self, finder: TaskFinder) -> None:
        self.__finder = finder

    async def handle(self, query: GetTasksQuery) -> List[TaskDto]:
        return await self.__finder.all()
