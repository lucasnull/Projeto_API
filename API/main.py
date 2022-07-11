import uvicorn
from fastapi import FastAPI, APIRouter
from API.controller import users_controller, authors_controller, papers_controller
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

router = APIRouter()
router.include_router(users_controller.router)
router.include_router(authors_controller.router)
router.include_router(papers_controller.router)
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8001, log_level="info", reload=True)
    print("running")