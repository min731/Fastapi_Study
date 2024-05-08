from database import Base # database.py에서 선언한 db 객체 가져옴
from sqlalchemy import Column, Integer, String, Boolean

class Todos(Base):
    __tablename__ = 'todos'
    
    id = Column(Integer, primary_key=True, index=True) # id라는 PK 컬럼 만듬
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    