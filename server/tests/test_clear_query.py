from server.database import clear_query

example_query = {
                'name': {
                    'eq': None, 'ne': 'Stuart Austin',
                    'regex': None, 'in_': [], 'nin': []
                },
                'email': {
                    'eq': None, 'ne': None, 'regex': 'net$',
                    'in_': [], 'nin': []
                },
                'age': {
                    'eq': 66, 'ne': None, 'gt': None, 'lt': None,
                    'gte': None, 'lte': None, 'in_': [], 'nin': []
                },
                'company': {
                    'eq': None, 'ne': None, 'regex': None,
                    'in_': ['Twitter'], 'nin': []
                },
                'join_date': {
                    'eq': None, 'ne': None, 'gt': None,
                    'lt': '2013-02-22T16:08:10-08:00', 'gte': None,
                    'lte': None, 'in_': [], 'nin': []
                },
                'job_title': {
                    'eq': None, 'ne': 'driver', 'regex': None,
                    'in_': [], 'nin': []
                },
                'gender': {
                    'eq': None, 'ne': None,
                    'in_': [], 'nin': ['female']
                },
                'salary': {
                    'eq': None, 'ne': None, 'gt': 6400, 'lt': 8400,
                    'gte': None, 'lte': None, 'in_': [], 'nin': []
                }
            }


cleared_for_mongo = {
    'name': {'$ne': 'Stuart Austin'},
    'email': {'$regex': 'net$'},
    'age': {'$eq': 66},
    'company': {'$in': ['Twitter']},
    'join_date': {'$lt': '2013-02-22T16:08:10-08:00'},
    'job_title': {'$ne': 'driver'},
    'gender': {'$nin': ['female']},
    'salary': {'$gt': 6400, '$lt': 8400}
}


def test_clear_query():
    result = clear_query(example_query)
    assert result == cleared_for_mongo
