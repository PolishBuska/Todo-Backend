from typing import NewType, List, Annotated
from dataclasses import dataclass

TodoID = NewType('TodoID', int)


@dataclass
class Note:
    title: str
    content: str


@dataclass
class EmptyTodo:
    name: str
    desc: str


@dataclass
class Todo(EmptyTodo):
    todo_id: TodoID
    notes: Annotated[List[Note], None]
