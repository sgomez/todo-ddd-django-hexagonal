from asgiref.sync import sync_to_async

from ....task.domain import model
from ....task.domain.repository import TaskRepository
from .models import Task


class DjangoTaskRepository(TaskRepository):
    @sync_to_async
    def save(self, task: model.Task) -> None:
        Task.objects.create(id=task.id, title=task.title.value, is_completed=task.is_completed)
