from typing import Annotated
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
import uuid
import datetime
from dataclasses import asdict

from sqlalchemy.exc import IntegrityError


from src.domain.exceptions import TodoAlreadyExist, TodoNotFoundByPk, TodoNotFoundError
from src.infrastucture.impl_dependencies.create_todo import todo_ioc_factory

from src.domain.todo_ioc_interface import ITodoIoC

from src.domain.models import EmptyTodo, Todo, Note, NoteID


class TestDbReturnedRaw:
    def __init__(self, res):
        self._res = res

    def to_dict(self):
        return asdict(self._res)


class TestDbTodoScalar:
    def __init__(self, res):
        self._res = res
        self._return = TestDbReturnedRaw

    def scalar(self):
        return self._return(res=self._res)


class TestTodo(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.session = AsyncMock()
        self.session.execute = AsyncMock()
        self.session.scalar = AsyncMock()
        self.session.scalars = AsyncMock()
        self.session.commit = AsyncMock()
        self.owner_id = uuid.uuid4()
        self.empty_todo = EmptyTodo(
            name='test',
            desc='test'
        )
        self.todo_id = uuid.uuid4()
        self.note = Note(
            note_id=Annotated[uuid.uuid4(), NoteID],
            owner_id=self.owner_id,
            content='test',
            name='test',
            created_at='test',
            updated_at='test',
            status=False
        )
        self.ready_todo = Todo(
            todo_id=self.todo_id,
            owner_id=self.owner_id,
            name='test',
            desc='test',
            created_at=Annotated[datetime.datetime.now(), str],
            updated_at=Annotated[datetime.datetime.now(), str],
            status=True,
            notes=[self.note]

        )
        self.ioc: ITodoIoC = await todo_ioc_factory(
            session=self.session,
        )

    async def test_create_todo(self):
        self.session.execute.return_value = TestDbTodoScalar(res=self.ready_todo)

        async with self.ioc.create_todo(
            todo=self.empty_todo,
            owner_uuid=self.owner_id

        ) as interactor:
            res = await interactor()
            self.assertEqual(self.ready_todo.notes, res.notes)

    async def test_create_todo_integrity(self):
        self.session.execute.side_effect = IntegrityError(statement=None, params=None, orig=None)
        with self.assertRaises(TodoAlreadyExist):
            async with self.ioc.create_todo(
                todo=self.empty_todo,
                owner_uuid=self.owner_id

            ) as interactor:
                res = await interactor()
                self.assertIn(self.note, self.ready_todo.notes)

    async def test_get_todo(self):
        self.session.scalar.return_value = TestDbReturnedRaw(res=self.ready_todo)
        async with self.ioc.get_todo(todo_id=self.todo_id, owner_id=self.owner_id) as interactor:
            res = await interactor()
            self.assertEqual(str(res.todo_id), str(self.todo_id))

    async def test_get_todo_not_found(self):
        self.session.scalar.return_value = None

        with self.assertRaises(TodoNotFoundByPk):
            async with self.ioc.get_todo(todo_id=self.todo_id, owner_id=self.owner_id) as interactor:
                res = await interactor()

    async def test_update_not_found(self):
        self.session.execute.side_effect = TodoNotFoundError

        with self.assertRaises(TodoNotFoundByPk):
            async with self.ioc.update_todo(
                    todo_id=self.todo_id,
                    owner_id=self.owner_id,
                    todo=self.empty_todo
            ) as interactor:
                await interactor()

    async def test_get_todos_owner_not_found(self):
        self.session.scalars.side_effect = TodoNotFoundError

        with self.assertRaises(TodoNotFoundByPk):
            async with self.ioc.get_todos_owner(self.owner_id) as interactor:
                await interactor()

    async def test_get_todos_notes_not_found(self):
        self.session.scalar.side_effect = TodoNotFoundError

        with self.assertRaises(TodoNotFoundByPk):
            async with self.ioc.get_todo_notes(owner_id=self.owner_id, todo_id=self.todo_id) as interactor:
                await interactor()

    async def test_get_todos_notes(self):
        self.session.scalar.return_value = TestDbReturnedRaw(self.ready_todo)

        async with self.ioc.get_todo_notes(owner_id=self.owner_id, todo_id=self.todo_id) as interactor:
            res = await interactor()

            self.assertEqual(asdict(self.ready_todo.notes[0]), res.notes[0])

