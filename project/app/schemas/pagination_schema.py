from typing import Generic, List, TypeVar

from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginationOutputSchema(GenericModel, Generic[T]):

    page_number: int
    page_size: int
    total_pages: int
    total_record: int
    content: List[T]
