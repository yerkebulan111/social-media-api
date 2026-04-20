from sqlmodel import Session, select

from app.models.like import Like


class LikeRepository:

    @staticmethod
    def get(user_id: int, post_id: int, session: Session) -> Like | None:
        return session.exec(
            select(Like).where(Like.user_id == user_id, Like.post_id == post_id)
        ).one_or_none()

    @staticmethod
    def count_by_post(post_id: int, session: Session) -> int:
        return len(session.exec(select(Like).where(Like.post_id == post_id)).all())

    @staticmethod
    def create(like: Like, session: Session) -> Like:
        session.add(like)
        session.commit()
        session.refresh(like)
        return like

    @staticmethod
    def delete(like: Like, session: Session) -> None:
        session.delete(like)
        session.commit()