#!/usr/bin/python3
"""
    RESTful API for Amenities of a Place
"""

from flask import jsonify, abort, request
from models import storage
from os import environ
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_place(place_id):
    '''
    Get for places
    and returns JSON
    '''
    getplace = storage.get(Place, place_id)
    if not getplace:
        abort(404)
    if environ.get("HBNB_TYPE_STORAGE") == "db":
        amen = getplace.amenities
    else:
        amen = []
        amenity_id_s = getplace.amenities
        all_amenities = storage.all(Amenity)
        for item in amenity_id_s:
            amen.append(storage.get(Amenity, item))
    amenity_obj = [amenity.to_dict() for amenity in amen]
    return jsonify(amenity_obj)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)

def delete_amenity(place_id, amenity_id):
    '''
    DELETE for amenities
    and returns JSON
    '''
    getplace = storage.get(Place, place_id)
    if not getplace:
        abort(404)

    getamenity = storage.get(Amenity, amenity_id)
    if not getamenity:
        abort(404)

    for item in getamenity:
        if item.id not in getplace.amenity_ids:
            abort(404)
    if environ.get("HBNB_TYPE_STORAGE") == "db":
        storage.delete(getamenity)
    else:
        storage.delete(getamenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def create_amenity(place_id, amenity_id):
    '''
    POST for place amenity
    and returns JSON
    '''
    getplace = storage.get(Place, place_id)
    if not getplace:
        abort(404)

    getamenity = storage.get(Amenity, amenity_id)
    if not getamenity:
        abort(404)

    for item in getamenity:
        if item.id in getplace.amenity_ids:
            return jsonify(item.to_dict()), 200

    if environ.get("HBNB_TYPE_STORAGE") == "db":
        getplace.amenities.append(getamenity)
    else:
        getplace.amenities = getamenity
    return jsonify(getamenity.to_dict()), 201
