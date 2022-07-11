from dataclasses import dataclass
from turtle import title


class Command:
    ...


@dataclass(frozen=True)
class AddTaskCommand(Command):
    id: int
    title: str
