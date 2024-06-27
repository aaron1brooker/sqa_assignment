import logging

from src.flask.router import app


def main():
    logging.basicConfig(level=logging.INFO)
    app.run()
    return 0


if __name__ == "__main__":
    main()
