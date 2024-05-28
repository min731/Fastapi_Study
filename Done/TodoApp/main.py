from fastapi import FastAPI
from . import models
from .database import engine


app = FastAPI()
# uvicorn main:app --reload
# todos.db 와 pycache 생성

models.Base.metadata.create_all(bind=engine) # 해당 .db가 없을 때만 실행

from .routers import auth,todos,admin,users
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)


# test
@app.get("/healthy")
def health_check():
    return {'status' : 'Healthy'}