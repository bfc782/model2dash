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
# @permission_required(Permission.WRITE)
def new_user():
    new_user = User.from_json(request.json)
    # new_user.author = g.current_user
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_json()), 201, \
        {'Location': url_for('api.get_user', id=new_user.id)}
