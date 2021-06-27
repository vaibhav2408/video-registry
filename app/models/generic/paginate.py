from pydantic import BaseModel


class Paginate(BaseModel):
    """Wrapper for pagination"""

    offset: int = 0
    count_per_page: int = 2000
    total_count: int = 0
