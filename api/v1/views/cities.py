#!/usr/bin/python3

from flask import Flask, jsonify, request, abort
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_all_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)  # Récupérer l'objet State par ID

    if state is None:
        abort(404)  # Si l'objet n'est pas trouvé, renvoyer une erreur 404
    cities = [city.to_dict() for city in state.cities]  # Récupérer les villes associées à l'État
    return jsonify(cities)  # Renvoyer la liste des villes en tant que réponse JSON

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """Retrieves a City object by ID"""
    city = storage.get(City, city_id)  # Récupérer l'objet City par ID

    if city is None:
        abort(404)  # Si l'objet n'est pas trouvé, renvoyer une erreur 404

    return jsonify(city.to_dict())  # Convertir l'objet en dictionnaire et le renvoyer en tant que réponse JSON

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Creates a new City object"""
    state = storage.get(State, state_id)  # Récupérer l'objet State par ID

    if not state:
        abort(404)  # Si l'objet State n'est pas trouvé, renvoyer une erreur 404

    data = request.get_json()  # Obtenir le corps de la requête en tant que dictionnaire JSON

    if not data:
        abort(400, "Not a JSON")  # Si ce n'est pas un JSON valide, renvoyer une erreur 400

    if "name" not in data:
        abort(400, "Missing name")  # Si la clé "name" est manquante, renvoyer une erreur 400

    # Ajouter l'ID de l'État au dictionnaire des données
    data['state_id'] = state_id

    new_city = City(**data)  # Créer un nouvel objet City avec les données du JSON
    storage.new(new_city)  # Ajouter le nouvel objet au système de stockage
    storage.save()  # Sauvegarder les modifications dans le système de stockage

    return jsonify(new_city.to_dict()), 201  # Renvoyer le nouvel objet avec le code de statut 201

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object by ID"""
    city = storage.get(City, city_id)  # Récupérer l'objet City par ID

    if city is None:
        abort(404)  # Si l'objet n'est pas trouvé, renvoyer une erreur 404

    data = request.get_json()  # Obtenir le corps de la requête en tant que dictionnaire JSON

    if not data:
        abort(400, "Not a JSON")  # Si ce n'est pas un JSON valide, renvoyer une erreur 400

    # Mettre à jour l'objet City avec les nouvelles données
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    storage.save()  # Sauvegarder les modifications dans le système de stockage

    return jsonify(city.to_dict()), 200  # Renvoyer l'objet mis à jour avec le code de statut 200

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object by ID"""
    city = storage.get(City, city_id)  # Récupérer l'objet City par ID

    if city is None:
        abort(404)  # Si l'objet n'est pas trouvé, renvoyer une erreur 404

    storage.delete(city)  # Supprimer l'objet City
    storage.save()  # Sauvegarder les modifications dans le système de stockage

    return jsonify({}), 200  # Renvoyer un dictionnaire vide avec le code de statut 200
