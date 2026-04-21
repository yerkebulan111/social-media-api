from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User


class Follow(SQLModel, table=True):
    __tablename__ = "follows"

    follower_id: int = Field(
        foreign_key="users.id", primary_key=True, ondelete="CASCADE"
    )
    followed_id: int = Field(
        foreign_key="users.id", primary_key=True, ondelete="CASCADE"
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    follower: "User" = Relationship(
        back_populates="following",
        sa_relationship_kwargs={"foreign_keys": "[Follow.follower_id]"},
    )
    followed: "User" = Relationship(
        back_populates="followers",
        sa_relationship_kwargs={"foreign_keys": "[Follow.followed_id]"},
    )


class FollowPublic(SQLModel):
    follower_id: int
    followed_id: int
    message: str