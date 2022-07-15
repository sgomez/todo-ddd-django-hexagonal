from dataclasses import dataclass

from tododdd.task.application.commands import Command


@dataclass
class GetTasksQuery(Command):
    ...
