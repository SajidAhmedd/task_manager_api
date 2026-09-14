from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from src.user.dtos import UserSchema, UserLoginSchema
from src.user.models import UserModel
from src.utils.settings import settings


password_hasher = PasswordHash.recommended()


def get_password_hash(password: str):
    return password_hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return password_hasher.verify(plain_password, hashed_password)


def exp_time():
    return datetime.now(timezone.utc) + timedelta(
        minutes=settings.EXPIRE_MINUTES
    )


def register(body: UserSchema, db: Session):
    is_user = (
        db.query(UserModel)
        .filter(UserModel.username == body.username)
        .first()
    )

    if is_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    hash_password = get_password_hash(body.password)

    new_user = UserModel(
        name=body.name,
        username=body.username,
        email=body.email,
        hash_password=hash_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login(body: UserLoginSchema, db: Session):
    user = (
        db.query(UserModel)
        .filter(UserModel.username == body.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not verify_password(body.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )

    token = jwt.encode(
        {
            "user_id": user.id,
            "exp": exp_time()
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return {"token": token}
