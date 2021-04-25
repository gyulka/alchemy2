from flask_restful import reqparse, abort, Api, Resource
from db import db_unit
from flask import jsonify

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('city', required=True)
parser.add_argument('password', required=True)
parser.add_argument('speciality', required=True)


def abort_if_news_not_found(user_id):
    session = db_unit.create_session()
    news = session.query(db_unit.User).get(user_id)
    if not news:
        abort(404, message=f"user {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_unit.create_session()
        user = session.query(db_unit.User).get(user_id)
        return jsonify({'user': user.to_dict()})

    def delete(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_unit.create_session()
        news = session.query(db_unit.User).get(user_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_unit.create_session()
        users = session.query(db_unit.User).all()
        return jsonify({'users': [user.to_dict(
        ) for user in users]})

    def post(self):
        try:
            args = parser.parse_args()
            session = db_unit.create_session()
            user = db_unit.User(
                name=args['name'],
                speciality=args['speciality'],
                city=args['city']
            )
            user.set_password(args['password'])
            user.id = args['id']
            session.add(user)
            session.commit()
            return jsonify({'success': 'OK'})
        except Exception as error:
            return jsonify(error=error.__str__())
