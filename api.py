from db import db_unit
from flask import Flask, Blueprint, jsonify

blueprint = Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)
db_unit.global_init('db/blogs.db')


@blueprint.route('/api/jobs')
def get_jobs():
    sess = db_unit.create_session()
    return jsonify({'response':[item.to_dict() for item in  sess.query(db_unit.Job).all()]})
