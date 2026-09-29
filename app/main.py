from fastapi import FastAPI


app = FastAPI(
    title="API for personal Library",
)


from app.routes.book import router as book_router
from app.routes.author import router as author_router

app.include_router(book_router)
app.include_router(author_router)
