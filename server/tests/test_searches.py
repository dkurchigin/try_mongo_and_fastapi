import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from server.my_app import my_app

client = TestClient(my_app)

successed_by_name_and_age = {
    'data':
        {
            'employees': [
                {
                    'name': 'Josiah Pacheco',
                    'email': 'lacinia@diamnunc.org',
                    'age': 66,
                    'company': 'Google',
                    'join_date': '2013-08-02T15:52:58-07:00',
                    "job_title": 'janitor',
                    'gender': 'female',
                    'salary': 8141
                },
                {
                    'name': 'Brennan Wiley',
                    'email': 'fermentum.fermentum.arcu@nostra.edu',
                    'age': 66,
                    'company': 'Amazon',
                    'join_date': '2003-05-03T03:26:50-07:00',
                    'job_title': 'driver',
                    'gender': 'male',
                    'salary': 6827
                }
            ]
        },
    'message': 'Finded employees there!'
}


def test_read_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'You can find employees there'}


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(app=my_app, base_url='http://localhost') as ac:
        response = await ac.post(
            '/employee/searches',
            headers={'Content-Type': 'application/json'},
            json={'name': {
                'in_': ['Brennan Wiley', 'Josiah Pacheco']
            },
                'age': {
                    'eq': 66
                }
            },
        )
    assert response.status_code == 200
    assert response.json() == successed_by_name_and_age
