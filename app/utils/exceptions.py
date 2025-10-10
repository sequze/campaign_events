class AppError(Exception):
    message = "Application error"

    def __init__(self, detail: str | None = None):
        super().__init__(detail or self.message)
        self.detail = detail or self.message


class NotFoundError(AppError):
    message = "Resource not found"


class AlreadyExistsError(AppError):
    message = "Resource already exists"


class EventNotFound(NotFoundError):
    message = "Event not found"


class CampaignNotFound(NotFoundError):
    message = "Campaign not found"


class EventAlreadyExists(AlreadyExistsError):
    message = "Event already exists"


class CampaignAlreadyExists(AlreadyExistsError):
    message = "Campaign already exists"
