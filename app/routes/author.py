from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.author import (
    get_author_by_id,
    get_authors,
    create_author,
    delete_author,
    upd_author,
)
from app.database import get_db
from app.schemas.author import SAuthorCreate

router = APIRouter(
    prefix="/authors",
    tags=["authors"],
)


@router.post("/")
async def create_new_author(
    author_data: SAuthorCreate,
    session: AsyncSession = Depends(get_db),
):
    return await create_author(session, author_data)


@router.get("/{author_id}")
async def get_author(
    author_id: int,
    session: AsyncSession = Depends(get_db),
):
    author = await get_author_by_id(
        session=session,
        author_id=author_id,
    )

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return author


@router.get("/")
async def get_all_authors(
    session: AsyncSession = Depends(get_db),
):
    authors = await get_authors(session)

    return authors


@router.put("/{author_id}")
async def update_author_route(
    author_id: int,
    author_data: SAuthorCreate,
    session: AsyncSession = Depends(get_db),
):
    author = await upd_author(
        session=session,
        author_id=author_id,
        author_data=author_data,
    )

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return author


@router.delete("/{author_id}")
async def delete_author_route(
    author_id: int,
    session: AsyncSession = Depends(get_db),
):
    author = await get_author_by_id(
        session=session,
        author_id=author_id,
    )

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    await delete_author(
        session=session,
        author=author,
    )

    return {
        "message": "Author deleted successfully"
    }