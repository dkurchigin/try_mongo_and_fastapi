""" МОДЕЛИ """
from enum import Enum
from typing import Optional, Union, List
from datetime import datetime
from pydantic import BaseModel, root_validator
from fastapi import HTTPException


def check_and_raise(cls, values, field_info):
    """ ФУНКЦИЯ ДЛЯ ПРОВЕРКИ ПОЛЕЙ ЗАПРОСА ОТНОСИТЕЛЬНО ПОЛЕЙ КЛАССА """
    class_fields = cls.__fields__.keys()
    if set(values.keys()) - set(class_fields) != set() or set(values.keys()) == set():
        raise ValueError(f'Check field! Allowed comparisons is {class_fields} for {field_info}')
    return values


class GenderEnum(str, Enum):
    """ КЛАСС ДЛЯ ГЕНДЕРОВ, ВСЁ ТОЛЕРАНТНО """
    male = 'male'
    female = 'female'
    other = 'other'


class GenderType(BaseModel):
    """ КЛАСС ДЛЯ ПОЛА """
    eq: Optional[GenderEnum] = None
    ne: Optional[GenderEnum] = None
    in_: Optional[List[GenderEnum]] = []
    nin: Optional[List[GenderEnum]] = []

    @root_validator(pre=True)
    def check_genrer_root(cls, values):
        """ ФУНКЦИЯ ДЛЯ ВАЛИДАЦИИ ПОЛЕЙ ГЕНДЕРА """
        return check_and_raise(cls, values, 'gender')


class StrType(BaseModel):
    """ КЛАСС ДЛЯ СТРОЧНЫХ ТИПОВ """
    eq: Optional[str] = None
    ne: Optional[str] = None
    regex: Optional[str] = None
    in_: Optional[List[str]] = []
    nin: Optional[List[str]] = []

    @root_validator(pre=True)
    def check_str_root(cls, values):
        """ ФУНКЦИЯ ДЛЯ ВАЛИДАЦИИ СТРОКОВЫХ ПОЛЕЙ """
        return check_and_raise(cls, values, 'string/email')


class EmailType(StrType):
    """ КЛАСС ДЛЯ ПОЧТЫ, КАК СТРОКОВЫЙ ТИП """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class NumericType(BaseModel):
    """ КЛАСС ДЛЯ ЦИФРОВЫХ ТИПОВ """
    eq: Optional[Union[int, float]] = None
    ne: Optional[Union[int, float]] = None
    gt: Optional[Union[int, float]] = None
    lt: Optional[Union[int, float]] = None
    gte: Optional[Union[int, float]] = None
    lte: Optional[Union[int, float]] = None
    in_: Optional[List[Union[int, float]]] = []
    nin: Optional[List[Union[int, float]]] = []

    @root_validator(pre=True)
    def check_numeric_int(cls, values):
        """ ФУНКЦИЯ ДЛЯ ВАЛИДАЦИИ ЧИСЛОВЫХ ПОЛЕЙ """
        return check_and_raise(cls, values, 'numeric')


class DateType(NumericType):
    """ КЛАСС ДЛЯ ДАТЫ """
    eq: Optional[datetime] = None
    ne: Optional[datetime] = None
    gt: Optional[datetime] = None
    lt: Optional[datetime] = None
    gte: Optional[datetime] = None
    lte: Optional[datetime] = None
    in_: Optional[List[datetime]] = []
    nin: Optional[List[datetime]] = []

    @root_validator(pre=True)
    def check_numeric_datetime(cls, values):
        """ ФУНКЦИЯ ДЛЯ ВАЛИДАЦИИ ПОЛЕЙ С ДАТОЙ """
        return check_and_raise(cls, values, 'datetime')


class EmployeeSchema(BaseModel):
    """ КЛАСС ДЛЯ СОТРУДНИКОВ, ПОЛЯ СДЕЛАЛ НЕОБЯЗАТЕЛЬНЫМИ """
    name: Optional[StrType] = None
    email: Optional[EmailType] = None
    age: Optional[NumericType] = None
    company: Optional[StrType] = None
    join_date: Optional[DateType] = None
    job_title: Optional[StrType] = None
    gender: Optional[GenderType] = None
    salary: Optional[NumericType] = None

    class Config:
        schema_extra = {
            'example': {
                'name': {'ne': 'Stuart Austin'},
                'email': {'regex': 'net$'},
                'age': {'eq': 66.0},
                'company': {'in_': ['Twitter']},
                'join_date': {'lt': '2013-02-22T16:08:10-08:00'},
                'job_title': {'ne': 'driver'},
                'gender': {'nin': ['female']},
                'salary': {'lt': 8400, 'gt': 6400.5}
            }
        }


CLASS_COMPARISONS = [GenderType, StrType, NumericType, DateType]


def response_model(data, message):
    """ ФУНКЦИЯ ДЛЯ УСПЕШНОГО ОТВЕТА """
    return {
        'data': data,
        'message': message,
    }


def error_response_model(code, detail):
    """ ФУНКЦИЯ ДЛЯ НЕУСПЕШНОГО ОТВЕТА """
    raise HTTPException(status_code=code, detail=detail)
