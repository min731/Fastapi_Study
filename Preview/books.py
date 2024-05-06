from fastapi import FastAPI
from fastapi import Body

# uvicorn books:app --reload
# uvicorn은 웹서버
app = FastAPI()

BOOKS = [
            {'title' : 'Title1', 'author' : 'Author1', 'category' : 'Category1'},
            {'title' : 'Title2', 'author' : 'Author2', 'category' : 'Category2'},
            {'title' : 'Title3', 'author' : 'Author3', 'category' : 'Category3'}
        ]

# 정적
@app.get("/books") # GET, 엔드포인트
async def read_all_books(): # 비동기 함수, 명시적으로 사용
    return BOOKS

# 동적
@app.get("/books/{dynamic_param}")
async def read_all_books(dynamic_param):
    return {'dynamic_param':dynamic_param}

# 파라미터
@app.get("/books/especially/{book_title}")
async def read_book(book_title:str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold(): # casefold() 문자열 소문자로
            return book

# Query Parameters (1)
# http://127.0.0.1:8000/books/?category=Category3
@app.get("/books/")
async def read_category_by_query(category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold()==category.casefold():
            books_to_return.append(book)

    return books_to_return

# Project1: end-point가 짧은 것을 먼저
@app.get("/books/byauthor/")
async def read_books_by_author_path(author:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold()==author.casefold():
            books_to_return.append(book)
    return books_to_return
    

# Query Parameters (2)
# http://127.0.0.1:8000/books/Author2/?category=Category2
@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author:str, category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold()==book_author.casefold() and book.get('category').casefold()==category.casefold():
            books_to_return.append(book)

    return books_to_return

# Post는 Body()가 있음, GET은 없음
@app.post("/books/creat_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

# PUT
@app.put("/books/update_book")
async def update_book(update_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold()== update_book.get('title').casefold():
            BOOKS[i] = update_book

# DELETE
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break

# Project2 : 데이터 유효성, 예외 처리 등
# dict() => .model.dump()
# schema_extra => json_schema_extra
# id: Optional[int] = None

# Pydantics => 데이터 유효성 검사