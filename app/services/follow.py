from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.follow import Follow, FollowPublic
from app.models.user import User
from app.repository.follow import FollowRepository
from app.repository.user import UserRepository


class FollowService:

    @staticmethod
    def toggle_follow(followed_id: int, follower_id: int, session: Session) -> FollowPublic:
        if follower_id == followed_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot follow yourself",
            )

        target = UserRepository.get_by_id(followed_id, session)
        if not target:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        existing = FollowRepository.get(follower_id, followed_id, session)
        if existing:
            FollowRepository.delete(existing, session)
            return FollowPublic(follower_id=follower_id, followed_id=followed_id, message="Unfollowed")

        follow = Follow(follower_id=follower_id, followed_id=followed_id)
        FollowRepository.create(follow, session)
        return FollowPublic(follower_id=follower_id, followed_id=followed_id, message="Following")

    @staticmethod
    def get_following(user_id: int, session: Session) -> list[User]:
        follows = FollowRepository.get_following(user_id, session)
        return [
            UserRepository.get_by_id(f.followed_id, session)
            for f in follows
        ]

    @staticmethod
    def get_followers(user_id: int, session: Session) -> list[User]:
        follows = FollowRepository.get_followers(user_id, session)
        return [
            UserRepository.get_by_id(f.follower_id, session)
            for f in follows
        ]