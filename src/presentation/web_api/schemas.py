from enum import Enum
from typing import Annotated, List, Optional
from uuid import UUID
import datetime

from pydantic import BaseModel, Field, ConfigDict, validator, field_validator

from domain.models import Todo


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
    status: bool


class TodoReturned(TodoBase):
    todo_id: UUID
    owner_id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    status: bool
    notes: List[NoteReturned] | None = None
    model_config = ConfigDict(from_attributes=True)


class Status(str, Enum):
    confirmed = 'confirmed'
    unconfirmed = 'unconfirmed'


class TodoNotesStatus(BaseModel):
    todo_id: UUID
    select_status: Optional[Status] = Field(None, description="Please enter either 'confirmed' or 'unconfirmed'")


class ListTodoReturned(BaseModel):
    todos: List[Todo]
    model_config = ConfigDict(from_attributes=True)


class TodoDeleted(BaseModel):
    item_id: UUID
    success: bool
