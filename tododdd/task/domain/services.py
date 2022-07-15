from typing import List, Protocol

from tododdd.task.application.dto import TaskDto


class TaskFinder(Protocol):
    async def all(self) -> List[TaskDto]:
        raise NotImplementedError
