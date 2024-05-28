from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# pip install sqlAlchemy
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db' # db 위치
engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread' : False}) # 하나의 스레드만 허용

# Postgre로 변경
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1234@localhost/TodoApplicationDatabase' # db 위치
# connect_args는 sqlite 전용
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Mysql로 변경
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:1234@127.0.0.1:3306/TodoApplicationDatabase' # db 위치
# connect_args는 sqlite 전용
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine) # 세션 로컬 인스턴스
Base = declarative_base() # db 호출