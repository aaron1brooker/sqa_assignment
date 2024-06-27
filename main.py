import logging

from src.flask.router import app


def main():
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=5001)
    return 0


if __name__ == "__main__":
    main()