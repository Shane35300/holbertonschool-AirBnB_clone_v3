#!/usr/bin/python3

from flask import Flask, jsonify, request, abort
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """retrieves the list of all user objects"""
    users = storage.all(User).values() # récupéré les users

    if users is None:
        abort(404)

    user_list = [user.to_dict() for user in users]
    # mettre dans une list
    return jsonify(user_list) # renvoie la list en json

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """retrieves a user object by id"""
    user = storage.get(User, user_id) # récuperer le user

    if user is None:
        abort(404)

    return jsonify(user.to_dict()) # renvoie la list en json

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user_object(user_id):
    """Delete user object by id"""
    user = storage.get(User, user_id)
    #récupère l'objet user par l'id

    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates new user object"""
    data = request.get_json()
    # Obtiens le corps de la requête en temps que dictionnaire

    if data is None:
        abort(400, "Not a JSON")

    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")

    new_user = User(**data)
    # crée un nouvelle objet user avec les donner du JSON
    storage.new(new_user) # envois au stokage
    storage.save() # sauvegarde les modifications
    return jsonify(new_user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update user by id"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not JSON")

    # parcourir chaque key/value dans data
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200
