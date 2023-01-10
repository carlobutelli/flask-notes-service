#!/usr/bin/env python3
from flask import g, jsonify

from api.core import get_db
from api.core.logs import log_debug_with_txn_id, log_error_with_txn_id
from api.user.model import User


def check_services():
    db = get_db()
    response = {}
    service = None
    try:
        service = "PostgreSQL"
        User.query.limit(0).all()
        log_debug_with_txn_id("[HEALTH-CHECK]", g.transaction_id, f"{service} is healthy")
        response["PostgreSQL"] = {"healthy": True}
    #     other services to be checked
    except Exception as e:
        log_error_with_txn_id("[HEALTH-CHECK]",
                              g.transaction_id,
                              f"service {service} returned unhealthy healthcheck: {e}")
        response[service] = {
            "healthy": False,
            "message": f"Error: {e}"
        }
        return jsonify(response), 500
    else:
        return jsonify(response), 200
    finally:
        db.session.close()
