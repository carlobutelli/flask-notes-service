#!/usr/bin/env python3
from flask import jsonify, g
from flask_api import status


def base_response(status: str, status_code: int, transaction_id: str, message: str = "", data: {} = None):  # pragma: no cover
    meta = {
        "status": status,
        "status_code": status_code,
        "transaction_id": transaction_id,
        "message": message
    }
    if data:
        return jsonify(data=data, meta=meta)
    return jsonify(meta=meta)


def base_error_response(status: str, status_code: int, transaction_id: str, message: str = ""):  # pragma: no cover
    meta = {
        "status": status,
        "status_code": status_code,
        "transaction_id": transaction_id,
        "message": message
    }
    return jsonify(meta=meta)


def internal_server_error_response(message: str = "internal server error"):
    return base_error_response("ERROR", 500, g.transaction_id, message), status.HTTP_500_INTERNAL_SERVER_ERROR


def bad_request_response(message: str = "bad request"):
    return base_error_response("ERROR", 400, g.transaction_id, message), status.HTTP_400_BAD_REQUEST


def not_found_response(message: str = "not found"):
    return base_response("NOT FOUND", 404, g.transaction_id, message), status.HTTP_404_NOT_FOUND
