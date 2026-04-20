from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.security import get_current_user_id
from app.database import SessionDep
from app.models.comment import CommentCreate, CommentPublic, CommentUpdate
from app.services.comment import CommentService

router = APIRouter()

CurrentUser = Annotated[int, Depends(get_current_user_id)]


@router.get("/post/{post_id}", response_model=list[CommentPublic])
def get_comments_for_post(post_id: int, session: SessionDep):
    return CommentService.get_comments_for_post(post_id, session)


@router.post("/post/{post_id}", response_model=CommentPublic, status_code=status.HTTP_201_CREATED)
def create_comment(post_id: int, comment: CommentCreate, session: SessionDep, current_user_id: CurrentUser):
    return CommentService.create_comment(post_id, comment, current_user_id, session)


@router.patch("/{comment_id}", response_model=CommentPublic)
def update_comment(comment_id: int, data: CommentUpdate, session: SessionDep, current_user_id: CurrentUser):
    return CommentService.update_comment(comment_id, data, current_user_id, session)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, session: SessionDep, current_user_id: CurrentUser):
    CommentService.delete_comment(comment_id, current_user_id, session)