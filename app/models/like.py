from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.post import Post


class Like(SQLModel, table=True):
    __tablename__ = "likes"

    user_id: int = Field(foreign_key="users.id", primary_key=True, ondelete="CASCADE")
    post_id: int = Field(foreign_key="posts.id", primary_key=True, ondelete="CASCADE")

    user: "User" = Relationship(back_populates="likes")
    post: "Post" = Relationship(back_populates="likes")


class LikePublic(SQLModel):
    user_id: int
    post_id: int
    message: str