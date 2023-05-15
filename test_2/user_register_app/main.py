import uvicorn
from fastapi import FastAPI
from user_register_app.apis.user_register_api import router

app = FastAPI()
app.include_router(router, prefix='/apis')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
