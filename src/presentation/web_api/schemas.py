from pydantic import BaseModel, Field


class TodoBase(BaseModel):
    name: str = Field(min_length=1, max_length=40)
    desc: str = Field(min_length=1, max_length=200)


class TodoCreated(TodoBase):
    ...
