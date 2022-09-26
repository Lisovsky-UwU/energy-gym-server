from quart import Blueprint

api = Blueprint('api', __name__)

from . import routes
