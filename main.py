from fastapi import FastAPI
from src.user.utils.db import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI(title="My FastAPI Application",)
