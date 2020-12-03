from typing import List, Any

from pydantic import BaseModel


class Pagination(BaseModel):
    data: List[Any]
    page: int
    per_page: int = 20
    total: int
