""" СКРИПТ ДЛЯ ЗАПОЛНЕНИЯ МОНГИ.
МОЖНО РАСШИРИТЬ ЛОГИКУ ДЛЯ ЛОГГИРОВАНИЯ, НО ПОКА ОСТАВЛЮ ТАК.
СДЕЛАЛ ЧТОБЫ КОНТЕЙНЕР ПОСЛЕ ЗАГРУЗКИ НЕ ЗАКРЫВАЛСЯ """
from typing import List
import logging
import argparse
from pymongo import MongoClient
import simplejson as json


MONGO_SERVER = 'mongo'
MONGO_PORT = 27017
USER = 'user'
PASS = 'password'

LOG_PATH = './loader.log'
YES_ANSWER = ('1', 'true', 'True', 'yes', 'Yes', 'y', 'Y')
MAIN_JSON = 'employees.json'


def load_json(filename: str) -> List[dict]:
    """ ЗАГРУЗКА ФАЙЛА, ВЫНЕС ОТДЕЛЬНО
    Т.К. В ДАЛЬНЕЙШЕМ МОЖНО ЧТО-ТО НА НЕЁ НАВЕСИТЬ """
    with open(filename, 'r') as file_handler:
        return json.load(file_handler)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='JSON LOADER')
    parser.add_argument('-debug', type=str, required=False, help='Debug flag')
    input_args = parser.parse_args()

    log_level = logging.DEBUG if input_args.debug in YES_ANSWER else logging.INFO
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    log_file = logging.FileHandler(LOG_PATH)
    log_file.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    log_file.setLevel(log_level)

    stream_logger = logging.StreamHandler()
    stream_logger.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    stream_logger.setLevel(log_level)

    logger.addHandler(log_file)
    logger.addHandler(stream_logger)

    logger.info('Try to connect to DB')
    client = MongoClient(f'mongodb://{USER}:{PASS}@{MONGO_SERVER}:{MONGO_PORT}/')
    db = client['employees_db']
    try:
        employees = db['employees']
        employees.delete_many({})
        logger.info(f'Try to load {MAIN_JSON}')

        json_data = load_json(MAIN_JSON)
        employees.insert_many(json_data)

        finded_employees = db['employees']
        res = finded_employees.find()
        for one_res in res:
            logger.debug(one_res)

    except Exception as our_exception:
        logger.exception(f'Something went wrong with exception:\n{our_exception}')
    finally:
        client.close()
        logger.info('Close connection')
