import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from user_register_app.database_connection import Base, mongo_client


class UserRegistration(Base):
    __tablename__ = "user_registration"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    full_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    phone = Column(String, unique=True)
    created_time = Column(DateTime, default=datetime.utcnow)
    updated_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


mongo_db = mongo_client["user_profile"]
user_profile_collection = mongo_db['user_profile_collection']
