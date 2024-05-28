from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


# static(css or js) 파일 추가
from starlette.staticfiles import StaticFiles
app.mount("/static",StaticFiles(directory="static"),name="static")



app.include_router(auth.router)
app.include_router(todos.router)