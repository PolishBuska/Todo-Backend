from typing import Annotated

import pytest
import uuid
import datetime
from dataclasses import asdict
from unittest.mock import AsyncMock
from sqlalchemy.exc import IntegrityError

from src.domain.exceptions import TodoAlreadyExist, TodoNotFoundByPk, TodoNotFoundError, TodoIntegrityError

from src.infrastucture.impl_dependencies.create_todo import todo_ioc_factory
from src.infrastucture.gateways.todo_gateway import TodoGateway
from src.presentation.todo_ioc_interface import ITodoIoC

from src.application.ioc.todo import CTodoIoC
from src.domain.models import EmptyTodo, Todo, Note, NoteID, TodoNotesStatusDTO

from tests.unit.common import TestDbScalar, TestDbReturnedRaw


@pytest.fixture
def session():
    session = AsyncMock()
    return session


@pytest.fixture
def owner_id():
    return uuid.uuid4()


@pytest.fixture
def empty_todo():
    return EmptyTodo(name='test', desc='test')


@pytest.fixture
def todo_id():
    return uuid.uuid4()


@pytest.fixture
def note():
    owner_id_val = uuid.uuid4()
    return Note(
        note_id=uuid.uuid4(),
        owner_id=owner_id_val,
        content='test',
        name='test',
        created_at='test',
        updated_at='test',
        status=False
    )


@pytest.fixture
def ready_todo(todo_id, owner_id, note):
    return Todo(
        todo_id=todo_id,
        owner_id=owner_id,
        name='test',
        desc='test',
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
        status=True,
        notes=[note]
    )


@pytest.fixture
def todo_db_gateway_mock(session):
    gateway: TodoGateway = AsyncMock()

    return gateway

@pytest.fixture
def todo_db_gateway():
    return TodoGateway

@pytest.fixture
def ioc(todo_db_gateway) -> type(CTodoIoC):
    ioc = CTodoIoC
    return ioc


@pytest.mark.asyncio
async def test_create_todo(
        ioc,
        todo_db_gateway,
        ready_todo,
        empty_todo,
        owner_id
):
    gate = todo_db_gateway
    gate.create_todo = AsyncMock()
    gate.create_todo.return_value = ready_todo
    ioc = ioc(
        todo_db_gateway=gate
    )

    async with ioc.create_todo(
        todo=empty_todo,
        owner_uuid=owner_id
    ) as interactor:
        res = await interactor()
        assert ready_todo == res


@pytest.mark.asyncio
async def test_create_todo_integrity(ioc, todo_db_gateway, empty_todo, owner_id):
    gate = todo_db_gateway
    gate.create_todo = AsyncMock()
    gate.create_todo.side_effect = TodoAlreadyExist
    ioc = ioc(
        todo_db_gateway=gate
    )

    with pytest.raises(TodoAlreadyExist):
        async with ioc.create_todo(
            todo=empty_todo,
            owner_uuid=owner_id
        ) as interactor:
            await interactor()


@pytest.mark.asyncio
async def test_get_todo(
        ioc,
        todo_db_gateway,
        ready_todo,
        todo_id,
        owner_id
):
    gate = todo_db_gateway
    gate.get_todo = AsyncMock()
    gate.get_todo.return_value = ready_todo
    ioc = ioc(
        todo_db_gateway=gate
    )
    async with ioc.get_todo(todo_id=todo_id, owner_id=owner_id) as interactor:
        res = await interactor()
        assert ready_todo == res


@pytest.mark.asyncio
async def test_get_todo_not_found(
        ioc,
        session,
        todo_db_gateway,
        todo_id,
        owner_id
):
    session = session
    session.scalar.return_value = None
    ioc: CTodoIoC = await todo_ioc_factory(
        session=session
    )
    with pytest.raises(TodoNotFoundByPk):
        async with ioc.get_todo(todo_id=todo_id, owner_id=owner_id) as interactor:
            await interactor()


@pytest.mark.asyncio
async def test_update_not_found(
        session,
        todo_id,
        owner_id,
        empty_todo,
        ready_todo
):
    session = session
    session.execute.side_effect = TodoNotFoundError

    ioc: CTodoIoC = await todo_ioc_factory(
        session=session
    )

    with pytest.raises(TodoNotFoundByPk):
        async with ioc.update_todo(
                todo_id=todo_id,
                owner_id=owner_id,
                todo=empty_todo
        ) as interactor:
            await interactor()


@pytest.mark.asyncio
async def test_get_todos_owner_not_found(session, owner_id):
    session = session
    session.scalars.side_effect = TodoNotFoundError

    ioc: CTodoIoC = await todo_ioc_factory(
        session=session
    )
    with pytest.raises(TodoNotFoundByPk):
        async with ioc.get_todos_owner(owner_id) as interactor:
            await interactor()


@pytest.mark.asyncio
async def test_get_todos_notes_not_found(session, owner_id, todo_id):
    session = session
    session.scalar.side_effect = TodoNotFoundError
    todo_note_status = TodoNotesStatusDTO(
        select_status=True,
        todo_id=todo_id
    )

    ioc: CTodoIoC = await todo_ioc_factory(
        session=session
    )

    with pytest.raises(TodoNotFoundByPk):
        async with ioc.get_todo_notes(owner_id=owner_id, todo_notes_query_dto=todo_note_status) as interactor:
            await interactor()
