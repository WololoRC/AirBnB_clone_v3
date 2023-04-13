#!/usr/bin/python3
"""Places API module"""
from flask import jsonify, abort, Blueprint, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def get_places(city_id):
    """
    Method : GET
        returns the list of all Place objects linked of a State

    Method : POST
        creates a new Place
    """
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)

    if request.method == 'GET':
        places = storage.all(Place)
        return jsonify([obj.to_dict() for obj in places.values()
                        if obj.city_id == city_id])

    if request.method == 'POST':
        if not request.json:
            return 'Not a JSON\n', 400
        elif 'name' not in request.json:
            return 'Missing name\n', 400
        else:
            new_place = Place()
            new_place.name = request.get_json().get('name')
            new_place.city_id = city_id
            new_place.save()
            return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_places_by_id(city_id):
    """
    Method : GET
        returns a Place object with provided the id.

    Method : DELETE
        deletes a Place

    Method : PUT
        updates a Place
    """
    obj = storage.get(Place, place_id)
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
