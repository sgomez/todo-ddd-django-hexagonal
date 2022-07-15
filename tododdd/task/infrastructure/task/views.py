from dataclasses import dataclass
from typing import Any, Dict, Type

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from strawberry.django.views import AsyncGraphQLView as BaseAsyncGraphQLView
from strawberry.django.views import StrawberryDjangoContext

from tododdd.task.application.command_handlers import AddTaskCommandHandler, Handler
from tododdd.task.application.commands import AddTaskCommand, Command
from tododdd.task.application.queries import GetTasksQuery
from tododdd.task.application.query_handlers import GetTasksQueryHandler
from tododdd.task.infrastructure.task.services import DjangoTaskFinder

from .repository import DjangoTaskRepository

# Create your views here.


@dataclass
class Dispatcher:
    handlers: Dict[Type[Command], Handler]

    async def dispatch(self, command: Command) -> Any:
        handler = self.handlers.get(command.__class__)
        if not handler:
            raise RuntimeError(f"Not found handler for {command.__class__}")

        return await handler.handle(command)


repository = DjangoTaskRepository()
finder = DjangoTaskFinder()

command_bus = Dispatcher(handlers={})
command_bus.handlers[AddTaskCommand] = AddTaskCommandHandler(repository=repository)


query_bus = Dispatcher(handlers={})
query_bus.handlers[GetTasksQuery] = GetTasksQueryHandler(finder=finder)


@dataclass
class Context(StrawberryDjangoContext):
    command_bus: Dispatcher
    query_bus: Dispatcher


class AsyncGraphQLView(BaseAsyncGraphQLView):
    async def get_context(self, request: HttpRequest, response: HttpResponse) -> Any:
        return Context(request=request, response=response, command_bus=command_bus, query_bus=query_bus)
