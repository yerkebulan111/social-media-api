from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User, UserPublicBrief
    from app.models.post import Post


class CommentBase(SQLModel):
    content: str


class Comment(CommentBase, table=True):
    __tablename__ = "comments"

    id: int = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="posts.id", ondelete="CASCADE")
    author_id: int = Field(foreign_key="users.id", ondelete="CASCADE")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    post: "Post" = Relationship(back_populates="comments")
    author: "User" = Relationship(back_populates="comments")


# response models

class CommentPublic(CommentBase):
    id: int
    post_id: int
    author_id: int
    created_at: datetime


class CommentPublicDetailed(CommentPublic):
    from app.models.user import UserPublicBrief
    author: "UserPublicBrief"


# Request models

class CommentCreate(CommentBase):
    pass


class CommentUpdate(SQLModel):
    content: str | None = None