from typing import NewType, List, Annotated, NamedTuple, TypeVar
from uuid import UUID
from dataclasses import dataclass


TodoID = NewType('TodoID', UUID)
NoteID = NewType('NoteID', UUID)


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
    owner_id: UUID
    todo_id: TodoID
    created_at: str
    updated_at: str
    notes: Annotated[List[Note], None] = None


@dataclass
class EmptyNote:
    name: str
    content: str


@dataclass
class Note(EmptyNote):
    owner_id: UUID
    note_id: NoteID
    created_at: str
    updated_at: str


@dataclass
class DeletedResult:
    item_id: UUID
    success: bool
