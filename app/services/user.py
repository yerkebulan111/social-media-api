from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.user import User, UserCreate, UserUpdate
from app.repository.user import UserRepository


class UserService:
    @staticmethod
    def get_user(user_id: int, session: Session) -> User:
        user = UserRepository.get_by_id(user_id, session)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @staticmethod
    def get_me(current_user_id: int, session: Session) -> User:
        return UserService.get_user(current_user_id, session)

    @staticmethod
    def update_me(data: UserUpdate, current_user_id: int, session: Session) -> User:
        user = UserRepository.get_by_id(current_user_id, session)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserRepository.update(user, data, session)

    @staticmethod
    def delete_me(current_user_id: int, session: Session) -> None:
        user = UserRepository.get_by_id(current_user_id, session)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        UserRepository.delete(user, session)