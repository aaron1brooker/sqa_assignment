import logging

from pydantic import ValidationError  # type: ignore

from flask import Flask, Response, render_template, request  # type: ignore

from src.flask.types import CheckItemRequest, DeleteItemRequest, AddItemRequest, FetchItemsRequest
from src.flask.utils import execution_status_response

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Route to html page
@app.route("/")
def checklist_page() -> str:
    return render_template("checklist_page.html")


# The request gets routed here first so that we can do some validation
@app.before_request
def validate_request_payload():
    if request.method == "POST":
        request_payload = request.get_json()
        try:
            match request.endpoint:
                case "check_item":
                    CheckItemRequest(**request_payload)
                case "delete_item":
                    DeleteItemRequest(**request_payload)
                case "fetch_items":
                    FetchItemsRequest(**request_payload)
                case "add_item":
                    AddItemRequest(**request_payload)
                case _:
                    logger.error(f"Unknown request type: {request.endpoint}")
                    return execution_status_response(False)
        except ValidationError as e:
            logger.error(f"Payload invalid: {e}")
            return execution_status_response(False)


# Below are endpoints that can be fetched on the web app
@app.route("/check-item", methods=["POST"])
def check_item() -> Response:
    check_item_request = CheckItemRequest(**request.get_json())
    logger.info(f"Received check item request with value: {check_item_request}")

    # TODO(Alex): add operation
    return execution_status_response(True)


@app.route("/delete-item", methods=["POST"])
def delete_item() -> Response:
    delete_item_request = DeleteItemRequest(**request.get_json())
    logger.info(f"Received delete item request with value: {delete_item_request}")

    # TODO(Alex): add operation
    return execution_status_response(True)


@app.route("/add-item", methods=["POST"])
def add_item() -> Response:
    add_item_request = AddItemRequest(**request.get_json())
    logger.info(f"Received add item request with value: {add_item_request}")

    # TODO(Alex): add operation
    return execution_status_response(True)


@app.route("/fetch-items", methods=["POST"])
def fetch_items() -> Response:
    fetch_items_request = FetchItemsRequest(**request.get_json())
    logger.info(f"Received fetch items request with value: {fetch_items_request}")

    # TODO(Alex): add operation
    return execution_status_response(True)
