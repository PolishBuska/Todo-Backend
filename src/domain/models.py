from typing import NewType, List, Annotated, NamedTuple, TypeVar, Optional
from uuid import UUID
from dataclasses import dataclass


TodoID = NewType('TodoID', UUID)
NoteID = NewType('NoteID', UUID)


@dataclass
class EmptyTodo:
    name: str
    desc: str


@dataclass
class TodoNotesStatusDTO:
    todo_id: UUID
    select_status: Optional[bool] = None


@dataclass
class EmptyNote:
    name: str
    content: str


@dataclass
class Note(EmptyNote):
    owner_id: UUID
    note_id: UUID
    created_at: str
    updated_at: str
    status: bool


@dataclass
class Todo(EmptyTodo):
    owner_id: UUID
    todo_id: UUID
    created_at: str
    updated_at: str
    status: bool
    notes: Annotated[List[Note], None] = None


@dataclass
class DeletedResult:
    item_id: UUID
    success: bool
