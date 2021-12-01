from fastapi import FastAPI, Request, APIRouter
from server.routes.employee import router as employee_router
from fastapi.encoders import jsonable_encoder

my_app = FastAPI()
my_app.include_router(employee_router, tags=['Employee'], prefix='/employee')


@my_app.get('/', tags=['Root'])
async def read_root():
    return {'message': 'You can find employees there'}
