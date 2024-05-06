from fastapi import FastAPI

app = FastAPI()

@app.get ("/api-endpoint")
async def first_api():
    return {'message':'Hello Jungmin!'}
    # fastapi에서 async는 필요없지만 명시
    # 기본적으로 구현되어 있음
    # async 함수안에 await