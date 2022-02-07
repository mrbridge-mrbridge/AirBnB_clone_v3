#!/usr/bin/python3
'''
    RESTful API for City Class
'''
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_city_by_state(state_id):
    '''
    city by state
    and returns JSON
    '''
    data = storage.get("State", state_id)
    if data is None:
        abort(404)
    city_list = [c.to_dict() for c in data.cities]
    return jsonify(city_list), 200


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_id(city_id):
    '''
    city by id
    and returns JSON
    '''
    data = storage.get("City", city_id)
    if data is None:
        abort(404)
    return jsonify(data.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    '''
    Delete city
    and returns JSON
    '''
    data = storage.get("City", city_id)
    if data is None:
        abort(404)
    data.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def make_city(state_id):
    '''
    create city POST
    and returns JSON
    '''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        data = request.get_json()
        state = storage.get("State", state_id)
        if state is None:
            abort(404)
        data['state_id'] = state.id
        obj = City(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''
        update existing city object using PUT
    '''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    obj.name = data['name']
    obj.save()
    return jsonify(obj.to_dict()), 200
