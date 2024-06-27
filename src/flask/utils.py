from flask import jsonify, Response  # type: ignore


def execution_status_response(success: bool) -> Response:
    return jsonify({"success": success})
