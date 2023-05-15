import base64
import uuid

import bcrypt
from fastapi import APIRouter
from fastapi import status, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from pyfa_converter import FormDepends
from user_register_app.database_connection import db
from user_register_app.models.user_register_models import UserRegistration, user_profile_collection
from user_register_app.schemas.user_register_schema import UserDetailsValidation
from user_register_app.schemas.user_register_schema import UserRegisterSchema, UserProfileSchema

router = APIRouter(prefix='/users', tags=['apis'])


@router.post("/register-user", status_code=status.HTTP_201_CREATED)
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
            db_user = UserRegistration(id=user_id, full_name=user.full_name, email=user.email,
                                       password=hashed_password, phone=user.phone)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            image_bytes = await profile_picture.read()
            profile_picture = UserProfileSchema(id=user_id, profile_picture=image_bytes)
            profile_picture.save()
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
        Get all the details of registered users from both postgresql and mongodb

        :param page_no: The token representing the next page of results

        :param page_size: The number of users to fetch per page

        :return: All details of registered users
    """
    try:
        total_count = db.query(UserRegistration).count()
        skip = (page_no - 1) * page_size
        limit = page_size
        user = db.query(UserRegistration).offset(skip).limit(limit).all()
        data_list = []
        for key in user:
            user_data = UserRegisterSchema.from_orm(key).dict()
            user_data['user_id'] = str(key.id)
            profile_picture = user_profile_collection.find_one({'id': str(key.id)})
            base64_data = base64.b64encode(profile_picture.get('profile_picture')).decode('utf-8')
            mime_type = 'image/jpeg'
            data_url = f'data:{mime_type};base64,{base64_data}'
            user_data['profile_picture'] = data_url
            data_list.append(user_data)
        response = {
            "page": page_no,
            "per_page": page_size,
            "total_pages": total_count,
            "total_results": total_count,
            "results": data_list
        }
        return JSONResponse(content=response, media_type="application/json")

    except Exception as error:
        raise HTTPException(status_code=500, detail=error)

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
        user = db.query(UserRegistration).filter(UserRegistration.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        profile_picture = user_profile_collection.find_one({'id': str(user_id)})
        if profile_picture is None:
            raise HTTPException(status_code=404, detail="Profile picture not found")

        base64_data = base64.b64encode(profile_picture.get('profile_picture')).decode('utf-8')
        mime_type = 'image/jpeg'
        data_url = f'data:{mime_type};base64,{base64_data}'
        user_data = UserRegisterSchema.from_orm(user).dict()
        user_data['profile_picture'] = data_url
        response = {
            "user_id": user_id,
            "results": user_data
        }
        return JSONResponse(content=response, media_type="application/json")

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
