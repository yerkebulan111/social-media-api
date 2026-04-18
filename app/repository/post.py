from typing import Sequence

from sqlmodel import Session, select

from app.models.post import Post, PostCreate, PostUpdate


class PostRepository:

    @staticmethod
    def get_all(session: Session, skip: int = 0, limit: int = 20) -> Sequence[Post]:
        return session.exec(select(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit)).all()

    @staticmethod
    def get_by_id(post_id: int, session: Session) -> Post | None:
        return session.exec(select(Post).where(Post.id == post_id)).one_or_none()

    @staticmethod
    def create(post: Post, session: Session) -> Post:
        session.add(post)
        session.commit()
        session.refresh(post)
        return post

    @staticmethod
    def update(post: Post, data: PostUpdate, session: Session) -> Post:
        update_data = data.model_dump(exclude_unset=True)
        post.sqlmodel_update(update_data)
        session.add(post)
        session.commit()
        session.refresh(post)
        return post

    @staticmethod
    def delete(post: Post, session: Session) -> None:
        session.delete(post)
        session.commit()