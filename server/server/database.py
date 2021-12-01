""" СКРИПТ РЕАЛИЗУЮЩИЙ МАНИПУЛЯЦИИ С ЛОГИКОЙ ПОИСКА СОТРУДНИКА """
from typing import List
import motor.motor_asyncio
import simplejson as json


MONGO_SERVER = 'mongo'
MONGO_PORT = 27017
USER = 'user'
PASS = 'password'

client = motor.motor_asyncio.AsyncIOMotorClient(
    f'mongodb://{USER}:{PASS}@{MONGO_SERVER}:{MONGO_PORT}/')
database = client.employees_db
employees_collection = database.get_collection('employees')


async def clear_query(some_dict: dict) -> dict:
    """ ФУНКЦИЯ ПО ОЧИСТКЕ ЗНАЧЕНИЙ, КОТОРЫЕ NONE
     Т.К. ВСЕ ПОЛЯ JSON СДЕЛАЛ НЕОБЯЗАТЕЛЬНЫМИ И ОНИ ПРИХОДЯТ NONE """
    result_dict: dict = {}
    for key, value in some_dict.items():
        if value:
            result_dict[key] = value
    return result_dict


async def find_employees(employee_data: dict) -> dict:
    """ ФУНКЦИЯ ПО ПОИСКУ В БАЗЕ ПО ЗАПРОСУ ИЗ POST """
    results: List[dict] = []

    query = await clear_query(employee_data)
    if not query:
        return json.dumps(None)

    finded_employees = employees_collection.find(query)
    for one_employee in await finded_employees.to_list(length=None):
        one_employee['_id'] = str(one_employee['_id'])
        results.append(one_employee)

    if results:
        return json.dumps(results)
    return json.dumps(None)
