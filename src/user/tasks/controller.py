from src.user.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.user.tasks.models import TaskModel
from fastapi import HTTPException, status

def create_task(body: TaskSchema, db: Session):
    new_task = TaskModel(
        title=body.title,
        description=body.description,
        is_completed=body.is_completed
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task



def get_tasks(db: Session):
    task = db.query(TaskModel).all()
    return task

def get_one_task(task_id: int, db: Session):
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise  HTTPException(404, detail=f"Task with id {task_id} not found")
    
    return one_task
    
    
def update_task(body: TaskSchema, task_id: int, db: Session):
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise  HTTPException(404, detail=f"Task with id {task_id} not found")
    
    body = body.model_dump()
    for key, value in body.items():
        setattr(one_task, key, value)
    db.add(one_task)
    db.commit()
    db.refresh(one_task)
    return one_task

def delete_task(task_id: int, db: Session):
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise  HTTPException(404, detail=f"Task with id {task_id} not found")
    
    db.delete(one_task)
    db.commit()
    
    return None