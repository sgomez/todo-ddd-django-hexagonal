from dataclasses import dataclass


@dataclass(frozen=True)
class TaskTitle:
    value: str

    def __post_init__(self):
        if 0 == len(self.value.strip()):
            raise Exception("Empty title cannot be empty.")

        if len(self.value.strip()) > 200:
            raise Exception("Invalid length.")

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TaskTitle) and self.value == other.value


class Task:
    __id: int
    __title: TaskTitle
    __is_completed: bool

    def __init__(self, id: int, title: TaskTitle) -> None:
        self.__id = id
        self.__title = title
        self.__is_completed = False

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Task) and self.__id == other.__id and self.__title == other.__title

    @property
    def id(self) -> int:
        return self.__id

    @property
    def title(self) -> TaskTitle:
        return self.__title

    @property
    def is_completed(self) -> bool:
        return self.__is_completed
