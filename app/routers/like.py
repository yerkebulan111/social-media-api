from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import get_current_user_id
from app.database import SessionDep
from app.models.like import LikePublic
from app.services.like import LikeService

router = APIRouter()

CurrentUser = Annotated[int, Depends(get_current_user_id)]


@router.post("/post/{post_id}", response_model=LikePublic)
def toggle_like(post_id: int, session: SessionDep, current_user_id: CurrentUser):
    """Toggle a post like: like a post if not liked yet, or unlike it if already liked"""
    return LikeService.toggle_like(post_id, current_user_id, session)