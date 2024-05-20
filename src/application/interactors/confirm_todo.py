from uuid import UUID

from domain.exceptions import TodoNotesEmptyError, TodoNotesStatusFalse


class ConfirmTodo:
    def __init__(self, todo_db_gateway, todo_id: UUID, owner_id: UUID):
        self._todo_db_gateway = todo_db_gateway
        self._todo_id = todo_id
        self._owner_id = owner_id

    async def __call__(self):
        try:
            todo = await self._todo_db_gateway.get_todo_notes(todo_id=self._todo_id, owner_id=self._owner_id)
            notes = todo.notes

            if not notes:
                raise AttributeError('Todo is empty')

            if all(note.status for note in notes):
                todo.status = True
                await self._todo_db_gateway.update_todo(todo)
            else:
                raise ValueError("Cannot confirm todo, not all notes are confirmed")

        except ValueError as ve:
            raise TodoNotesStatusFalse("All notes must be set to True") from ve
        except AttributeError as ae:
            raise TodoNotesEmptyError("No notes found") from ae
