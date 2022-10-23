from flask import Flask
from flask_cors import CORS

from .config_module import config
from .blueprints import api_bl


def build_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(api_bl, url_prefix='/api')

    if config.default.use_dev == True:
        CORS(app, allow_origin='*')

    return app
