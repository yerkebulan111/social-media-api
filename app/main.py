from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_db_and_tables
from app.routers import post, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="SocialMediaAPI",
    description="A social media REST API built with FastAPI and PostgreSQL"
)

app.include_router(post.router, prefix="/posts", tags=["posts"])
app.include_router(user.router, prefix="/users", tags=["users"])


@app.get("/", tags=["root"])
def root():
    return {"message": "SocialMediaAPI is working"}