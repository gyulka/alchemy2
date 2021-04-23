import sys
from db import db_unit
from flask import Flask, Blueprint, jsonify, request

blueprintJobs = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)
blueprintUser = Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)
db_unit.global_init('db/blogs.db')


@blueprintJobs.route('/api/jobs', methods=['POST', 'GET', 'DELETE', 'PUT'])
def get_jobs():
    sess = db_unit.create_session()
    if request.method == 'GET':
        return jsonify({'response': [item.to_dict() for item in sess.query(db_unit.Job).all()]})
    elif request.method == 'POST':
        try:
            if [i for i in sess.query(db_unit.Job).filter(db_unit.Job.id == int(request.args['id'])).all()]:
                return jsonify(success=False, error='already exist')
            job = db_unit.Job()
            job.id = int(request.args['id'])
            job.team_leader = int(request.args['team_leader'])
            job.description = request.args['description']
            job.hazard = int(request.args['hazard'])
            job.team = request.args['team']
            job.is_finished = False if request.args['is_finished'] == 'False' else True
            job.id_created = int(request.args['id_created'])
            # остальное не используется, понадобится, допишу
            sess.add(job)
            sess.commit()
            return jsonify(response={'success': True})
        except Exception as error:
            return jsonify(respone={'success': False, 'error': error.__str__()})
    if request.method == 'DELETE':
        try:
            id = int(request.args['id'])
            job = sess.query(db_unit.Job).filter(db_unit.Job.id == id).first()
            print(job)
            sess.delete(job)
            sess.commit()
            return jsonify(response={'success': True})
        except Exception as error:
            return jsonify(respone={'success': False, 'error': error.__str__()})
    if request.method == 'PUT':
        try:
            job = [i for i in sess.query(db_unit.Job).filter(db_unit.Job.id == int(request.args['id'])).all()][0]
            job.team_leader = int(request.args['team_leader'])
            job.description = request.args['description']
            job.hazard = int(request.args['hazard'])
            job.team = request.args['team']
            job.is_finished = False if request.args['is_finished'] == 'False' else True
            job.id_created = int(request.args['id_created'])
            sess.commit()
            return jsonify(response={'success': True})
        except IndexError as error:
            return jsonify(response={'success': False, 'error': 'не существует работы'})
        except Exception as error:
            return jsonify(respone={'success': False, 'error': error.__str__()})


@blueprintJobs.route('/api/jobs/<int:job_id>')
def get_job(job_id):
    sess = db_unit.create_session()
    ans = [item.to_dict() for item in sess.query(db_unit.Job).filter(db_unit.Job.id == job_id).all()]
    if ans:
        return jsonify(
            {'response': ans[0]})
    return jsonify({'response': {'success': False, 'error': 'не найдено'}})


@blueprintJobs.route('/api/jobs/<job_id>')
def get_job_except(job_id):
    return jsonify({'response': 'неверный id'})


@blueprintUser.route('/api/users', methods=['POST', 'GET', 'DELETE', 'PUT'])
def get_users():
    sess = db_unit.create_session()
    if request.method == 'GET':
        return jsonify({'response': [item.to_dict() for item in sess.query(db_unit.User).all()]})
    elif request.method == 'POST':
        try:
            if [i for i in sess.query(db_unit.User).filter(db_unit.User.id == int(request.args['id'])).all()]:
                return jsonify(success=False, error='already exist')
            user = db_unit.User()
            user.id = int(request.args['id'])
            user.name = request.args['name']
            user.password = request.args['password'].__hash__()
            user.speciality = request.args['speciality']
            user.city = request.args['city']
            # остальное не используется, понадобится, допишу
            sess.add(user)
            sess.commit()
            return jsonify(response={'success': True})
        except Exception as error:
            return jsonify(respone={'success': False, 'error': error.__str__()})
    if request.method == 'DELETE':
        try:
            id = int(request.args['id'])
            user = sess.query(db_unit.User).filter(db_unit.User.id == id).first()
            print(user)
            sess.delete(user)
            sess.commit()
            return jsonify(response={'success': True})
        except Exception as error:
            return jsonify(respone={'success': False, 'error': error.__str__()})
    if request.method == 'PUT':
        try:
            user = [i for i in sess.query(db_unit.User).filter(db_unit.User.id == int(request.args['id'])).all()][0]
            user.id = int(request.args['id'])
            user.name = request.args['name']
            user.password = request.args['password'].__hash__()
            user.speciality = request.args['speciality']
            sess.commit()
            return jsonify(response={'success': True})
        except IndexError as error:
            return jsonify(response={'success': False, 'error': 'не существует человека'})
        except Exception as error:
            return jsonify(respone={'success': False, 'error': error.__str__()})


@blueprintUser.route('/api/user/<int:user_id>')
def get_user(user_id):
    sess = db_unit.create_session()
    ans = [item.to_dict() for item in sess.query(db_unit.User).filter(db_unit.User.id == int(user_id)).all()]
    print(ans)
    if ans:
        return jsonify(
            {'response': {'response': ans[0], 'success': True}})
    return jsonify({'response': {'success': False, 'error': 'не найдено'}})


@blueprintUser.route('/api/user/<user_id>')
def get_user_except(user_id):
    return jsonify({'response': 'неверный id'})
