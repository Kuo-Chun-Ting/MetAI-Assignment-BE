class ServiceError(Exception):
    status_code: int
    detail: str

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(self.detail)


class BadRequestError(ServiceError):
    status_code = 400


class UnauthorizedError(ServiceError):
    status_code = 401


class NotFoundError(ServiceError):
    status_code = 404


class ConflictError(ServiceError):
    status_code = 409
