from typing import Annotated, List
from uuid import UUID
import datetime

from pydantic import BaseModel, Field, ConfigDict


class TodoBase(BaseModel):
    name: str = Field(min_length=1, max_length=40)
    desc: str = Field(min_length=1, max_length=200)


class TodoCreated(TodoBase):
    ...


class NoteBase(BaseModel):
    name: str = Field(min_length=1, max_length=40)
    content: str = Field(min_length=1, max_length=200)


class NoteCreated(NoteBase):
    ...


class NoteReturned(NoteBase):
    owner_id: UUID
    note_id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime


class TodoReturned(TodoBase):
    todo_id: UUID
    owner_id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    notes: List[NoteBase] | None = None
    model_config = ConfigDict(from_attributes=True)


class TodoDeleted(BaseModel):
    item_id: UUID
    success: bool
