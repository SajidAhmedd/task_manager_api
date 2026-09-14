from pydantic import BaseModel

class UserSchema(BaseModel):
    name: str
    username: str
    email: str
    password: str


        
        
class UserResponseSchema(BaseModel):
    id: int
    name: str
    username: str
    email: str

    class Config:
        orm_mode = True
        

class UserLoginSchema(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
        
        
class TokenResponseSchema(BaseModel):
    token: str
