from app import build_app


def start():
    try:
        app = build_app()
    except KeyboardInterrupt:
        pass
