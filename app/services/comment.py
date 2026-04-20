from typing import Sequence

from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.comment import Comment, CommentCreate, CommentUpdate
from app.repository.comment import CommentRepository
from app.repository.post import PostRepository


class CommentService:

    @staticmethod
    def get_comments_for_post(post_id: int, session: Session) -> Sequence[Comment]:
        post = PostRepository.get_by_id(post_id, session)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return CommentRepository.get_by_post(post_id, session)

    @staticmethod
    def create_comment(post_id: int, data: CommentCreate, author_id: int, session: Session) -> Comment:
        post = PostRepository.get_by_id(post_id, session)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        comment = Comment(content=data.content, post_id=post_id, author_id=author_id)
        return CommentRepository.create(comment, session)

    @staticmethod
    def update_comment(comment_id: int, data: CommentUpdate, current_user_id: int, session: Session) -> Comment:
        comment = CommentRepository.get_by_id(comment_id, session)
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        if comment.author_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your comment")
        return CommentRepository.update(comment, data, session)

    @staticmethod
    def delete_comment(comment_id: int, current_user_id: int, session: Session) -> None:
        comment = CommentRepository.get_by_id(comment_id, session)
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        if comment.author_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your comment")
        CommentRepository.delete(comment, session)