
from fastapi import APIRouter, Query, status


from app.database import SessionDep
from app.models.post import PostCreate, PostPublic, PostUpdate
from app.services.post import PostService

router = APIRouter()


@router.get("/", response_model=list[PostPublic])
def get_posts(
    session: SessionDep,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
):
    return PostService.get_posts(session, skip=skip, limit=limit)


@router.get("/{post_id}", response_model=PostPublic)
def get_post(post_id: int, session: SessionDep):
    return PostService.get_post_by_id(post_id, session)


@router.post("/", response_model=PostPublic, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, session: SessionDep):
    return PostService.create_post(post, session)


@router.patch("/{post_id}", response_model=PostPublic)
def update_post(post_id: int, post: PostUpdate, session: SessionDep):
    return PostService.update_post(post_id, post, session)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, session: SessionDep):
    PostService.delete_post(post_id, session)