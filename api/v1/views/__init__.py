#!/usr/bin/python3
"""
Blueprint module for organizing API routes related to HBNB application.

This module sets up a Flask Blueprint named 'app_views' with a URL prefix '/api/v1'.
It imports and registers routes related to different parts of the application,
including states, cities, and index views.
"""

from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.user import *
from api.v1.views.places import *
