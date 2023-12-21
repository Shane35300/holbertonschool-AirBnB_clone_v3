#!/usr/bin/python3

from flask import Flask, jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from api.v1.views import app_views
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """retrieves the list of all place object in a city id"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    places = city.places
    place_list = [place.to_dict() for place in places]
    # mettre dans une list
    return jsonify(place_list) # renvoie la list en json

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    """retrieves a place object by id"""
    place = storage.get(Place, place_id) # récuperer le lieu

    if place is None:
        abort(404)

    return jsonify(place.to_dict()) # renvoie le lieux

@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_object(place_id):
    """Delete place object by id"""
    place = storage.get(Place, place_id)
    #récupère l'objet user par l'id

    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route('cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates new place object"""
    city = storage.get(City, city_id)  # Récupérer l'objet State par ID

    if not city:
        abort(404)  # Si l'objet State n'est pas trouvé
    data = request.get_json()
    # Obtiens le corps de la requête en temps que dictionnaire

    if data is None:
        abort(400, "Not a JSON")

    if "user_id" not in data:
        abort(400, "Missing user_id")
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if "name" not in data:
        abort(400, "Missing name")

    data['city_id'] = city_id

    new_place = Place(**data)
    # crée un nouvelle objet place avec les données du JSON
    storage.new(new_place) # envois au stokage
    storage.save() # sauvegarde des modifications
    return jsonify(new_place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update place by id"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    # parcourir chaque key/value dans data
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
