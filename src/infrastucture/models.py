from sqlalchemy.orm import Mapped, mapped_column

from src.infrastucture.database import get_base

Base = get_base()


class Todo(Base):
    __tablename__ = "todo"

    todo_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    desc: Mapped[str] = mapped_column(nullable=True)

