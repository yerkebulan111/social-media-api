from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    from app.models.post import Post



class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True)
    full_name: str
    bio: str | None = Field(default=None)
    profile_picture: str | None = Field(default=None)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    password_hashed: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# Public response models

class UserPublic(UserBase):
    id: int
    created_at: datetime


class UserPublicBrief(SQLModel):
    """User info for posts, comments and likes"""
    id: int
    username: str
    profile_picture: str | None = None


# Request models

class UserCreate(SQLModel):
    email: str
    username: str
    full_name: str
    password: str
    bio: str | None = None
    profile_picture: str | None = None


class UserUpdate(SQLModel):
    full_name: str | None = None
    bio: str | None = None
    profile_picture: str | None = None


class UserLogin(SQLModel):
    email: str
    password: str