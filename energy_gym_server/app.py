from quart import Quart
from quart_cors import cors

from config_module import config


def build_app() -> Quart:
    app = Quart(__name__)

    if config.useDev == True:
        app = cors(app, allow_origin='*')

    return app
