import sys
from db import db_unit
from flask import Flask, Blueprint, jsonify, request

blueprint = Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)
db_unit.global_init('db/blogs.db')


@blueprint.route('/api/jobs', methods=['POST', 'GET', 'DELETE','PUT'])
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
    if request.method =='DELETE':
        try:
            id = int(request.args['id'])
            job = sess.query(db_unit.Job).filter(db_unit.Job.id == id).first()
            print(job)
            sess.delete(job)
            sess.commit()
            return jsonify(response={'success': True})
        except Exception as error:
            return jsonify(respone={'success': False, 'error': error.__str__()})
    if request.method =='PUT':
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
            return jsonify(response = {'success':False,'error':'не существует работы'})
        except Exception as error:
            return jsonify(respone={'success': False, 'error': error.__str__()})


@blueprint.route('/api/jobs/<int:job_id>')
def get_job(job_id):
    sess = db_unit.create_session()
    ans = [item.to_dict() for item in sess.query(db_unit.Job).filter(db_unit.Job.id == job_id).all()]
    if ans:
        return jsonify(
            {'response': ans[0]})
    return jsonify({'response': {'success': False, 'error': 'не найдено'}})


@blueprint.route('/api/jobs/<job_id>')
def get_job_except(job_id):
    return jsonify({'response': 'неверный id'})
