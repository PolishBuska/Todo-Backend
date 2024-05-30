from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
import uuid

from sqlalchemy.exc import IntegrityError

from src.domain.exceptions import NoteAlreadyExist, NotFoundError, NoteNotFoundError

from src.infrastucture.impl_dependencies.note import note_ioc_factory
from tests.unit.common import TestDbScalar, TestDbReturnedRaw

from src.presentation.note_ioc_interface import INoteIoC

from src.domain.models import EmptyNote, Note


class TestNote(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.session = AsyncMock()
        self.session.execute = AsyncMock()
        self.session.scalar = AsyncMock()
        self.session.scalars = AsyncMock()
        self.session.commit = AsyncMock()
        self.owner_id = uuid.uuid4()
        self.todo_id = uuid.uuid4()
        self.note_id = uuid.uuid4()
        self.empty_note = EmptyNote(
            name='test',
            content='test'
        )
        self.note = Note(

            note_id=self.note_id,
            owner_id=self.owner_id,
            content='test',
            name='test',
            created_at='test',
            updated_at='test',
            status=False
        )
        self.ioc: INoteIoC = await note_ioc_factory(session=self.session)

    async def test_create_note(self):
        self.session.execute.return_value = TestDbScalar(self.note)
        async with self.ioc.create_note(
                note=self.empty_note,
                owner_id=self.owner_id,
                todo_id=self.todo_id
        ) as interactor:
            res = await interactor()
            self.assertEqual(self.note.name, res.name)

    async def test_create_note_integrity(self):
        self.session.execute.side_effect = IntegrityError(statement=None, params=None, orig=None)
        with self.assertRaises(NoteAlreadyExist):
            async with self.ioc.create_note(
                    note=self.empty_note,
                    owner_id=self.owner_id,
                    todo_id=self.todo_id
            ) as interactor:
                await interactor()

    async def test_get_note(self):
        self.session.scalar.return_value = TestDbReturnedRaw(self.note)

        async with self.ioc.get_note(
            todo_id=self.todo_id,
            owner_id=self.owner_id,
            note_id=self.note_id
        ) as interactor:
            res: Note = await interactor()
            self.assertEqual(self.note, res)
            self.assertTrue(expr=isinstance(res, Note))

    async def test_get_note_not_found(self):
        self.session.scalar.side_effect = NotFoundError
        with self.assertRaises(NoteNotFoundError):
            async with self.ioc.get_note(
                    todo_id=self.todo_id,
                    owner_id=self.owner_id,
                    note_id=self.note_id
            ) as interactor:
                await interactor()

    async def test_update_note_not_found(self):
        self.session.execute.side_effect = NoteNotFoundError
        with self.assertRaises(NoteNotFoundError):
            async with self.ioc.update_note(
                note=self.empty_note,
                todo_id=self.todo_id,
                owner_id=self.owner_id,
                note_id=self.note_id
            ) as interactor:
                await interactor()


