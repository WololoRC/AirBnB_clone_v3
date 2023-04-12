#!/usr/bin/python3
"""API states module"""
from flask import jsonify, abort, Blueprint
from models.state import State
from api.v1.views import app_views
from models import storage

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    a_list = []

    for key, value in storage.all(State).items():
        a_list.append(value.to_dict())

    return jsonify(a_list)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_by_id(state_id):
    try:
        return jsonify(storage.get(State, state_id).to_dict())
    except Exception:
        abort(404)
