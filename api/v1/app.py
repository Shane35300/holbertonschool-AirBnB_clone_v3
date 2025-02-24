#!/usr/bin/python3
"""Main module to start the HBNB API server."""

from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
import os

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Close the current SQLAlchemy session"""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """Returns:
        JSON response with a 404 status code."""
    return jsonify({"error": 'Not found'}), 404


if __name__ == '__main__':
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
