from .config_module import config
from .app import build_app


def start():
    try:
        app = build_app()
        app.run(
            host='0.0.0.0',
            port=config.server_port,
            use_reloader=False
        )
    except KeyboardInterrupt:
        pass
