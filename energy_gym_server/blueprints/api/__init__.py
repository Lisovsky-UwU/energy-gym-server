from flask import Blueprint
from .api_blueprints import authorization_bl, available_time_bl, users_bl, entries_bl


api = Blueprint('api', __name__)

api.register_blueprint(authorization_bl,    url_prefix='/authorization')
api.register_blueprint(available_time_bl,   url_prefix='/available-time')
api.register_blueprint(users_bl,            url_prefix='/users')
api.register_blueprint(entries_bl,          url_prefix='/entries')

from . import handlers
