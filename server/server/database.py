""" СКРИПТ РЕАЛИЗУЮЩИЙ МАНИПУЛЯЦИИ С ЛОГИКОЙ ПОИСКА СОТРУДНИКА """
from typing import List
import motor.motor_asyncio
from server.models.employee import CLASS_COMPARISONS


MONGO_SERVER = 'mongo'
MONGO_PORT = 27017
USER = 'user'
PASS = 'password'

client = motor.motor_asyncio.AsyncIOMotorClient(
    f'mongodb://{USER}:{PASS}@{MONGO_SERVER}:{MONGO_PORT}/')
database = client.employees_db
employees_collection = database.get_collection('employees')


def clear_query(some_dict: dict) -> dict:
    """ ФУНКЦИЯ ПО ОЧИСТКЕ ЗНАЧЕНИЙ:
     0) получить поля у всех используемых классов
     1) отбрасываем все ключи со значениями NONE
     2) проверяем, можно ли форматировать ключ к формату монги
     3) проверяем значение на NONE """
    result_dict: dict = {}
    print('there')
    print(some_dict)

    all_comparisons = []
    for one_class in CLASS_COMPARISONS:
        all_comparisons.extend(list(one_class.__fields__.keys()))

    for key, value in some_dict.items():
        if value:
            converted_key_name = f'${key}' if key in all_comparisons else key
            converted_key_name = '$in' if converted_key_name == '$in_' else converted_key_name

            cleared_value = clear_query(value) if isinstance(value, dict) else value
            result_dict[converted_key_name] = cleared_value
    print(result_dict)
    return result_dict


# TODO реализовать функцию сортировки и тд
async def find_employees(employee_data: dict) -> dict:
    """ ФУНКЦИЯ ПО ПОИСКУ В БАЗЕ ПО ЗАПРОСУ ИЗ POST """
    results: List[dict] = []

    query = clear_query(employee_data)
    if not query:
        return {'employees': None}

    finded_employees = employees_collection.find(query)
    for one_employee in await finded_employees.to_list(length=None):
        one_employee['_id'] = str(one_employee['_id'])

        result_one = one_employee
        result_one.pop('_id', None)
        results.append(result_one)

    if results:
        return {'employees': results}
    return {'employees': None}
