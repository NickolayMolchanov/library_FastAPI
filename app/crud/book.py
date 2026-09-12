from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.author import Author
from app.models.book import Book
from app.schemas.book import SBookCreate


async def create_book(
    session: AsyncSession,
    book_data: SBookCreate,
) -> Book:
    result = await session.execute(
        select(Author).where(
            Author.id.in_(book_data.author_ids)
        )
    )

    authors = list(result.scalars().all())

    if len(authors) != len(book_data.author_ids):
        raise HTTPException(
            status_code=404,
            detail="One or more authors not found"
        )

    new_book = Book(
        title=book_data.title,
        description=book_data.description,
        authors=authors,
        year=book_data.year,
    )

    if authors is None:
        raise HTTPException(
            status_code=404,
            detail="No author found",
        )

    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return new_book


async def get_books(
    session: AsyncSession,
    year: int | None = None,
    author_id: int | None = None,
    search: str | None = None,
) -> list[Book]:

    query = select(Book)

    if year is not None:
        query = query.where(Book.year == year)

    if author_id is not None:
        query = query.join(Book.authors).where(Author.id == author_id)

    if search is not None:
        query = query.where(Book.title.ilike(f"%{search}%"))

    result = await session.execute(query)
    return list(result.scalars().all())


async def get_book_by_id(
    session: AsyncSession,
    book_id: int,
) -> Book | None:
    stmt = select(Book).where(Book.id == book_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def upd_book(
    session: AsyncSession,
    book_id: int,
    book_data: SBookCreate,
):
    result = await session.execute(
        select(Book)
        .options(selectinload(Book.authors))
        .where(Book.id == book_id)
    )

    book = result.scalar_one_or_none()

    if book is None:
        return None

    book.title = book_data.title
    book.description = book_data.description

    if book_data.author_ids is not None:
        authors_result = await session.execute(
            select(Author).where(Author.id.in_(book_data.author_ids))
        )

        authors = authors_result.scalars().all()

        if len(authors) != len(book_data.author_ids):
            raise HTTPException(
                status_code=404,
                detail="One or more authors not found"
            )

        book.authors = authors

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


