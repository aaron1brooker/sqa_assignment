import logging
from flask import jsonify, Response  # type: ignore

from src.flask.types import OutcomeResponse

logger = logging.getLogger(__name__)


def execution_status_response(success: bool) -> Response:
    response = OutcomeResponse(success=success)
    return jsonify(response.model_dump_json())
