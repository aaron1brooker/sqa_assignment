import logging

from flask import Flask, render_template, request # type: ignore

from src.flask.utils import execution_status_response

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Route to html page
@app.route("/")
def checklist_page() -> str:
    return render_template("checklist_page.html")


# Below are endpoints that can be fetched on the web app
@app.route("/check-item", methods=["POST"])
def check_item():
    data = request.get_json()
    if data is None or (not isinstance(data.get("is_checked"), bool)):
        logger.error(f"Invalid request provided: {request.get_json()}")
        return execution_status_response(False)

    # TODO(Alex): add operation
    return execution_status_response(True)


@app.route("/delete-item", methods=["POST"])
def delete_item():
    # TODO(Alex): add operation
    return execution_status_response(True)


@app.route("/add-item", methods=["POST"])
def add_item():
    # TODO(Azra): Add types to all of request/response
    # TODO(Alex): add operation
    return execution_status_response(True)
