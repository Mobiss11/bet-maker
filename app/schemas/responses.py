from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

from app.models.common import StatusEnum

T = TypeVar('T')


class BaseResponse(BaseModel):
    status: StatusEnum
    message: str = ""


class DataResponse(BaseResponse, Generic[T]):
    data: Optional[T] = None
