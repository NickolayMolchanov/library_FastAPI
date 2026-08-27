from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.author import Author
from app.schemas.author import SAuthorCreate


async def create_author(
    session: AsyncSession,
    author_data: SAuthorCreate,
) -> Author:
    author = Author(
        name=author_data.name,
        biography=author_data.biography,
        birthdate=author_data.birthdate,
    )

    session.add(author)
    await session.commit()
    await session.refresh(author)

    return author


async def get_authors(
    session: AsyncSession,
) -> list[Author]:
    stmt = select(Author)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_author_by_id(
    session: AsyncSession,
    author_id: int,
) -> Author | None:
    stmt = select(Author).where(Author.id == author_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def upd_author(
    session: AsyncSession,
    author_id: int,
    author_data: SAuthorCreate,
) -> Author | None:
    stmt = select(Author).where(Author.id == author_id)
    result = await session.execute(stmt)

    author = result.scalar_one_or_none()

    if author is None:
        return None

    author.name = author_data.name
    author.biography = author_data.biography
    author.birthdate = author_data.birthdate

    await session.commit()
    await session.refresh(author)

    return author


async def delete_author(
    session: AsyncSession,
    author: Author,
) -> None:
    await session.delete(author)
    await session.commit()