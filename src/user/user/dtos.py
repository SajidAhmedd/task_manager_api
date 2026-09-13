from pydantic import BaseModel

class UserSchema(BaseModel):
    name: str
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True