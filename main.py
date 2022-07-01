import uvicorn
from fastapi import FastAPI
from controller.users_controller import *


app = FastAPI()

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8001, log_level="info", reload=True)
    print("running")