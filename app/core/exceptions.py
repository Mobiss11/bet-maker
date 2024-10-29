from fastapi import HTTPException


class BetValidationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)


class EventNotFoundError(HTTPException):
    def __init__(self, event_id: str):
        super().__init__(
            status_code=404,
            detail=f"Событие с ID {event_id} не найдено"
        )


class DeadlinePassedError(HTTPException):
    def __init__(self, event_id: str):
        super().__init__(
            status_code=400,
            detail=f"Время для ставок на событие {event_id} истекло"
        )


class LineProviderError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=502,
            detail=f"Ошибка при обращении к Line Provider: {detail}"
        )
