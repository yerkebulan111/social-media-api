from typing import Sequence

from sqlmodel import Session, select

from app.models.comment import Comment, CommentUpdate


class CommentRepository:

    @staticmethod
    def get_by_post(post_id: int, session: Session) -> Sequence[Comment]:
        return session.exec(select(Comment).where(Comment.post_id == post_id).order_by(Comment.created_at.desc())
        ).all()

    @staticmethod
    def get_by_id(comment_id: int, session: Session) -> Comment | None:
        return session.exec(
            select(Comment).where(Comment.id == comment_id)
        ).one_or_none()

    @staticmethod
    def create(comment: Comment, session: Session) -> Comment:
        session.add(comment)
        session.commit()
        session.refresh(comment)
        return comment

    @staticmethod
    def update(comment: Comment, data: CommentUpdate, session: Session) -> Comment:
        update_data = data.model_dump(exclude_unset=True)
        comment.sqlmodel_update(update_data)
        session.add(comment)
        session.commit()
        session.refresh(comment)
        return comment

    @staticmethod
    def delete(comment: Comment, session: Session) -> None:
        session.delete(comment)
        session.commit()