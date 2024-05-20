from uuid import UUID

from domain.exceptions import TodoNotFoundError, TodoNotFoundByPk
from domain.models import Todo, TodoNotesStatusDTO


class GetTodoNotes:
    def __init__(
            self,
            owner_id: UUID,
            todo_notes_status_dto: TodoNotesStatusDTO,
            todo_db_gateway
    ):
        self._owner_id = owner_id
        self._dto = todo_notes_status_dto
        self._todo_db_gateway = todo_db_gateway

    async def __call__(self) -> Todo:
        try:
            if self._dto.select_status is None:
                result = await self._todo_db_gateway.get_todo_notes(owner_id=self._owner_id, dto=self._dto)
                return result
            else:
                if self._dto.select_status is True:
                    result = await self._todo_db_gateway.get_todo_notes_option(
                        owner_id=self._owner_id,
                        todo_id=self._dto.todo_id,
                        select_option=self._dto.select_status
                    )
                    return result
                elif self._dto.select_status is False:
                    result = await self._todo_db_gateway.get_todo_notes_option(
                        owner_id=self._owner_id,
                        todo_id=self._dto.todo_id,
                        select_option=self._dto.select_status
                    )
                    return result
        except TodoNotFoundError as tnf:
            raise TodoNotFoundByPk from tnf
