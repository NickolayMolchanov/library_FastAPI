from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import engine, Base

from app.models.author import Author
from app.models.book import Book

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="API for personal Library",
    lifespan=lifespan,
)

from app.routes.book import router as book_router
from app.routes.author import router as author_router

app.include_router(book_router)
app.include_router(author_router)



