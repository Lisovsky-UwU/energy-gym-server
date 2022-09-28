from quart import Quart
from quart_cors import cors

from .config_module import config
from .blueprints import api_bl


def build_app() -> Quart:
    app = Quart(__name__)
    app.register_blueprint(api_bl, url_prefix='/api')

    if config.default.use_dev == True:
        app = cors(app, allow_origin='*')

    return app
