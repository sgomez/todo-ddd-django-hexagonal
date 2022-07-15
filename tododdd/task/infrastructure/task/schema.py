from dataclasses import dataclass
from typing import Any, List

import strawberry
from strawberry.scalars import JSON
from strawberry.types import Info

from tododdd.task.application.commands import AddTaskCommand
from tododdd.task.application.queries import GetTasksQuery
from tododdd.task.domain.exception import DomainError
from tododdd.task.infrastructure.task.views import Context


@dataclass
@strawberry.type
class TaskResponse:
    id: int
    title: str
    is_completed: bool
    success: bool
    errors: JSON


@dataclass
@strawberry.type
class TaskNode:
    id: int
    title: str
    is_completed: bool


@strawberry.type
class Query:
    @strawberry.field
    async def tasks(self, info: Info[Context, Any]) -> List[TaskNode]:
        result = await info.context.query_bus.dispatch(GetTasksQuery())

        return result


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_task(self, info: Info[Context, Any], id: int, title: str) -> "TaskResponse":
        command = AddTaskCommand(id=id, title=title)
        success = True
        errors = {}

        try:
            await info.context.command_bus.dispatch(command=command)
        except DomainError:
            success = False
            errors["title"] = "Wrong title"

        return TaskResponse(id=id, title=title, is_completed=False, success=success, errors=errors)


schema = strawberry.Schema(mutation=Mutation, query=Query)
