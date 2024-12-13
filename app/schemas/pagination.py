from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional
# from pydantic.generics import GenericModel

T = TypeVar("T")

class PaginationBase(BaseModel):
    total: int
    limit: int
    offset: int
    next_offset: Optional[int]
    prev_offset: Optional[int]

class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    pagination: PaginationBase
