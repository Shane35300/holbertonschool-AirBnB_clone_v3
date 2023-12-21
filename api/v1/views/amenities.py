#!/usr/bin/python3

from flask import Flask, jsonify, request, abort
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """retrieves the list of all amenity objects"""
    amenities = storage.all(Amenity).values() #  récupéré les amenities

    if amenities is None:
        abort(404)

    amenities_list = [amenity.to_dict() for amenity in amenities]
    # mettre dans une list
    return jsonify(amenities_list) # renvoie la list en json

@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """retrieves a amenity object"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_object(amenity_id):
    """Delete amenity object by id"""
    amenity = storage.get(Amenity, amenity_id)
    #récupère l'objet amenity par l'id

    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates new amenity object"""
    data_amenity = request.get_json()
    # Obtiens le corps de la requête en temps que dictionnaire

    if data_amenity is None:
        abort(400, "Not a JSON")

    if "name" not in data_amenity:
        abort(400, "Missing name")

    new_amenity = Amenity(**data_amenity)
    # crée un nouvelle objet amenity avec les donner du JSON(data_amenity)
    storage.new(new_amenity) # envois au stokage
    storage.save() # sauvegarde les modifications
    return jsonify(new_amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update amenity by id"""
    amenity_obj = storage.get(Amenity, amenity_id)

    if amenity_obj is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    # parcourir chaque key/value dans data
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity_obj, key, value)

    storage.save()
    return jsonify(amenity_obj.to_dict()), 200
