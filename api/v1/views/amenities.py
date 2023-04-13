#!/usr/bin/python3
"""API states module"""
from flask import jsonify, abort, Blueprint, request
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def get_amenities():
    """
    Method : GET
        returns the list of all Amenity objects

    Method : POST
        create new Amenity
    """
    if request.method == 'GET':
        a_list = []

        for key, value in storage.all(Amenity).items():
            a_list.append(value.to_dict())

        return jsonify(a_list)

    if request.method == 'POST':
        if not request.json:
            return 'Not a JSON\n', 400
        elif 'name' not in request.json:
            return 'Missing name\n', 400
        else:
            new_amenity = Amenity()
            new_amenity.name = request.get_json().get('name')
            new_amenity.save()
            return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def amenities_by_id(amenity_id):
    """
    Method : GET
        returns an Amenity object with provided the id.

    Method : DELETE
        deletes an Amenity instance

    Method : PUT
        updates an Amenity instance
    """
    if request.method == 'GET':
        try:
            return jsonify(storage.get(Amenity, amenity_id).to_dict())
        except Exception:
            abort(404)

    if request.method == 'DELETE':
        obj = storage.get(Amenity, amenity_id)
        if obj is None:
            abort(404)
        else:
            storage.delete(obj)
            storage.save()
            return jsonify({}), 200

    if request.method == 'PUT':
        obj = storage.get(Amenity, amenity_id)
        if not obj:
            abort(404)
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
