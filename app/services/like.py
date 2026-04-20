from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.like import Like, LikePublic
from app.repository.like import LikeRepository
from app.repository.post import PostRepository


class LikeService:

    @staticmethod
    def toggle_like(post_id: int, user_id: int, session: Session) -> LikePublic:
        post = PostRepository.get_by_id(post_id, session)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        existing = LikeRepository.get(user_id, post_id, session)
        if existing:
            LikeRepository.delete(existing, session)
            return LikePublic(user_id=user_id, post_id=post_id, message="Like removed")

        like = Like(user_id=user_id, post_id=post_id)
        LikeRepository.create(like, session)
        return LikePublic(user_id=user_id, post_id=post_id, message="Post liked")