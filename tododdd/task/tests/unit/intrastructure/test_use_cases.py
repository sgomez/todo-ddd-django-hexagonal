from asgiref.sync import sync_to_async
from django.http import HttpRequest, HttpResponse
from django.test import TestCase

from tododdd.task.infrastructure.task.models import Task
from tododdd.task.infrastructure.task.schema import schema
from tododdd.task.infrastructure.task.views import Context, command_bus, query_bus


class TestQueries(TestCase):
    async def test_get_empty_tasks_set(self):
        # Arrange
        query = """
            query TestTasks {
                tasks {
                    id
                    title
                    isCompleted
                }
            }
        """
        context_value = Context(
            request=HttpRequest(), response=HttpResponse(), command_bus=command_bus, query_bus=query_bus
        )

        # Act

        rest = await schema.execute(query, context_value=context_value)

        # Assert

        self.assertEqual(rest.data["tasks"], [])

    async def test_get_current_tasks(self):
        # Arrange
        @sync_to_async
        def arrange():
            Task.objects.create(id=1, title="Test task", is_completed=False)

        await arrange()

        query = """
            query TestTasks {
                tasks {
                    id
                    title
                    isCompleted
                }
            }
        """
        context_value = Context(
            request=HttpRequest(), response=HttpResponse(), command_bus=command_bus, query_bus=query_bus
        )

        # Act

        rest = await schema.execute(query, context_value=context_value)

        # Assert

        self.assertEqual(rest.data["tasks"], [{"id": 1, "title": "Test task", "isCompleted": False}])


class TestMutation(TestCase):
    async def test_add_task_mutation(self):
        # Arrange
        mutation = """
            mutation TestCreateTask($id: Int!, $title: String!) {
                createTask(id: $id, title: $title) {
                    id
                    title
                    isCompleted
                }
            }
        """
        variable_values = {"id": 1, "title": "Test task"}
        context_value = Context(
            request=HttpRequest(), response=HttpResponse(), command_bus=command_bus, query_bus=query_bus
        )

        # Act

        resp = await schema.execute(mutation, variable_values=variable_values, context_value=context_value)

        # Assert

        @sync_to_async
        def test():
            found = Task.objects.get(pk=1)
            self.assertEqual(found.title, "Test task")

        await test()

    async def test_task_title_cannot_be_empty(self):
        # Arrange
        mutation = """
            mutation TestCreateTask($id: Int!, $title: String!) {
                createTask(id: $id, title: $title) {
                    id
                    title
                    isCompleted
                }
            }
        """
        variable_values = {"id": 1, "title": " "}
        context_value = Context(
            request=HttpRequest(), response=HttpResponse(), command_bus=command_bus, query_bus=query_bus
        )

        # Act

        resp = await schema.execute(mutation, variable_values=variable_values, context_value=context_value)

        # Assert

        self.assertFalse(resp.data.get("success"))
