
import time  # for adding a delay to database reconnecting

import psycopg2
from psycopg2.extras import \
    RealDictCursor  # for returning data as column & row wise data
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# SQLALCHEMY_DATABASE_URL  = 'postgresql://<password>@<ip-address/hostname>/<database_name>'  -> format for database connection
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port} /{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
# for connecting database directly without orm
# while True:
#     try:
#         # for proding rquired info to connect with database
#         conn = psycopg2.connect(host='localhost', database='fastapi',
#                                 user='postgres', password='king1299', cursor_factory=RealDictCursor)
#         cursor = conn.cursor() # connecting database
#         print("Database connection was succesfully!")
#         break
#     except Exception as error:
#         print("Connecting to database failed!")
#         print("Error: ", error)
#         time.sleep(2) # added 2 sec dealy for reconnecting database
