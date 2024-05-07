from typing import Optional
from fastapi import FastAPI,Body
from pydantic import BaseModel,Field

app = FastAPI()
# uvicorn books_pj2:app --reload

class Book:
    id : int
    title : str
    author : str
    description : str
    rating : int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    # id : Optional[int] = Field(title='id is not needed') 
    id : Optional[int] = None # id 는 unique 값, 자동으로 생성
    title : str = Field(min_length=3)
    author : str = Field(min_length=1)
    description : str = Field(min_length=1, max_length=100)
    rating : int = Field(gt=-1, lt=6)
    # 객체를 생성하기 전 데이터 유효성 검사를 진행함

    class Config: # /docs 입력값 예시 및 Try it out 디폴트값
                  # 명시해 놓으면 Optional 값이 안들어오게 할 수 있음
        json_schema_extra = {
            'example' : {
                'title' : 'A new book',
                'author' : 'codingwithroby',
                'description' : 'A new description of a book',
                'rating' : 5
            }
        } 


BOOKS = [
    Book(1,'Computer Science Pro','codingwithroby','A very nice book',5),
    Book(2,'Be Fast with FastAPI','codingwithroby','A great book!',5),
    Book(3,'Master Endpoints','codingwithroby','A awesone book!',5),
    Book(4,'HP1','Author 1','Book Description',2),
    Book(5,'HP2','Author 2','Book Description',3),
    Book(6,'HP3','Author 3','Book Description',1),
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}")
async def read_book(book_id : int):
    for book in BOOKS:
        if book.id == book_id:
            return book

@app.get("/books/")
async def read_book(book_rating : int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book")
async def create_book(book_request = Body()):
    BOOKS.append(book_request)

@app.post("/create-book-request")
async def create_book_request(book_request : BookRequest): # pydantic 선언한 내 클래스로
    new_book = Book(**book_request.model_dump()) 
    # K,V를 생성자로 넣음
    # .dict()은 소멸
    BOOKS.append(find_book_id(new_book))

def find_book_id(book : Book):
    # if len(BOOKS)>0:
    #     book.id = BOOKS[-1].id+1
    # else:
    #     book.id = 1
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id+1
    return book

@app.put("/books/update_book") # PUT 시 id값이 없을 때의 예외처리
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book

@app.delete("/books/{book_id}")
async def delete_book(book_id : int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break