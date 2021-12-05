""" РОУТЫ """
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    find_employees
)

from server.models.employee import (
    error_response_model,
    response_model,
    EmployeeSchema
)

router = APIRouter()


@router.post("/searches", response_description='Employee search in database')
async def find_employees_method(employees: EmployeeSchema = Body(...)):
    """ ФУНКЦИЯ ДЛЯ ЭНДПОИНТА SEARCHES """
    employees_data = jsonable_encoder(employees)
    results = await find_employees(employees_data)

    if results['employees']:
        return response_model(results, 'Finded employees there!')
    return error_response_model(code=404, detail='Employees not found')
