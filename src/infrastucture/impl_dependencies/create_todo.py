from application.create_todo import CreateTodo
from domain.models import EmptyTodo

from application.interactors.todo import CTodoInteractor


class DbGateway:
    def __init__(self):
        self._cont = []

    async def create_todo(self, todo: EmptyTodo, owner_id):
        self._cont.append(
            (todo, owner_id)
        )
        return self._cont


async def todo_interactor_factory():
    return CTodoInteractor(DbGateway())
