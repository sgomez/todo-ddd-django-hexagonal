from turtle import title
from unittest import mock

import pytest
from django.test import SimpleTestCase

from tododdd.task.application.command_handlers import AddTaskCommandHandler
from tododdd.task.application.commands import AddTaskCommand
from tododdd.task.domain.model import Task, TaskTitle
from tododdd.task.domain.repository import TaskRepository


class TestAddTask(SimpleTestCase):
    @pytest.mark.asyncio
    @mock.patch.object(TaskRepository, "save")
    async def test_add_a_new_task(self, repository_add_mocked):
        # Arrange
        task = Task(id=1, title=TaskTitle("To do a DDD workshop"))

        # Act
        command = AddTaskCommand(id=1, title="To do a DDD workshop")
        handler = AddTaskCommandHandler(repository=repository_add_mocked)

        await handler.handle(command=command)

        # Assert
        repository_add_mocked.save.assert_called_once_with(task)
