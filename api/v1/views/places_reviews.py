#!/usr/bin/python3

from flask import Flask, jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """retrieves the list of all reviews in a place id"""
    place = storage.get(Place, place_id)  # Récupérer l'objet place par ID

    if place is None:
        abort(404)  # Si l'objet n'est pas trouvé, renvoyer une erreur 404
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)  # Renvoyer la liste des villes


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_by_id(review_id):
    """Retrieves a Review object by ID"""
    review = storage.get(Review, review_id)  # Récupérer l'objet review par ID

    if review is None:
        abort(404)  # Si l'objet n'est pas trouvé, renvoyer une erreur 404

    return jsonify(review.to_dict())  # Convertir l'objet en dictionnaire


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a new Review object"""
    place = storage.get(Place, place_id)  # Récupérer l'objet Place par ID

    if not place:
        abort(404)  # Si l'objet State n'est pas trouvé

    data = request.get_json()  # Obtenir le corps de la requête

    if not data:
        abort(400, "Not a JSON")  # Si ce n'est pas un JSON valide

    if "user_id" not in data:
        abort(400, "Missing user_id")  # Si la clé "name" est manquante
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if "text" not in data:
        abort(400, "Missing text")
    data['place_id'] = place_id

    new_review = Review(**data)  # Créer un nouvel objet Review
    storage.new(new_review)  # Ajouter le nouvel objet au système de stockage
    storage.save()  # Sauvegarder les modifications dans le système de stockage

    return jsonify(new_review.to_dict()), 201  # Renvoyer le nouvel objet


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object by ID"""
    review = storage.get(Review, review_id)  # Récupérer l'objet Review par ID

    if review is None:
        abort(404)  # Si l'objet n'est pas trouvé, renvoyer une erreur 404

    data = request.get_json()  # Obtenir le corps de la requête

    if not data:
        abort(400, "Not a JSON")  # Si ce n'est pas un JSON valide

    # Mettre à jour l'objet City avec les nouvelles données
    for key, value in data.items():
        if key not in ['id', 'place_id',
                       'created_at', 'updated_at', 'user_id']:
            setattr(review, key, value)

    storage.save()  # Sauvegarder les modifications dans le système de stockage

    return jsonify(review.to_dict()), 200  # Renvoyer l'objet mis à jour


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object by ID"""
    review = storage.get(Review, review_id)  # Récupérer l'objet Review par ID

    if review is None:
        abort(404)  # Si l'objet n'est pas trouvé, renvoyer une erreur 404

    storage.delete(review)  # Supprimer l'objet Review
    storage.save()  # Sauvegarder les modifications dans le système de stockage

    return jsonify({}), 200  # Renvoyer un dictionnaire vide
