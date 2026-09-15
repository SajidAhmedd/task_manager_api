from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException, status, Request
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from src.user.dtos import UserSchema, UserLoginSchema
from src.user.models import UserModel
from src.utils.settings import settings
from src.utils import db


password_hasher = PasswordHash.recommended()


def get_password_hash(password: str):
    return password_hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return password_hasher.verify(plain_password, hashed_password)


def exp_time():
    return datetime.now(timezone.utc) + timedelta(minutes=settings.EXPIRE_MINUTES)


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


def is_authenticated(request: Request, db: Session):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )    
        user_id = payload.get("user_id")
        user = db.query(UserModel).filter(
            UserModel.id == user_id
        ).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        return user
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )