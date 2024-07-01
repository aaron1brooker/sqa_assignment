import logging
from flask import jsonify
from pydantic import ValidationError

from flask import Flask, Response, render_template, request, jsonify

from src.flask.types import CheckItemRequest, DeleteItemRequest, AddItemRequest, FetchItemsRequest, FetchItemsResponse
from src.flask.utils import execution_status_response

from src.business_logic.db_interactions import add_item_to_db, get_all_items, delete_item_from_db, check_item_in_db

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
                    logger.error("Invalid request endpoint")
                    return execution_status_response(False)
        except ValidationError as e:
            logger.error(f"Payload invalid: {e}")
            return execution_status_response(False)


# Below are endpoints that can be fetched on the web app
@app.route("/check-item", methods=["POST"])
def check_item() -> Response:
    check_item_request = CheckItemRequest(**request.get_json())
    logger.info(f"Received check item request with value: {check_item_request}")

    check_item_in_db(check_item_request.item_id)

    return execution_status_response(True)


@app.route("/delete-item", methods=["POST"])
def delete_item() -> Response:
    delete_item_request = DeleteItemRequest(**request.get_json())
    logger.info(f"Received delete item request with value: {delete_item_request}")

    delete_item_from_db(delete_item_request.item_id)
    return execution_status_response(True)


@app.route("/add-item", methods=["POST"])
def add_item() -> Response:
    add_item_request = AddItemRequest(**request.get_json())
    logger.info(f"Received add item request with value: {add_item_request}")
    george = add_item_to_db(add_item_request.item_id, add_item_request.message, add_item_request.checked)
    return execution_status_response(george)


@app.route("/fetch-items", methods=["POST"])
def fetch_items() -> Response:
    fetch_items_request = FetchItemsRequest(**request.get_json())
    logger.info(f"Received fetch items request with value: {fetch_items_request}")

    return jsonify(FetchItemsResponse(items=get_all_items()).model_dump_json())
