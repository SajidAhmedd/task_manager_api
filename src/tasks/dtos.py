from pydantic import BaseModel

class TaskSchema(BaseModel):
    title: str
    description: str
    is_completed: bool = False

    class Config:
        orm_mode = True
        
class TaskResponseSchema(TaskSchema):
    title: str
    description: str
    is_completed: bool
    user_id: int