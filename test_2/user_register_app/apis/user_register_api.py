import base64
import uuid

import bcrypt
from fastapi import APIRouter, Query
from fastapi import status, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pyfa_converter import FormDepends
from sqlalchemy.orm import joinedload
from user_register_app.database_connection import db
from user_register_app.models.user_register_models import Users, Profile
from user_register_app.schemas.user_register_schema import UserDetailsValidation

router = APIRouter(prefix='/users', tags=['apis'])


@router.post("/register-user")
async def register_user(user: UserDetailsValidation = FormDepends(UserDetailsValidation),
                        profile_picture: UploadFile = File(...)):
    """
        This function is used to register the data of users.
        Full name, email, password and phone will be saved in postgresql database.
        Profile picture will be saved in mongodb database.
    """
    try:
        if validate_profile_picture(profile_picture):
            user_id = str(uuid.uuid4())
            input_password = user.password.encode('utf-8')
            hashed_password = bcrypt.hashpw(input_password, bcrypt.gensalt())

            image_bytes = await profile_picture.read()
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')
            db_user = Users(id=user_id, full_name=user.full_name, email=user.email,
                            password=hashed_password, phone=user.phone)
            db.add(db_user)
            db.commit()

            db_profile = Profile(id=user_id, user_id=db_user.id, profile_picture=encoded_image)
            db.add(db_profile)
            db.commit()
            response = {
                'message': 'Successfully registered',
                'status_code': status.HTTP_201_CREATED
            }
    except Exception as e:
        response = {
            'message': e,
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    finally:
        db.close()
    return response


@router.get("/get-user/", status_code=status.HTTP_200_OK)
async def get_user_details(page_no: int = Query(1, ge=1), page_size: int = Query(10, ge=1)):
    """
        Get all the details of registered users from postgresql database

        :param page_no: The token representing the next page of results

        :param page_size: The number of users to fetch per page

        :return: All details of registered users
    """
    try:
        query = db.query(Profile, Users).join(Users, Profile.user_id == Users.id).options(joinedload(Profile.relation))
        total_results = query.count()
        total_pages = (total_results + page_no - 1) // page_no
        results = query.limit(page_size).offset((page_no - 1) * page_size).all()
        details = [
            {
                "user_id": str(user.id),
                "full_name": user.full_name,
                "email": user.email,
                "phone": user.phone,
                "profile_picture": profile.profile_picture
            }
            for profile, user in results
        ]

        response = {
            "page": page_no,
            "per_page": page_size,
            "total_pages": total_pages,
            "total_results": total_results,
            "results": details
        }
        return JSONResponse(content=response, media_type="application/json")

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    finally:
        db.close()


@router.get("/get-user-by-id/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: str):
    """
        Get all the details of specific user from both postgresql and mongodb
        :param user_id: id of user(uuid)
        :return: All details of specific user
    """
    try:
        query = db.query(Profile, Users).join(Users, Profile.user_id == Users.id).options(joinedload(Profile.relation))
        user = query.filter(Users.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        profile_data = {
            'profile_picture': user[0].profile_picture
        }
        user_data = {
            'full_name': user[1].full_name,
            'email': user[1].email,
            'phone': user[1].phone,
            'password': user[1].password,
            'profile': profile_data
        }
        return JSONResponse(content=user_data, media_type="application/json")

    except Exception as error:
        raise HTTPException(status_code=500, detail=error)

    finally:
        db.close()


ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png']


def validate_profile_picture(profile_picture):
    file_extension = profile_picture.filename.split('.')[-1].lower()
    content_type = profile_picture.content_type.lower()
    if file_extension not in ALLOWED_EXTENSIONS and 'image' not in content_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The profile picture format is invalid'
        )
    return profile_picture
