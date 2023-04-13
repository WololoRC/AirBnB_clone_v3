#!/usr/bin/python3
""" Review module"""
from flask import jsonify, abort, Blueprint, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
def get_reviews(place_id):
    """
    Method : GET
        returns the list of all Review objects of a Place

    Method : POST
        creates a new Review
    """
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)

    if request.method == 'GET':
        reviews = storage.all(Review)
        return jsonify([obj.to_dict() for obj in reviews.values()
                        if obj.place_id == place_id])

    if request.method == 'POST':
        if not request.json:
            return 'Not a JSON\n', 400
        if 'text' not in request.json:
            return 'Missing text\n', 400
        if 'user_id' not in request.json:
            return 'Missing user_id\n', 400
        usr_obj = storage.get(User, request.get_json().get('user_id'))
        if not usr_obj:
            abort(404)
        else:
            new_review = Review()
            new_review.place_id = place_id
            new_review.user_id = request.get_json().get('user_id')
            new_review.text = request.get_json().get('text')
            new_review.save()
            return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_reviews_by_id(review_id):
    """
    Method : GET
        returns a Review object with provided the id.

    Method : DELETE
        deletes a Review

    Method : PUT
        updates a Review
    """
    obj = storage.get(Review, review_id)
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
            update_data.pop("user_id", None)
            update_data.pop("place_id", None)
            for key, value in update_data.items():
                setattr(obj, key, value)
            obj.save()
            return jsonify(obj.to_dict()), 200

        except Exception:
            return 'Not a JSON\n', 400
