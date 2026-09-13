from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.user.dtos import UserSchema
user_router = APIRouter(prefix="/user")


@user_router.post("/register")
def register(body: UserSchema, db: Session):