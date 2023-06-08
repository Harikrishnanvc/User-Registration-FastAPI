from datetime import datetime

from fastapi import status, HTTPException, UploadFile
from pydantic import BaseModel, EmailStr, validator, Field
from user_register_app.database_connection import db
from user_register_app.models.user_register_models import Users


class UserRegisterSchema(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone: str

    class Config:
        orm_mode = True


class UserDetailsValidation(BaseModel):
    full_name: str
    email: EmailStr
    phone: str = Field(min_length=10, max_length=10, regex=r'^[0-9]+$')
    password: str = Field(regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")

    @validator("email")
    def validate_email(cls, email: EmailStr):
        email_exist = db.query(Users).filter(Users.email == email).first()
        if email_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='This E-mail is already registered'
            )
        return email

    @validator("phone")
    def validate_phone(cls, phone: str):
        phone_exist = db.query(Users).filter(Users.phone == phone).first()
        if phone_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='This phone number is already registered'
            )
        return phone


class UserProfileSchema(BaseModel):
    id: str
    profile_picture: UploadFile
    created_time: datetime = datetime.utcnow()
    updated_time: datetime = datetime.utcnow()

    class Config:
        orm_mode = True
