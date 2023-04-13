#!/usr/bin/python3
""" User module"""
from flask import jsonify, abort, Blueprint, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users',
                 methods=['GET', 'POST'], strict_slashes=False)
def get_users():
    """
    Method : GET
        returns the list of all User objects

    Method : POST
        creates a new User
    """
    if request.method == 'GET':
        users = storage.all(User)
        return jsonify([obj.to_dict() for obj in users.values()])

    if request.method == 'POST':
        if not request.json:
            return 'Not a JSON\n', 400
        elif 'email' not in request.json:
            return 'Missing email\n', 400
        elif 'password' not in request.json:
            return 'Missing password\n', 400
        else:
            new_user = User()
            new_user.email = request.get_json().get('email')
            new_user.password = request.get_json().get('password')
            new_user.save()
            return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_users_by_id(user_id):
    """
    Method : GET
        returns a User object when is provided the id.

    Method : DELETE
        deletes a User

    Method : PUT
        updates a User
    """
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)

    if request.method == 'GET':
        return jsonify(obj.to_dict())

    if request.method == 'DELETE':
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        try:
            update_data = request.get_json()
            update_data.pop("created_at", None)
            update_data.pop("updated_at", None)
            update_data.pop("id", None)
            for key, value in update_data.items():
                setattr(obj, key, value)
            obj.save()
            return jsonify(obj.to_dict()), 200

        except Exception:
            return 'Not a JSON\n', 400
