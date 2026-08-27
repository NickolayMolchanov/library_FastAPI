from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book import Book
from app.schemas.book import SBookCreate


async def create_book(
    session: AsyncSession,
    book_data: SBookCreate,
) -> Book:
    book = Book(
        title=book_data.title,
        description=book_data.description,
    )
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book


async def get_book_by_id(
    session: AsyncSession,
    book_id: int,
) -> Book | None:
    stmt = select(Book).where(Book.id == book_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_books(
    session: AsyncSession,
) -> list[Book]:
    stmt = select(Book)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def upd_book(
    session: AsyncSession,
    book_id: int,
    data: SBookCreate,
):
    result = await session.execute(
        select(Book).where(Book.id == book_id)
    )

    book = result.scalar_one_or_none()

    if book is None:
        return None

    book.title = data.title
    book.description = data.description

    await session.commit()
    await session.refresh(book)

    return book


async def delete_book(
    session: AsyncSession,
    book_id: int,
):
    result = await session.execute(
        select(Book).where(Book.id == book_id)
    )

    book = result.scalar_one_or_none()

    if book is None:
        return None

    await session.delete(book)
    await session.commit()

    return book


