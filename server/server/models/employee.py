""" МОДЕЛИ """
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum
from typing import Optional


class GenderEnum(str, Enum):
    """ КЛАСС ДЛЯ ГЕНДЕРОВ, ВСЁ ТОЛЕРАНТНО """
    male = 'male'
    female = 'female'
    other = 'other'


class EmployeeSchema(BaseModel):
    """ КЛАСС ДЛЯ СОТРУДНИКОВ, ПОЛЯ СДЕЛАЛ НЕОБЯЗАТЕЛЬНЫМИ """
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    company: Optional[str] = None
    join_date: Optional[datetime] = None
    job_title: Optional[str] = None
    gender: Optional[GenderEnum] = None
    salary: Optional[float] = None

    class Config:
        schema_extra = {
            'example': {
                'name': 'Stuart Austin',
                'email': 'ac.turpis@atsem.edu',
                'age': 54,
                'company': 'Twitter',
                'join_date': '2013-02-22T16:08:10-08:00',
                'job_title': 'driver',
                'gender': 'other',
                'salary': 4114
            }
        }


def response_model(data, message):
    """ ФУНКЦИЯ ДЛЯ УСПЕШНОГО ОТВЕТА """
    return {
        'data': [data],
        'code': 200,
        'message': message,
    }


def error_response_model(error, code, message):
    """ ФУНКЦИЯ ДЛЯ НЕУСПЕШНОГО ОТВЕТА """
    return {'error': error, 'code': code, 'message': message}
