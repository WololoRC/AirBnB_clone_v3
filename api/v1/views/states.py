#!/usr/bin/python3
"""API states module"""
from flask import jsonify, abort, Blueprint, request
from models.state import State
from api.v1.views import app_views
from models import storage

@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_states():
    """
    Method : GET
        returns the list of all State objects

    Method : POST
        create new State
    """
    if request.method == 'GET':
        a_list = []

        for key, value in storage.all(State).items():
            a_list.append(value.to_dict())

        return jsonify(a_list)

    if request.method == 'POST':
        if not request.json or not 'name' in request.json:
            abort(404)
        else:
            new_state = State()
            new_state.name = request.get_json().get('name')
            new_state.save()
            return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_by_id(state_id):
    """
    Method : GET
        returns a State object with provided the id.

    Method : DELETE
        deletes a state
    """
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
            try:
                update_data = request.get_json()
                update_data.pop("created_at", None)
                update_data.pop("updated_at", None)
                update_data.pop("id", None)
                obj.__dict__.update(update_data)
                obj.save()
                return jsonify(obj.to_dict()), 200

            except Exception:
                return 'Not a JSON\n', 400
        else:
            abort(404)

