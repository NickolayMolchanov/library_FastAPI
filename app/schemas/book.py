from pydantic import BaseModel, ConfigDict


class SBookBase(BaseModel):
    title: str
    description: str | None = None

class SBookCreate(SBookBase):
    pass

class SBook(SBookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
