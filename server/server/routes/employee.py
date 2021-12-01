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


@router.post("/searches", response_description="Student data added into the database")
async def find_employees_method(employees: EmployeeSchema = Body(...)):
    """ ФУНКЦИЯ ДЛЯ ЭНДПОИНТА SEARCHES """
    employees_data = jsonable_encoder(employees)
    finded_employees = await find_employees(employees_data)
    if finded_employees:
        return response_model(finded_employees, 'Finded employees there!')
    return error_response_model("An error occurred.", 404, "Employees not found")
