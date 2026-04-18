from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User, UserPublicBrief


class PostBase(SQLModel):
    title: str
    content: str
    published: bool = Field(default=False)


class Post(PostBase, table=True):
    __tablename__ = "posts"

    id: int = Field(default=None, primary_key=True)
    author_id: int = Field(foreign_key="users.id", ondelete="CASCADE")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    author: "User" = Relationship(back_populates="posts")
    comments: list["Comment"] = Relationship(back_populates="post")
    likes: list["Like"] = Relationship(back_populates="post")


# Public response models

class PostPublic(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime


class PostPublicDetailed(PostPublic):
    from app.models.user import UserPublicBrief
    author: "UserPublicBrief"
    likes_count: int = 0
    comments_count: int = 0


# Request models

class PostCreate(PostBase):
    pass


class PostUpdate(SQLModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None