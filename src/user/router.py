from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user import controller
from src.user.dtos import UserSchema, UserResponseSchema, UserLoginSchema, TokenResponseSchema 
from src.utils.helpers import is_authenticated
from src.user.models import UserModel

user_router = APIRouter(prefix="/user")


@user_router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def register(body: UserSchema, db: Session = Depends(get_db)):
    return controller.register(body, db)

@user_router.post(
    "/login",
    response_model=TokenResponseSchema,
    status_code=status.HTTP_200_OK
)
def login(body: UserLoginSchema, db: Session = Depends(get_db)):
    return controller.login(body, db)

@user_router.get(
    "/is_authenticated",
    status_code=status.HTTP_200_OK)
def is_authenticated(request: Request, db: Session = Depends(get_db)):
    return controller.is_authenticated(request, db)