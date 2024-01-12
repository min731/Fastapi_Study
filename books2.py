from fastapi import FastAPI,Body
from pydantic import BaseModel,Field # 필드별 유효성 검사 -> Field
from typing import Optional

app = FastAPI()

class Book: # 책 요청
    id:int
    title:str
    author:str
    description:str
    rating:int

    def __init__(self,id,title,author,description,rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel): # 책 요청 데이터 유효성 검사
    id:Optional[int] = Field(None,description='id is not needed')# Request에서 있어도 좋고 없어도 좋음, 자동으로 Null or 0을 할당함
    title:str = Field(min_length=3)
    author:str = Field(min_length=1)
    description:str = Field(min_length=1,max_length=100)
    rating:int = Field(gt=0,lt=6) # 0 < x < 6

    # swagger docs의 기본 스키마 
    class Config:
        json_schema_extra = { # 안되면 json_schema_extra
                              # Optional한 Field도 없어짐
            'example' : {
                'title' : 'A new book',
                'author' : 'codingwithroby',
                'description' : 'A new description of a book',
                'rating' : 5
            }
        }



BOOKS = [
    Book(1,'Computer Science Pro','codingwithroby','A very nice book',5),
    Book(2,'Be Fast with FastAPI','codingwithroby','A great book',5),
    Book(3,'Master Endpoints','codingwithroby','A awesome book',5),
    Book(4,'HP1','Author 1','Book Description',2),
    Book(5,'HP2','Author 2','Book Description',3),
    Book(6,'HP3','Author 3','Book Description',1),
]

@app.get("/books")
async def read_all_books():
    return BOOKS

# id로 책 찾기
@app.get("/books/{book_id}")
async def read_book(book_id:int):
    for book in BOOKS:
        if book_id==book.id:
            return book
        
@app.get("/books/")
async def read_book_by_rating(book_rating:int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)

    return books_to_return
# Request 
#   {
#     "id": 1,
#     "title": "Computer Science Pro",
#     "author": "codingwithroby",
#     "description": "A very nice book",
#     "rating": 5
#   }
# @app.post("/create-book")
# async def create_book(book_request=Body()): # Body() 인증을 한다고 유효성 검사가 되는 것은 아님
#                                             # id를 건너뛸 수도 있음
#     BOOKS.append(book_request)

@app.post('/create-book')
async def create_book(book_request:BookRequest): # Body() -> BookRequest
                                                 # docs에서 request 기본 스키마를 제공함
    print(type(book_request)) # 현재까지 BookRequest 객체임
    new_book = Book(**book_request.dict()) # .dict() or .model_dump( )
    print(type(new_book))
    BOOKS.append(find_book_id(new_book))

# 고유 id값 갖게 하기
def find_book_id(book:Book):
    if len(BOOKS)>0:
        book.id = BOOKS[-1].id+1
    else:
        book.id = 1

    # book.id = 1 if len(BOOKS)==0 else BOOKS[-1].id+1
    return book

@app.put("/books/update_book")
async def update_book(book:BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book.id:
            print( BOOKS[i].id, book.id)
            BOOKS[i] = book
    print(BOOKS[i])