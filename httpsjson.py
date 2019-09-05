import json
import requests


def send_request(host, port):
    data = {
        'students': [
            {
                'id': 1,
                'fullname': 'Имя Фамилия',
                'rank': 'генерал вся руси',
                'role': 'teacher',
                'group': '7'
            },
            {
                'id': 1,
                'fullname': 'John Doe',
                'rank': 'генерал',
                'role': 'student',
                'group': '7'
            },
        ],
        'groups': [
            {
                'id': 7,
                'fullname': 'Первая учебная'
            },
            {
                'id': 8,
                'fullname': 'Вторая полевая'
            },
        ]
    }
    r = requests.post(f'http://{host}:{port}/', json=data)
    print(f'Response status: {r.status_code}')