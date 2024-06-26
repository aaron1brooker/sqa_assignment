from flask import jsonify, Response


def execution_status_response(success: bool) -> Response:
    return jsonify({"success": success})
