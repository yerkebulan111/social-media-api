from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.user import User, UserCreate, UserUpdate
from app.repository.user import UserRepository
from app.core.security import hash_password, verify_password, create_access_token


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

    @staticmethod
    def register(data: UserCreate, session: Session) -> User:
        if UserRepository.get_by_email(data.email, session):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        if UserRepository.get_by_username(data.username, session):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already taken",
            )
        user = User(
            email=data.email,
            username=data.username,
            full_name=data.full_name,
            bio=data.bio,
            profile_picture=data.profile_picture,
            password_hashed=hash_password(data.password),
        )
        return UserRepository.create(user, session)

    @staticmethod
    def login(email: str, password: str, session: Session) -> dict:
        user = UserRepository.get_by_email(email, session)
        if not user or not verify_password(password, user.password_hashed):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        token = create_access_token(data={"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer"}