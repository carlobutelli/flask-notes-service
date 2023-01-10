#!/usr/bin/env python3
from flasgger import swag_from
from flask import Blueprint, jsonify, g

from api.core.logs import log_info_with_txn_id

ping = Blueprint("ping", __name__)


@ping.route("/ping")
@swag_from("/api/docs/ping.yml")
def live_test_ping():
    log_info_with_txn_id("[PING]", g.transaction_id, "got new request for ping")
    return jsonify("pong"), 200
