#!/usr/bin/python3
'''
    RESTful API for  Review Class
'''
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review_by_place(place_id):
    '''
    Get for places
    and returns JSON
    '''
    getplace = storage.get(Place, place_id)
    if getplace is None:
        abort(404)
    review_list = [r.to_dict() for r in getplace.reviews]
    return jsonify(review_list), 200


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_id(review_id):
    '''
    GET for places
    and returns JSON
    '''
    getreview = storage.get(Review, review_id)
    if getreview is None:
        abort(404)
    return jsonify(getreview.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    '''
    DELETE for reviews
    and returns JSON
    '''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    '''
    POST for place reviews
    and returns JSON
    '''
    if storage.get(Place, place_id) is None:
        abort(404)
    elif not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "user_id" not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    elif storage.get("User", request.get_json()["user_id"]) is None:
        abort(404)
    elif "text" not in request.get_json():
        return jsonify({"error": "Missing text"}), 400
    else:
        data = request.get_json()
        obj = Review(**data)
        obj.place_id = place_id
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''
    Update route for place reviews
    and returns JSON
    '''
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    elif not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    else:
        obj_data = request.get_json()
        ignore = ("id", "user_id", "place_id", "created_at", "updated_at")
        for k in obj_data.keys():
            if k in ignore:
                pass
            else:
                setattr(obj, k, obj_data[k])
        obj.save()
        return jsonify(obj.to_dict()), 200
