#!/usr/bin/python3
'''
    RESTful API for Amenity
'''
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    '''GET amenities '''
    a_list = [a.to_dict() for a in storage.all('Amenity').values()]
    return jsonify(a_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity_id(amenity_id):
    '''amenity by id GET'''
    a = storage.get("Amenity", amenity_id)
    if a is None:
        abort(404)
    return jsonify(a.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    '''DELETE amenity by id'''
    a = storage.get("Amenity", amenity_id)
    if a is None:
        abort(404)
    a.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def make_amenities():
    '''make amenities POST'''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        data = request.get_json()
        obj = Amenity(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenities_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenities_id):
    '''updates by id PUT'''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    obj = storage.get("Amenity", amenities_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    obj.name = data['name']
    obj.save()
    return jsonify(obj.to_dict()), 200
