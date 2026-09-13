from src.user.dtos import UserSchema
from sql.alchemy.orm import Session
from src.user.models import UserModel

def register(body: UserSchema, db: Session):
    return 