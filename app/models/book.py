from typing import Optional, List
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.database import Base
from app.models.associations import association_table


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[Optional[str]] = mapped_column(String(30))

    authors: Mapped[List["Author"]] = relationship(
        secondary=association_table,
        back_populates="books",
    )