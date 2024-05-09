import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, ForeignKey, TIMESTAMP, func

from src.infrastucture.database import get_base


Base = get_base()


class Todo(Base):
    __tablename__ = "todos"

    owner_id = Column(UUID(as_uuid=True), nullable=False)
    todo_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    desc: Mapped[str] = mapped_column(nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=func.now(),
                        onupdate=func.now())

    def to_dict(self):
        return {
            "owner_id": str(self.owner_id),
            "todo_id": str(self.todo_id),
            "name": self.name,
            "desc": self.desc,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class Note(Base):
    __tablename__ = "notes"

    owner_id = Column(UUID(as_uuid=True), nullable=False)
    note_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    content: Mapped[str] = mapped_column(nullable=True)
    todo_id_fk = Column(UUID(as_uuid=True), ForeignKey('todos.todo_id'))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=func.now(),
                        onupdate=func.now())
