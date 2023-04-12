#!/usr/bin/python3
"""API states module"""
from flask import jsonify, abort, Blueprint, request
from models.state import State
from api.v1.views import app_views
from models import storage

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """returns the list of all State objects"""
    a_list = []

    for key, value in storage.all(State).items():
        a_list.append(value.to_dict())

    return jsonify(a_list)

@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_by_id(state_id):
    """returns a State object when provided the id"""
    if request.method == 'GET':
        try:
            return jsonify(storage.get(State, state_id).to_dict())
        except Exception:
            abort(404)
    if request.method == 'DELETE':
        obj = storage.get(State, state_id)
        if obj is None:
            abort(404)
        else:
            storage.delete(obj)
            storage.save()
            return jsonify({}), 200
    if request.method == 'PUT':
        obj = storage.get(State, state_id)
        if obj is not None:
            update_data = request.get_json()
            if type(update_data) == dict:
                raise Exception("Not a Json", 400)
            else:
                update_data.pop("created_at", None)
                update_data.pop("updated_at", None)
                update_data.pop("id", None)
                obj.__dict__.update(update_data)
                storage.save()
                return jsonify(obj.to_dict()), 200
        else:
            abort(404)

