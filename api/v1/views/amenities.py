#!/usr/bin/python3
'''
    RESTful API for Amenity Class
'''
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    '''
    GET amenities and
    returns JSON
    '''
    a_list = [a.to_dict() for a in storage.all('Amenity').values()]
    return jsonify(a_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity_id(amenity_id):
    '''
    amenity by id GET
    And returns JSON obj
    '''
    a = storage.get("Amenity", amenity_id)
    if a is None:
        abort(404)
    return jsonify(a.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    '''
    DELETE amenity by id
    And return JSON obj
    '''
    a = storage.get("Amenity", amenity_id)
    if a is None:
        abort(404)
    a.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def make_amenities():
    '''
    make amenities POST
    and creates a new JSON obj
    '''
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Amenity(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/amenities/<amenities_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenities_id):
    '''
    updates by id PUT
    and return JSON obj
    '''
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    amenity = storage.get(Amenity, amenities_id)

    if not amenity:
        abort(404)

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
