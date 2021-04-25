from pprint import pprint
import requests


def test1():
    print(
        requests.get('http://127.0.0.1:5000/api/jobs').json())
    print(
        requests.get('http://127.0.0.1:5000/api/jobs/2').json())
    print(
        requests.get('http://127.0.0.1:5000/api/jobs/21').json())
    print(
        requests.get('http://127.0.0.1:5000/api/jobs/2f').json())


def test2():
    print(requests.post('http://127.0.0.1:5000/api/jobs', params={
        'id': 10,
        'team_leader': 2,
        'hazard': 2,
        'description': '''desc''',
        'team': '1, 2, 3',
        'is_finished': True,
        'id_created': 1
    }).json())
    print(requests.post('http://127.0.0.1:5000/api/jobs', params={
        'id': '10f',  # не инт
        'team_leader': 2,
        'hazard': 2,
        'description': '''desc''',
        'team': '1, 2, 3',
        'is_finished': True,
        'id_created': 1
    }).json())
    print(requests.post('http://127.0.0.1:5000/api/jobs', params={
        'id': 10,  # уже будет существовать тк первый тест с таким же id
        'team_leader': 2,
        'hazard': 2,
        'description': '''desc''',
        'team': '1, 2, 3',
        'is_finished': True,
        'id_created': 1
    }).json())
    print(requests.post('http://127.0.0.1:5000/api/jobs', params={
        'id': 11,
        'team_leader': 2,
        'hazard': 'f2',  # опять же не инт
        'description': '''desc''',
        'team': '1, 2, 3',
        'is_finished': True,
        'id_created': 1
    }).json())
    print(
        requests.get('http://127.0.0.1:5000/api/jobs/10').json())


def test3():
    test2()
    print(requests.delete('http://127.0.0.1:5000/api/jobs', params={'id': 10}).json())
    print(
        requests.get('http://127.0.0.1:5000/api/jobs/10').json())  # должна быть ощибка так как такой строки в бд нет


def test4():
    test2()
    print(requests.put('http://127.0.0.1:5000/api/jobs', params={
        'id': 10,
        'team_leader': 2,
        'hazard': '2',  # опять же не инт
        'description': '''desc''',
        'team': '1',
        'is_finished': True,
        'id_created': 1
    }).json())
    print(
        requests.get('http://127.0.0.1:5000/api/jobs/10').json())


def add_user(api=''):
    print(requests.post(f'http://127.0.0.1:5000/api/{api}users', params={
        'id': 10,
        'name': 'roma',
        'speciality': 'none',
        'password': 'password',
        'city': '55.449,56.001'

    }).json())


# add_user()

def test_resources_user():  # с пустой базой id будет 0 поставить id=0 нельзя
    try:
        pprint(
            requests.get('http://127.0.0.1:5000/api/v2/users').json())
    except Exception:
        pass
    add_user('v2/')  # на нём проверка будет идти
    pprint(
        requests.get('http://127.0.0.1:5000/api/v2/users').json())
    x = requests.get('http://127.0.0.1:5000/api/v2/users/1')
    print(x)
    pprint(
        x.json())  # конкретный пользователь
    pprint(requests.delete('http://127.0.0.1:5000/api/v2/users/1').json())
    pprint(
        requests.get('http://127.0.0.1:5000/api/v2/users').json())


def test_job_resource():
    try:  # чтобы не заканчивалось при пустой базе. там будет ответ 404
        pprint(requests.get('http://127.0.0.1:5000/api/v2/jobs').json())
    except Exception:
        pass
    pprint(requests.post('http://127.0.0.1:5000/api/v2/jobs', params={
        'team_leader': 1,
        'hazard': 1,
        'description': 'desc',
        'team': '1,2,3',
        'is_finished': True,
        'id_created': 1
    }).json())
    pprint(requests.get('http://127.0.0.1:5000/api/v2/jobs/1').json())
    pprint(requests.delete('http://127.0.0.1:5000/api/v2/jobs/1').json())
    try:  # чтобы не заканчивалось при пустой базе. там будет ответ 404
        pprint(requests.get('http://127.0.0.1:5000/api/v2/jobs').json())
    except Exception:
        pass


test_job_resource()
