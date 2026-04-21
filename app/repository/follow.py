from pyasn1.type.univ import Sequence
from sqlmodel import Session, select

from app.models.follow import Follow


class FollowRepository:

    @staticmethod
    def get(follower_id: int, followed_id: int, session: Session) -> Follow | None:
        return session.exec(
            select(Follow).where(
                Follow.follower_id == follower_id,
                Follow.followed_id == followed_id,
            )
        ).one_or_none()

    @staticmethod
    def get_following(user_id: int, session: Session) -> Sequence[Follow]:
        return session.exec(select(Follow).where(Follow.follower_id == user_id)).all()

    @staticmethod
    def get_followers(user_id: int, session: Session) -> Sequence[Follow]:
        return session.exec(select(Follow).where(Follow.followed_id == user_id)).all()

    @staticmethod
    def create(follow: Follow, session: Session) -> Follow:
        session.add(follow)
        session.commit()
        session.refresh(follow)
        return follow

    @staticmethod
    def delete(follow: Follow, session: Session) -> None:
        session.delete(follow)
        session.commit()