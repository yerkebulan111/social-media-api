from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.security import get_current_user_id
from app.database import SessionDep
from app.models.user import UserCreate, UserPublic, UserUpdate
from app.services.user import UserService

router = APIRouter()


CurrentUser = Annotated[int, Depends(get_current_user_id)]

@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, session: SessionDep):
    return UserService.register(user, session)


@router.post("/login")
def login(email: str, password: str, session: SessionDep):
    return UserService.login(email, password, session)

@router.get("/me", response_model=UserPublic)
def get_me(session: SessionDep, current_user_id: CurrentUser):
    return UserService.get_me(session)


@router.patch("/me", response_model=UserPublic)
def update_me(data: UserUpdate, session: SessionDep, current_user_id: CurrentUser):
    return UserService.update_me(data, session)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(session: SessionDep, current_user_id: CurrentUser):
    UserService.delete_me(session)


@router.get("/{user_id}", response_model=UserPublic)
def get_user(user_id: int, session: SessionDep):
    return UserService.get_user(user_id, session)