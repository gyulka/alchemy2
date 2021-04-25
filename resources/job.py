from flask_restful import reqparse, abort, Api, Resource
from db import db_unit
from flask import jsonify

parser = reqparse.RequestParser()
parser.add_argument('team_leader', required=True, type=int)
parser.add_argument('description', required=True)
parser.add_argument('hazard', required=True, type=int)
parser.add_argument('team', required=True)
parser.add_argument('is_finished', required=True, type=bool)
parser.add_argument('id_created', required=True, type=int)


def abort_if_news_not_found(job_id):
    session = db_unit.create_session()
    news = session.query(db_unit.Job).get(job_id)
    if not news:
        abort(404, message=f"job {job_id} not found")


class JobResource(Resource):
    def get(self, job_id):
        abort_if_news_not_found(job_id)
        session = db_unit.create_session()
        job = session.query(db_unit.Job).get(job_id)
        return jsonify({'job': job.to_dict()})

    def delete(self, job_id):
        abort_if_news_not_found(job_id)
        session = db_unit.create_session()
        news = session.query(db_unit.Job).get(job_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class JobListResource(Resource):
    def get(self):
        session = db_unit.create_session()
        jobs = session.query(db_unit.Job).all()
        return jsonify({'jobs': [job.to_dict(
        ) for job in jobs]})

    def post(self):
        try:
            args = parser.parse_args()
            session = db_unit.create_session()
            job = db_unit.Job()
            job.team_leader = int(args['team_leader'])
            job.description = args['description']
            job.hazard = int(args['hazard'])
            job.team = args['team']
            job.is_finished = args['is_finished']
            job.id_created = int(args['id_created'])
            session.add(job)
            session.commit()
            return jsonify({'success': 'OK'})
        except Exception as error:
            return jsonify(error=error.__str__())
