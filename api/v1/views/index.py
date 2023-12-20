#!/usr/bin/python3
"""Module containing routes for the HBNB API."""

from flask import jsonify
from . import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.state import State
from models.place import Place
from models.user import User


@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns:
        JSON response with status OK if the server is running."""
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def count_type():
    """Returns:
        JSON response containing counts of amenities, cities, places,
        reviews, states, and users."""
    count_type = {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User),
    }

    return jsonify({'stats': count_type})
