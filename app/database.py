from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db(): # Dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# # use this code if you want to write raw sql codes instead of sqlalchemy code
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',
#                                 database='fastapi',
#                                 user='postgres',
#                                 password='megalobox1997',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("database connection was successful...")
#         break
#     except Exception as error:
#         print("connection to database failed")
#         print("Error: " ,error )
#         time.sleep(2) # it will not work ,look at the reason on chat-gpt