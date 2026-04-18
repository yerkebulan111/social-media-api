from typing import Sequence

from sqlmodel import Session, select

from app.models.user import User, UserCreate, UserUpdate


class UserRepository:

    @staticmethod
    def get_all(session: Session, skip: int = 0, limit: int = 20) -> Sequence[User]:
        return session.exec(select(User).offset(skip).limit(limit)).all()

    @staticmethod
    def get_by_id(user_id: int, session: Session) -> User | None:
        return session.exec(select(User).where(User.id == user_id)).one_or_none()

    @staticmethod
    def get_by_email(email: str, session: Session) -> User | None:
        return session.exec(select(User).where(User.email == email)).one_or_none()

    @staticmethod
    def get_by_username(username: str, session: Session) -> User | None:
        return session.exec(select(User).where(User.username == username)).one_or_none()

    @staticmethod
    def create(user: User, session: Session) -> User:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def update(user: User, data: UserUpdate, session: Session) -> User:
        update_data = data.model_dump(exclude_unset=True)
        user.sqlmodel_update(update_data)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def delete(user: User, session: Session) -> None:
        session.delete(user)
        session.commit()