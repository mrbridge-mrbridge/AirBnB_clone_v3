#!/usr/bin/python3
"""
Restful for State
"""

from flask import Flask, jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_state():
    """sends state information"""
    slist = [s.to_dict() for s in storage.all('State').values()]
    return jsonify(slist)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes state"""
    data = storage.get("State", state_id)
    if data is None:
        abort(404)
    storage.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """creates state  from user input"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        data = request.get_json()
        obj = State(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slash=False)
def update_state(state_id):
    """updates state"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    obj.name = data['name']
    obj.save()
    return jsonify(obj.to_dict()), 200
