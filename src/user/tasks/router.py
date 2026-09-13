from fastapi import APIRouter, Depends, status
from src.user.tasks import controller
from src.user.tasks.dtos import TaskSchema, TaskResponseSchema
from src.user.utils.db import get_db
from typing import List
from sqlalchemy.orm import Session


task_router = APIRouter(prefix="/tasks")


@task_router.post("/create", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED)
def create_task(body: TaskSchema, db: Session = Depends(get_db)):
    return controller.create_task(body, db)

@task_router.get("/get", response_model=List[TaskResponseSchema], status_code=status.HTTP_200_OK)
def get_tasks(db: Session = Depends(get_db)):
    return controller.get_tasks(db)

@task_router.get("/get/{task_id}", response_model=TaskResponseSchema, status_code=status.HTTP_200_OK)
def get_one_task(task_id: int, db: Session = Depends(get_db)):
    return controller.get_one_task(task_id, db)


@task_router.put("/update/{task_id}", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED)
def update(body: TaskSchema, task_id: int, db: Session = Depends(get_db)):
    return controller.update_task(body, task_id, db)

@task_router.delete("/delete/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return controller.delete_task(task_id, db)
