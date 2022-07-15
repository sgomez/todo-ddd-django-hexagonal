from dataclasses import dataclass
from turtle import title


@dataclass
class TaskDto:
    id: int
    title: str
    is_completed: bool
