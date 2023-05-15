
# User Registration System

This project is a user registration application that uses Postgresql as database


## Requirements

Python 3.8 or higher

FastAPI

PostgreSQL


## Installation

Clone the repository

```
https://github.com/Harikrishnanvc/user_registration_test.git
```
Install the dependencies
```
pip install -r requirements.txt    
```
# Usage
Create a postgresql database on you local (make sure you have all privileges)


Create a .env file and add credentials

## Migrate
This will create a migrations folder
```
alembic init alembic init user_register_app/migrations
```

To make changes
```
alembic revision --autogenerate -m "message"
```
To make changes in database
```
alembic upgrade head

```

## Run

To start the application, run the following command:
Make sure your location is inside test folder
```
uvicorn user_register_app.main:app --reload

```
The application will be running on http://localhost:8000.
## API Reference

#### Register users

```http
  POST /api/users/register-user
```
* `full_name`: The user's full name.
* `email`: The user's email address.
* `phone`: The user's phone number.
* `profile_picture`: The user's profile picture.


#### Get all users

```http
  GET /api/users/get-users
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `page_no` | `integer` | **Required**. page number used for pagination |
| `page_size` | `integer` | **Required**. no. of users to get per page|



#### GET user by id
```http
  GET /api/users/get-user-by-id/{user_id}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `user_id` | `str` | **Required**. user id which is auto generated uuid |

