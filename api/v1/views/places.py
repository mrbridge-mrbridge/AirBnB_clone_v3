#!/usr/bin/python3
'''
    RESTful API for Place Class
'''
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_place_city(city_id):
    '''
    GET place by City
    and returns JSON
    '''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places_list = [p.to_dict() for p in city.places]
    return jsonify(places_list), 200


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_placeid(place_id):
    '''
    GET place by ID
    and returns JSON
    '''
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    '''
    DELETE PLACE
    and returns JSON
    '''
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def make_place(city_id):
    '''
    POST/CREATE new place
    and returns JSON
    '''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    elif "user_id" not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    else:
        data = request.get_json()
        city = storage.get("City", city_id)
        user = storage.get("User", data['user_id'])
        if city is None or user is None:
            abort(404)
        data['city_id'] = city.id
        data['user_id'] = user.id
        obj = Place(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''
    PUT/UPDATE PLACE
    and returns JSON
    '''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    ignore = ("id", "user_id", "created_at", "updated_at")
    for k, v in data.items():
        if k not in ignore:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200
