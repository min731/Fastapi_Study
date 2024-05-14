from fastapi import FastAPI
from fastapi import Body

app = FastAPI()
# 기본 URL : 127.0.0.1:8000
# 실행
# uvicorn books:app --reload
# uvicorn은 웹서버, books는 python파일, app은 FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]
# {"title": "Title Six", "author": "Author Two", "category": "IT"}

### GET ###
@app.get ("/api-endpoint") # 먼저 선언한 endpoint로 작동
async def first_api():
    return {'message':'Hello Jungmin!'}
    # fastapi에서 async는 필요없지만 명시
    # 기본적으로 구현되어 있음
    # async 함수안에 await

@app.get ("/books") # static path
async def read_all_books():
    return BOOKS

### 정적 API는 동적 API 위에 위치해야 작동함
@app.get ("/books/mybook") # static path
async def read_my_book():
    return {'book_title' :'My Favorite Book'}

@app.get ("/books_dynamic/{dynamic_param}") # dynamic path
async def read_all_books(dynamic_param):
    return {'dynamic_param' : dynamic_param}

# # 정적 API는 동적 API 위에 위치해야 작동함
# @app.get ("/books/mybook") # dynamic path
# async def read_all_books():
#     return {'book_title' :'My Favorite Book'}

@app.get("/books/{book_title}")
async def read_book(book_title: str):
# async def read_book(book_title: str,new_book=Body()):
# GET은 Body를 가질 수 없음
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book # casefold()는 다국어 lower()
        
### Query Parameters 1 
@app.get("/books/")
async def read_category_by_query(category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

# query parameter test
# 순서가 중요!
# 더 작은 end-point를 앞으로!
@app.get("/books/byauthor/")
async def read_books_by_author_path(author:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return

### Query Parameters 2 (path parameter + query parameter)
# http://127.0.0.1:8000/books/author%20four/?category=math
@app.get("/books/{book_author}/")
async def read_category_by_query(book_author: str, category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
            book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

### POST ###
# POST는 body로 데이터를 담음, header에는 요청에 대한 메타데이터(or content-type)를 담음
# GET은 body가 없음
# Json형식으로 POST 시 {"title":"title1"} 큰 따옴표 사용
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

### PUT ###
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book

### DELETE ###
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break

# path parameter 
# @app.get("/books/byauthor/{author}")
# async def read_books_by_author_path(author:str):
#     books_to_return = []
#     for book in BOOKS:
#         if book.get('author').casefold() == author.casefold():
#             books_to_return.append(book)
#     return books_to_return

# # query parameter test
# # 순서가 중요!
# @app.get("/books/byauthor/")
# async def read_books_by_author_path(author:str):
#     books_to_return = []
#     for book in BOOKS:
#         if book.get('author').casefold() == author.casefold():
#             books_to_return.append(book)
#     return books_to_return