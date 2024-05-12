class AppError(Exception):
    ...


"""Interactors errors"""


class InteractorError(AppError):
    ...


class TodoInteractorError(InteractorError):
    ...


class NoteInteractorError(InteractorError):
    ...


class TodoAlreadyExist(TodoInteractorError):
    ...


class NoteAlreadyExist(NoteInteractorError):
    ...


class TodoNotFoundByPk(TodoInteractorError):
    ...


""" Gateway errors """


class GatewayError(AppError):
    ...


class NotFoundError(GatewayError):
    ...


class NoteNotFoundError(NotFoundError):
    ...


class TodoNotFoundError(NotFoundError):
    ...


class IntegrityError(GatewayError):
    ...


class NoteIntegrityError(IntegrityError):
    ...


class TodoIntegrityError(IntegrityError):
    ...
