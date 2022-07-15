from typing import List

from asgiref.sync import sync_to_async

from tododdd.task.application.dto import TaskDto
from tododdd.task.domain.services import TaskFinder
from tododdd.task.infrastructure.task.models import Task


class DjangoTaskFinder(TaskFinder):
    @sync_to_async
    def all(self) -> List[TaskDto]:
        tasks = Task.objects.all()

        return [TaskDto(id=task.id, title=task.title, is_completed=task.is_completed) for task in tasks]
