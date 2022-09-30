from .config_module import config
from .app import build_app
from .containers import Application


def start():
    try:
        Application(
            config=config
        )
        app = build_app()
        app.run(
            host='0.0.0.0',
            port=config.default.server_port,
            use_reloader=False
        )
    except KeyboardInterrupt:
        pass
