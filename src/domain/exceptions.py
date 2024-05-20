class AppError(Exception):
    ...


"""Interactors errors"""


class InteractorError(AppError):
    ...


class TodoInteractorError(InteractorError):
    ...


class NoteInteractorError(InteractorError):
    ...


class TodoNotesEmptyError(InteractorError):
    ...


class TodoNotesStatusFalse(InteractorError):
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


class NoteNotFoundByPk(NoteNotFoundError):
    ...


class TodoNotFoundError(NotFoundError):
    ...


class IntegrityError(GatewayError):
    ...


class NoteIntegrityError(IntegrityError):
    ...


class TodoIntegrityError(IntegrityError):
    ...
