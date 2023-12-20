#!/usr/bin/python3

from flask import Flask, jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()  # Récupérer tous les objets State
    state_list = [state.to_dict() for state in states]  # Convertir en liste de dictionnaires
    return jsonify(state_list)  # Renvoyer la liste en tant que réponse JSON

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """Retrieves a State object by ID"""
    state = storage.get(State, state_id)  # Récupérer l'objet State par ID

    if state is None:
        abort(404)  # Si l'objet n'est pas trouvé, renvoyer une erreur 404

    return jsonify(state.to_dict())  # Convertir l'objet en dictionnaire et le renvoyer en tant que réponse JSON

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State object"""
    data = request.get_json()  # Obtenir le corps de la requête en tant que dictionnaire JSON

    if not data:
        abort(400, "Not a JSON")  # Si ce n'est pas un JSON valide, renvoyer une erreur 400

    if "name" not in data:
        abort(400, "Missing name")  # Si la clé "name" est manquante, renvoyer une erreur 400

    new_state = State(**data)  # Créer un nouvel objet State avec les données du JSON
    storage.new(new_state)  # Ajouter le nouvel objet au système de stockage
    storage.save()  # Sauvegarder les modifications dans le système de stockage

    return jsonify(new_state.to_dict()), 201  # Renvoyer le nouvel objet avec le code de statut 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object by ID"""
    state = storage.get(State, state_id)  # Récupérer l'objet State par ID

    if state is None:
        abort(404)  # Si l'objet n'est pas trouvé, renvoyer une erreur 404

    data = request.get_json()  # Obtenir le corps de la requête en tant que dictionnaire JSON

    if not data:
        abort(400, "Not a JSON")  # Si ce n'est pas un JSON valide, renvoyer une erreur 400

    # Mettre à jour l'objet State avec les nouvelles données
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    storage.save()  # Sauvegarder les modifications dans le système de stockage

    return jsonify(state.to_dict()), 200  # Renvoyer l'objet mis à jour avec le code de statut 200

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object by ID"""
    state = storage.get(State, state_id)  # Récupérer l'objet State par ID

    if state is None:
        abort(404)  # Si l'objet n'est pas trouvé, renvoyer une erreur 404

    storage.delete(state)  # Supprimer l'objet State
    storage.save()  # Sauvegarder les modifications dans le système de stockage

    return jsonify({}), 200  # Renvoyer un dictionnaire vide avec le code de statut 200
