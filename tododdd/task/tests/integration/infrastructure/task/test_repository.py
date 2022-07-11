from asgiref.sync import sync_to_async
from django.test import TestCase

from tododdd.task.domain import model
from tododdd.task.infrastructure.task.models import Task
from tododdd.task.infrastructure.task.repository import DjangoTaskRepository


class TestDjangoTaskRepository(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.repository = DjangoTaskRepository()

    ...

    async def test_save_new_task(self):
        # Arrange
        title = model.TaskTitle("Demo task")
        task = model.Task(1, title)

        # Act
        await self.repository.save(task)

        # Assert
        @sync_to_async
        def test():
            found = Task.objects.get(pk=1)
            self.assertEqual(found.title, "Demo task")

        await test()
