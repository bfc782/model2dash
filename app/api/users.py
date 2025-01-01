from flask import jsonify, request, url_for
from ..models import User, Team, Roster
from . import api
from ..extensions import db

@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())

@api.route('/users/')
def get_users():
    users = User.query.all()
    return jsonify({ 'users': [user.to_json() for user in users] })

@api.route('/users/', methods=['POST'])
def registration():
    data = request.get_json()
    new_user_id = data.get('user_id')
    new_user_name = data.get('user_name')

    new_user = User(new_user_id, new_user_name)

    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_json())