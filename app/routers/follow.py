from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import get_current_user_id
from app.database import SessionDep
from app.models.follow import FollowPublic
from app.models.user import UserPublic
from app.services.follow import FollowService

router = APIRouter()

CurrentUser = Annotated[int, Depends(get_current_user_id)]


@router.post("/{user_id}", response_model=FollowPublic)
def toggle_follow(user_id: int, session: SessionDep, current_user_id: CurrentUser):
    """Follow a user if not following yet, or unfollow if already following."""
    return FollowService.toggle_follow(user_id, current_user_id, session)


@router.get("/{user_id}/following", response_model=list[UserPublic])
def get_following(user_id: int, session: SessionDep):
    return FollowService.get_following(user_id, session)


@router.get("/{user_id}/followers", response_model=list[UserPublic])
def get_followers(user_id: int, session: SessionDep):
    return FollowService.get_followers(user_id, session)