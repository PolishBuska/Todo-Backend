class AppError(Exception):
    ...


class InteractorError(AppError):
    ...


class TodoInteractorError(InteractorError):
    ...


class TodoAlreadyExist(TodoInteractorError):
    ...


class GatewayError(AppError):
    ...


class IntegrityError(GatewayError):
    ...


class TodoIntegrityError(IntegrityError):
    ...
