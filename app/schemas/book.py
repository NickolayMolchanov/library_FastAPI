from pydantic import BaseModel, ConfigDict


class SBookBase(BaseModel):
    title: str
    description: str | None = None
    year: int | None = None

class SBookCreate(SBookBase):
    author_ids: list[int]


class SBook(SBookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SBookList(BaseModel):
    books: list[SBook]
    total: int
    page: int
    limit: int
