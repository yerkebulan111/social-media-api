from typing import Annotated

from fastapi import APIRouter, Query, status, Depends

from app.core.security import get_current_user_id
from app.database import SessionDep
from app.models.post import PostCreate, PostPublic, PostUpdate
from app.services.post import PostService

router = APIRouter()


CurrentUser = Annotated[int, Depends(get_current_user_id)]

@router.get("/", response_model=list[PostPublic])
def get_posts(
    session: SessionDep,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
):
    return PostService.get_posts(session, skip=skip, limit=limit)


@router.get("/{post_id}", response_model=PostPublic)
def get_post(post_id: int, session: SessionDep):
    return PostService.get_post_by_id(post_id, session)


@router.post("/", response_model=PostPublic, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, session: SessionDep, current_user_id: CurrentUser):
    return PostService.create_post(post, current_user_id, session)


@router.patch("/{post_id}", response_model=PostPublic)
def update_post(post_id: int, post: PostUpdate, session: SessionDep, current_user_id: CurrentUser):
    return PostService.update_post(post_id, post, current_user_id, session)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, session: SessionDep, current_user_id: CurrentUser):
    PostService.delete_post(post_id, current_user_id, session)