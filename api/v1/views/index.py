#!/usr/bin/python3

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
    return jsonify({"status": "OK"})

@app_views.route('/api/vi/stats')
def count_type():
    count_type = {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User),
    }

    return jsonify({'stats': count_type})
