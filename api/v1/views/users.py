#!/usr/bin/python3
'''
    RESTful API for User Class
'''
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    '''
    Get all users
    and returns JSON
    '''
    userl = [u.to_dict() for u in storage.all(User).values()]
    return jsonify(userl)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_userid(user_id):
    '''
    get user by id
    and returns JSON
    '''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    '''
    DELETE user
    and returns JSON
    '''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def make_user():
    '''
    creates User POST
    and returns JSON
    '''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "email" not in request.get_json():
        return jsonify({"error": "Missing email"}), 400
    elif "password" not in request.get_json():
        return jsonify({"error": "Missing password"}), 400
    else:
        data = request.get_json()
        obj = User(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''
    updates user info PUT
    and returns JSON
    '''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    ignore = ("id", "email", "created_at", "updated_at")
    for k in data.keys():
        if k in ignore:
            pass
        else:
            setattr(obj, k, data[k])
    obj.save()
    return jsonify(obj.to_dict()), 200
