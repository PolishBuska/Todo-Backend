class AppError(Exception):
    ...


class InteractorError(AppError):
    ...


class TodoInteractorError(InteractorError):
    ...


class TodoAlreadyExist(TodoInteractorError):
    ...


class TodoNotFoundByPk(TodoInteractorError):
    ...


class GatewayError(AppError):
    ...


class NotFoundError(GatewayError):
    ...


class TodoNotFoundError(NotFoundError):
    ...


class IntegrityError(GatewayError):
    ...


class TodoIntegrityError(IntegrityError):
    ...
