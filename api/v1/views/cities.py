#!/usr/bin/python3
from flask import jsonify, abort, Blueprint, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def get_cities(state_id):
    """
    Method : GET
        returns the list of all City objects of a State

    Method : POST
        creates a new City
    """
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)

    if request.method == 'GET':
        cities = storage.all(City)
        return jsonify([obj.to_dict() for obj in cities.values()
                        if obj.state_id == state_id])

    if request.method == 'POST':
        if not request.json:
            return 'Not a JSON\n', 400
        elif 'name' not in request.json:
            return 'Missing name\n', 400
        else:
            new_city = City()
            new_city.name = request.get_json().get('name')
            new_city.state_id = state_id
            new_city.save()
            return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_cities_by_id(city_id):
    """
    Method : GET
        returns a State object with provided the id.

    Method : DELETE
        deletes a state

    Method : PUT
        updates a state
    """
    obj = storage.get(City, city_id)
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
