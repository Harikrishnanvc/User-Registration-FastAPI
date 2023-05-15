import environ
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

env = environ.Env()
environ.Env.read_env("/home/harikrishnan/Desktop/test/test_1/.env")

#   postgresql connection
postgresql_connection = env("SQLALCHEMY_DATABASE_URI")
engine = create_engine(postgresql_connection)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = session()
Base = declarative_base()

#   mongo connection
mongo_host = env('MONGO_HOST')
mongo_port = env('MONGO_PORT')
mongo_database = env('MONGO_DATABASE')

mongo_client = MongoClient(f"mongodb://{mongo_host}:{mongo_port}")
mongo_db = mongo_client[mongo_database]
