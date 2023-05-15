import environ
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

env = environ.Env()
environ.Env.read_env("/home/harikrishnan/Desktop/test/test_2/.env")

postgresql_connection = env("SQLALCHEMY_DATABASE_URI")
engine = create_engine(postgresql_connection)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = session()
Base = declarative_base()
