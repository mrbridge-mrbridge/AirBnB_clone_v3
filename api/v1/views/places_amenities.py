#!/usr/bin/python3
"""
    RESTful API for Amenities of a Place
"""

from flask import jsonify, abort, request, make_response
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
        amen = [amenity.to_dict() for amenity in getplace.amenities]
    else:
        amen = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in getplace.amenity_ids]
    return jsonify(amen)



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

    if environ.get("HBNB_TYPE_STORAGE") == "db":
        if getamenity not in getplace.amenities:
            abort(404)
        getplace.amenities.remove(getamenity)
    else:
        if amenity_id not in getplace.amenity_ids:
            abort(404)
        getplace.amenity_ids.remove(amenity_id)

    storage.save()
    return make_response(jsonify({}), 200)


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


    if environ.get("HBNB_TYPE_STORAGE") == "db":
        if getamenity in getplace.amenities:
            return make_response(jsonify(getamenity.to_dict()), 200)
        else:
            getplace.amenities.append(getamenity)
    else:
        if amenity_id in getplace.amenity_ids:
            return make_response(jsonify(getamenity.to_dict()), 200)
        else:
            getplace.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(getamenity.to_dict()), 201)
