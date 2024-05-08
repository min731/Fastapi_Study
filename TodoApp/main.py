from fastapi import FastAPI
import models
from database import engine

app = FastAPI()
# uvicorn main:app --reload
# todos.db 와 pycache 생성

models.Base.metadata.create_all(bind=engine)

