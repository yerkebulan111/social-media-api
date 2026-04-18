from datetime import datetime, timezone
from typing import Sequence

from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.post import Post, PostCreate, PostPublic, PostUpdate
from app.repository.post import PostRepository


class PostService:

    @staticmethod
    def get_posts(session: Session, skip: int = 0, limit: int = 20) -> Sequence[Post]:
        return PostRepository.get_all(session, skip=skip, limit=limit)

    @staticmethod
    def get_post_by_id(post_id: int, session: Session) -> Post:
        post = PostRepository.get_by_id(post_id, session)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return post

    @staticmethod
    def create_post(data: PostCreate, author_id: int, session: Session) -> Post:
        post = Post.model_validate({**data.model_dump(), "author_id": author_id})
        return PostRepository.create(post, session)

    @staticmethod
    def update_post(post_id: int, data: PostUpdate, current_user_id: int, session: Session) -> Post:
        post = PostRepository.get_by_id(post_id, session)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if post.author_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your post")
        post.updated_at = datetime.now(timezone.utc)
        return PostRepository.update(post, data, session)

    @staticmethod
    def delete_post(post_id: int, current_user_id: int, session: Session) -> None:
        post = PostRepository.get_by_id(post_id, session)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if post.author_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your post")
        PostRepository.delete(post, session)